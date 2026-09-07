#!/usr/bin/env bash
# Dedicated checkout and lock: never resets /root/note-worker or touches the live blog code.
set -euo pipefail
umask 022
ref="${1:-main}"
mode="${2:-apply}"
[[ "$ref" == main || "$ref" =~ ^[0-9a-f]{40}$ ]] || { echo 'Expected main or a full commit SHA'; exit 2; }
[[ "$mode" == apply || "$mode" == preview ]] || exit 2
base=/opt/wiki-blog-sync
mkdir -p "$base"
exec 9>"$base/sync.lock"
flock -n 9 || { echo 'Another sync is running'; exit 1; }
if [ ! -d "$base/repo.git" ]; then
  git clone --bare https://github.com/wsjwu58-cmd/Obsidian-workFlow.git "$base/repo.git"
fi
git --git-dir="$base/repo.git" fetch origin "$ref"
snapshot=$(mktemp -d "$base/run.XXXXXXXX")
chmod 755 "$snapshot"
# Only remove our own uniquely-created directory under this fixed base.
cleanup() {
  case "$snapshot" in "$base"/run.*) rm -rf -- "$snapshot" ;; *) return 1 ;; esac
}
trap cleanup EXIT
git --git-dir="$base/repo.git" archive FETCH_HEAD | tar -x -C "$snapshot"
if [ ! -x "$base/venv/bin/python" ]; then python3 -m venv "$base/venv"; fi
"$base/venv/bin/python" -m pip install --disable-pip-version-check -r "$snapshot/scripts/requirements-blog.txt"
args=(--report "$base/last-report.json")
if [ "$mode" == apply ]; then args+=(--apply); fi
"$base/venv/bin/python" "$snapshot/scripts/sync_wordpress.py" "${args[@]}"
