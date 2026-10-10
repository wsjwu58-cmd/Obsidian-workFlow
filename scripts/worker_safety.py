"""Save dirty worker files before checkout/reset; backups stay outside review PRs."""
import argparse
import datetime
import json
import pathlib
import subprocess
import tarfile


def snapshot_worktree(root):
    root = pathlib.Path(root).resolve()

    def git(*args):
        return subprocess.run(["git", *args], cwd=root, check=True,
                              capture_output=True).stdout

    status = git("status", "--porcelain=v1", "--untracked-files=all", "-z")
    if not status:
        return None
    paths = []
    entries = iter(status.decode("utf-8", "surrogateescape").split("\0"))
    for entry in entries:
        if not entry:
            continue
        paths.append(entry[3:])
        if "R" in entry[:2] or "C" in entry[:2]:
            paths.append(next(entries))
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup = root / ".pipeline" / "recovery" / stamp
    backup.mkdir(parents=True, mode=0o700)
    # Fail closed: checkout/reset is allowed only after all backup writes succeed.
    (backup / "unstaged.patch").write_bytes(git("diff", "--binary"))
    (backup / "staged.patch").write_bytes(git("diff", "--cached", "--binary"))
    with tarfile.open(backup / "files.tar.gz", "w:gz", dereference=False) as archive:
        for name in dict.fromkeys(paths):
            path = root / name
            if path.exists() or path.is_symlink():
                archive.add(path, arcname=name, recursive=False)
    (backup / "manifest.json").write_text(json.dumps({
        "head": git("rev-parse", "HEAD").decode().strip(),
        "status": status.decode("utf-8", "replace"),
        "paths": paths,
        "recovery": "Use head + staged/unstaged binary patches and files.tar.gz in a separate checkout.",
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[worker] 已保存未提交成果：{backup}", flush=True)
    return backup


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=pathlib.Path, required=True)
    snapshot_worktree(parser.parse_args().root)
