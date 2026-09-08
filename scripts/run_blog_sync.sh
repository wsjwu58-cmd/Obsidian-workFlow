#!/usr/bin/env bash
# Dedicated checkout and lock: never resets /root/note-worker or touches the live blog code.
set -euo pipefail
umask 022
ref="${1:-main}"
mode="${2:-apply}"
[[ "$ref" == main || "$ref" =~ ^[0-9a-f]{40}$ ]] || { echo 'Expected main or a full commit SHA'; exit 2; }
[[ "$mode" == apply || "$mode" == preview ]] || exit 2
base=/opt/wiki-blog-sync
source_repo=${NOTE_SOURCE_REPO:-/root/note-worker}
mkdir -p "$base"
exec 9>"$base/sync.lock"
flock -n 9 || { echo 'Another sync is running'; exit 1; }
if [ ! -d "$source_repo/.git" ]; then
  echo "Source repository not found: $source_repo" >&2
  exit 1
fi
if ! git -C "$source_repo" cat-file -e "$ref^{commit}" 2>/dev/null; then
  # The scheduled job passes an exact main commit. Fetch the advertised branch
  # first; GitHub may not advertise an arbitrary SHA as a fetchable ref.
  git -C "$source_repo" -c http.version=HTTP/1.1 fetch --no-tags origin main
fi
if ! git -C "$source_repo" cat-file -e "$ref^{commit}" 2>/dev/null; then
  git -C "$source_repo" -c http.version=HTTP/1.1 fetch --no-tags origin "$ref"
fi
snapshot=$(mktemp -d "$base/run.XXXXXXXX")
chmod 755 "$snapshot"
# Only remove our own uniquely-created directory under this fixed base.
cleanup() {
  case "$snapshot" in "$base"/run.*) rm -rf -- "$snapshot" ;; *) return 1 ;; esac
}
trap cleanup EXIT
git -C "$source_repo" archive "$ref" | tar -x -C "$snapshot"
# Keep site presentation code in the same reviewed commit as the importer.
# The must-use plugin survives WordPress theme changes and is safe to replace
# idempotently on every sync.
mkdir -p /www/wwwroot/www.wsjaly.cn/wp-content/mu-plugins
install -o www -g www -m 0644 "$snapshot/scripts/wordpress_blog_features.php" \
  /www/wwwroot/www.wsjaly.cn/wp-content/mu-plugins/wiki-blog-features.php
install -o www -g www -m 0644 "$snapshot/scripts/wordpress_blog_front_page.php" \
  /www/wwwroot/www.wsjaly.cn/wp-content/mu-plugins/wiki-blog-front-page.php
if [ ! -x "$base/venv/bin/python" ]; then python3 -m venv "$base/venv"; fi
"$base/venv/bin/python" -m pip install --disable-pip-version-check -r "$snapshot/scripts/requirements-blog.txt"
args=(--report "$base/last-report.json")
if [ "$mode" == apply ]; then args+=(--apply); fi
"$base/venv/bin/python" "$snapshot/scripts/sync_wordpress.py" "${args[@]}"
