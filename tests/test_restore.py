import hashlib
import io
import shutil
import subprocess
import tarfile
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "restore_index.sh"


def make_fixture(root, members):
    data = root / "data"
    data.mkdir()
    archive = data / "index.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        for name, contents in members.items():
            if name.startswith(("../", "/")):
                info = tarfile.TarInfo(name)
                info.size = len(contents)
                tar.addfile(info, io.BytesIO(contents))
                continue
            path = root / name.replace("./", "", 1)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(contents)
            tar.add(path, arcname=name)
    (data / "index.tar.gz.sha256").write_text(
        hashlib.sha256(archive.read_bytes()).hexdigest() + "\n",
        encoding="utf-8",
    )
    scripts = root / "scripts"
    scripts.mkdir()
    shutil.copy2(SCRIPT, scripts / SCRIPT.name)
    return scripts / SCRIPT.name


def test_restore_extracts_only_expected_fixture(tmp_path):
    script = make_fixture(
        tmp_path,
        {
            "./faiss.index": b"faiss",
            "./documents.jsonl": b'{"doc_id":"a"}\n',
            "./metadata.jsonl": b'{"doc_id":"a"}\n',
        },
    )
    subprocess.run(["bash", str(script)], check=True, capture_output=True, text=True)
    assert (tmp_path / "index" / "faiss.index").read_bytes() == b"faiss"


def test_restore_rejects_checksum_mismatch(tmp_path):
    script = make_fixture(tmp_path, {"./faiss.index": b"faiss", "./documents.jsonl": b"", "./metadata.jsonl": b""})
    (tmp_path / "data" / "index.tar.gz.sha256").write_text("0" * 64 + "\n", encoding="utf-8")
    result = subprocess.run(["bash", str(script)], check=False, capture_output=True, text=True)
    assert result.returncode != 0
    assert not (tmp_path / "index").exists()


def test_restore_rejects_traversal_member(tmp_path):
    script = make_fixture(
        tmp_path,
        {
            "./faiss.index": b"faiss",
            "./documents.jsonl": b"",
            "./metadata.jsonl": b"",
            "../escape": b"must not extract",
        },
    )
    result = subprocess.run(["bash", str(script)], check=False, capture_output=True, text=True)
    assert result.returncode != 0
    assert not (tmp_path / "index").exists()
