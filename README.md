# PinCode

PinCode is a Windows-first development environment for building websites and applications for Pin Browser. It combines a VS Code-inspired editor, a local project workspace, a terminal panel, cloud synchronization, and publishing to the `.pin` namespace.

## Current foundation
- Monaco Editor (loaded from CDN) with language selection and browser-side diagnostics.
- Local project files in the browser workspace using IndexedDB; export/import project folders as ZIP is planned.
- FastAPI + MongoDB API for account-scoped cloud project sync and `.pin` publishing.
- Terminal UI currently supports safe PinCode helper commands. It does **not** run arbitrary Bash or PowerShell commands in the browser.
- AI integration is provided through a server-side endpoint placeholder; configure a provider key as an environment variable before enabling it.

## Run the API
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:MONGODB_URI="mongodb://127.0.0.1:27017"
$env:PINCODE_SECRET="replace-with-a-long-random-secret"
uvicorn app:app --reload
```

Set `PINCODE_DATABASE` optionally (default: `pincode`).

## Run the desktop shell
Install Node.js LTS and Rust, then from the project root:
```powershell
npm install
npm run tauri dev
```
The current UI can also be opened directly from `frontend/index.html` for a quick preview. The Tauri desktop shell is a starter and requires the Rust toolchain.

## Important
A `.pin` address is an application-level domain handled by Pin Browser/PinCode, not a public DNS domain by itself. Public access requires a resolver/hosting service and routing configuration. Cloud sync and publishing require a configured MongoDB connection and a valid account session.
