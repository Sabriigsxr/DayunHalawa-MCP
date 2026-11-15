#!/usr/bin/env bash
# Restore the bundled RIFT index from data/index.tar.gz into ./index/
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ARCHIVE="$DIR/data/index.tar.gz"
SUMS="$DIR/data/index.tar.gz.sha256"
DEST="$DIR/index"
FORCE="${1:-}"

if [ -L "$DEST" ]; then
  echo "[!] Refusing to replace symlink destination: $DEST" >&2
  exit 1
fi
if [ -e "$DEST" ] && [ ! -d "$DEST" ]; then
  echo "[!] Refusing to replace non-directory destination: $DEST" >&2
  exit 1
fi
if [ -d "$DEST" ] && [ "$FORCE" != "--force" ]; then
  echo "[✓] ./index already exists; skipping extraction (use --force to overwrite)."
  exit 0
fi

echo "[*] Verifying checksum..."
EXPECTED="$(tr -d '[:space:]' < "$SUMS")"
ACTUAL="$(sha256sum "$ARCHIVE" | awk '{print $1}')"
if [ "$EXPECTED" != "$ACTUAL" ]; then
  echo "[!] SHA-256 mismatch for $ARCHIVE" >&2
  exit 1
fi

echo "[*] Checking archive paths..."
python - "$ARCHIVE" <<'PY'
import posixpath
import sys
import tarfile

archive = sys.argv[1]
with tarfile.open(archive, "r:gz") as tar:
    for member in tar.getmembers():
        normalized = posixpath.normpath(member.name)
        if (
            member.name.startswith("/")
            or normalized == ".."
            or normalized.startswith("../")
            or member.issym()
            or member.islnk()
        ):
            raise SystemExit(f"unsafe archive member: {member.name}")
PY
while IFS= read -r entry; do
  [ "$entry" = "./" ] && continue
  clean="${entry#./}"
  case "$clean" in
    ""|"/"*|"../"*|*/../*|*/..)
      echo "[!] Unsafe archive path: $entry" >&2
      exit 1
      ;;
  esac
done < <(tar -tzf "$ARCHIVE")

TMP="$(mktemp -d "$DIR/.rift-index.XXXXXX")"
cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT
tar -xzf "$ARCHIVE" --no-same-owner -C "$TMP"

for required in faiss.index documents.jsonl metadata.jsonl; do
  [ -f "$TMP/$required" ] || { echo "[!] Missing archive member: $required" >&2; exit 1; }
done

if [ -e "$DEST" ]; then
  rm -rf "$DEST"
fi
mv "$TMP" "$DEST"
trap - EXIT
echo "[✓] Index restored to $DEST"
ls -lh "$DEST"
