#!/usr/bin/env bash
# Restore the bundled offensive-scenario index from data/index.tar.gz into ./index/
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ARCHIVE="$DIR/data/index.tar.gz"
SUMS="$DIR/data/index.tar.gz.sha256"
DEST="$DIR/index"
FORCE="${1:-}"

if [ -L "$DEST" ]; then
  echo "[*] ./index is a symlink -> $(readlink "$DEST"); removing symlink to restore a real directory here."
  rm "$DEST"
fi
if [ -d "$DEST" ] && [ "$FORCE" != "--force" ]; then
  echo "[✓] ./index already exists; skipping extraction (use --force to overwrite)."
  exit 0
fi

echo "[*] Verifying checksum..."
( cd "$DIR/data" && sha256sum -c <(echo "$(cat "$SUMS")  index.tar.gz") )
mkdir -p "$DEST"
tar -xzf "$ARCHIVE" -C "$DEST"
echo "[✓] Index restored to $DEST"
ls -lh "$DEST"
