# PinCode implementation roadmap

## Starter foundation committed
- VS Code-inspired workspace and Monaco syntax highlighting.
- File creation/editing and browser-local persistence.
- Safe terminal helper commands.
- FastAPI endpoints for project sync and publishing.
- MongoDB storage and Tauri 2 Windows shell scaffold.

## Next implementation milestones
1. Integrate Pinian Federation login using a verified shared session; do not trust a client-supplied user ID in production.
2. Add a real local filesystem bridge and project open/save dialogs through Tauri APIs.
3. Bundle Monaco and other assets locally for offline use and a more reliable Windows installer.
4. Add a real terminal process with explicit command approval, working-directory restrictions, and safe environment handling.
5. Connect a selected AI provider server-side and require confirmation before applying edits or running commands.
6. Connect Pin Browser's server-side resolver to published `.pin` projects.
7. Add conflict-aware sync, backups/version history, project restore, and automated tests.
8. Add Python/Node server project templates and isolated deployment/runtime support.

## Security notes
The current cloud API uses a temporary `X-PinCode-User` header to unblock development. It is not authentication and must not be exposed as a production deployment. Replace it with a verified portal session or signed, short-lived access token before storing private user projects.
