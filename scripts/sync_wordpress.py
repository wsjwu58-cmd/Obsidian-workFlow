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
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

import markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
import yaml

from scan_secrets import PATTERNS

ROOT = pathlib.Path(__file__).resolve().parent.parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def external_host_allowed(host, configured_hosts):
    """Allow an exact host or a real subdomain of a configured host."""
    host = (host or '').lower().rstrip('.')
    for candidate in configured_hosts or []:
        candidate = str(candidate).lower().strip().lstrip('.').rstrip('.')
        if host == candidate or host.endswith('.' + candidate):
            return True
    return False


def image_extension(data, content_type='', path=''):
    """Return a safe extension only for bytes that look like a supported image."""
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'png'
    if data.startswith(b'\xff\xd8\xff'):
        return 'jpg'
    if data.startswith((b'GIF87a', b'GIF89a')):
        return 'gif'
    if len(data) >= 12 and data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return 'webp'
    # Some CDNs return a generic content type, so use the URL extension only
    # after the byte signatures have been checked by the importer.
    suffix = pathlib.PurePosixPath(urlsplit(path).path).suffix.lower().lstrip('.')
    if suffix in ('png', 'jpg', 'jpeg', 'gif', 'webp'):
        return 'jpg' if suffix == 'jpeg' else suffix
    return None


def download_external_image(root, source, config, cache):
    """Download an allowlisted image into the ephemeral sync snapshot.

    The snapshot is removed by run_blog_sync.sh after the CLI importer exits;
    WordPress receives the bytes through the same local-media path as wiki
    attachments. No external URL is persisted in post content.
    """
    normalized = 'https:' + source if source.startswith('//') else source
    parts = urlsplit(normalized)
    if parts.scheme not in ('http', 'https'):
        raise ValueError('unsupported URL scheme')
    if not external_host_allowed(parts.hostname, config.get('external_image_hosts')):
        raise ValueError('external image host is not allowlisted')
    if normalized in cache:
        return cache[normalized]

    max_bytes = min(int(config.get('max_external_image_bytes', config['max_image_bytes'])), 10485760)
    request = Request(normalized, headers={
        'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
        'User-Agent': 'wiki-blog-sync/1.0 (+https://www.wsjaly.cn/)'
    })
    try:
        with urlopen(request, timeout=float(config.get('external_image_timeout', 20))) as response:
            final = urlsplit(response.geturl())
            if final.scheme not in ('http', 'https') or not external_host_allowed(
                final.hostname, config.get('external_image_hosts')
            ):
                raise ValueError('redirected to a non-allowlisted image host')
            length = response.headers.get('Content-Length')
            if length and int(length) > max_bytes:
                raise ValueError('image exceeds size limit')
            data = response.read(max_bytes + 1)
            if hasattr(response.headers, 'get_content_type'):
                content_type = response.headers.get_content_type()
            else:
                content_type = response.headers.get('Content-Type', '').split(';', 1)[0].strip().lower()
    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        if isinstance(exc, ValueError):
            raise
        raise ValueError('download failed: ' + str(exc)) from exc
    if len(data) > max_bytes:
        raise ValueError('image exceeds size limit')
    extension = image_extension(data, content_type, final.path)
    if not extension:
        raise ValueError('response is not a supported image')

    sha = digest(data)
    staging = root / '.blog-sync-external'
    staging.mkdir(exist_ok=True)
    target = staging / ('external-' + sha + '.' + extension)
    if not target.exists():
        target.write_bytes(data)
    result = sha, target.relative_to(root).as_posix()
    cache[normalized] = result
    return result


def discover_notes(root, config):
    """Return every publishable Markdown note under wiki, grouped by top folder."""
    wiki = (root / 'wiki').resolve()
    excluded = set(config.get('exclude_categories', []))
    items = []
    for path in sorted(wiki.rglob('*')):
        if not path.is_file() or path.suffix.lower() != '.md':
            continue
        relative = path.relative_to(wiki)
        if any(part.startswith('.') for part in relative.parts):
            continue
        category = relative.parts[0] if len(relative.parts) > 1 else '未分类'
        if category in excluded:
            continue
        relative_repo = path.relative_to(root).as_posix()
        # A path-derived key stays stable while the note content changes and
        # keeps two notes with the same title distinct.
        key = 'note-' + hashlib.sha256(relative_repo.encode('utf-8')).hexdigest()[:32]
        items.append({'id': key, 'path': relative_repo})
    return items


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
    def __init__(self, root, note, selected, config, external_cache):
        super().__init__(convert_charrefs=False)
        self.root, self.note, self.selected, self.config = root, note, selected, config
        self.external_cache = external_cache
        self.output, self.assets, self.warnings = [], {}, []

    def omit_image(self, src, reason):
        self.warnings.append('Image omitted: ' + src + ' (' + reason + ')')
        self.output.append('<p>[图片未同步]</p>')

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
                if urlsplit(src).scheme not in ('http', 'https') and not src.startswith('//'):
                    self.omit_image(src, 'unsupported URL scheme')
                    return
                try:
                    sha, relative = download_external_image(self.root, src, self.config, self.external_cache)
                    self.assets[sha] = relative
                    attrs = {'src': 'wiki-asset:' + sha, 'alt': attrs.get('alt', '')}
                except (OSError, ValueError) as exc:
                    self.omit_image(src, str(exc))
                    return
            else:
                try:
                    p = self.resolve(src)
                    if p.suffix.lower() not in ('.png', '.jpg', '.jpeg', '.gif', '.webp'):
                        self.omit_image(src, 'unsupported image type')
                        return
                    if p.stat().st_size > self.config['max_image_bytes']:
                        self.omit_image(src, 'image exceeds size limit')
                        return
                    sha = digest(p.read_bytes())
                    self.assets[sha] = p.relative_to(self.root).as_posix()
                    attrs = {'src': 'wiki-asset:' + sha, 'alt': attrs.get('alt', '')}
                except ValueError as exc:
                    self.omit_image(src, str(exc))
                    return
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
    if config.get('status') not in ('draft', 'publish'):
        raise ValueError('Sync status must be draft or publish')
    selected, keys = {}, set()
    configured_notes = config.get('notes')
    note_items = discover_notes(root, config) if configured_notes in (None, [], 'auto') else configured_notes
    for item in note_items:
        key = item['id']
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]{2,79}', key) or key in keys:
            raise ValueError('Invalid or duplicate note id')
        path = inside_wiki(root, root / item['path'])
        if path in selected:
            raise ValueError('Duplicate note path')
        selected[path] = key
        keys.add(key)
    posts, assets, warnings, missing = [], {}, [], []
    external_cache = {}
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
        renderer = AssetsAndLinks(root, path, selected, config, external_cache)
        renderer.feed(markdown.markdown(text, extensions=['fenced_code','tables','sane_lists',WikiExtension()]))
        body = ''.join(renderer.output)
        posts.append(dict(key=key, path=path.relative_to(root).as_posix(), title=title,
                          category=path.relative_to(root / 'wiki').parts[0], html=body))
        assets.update(renderer.assets)
        warnings.extend(renderer.warnings)
    return dict(version=1, site_url=config['site_url'], status=config['status'], author_id=config['author_id'],
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
