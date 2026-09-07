#!/usr/bin/env python3
"""Read-only wiki renderer. Apply through a CLI-only PHP importer on the WP host."""
import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
import os
import pathlib
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

import markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
import yaml

from scan_secrets import PATTERNS

ROOT = pathlib.Path(__file__).resolve().parent.parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inside_wiki(root, path):
    wiki = (root / 'wiki').resolve()
    resolved = path.resolve()
    if not resolved.is_relative_to(wiki):
        raise ValueError('Path outside wiki: ' + str(path))
    if any(part.startswith('.') for part in resolved.relative_to(wiki).parts):
        raise ValueError('Hidden wiki path is not publishable')
    return resolved


class WikiLinks(InlineProcessor):
    def handleMatch(self, match, data):
        target, _, alias = match.group(2).partition('|')
        node = ET.Element('img' if match.group(1) else 'a')
        if match.group(1):
            node.set('src', target)
            node.set('alt', alias or pathlib.PurePosixPath(target).stem)
        else:
            node.set('href', 'wiki-source:' + target)
            node.text = alias or target.split('#')[0].split('/')[-1]
        return node, match.start(0), match.end(0)


class WikiExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(WikiLinks(r'(!?)\[\[([^\]\n]+)\]\]', md), 'wikilinks', 175)


class AssetsAndLinks(HTMLParser):
    def __init__(self, root, note, selected, config):
        super().__init__(convert_charrefs=False)
        self.root, self.note, self.selected, self.config = root, note, selected, config
        self.output, self.assets, self.warnings = [], {}, []

    def resolve(self, target):
        value = unquote(target).replace('\\', '/')
        if re.match(r'^[A-Za-z]:', value) or '..' in pathlib.PurePosixPath(value).parts:
            raise ValueError('Unsafe attachment or link path: ' + target)
        value = value.lstrip('/')
        for p in (self.note.parent / value, self.root / 'wiki' / value, self.root / value):
            try:
                p = inside_wiki(self.root, p)
            except ValueError:
                continue
            if p.is_file():
                return p
        matches = list((self.root / 'wiki').rglob(pathlib.PurePosixPath(value).name))
        matches = [inside_wiki(self.root, p) for p in matches if p.is_file()]
        if len(matches) == 1:
            return matches[0]
        raise ValueError('Missing or ambiguous local path: ' + target)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'img':
            src = attrs.get('src', '')
            if urlsplit(src).scheme or src.startswith('//'):
                raise ValueError('External image requires a local copy before publishing: ' + src)
            p = self.resolve(src)
            if p.suffix.lower() not in ('.png', '.jpg', '.jpeg', '.gif', '.webp'):
                raise ValueError('Unsupported image type: ' + src)
            if p.stat().st_size > self.config['max_image_bytes']:
                raise ValueError('Image exceeds size limit: ' + src)
            sha = digest(p.read_bytes())
            self.assets[sha] = p.relative_to(self.root).as_posix()
            attrs = {'src': 'wiki-asset:' + sha, 'alt': attrs.get('alt', '')}
        if tag == 'a':
            href = attrs.get('href', '')
            if href.startswith('wiki-source:') or urlsplit(href).path.endswith('.md'):
                target = href.removeprefix('wiki-source:').split('#')[0]
                try:
                    p = self.resolve(target if target.endswith('.md') else target + '.md')
                    key = self.selected.get(p)
                except ValueError:
                    key = None
                attrs = {'href': 'wiki-note:' + key} if key else {'data-wiki-unpublished': 'true'}
                if not key:
                    self.warnings.append('Unpublished link rendered as text: ' + target)
        self.output.append('<' + tag + ''.join(' ' + k + '="' + html.escape(v or '', quote=True) + '"' for k,v in attrs.items()) + '>')

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag not in ('img', 'br', 'hr', 'input', 'meta', 'link'):
            self.output.append('</' + tag + '>')

    def handle_data(self, data):
        self.output.append(data)

    def handle_entityref(self, name):
        self.output.append('&' + name + ';')

    def handle_charref(self, name):
        self.output.append('&#' + name + ';')


def build(root, config):
    if config.get('status') != 'draft':
        raise ValueError('Initial sync supports drafts only; publish after review in WordPress')
    selected, keys = {}, set()
    for item in config['notes']:
        key = item['id']
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]{2,79}', key) or key in keys:
            raise ValueError('Invalid or duplicate note id')
        path = inside_wiki(root, root / item['path'])
        if path in selected:
            raise ValueError('Duplicate note path')
        selected[path] = key
        keys.add(key)
    posts, assets, warnings, missing = [], {}, [], []
    for path, key in selected.items():
        if not path.exists():
            missing.append(key)
            continue
        if path.suffix != '.md' or path.stat().st_size > config['max_note_bytes']:
            raise ValueError('Invalid or oversized Markdown: ' + str(path))
        text = path.read_text(encoding='utf-8-sig')
        if any(rx.search(text) for _,rx in PATTERNS):
            raise ValueError('Possible credential in selected note; refusing batch: ' + str(path))
        text = re.sub(r'\A---\s*\n.*?\n---\s*\n', '', text, count=1, flags=re.S)
        if len(re.sub(r'\W', '', text)) < 80:
            warnings.append('Skipped empty/short note: ' + str(path.relative_to(root)))
            continue
        heading = re.search(r'^#\s+(.+)$', text, re.M)
        title = heading.group(1).strip() if heading else path.stem
        if heading:
            text = text[:heading.start()] + text[heading.end():]
        renderer = AssetsAndLinks(root, path, selected, config)
        renderer.feed(markdown.markdown(text, extensions=['fenced_code','tables','sane_lists',WikiExtension()]))
        body = ''.join(renderer.output)
        posts.append(dict(key=key, path=path.relative_to(root).as_posix(), title=title,
                          category=path.relative_to(root / 'wiki').parts[0], html=body))
        assets.update(renderer.assets)
        warnings.extend(renderer.warnings)
    return dict(version=1, site_url=config['site_url'], author_id=config['author_id'],
                repo=str(root.resolve()), max_image_bytes=config['max_image_bytes'],
                posts=posts, assets=assets, missing=missing, warnings=warnings)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--config', type=pathlib.Path, default=ROOT / 'config/blog-sync.yml')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--report', type=pathlib.Path, default=ROOT / '.blog-sync/report.json')
    args = ap.parse_args()
    config = yaml.safe_load(args.config.read_text(encoding='utf-8'))
    payload = build(ROOT, config)
    if args.apply:
        command = [config['php_binary'], str(ROOT / 'scripts/wordpress_import.php'), config['wordpress_root']]
        if hasattr(os, 'geteuid') and os.geteuid() == 0:
            command = ['runuser', '-u', config['wordpress_user'], '--', *command]
        result = subprocess.run(command, input=json.dumps(payload, ensure_ascii=False),
                                text=True, encoding='utf-8', capture_output=True, timeout=300)
        if result.returncode != 0:
            raise RuntimeError('WordPress importer failed: ' + result.stderr[-1200:])
        report = json.loads(result.stdout)
    else:
        report = dict(mode='preview', posts=[{k:p[k] for k in ('key','path','title','category')} for p in payload['posts']],
                      images=len(payload['assets']))
    report['warnings'] = payload['warnings']
    report['missing'] = payload['missing']
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report.get('conflicts') or report.get('errors') or payload['missing'] else 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
