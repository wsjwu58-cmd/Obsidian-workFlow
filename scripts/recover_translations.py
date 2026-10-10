"""Read-only recovery of a pending translation batch from worker files and Git blobs."""
import argparse
import io
import json
import pathlib
import re
import subprocess
import tarfile


def queue_rows(text):
    match = re.search(r"<!-- pending:start -->(.*?)<!-- pending:end -->", text, re.S)
    rows = []
    for line in match.group(1).splitlines() if match else []:
        cells = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and cells[1].startswith(("https://", "http://")):
            title, url = cells[:2]
            slug = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", title)[:40].strip("-") or "item"
            rows.append({"title": title, "url": url, "name": slug + "-translation.md"})
    return rows


def translation_urls(data):
    text = data.decode("utf-8", "replace").lstrip("\ufeff")
    front = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not front or not all(re.search(rf"^{key}:.*", front[1], re.M)
                            for key in ("created", "updated", "sources", "tags")):
        return set()
    # Indexes and source captures must never stand in for an existing translation.
    if not re.search(r"translatedAt:|type/翻译|type/translation|sourceUrl:", front[1], re.I):
        return set()
    return set(re.findall(r"https?://[^\s\]\)\"'<>，]+", text[:6000]))


def recover(root, output, expected_count):
    root = pathlib.Path(root).resolve()

    def git(*args):
        return subprocess.run(["git", *args], cwd=root, capture_output=True, check=True).stdout

    queue = git("show", "origin/pipeline/queue:references/articles.md")
    rows = queue_rows(queue.decode("utf-8"))
    if len(rows) != expected_count or len({row['name'] for row in rows}) != len(rows):
        raise ValueError(f"Expected {expected_count} distinct pending translations, got {len(rows)}")
    matches = {row['name']: {} for row in rows}

    def inspect(data, origin, filename=None):
        urls = translation_urls(data)
        for row in rows:
            if row['url'] in urls and (filename is None or filename == row['name']):
                # Identical recovered copies are one candidate, regardless of origin.
                matches[row['name']].setdefault(data, origin)

    for row in rows:
        path = root / "working" / row['name']
        if path.is_file():
            inspect(path.read_bytes(), str(path), row['name'])
    candidates = root / ".pipeline" / "candidates"
    for path in candidates.glob("*/works-ready/*-translation.md"):
        inspect(path.read_bytes(), str(path), path.name)

    fsck = subprocess.run(["git", "fsck", "--no-reflogs", "--unreachable"], cwd=root,
                          capture_output=True, text=True)
    hashes = re.findall(r"(?:unreachable|dangling) blob ([0-9a-f]{40,64})", fsck.stdout)
    # Filter by size before reading blobs; images and large binary assets are excluded.
    if hashes:
        sizes = subprocess.run(
            ["git", "cat-file", "--batch-check"], cwd=root,
            input=("\n".join(hashes) + "\n").encode(), capture_output=True, check=True).stdout.decode()
        eligible = [line.split()[0] for line in sizes.splitlines()
                    if len(line.split()) == 3 and line.split()[1] == "blob"
                    and 200 <= int(line.split()[2]) <= 500000]
        with subprocess.Popen(["git", "cat-file", "--batch"], cwd=root,
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE) as process:
            for obj in eligible:
                process.stdin.write((obj + "\n").encode())
                process.stdin.flush()
                header = process.stdout.readline().split()
                data = process.stdout.read(int(header[2]))
                process.stdout.read(1)
                inspect(data, "git-blob:" + obj)
            process.stdin.close()
            process.wait()

    manifest = {"expected": expected_count, "recovered": [], "missing": [], "ambiguous": []}
    payloads = {"queue.md": queue}
    for row in rows:
        options = matches[row['name']]
        if len(options) == 1:
            data, origin = next(iter(options.items()))
            payloads['working/' + row['name']] = data
            manifest['recovered'].append({**row, "origin": origin, "bytes": len(data)})
        elif options:
            manifest['ambiguous'].append({**row, "origins": list(options.values())})
        else:
            manifest['missing'].append(row)
    payloads['manifest.json'] = json.dumps(manifest, ensure_ascii=False, indent=2).encode()
    with tarfile.open(output, "w:gz") as archive:
        for name, data in payloads.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mode = 0o600
            archive.addfile(info, io.BytesIO(data))
    print(json.dumps({"recovered": len(manifest['recovered']), "missing": manifest['missing'],
                      "ambiguous": manifest['ambiguous']}, ensure_ascii=False), flush=True)
    return 1 if manifest['missing'] or manifest['ambiguous'] else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--expected-count", type=int, default=22)
    args = parser.parse_args()
    raise SystemExit(recover(args.root, args.output, args.expected_count))
