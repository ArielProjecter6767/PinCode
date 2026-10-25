# Security checklist

PinCode is an early development scaffold. Do not deploy its cloud API for private projects until these items are addressed.

- The current `X-PinCode-User` header is a development placeholder, not authentication. A caller can impersonate another user by changing it. Replace it with a verified Pinian Federation session or signed short-lived token.
- Restrict CORS to the exact deployed application origins.
- Keep MongoDB credentials and AI provider keys only in backend environment variables.
- Add rate limits, request size limits at the reverse proxy, and audit logs.
- Treat terminal commands and AI-generated code as untrusted. Ask for explicit approval before executing commands or applying large changes.
- Run user server projects in isolated containers or sandboxes with CPU, memory, network, filesystem, and time limits.
- Published `.pin` names must be unique and resolved by the Pin Browser server. The current API stores content but does not configure public DNS.
- Add backups and restore tests before using cloud storage for important work.
