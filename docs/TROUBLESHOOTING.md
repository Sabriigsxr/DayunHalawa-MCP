# Troubleshooting

**Missing index files:** run `bash scripts/restore_index.sh`, or set
`RIFT_INDEX_DIR` to a directory containing all three required files.

**Checksum failure:** do not extract the archive. Re-download or restore the
repository file and verify `sha256sum data/index.tar.gz` against the recorded
hash.

**Dimension mismatch:** use the embedding model used to build the index, or
build a new authorized index with the selected model.

**Malformed JSONL or count mismatch:** inspect the reported file and line,
then restore the original archive or rebuild all three index artifacts
together. Do not mix files from different builds.

**Model unavailable offline:** remove offline mode only during initial model
setup, then enable `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1` for local-only
operation.

**HTTP client cannot connect:** confirm the process is running, the client
uses `/mcp`, and the configured host and port match. Keep the host on
`127.0.0.1` unless a protected deployment boundary is intentional.
