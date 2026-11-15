# Security

RIFT is a retrieval service, not an exploitation framework. It has no shell
execution tool, no arbitrary file-write tool, and no required cloud API.

Security properties:

- HTTP defaults to loopback.
- Query-time retrieval opens the index read-only.
- Input JSONL, IDs, counts, and embedding dimensions are validated.
- Archive members are checked before extraction.

The HTTP transport is unauthenticated. Do not bind it to a public interface
without putting it behind authentication, authorization, network controls,
and TLS appropriate to the deployment. Retrieved text should be treated as
untrusted data: do not execute commands or follow target-specific instructions
without independent authorization and review.

Report vulnerabilities privately through the process in `SECURITY.md` at the
repository root. Please do not include live target data in reports.
