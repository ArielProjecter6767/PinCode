from __future__ import annotations

import os
import re
import secrets
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field

MONGODB_URI = os.getenv("MONGODB_URI", "")
DATABASE_NAME = os.getenv("PINCODE_DATABASE", "pincode")
PINCODE_SECRET = os.getenv("PINCODE_SECRET", "")
client: AsyncIOMotorClient | None = AsyncIOMotorClient(MONGODB_URI) if MONGODB_URI else None
db = client[DATABASE_NAME] if client else None

app = FastAPI(title="PinCode Cloud API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("PINCODE_ALLOWED_ORIGINS", "http://localhost:1420,http://127.0.0.1:1420,http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "OPTIONS"],
    allow_headers=["*"],
)

class ProjectSync(BaseModel):
    project_id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=60)
    files: dict[str, str] = Field(default_factory=dict)
    updated_at: str | None = None

class PublishRequest(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    files: dict[str, str] = Field(default_factory=dict)
    entry_file: str = "index.html"

def require_db():
    if db is None:
        raise HTTPException(503, "Cloud database is not configured. Set MONGODB_URI.")
    return db

def owner_id(x_pincode_user: str | None) -> str:
    # Identity must come from a verified portal session in production. This starter
    # uses a required opaque client identity and must be replaced with shared auth.
    if not x_pincode_user or len(x_pincode_user) > 160:
        raise HTTPException(401, "Sign in to Pinian Federation or configure a verified PinCode session.")
    return x_pincode_user

def clean_site_name(name: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9-]", "-", name.strip().lower()).strip("-")
    if not value or not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,38}[a-z0-9])?", value):
        raise HTTPException(400, "Invalid site name. Use letters, numbers and hyphens.")
    return value

def validate_files(files: dict[str, str]) -> dict[str, str]:
    if len(files) > 300:
        raise HTTPException(413, "A project can contain at most 300 files.")
    total = 0
    clean: dict[str, str] = {}
    for path, content in files.items():
        path = path.replace("\\", "/").strip("/")
        if not path or path.startswith(".git/") or ".." in path.split("/") or len(path) > 240:
            raise HTTPException(400, f"Unsafe file path: {path}")
        if not isinstance(content, str):
            raise HTTPException(400, f"File content must be text: {path}")
        total += len(content.encode("utf-8"))
        clean[path] = content
    if total > 2_000_000:
        raise HTTPException(413, "Project size exceeds 2 MB for this starter API.")
    return clean

@app.get("/health")
async def health():
    return {"ok": True, "service": "PinCode Cloud API", "database_configured": db is not None}

@app.put("/api/projects/sync")
async def sync_project(payload: ProjectSync, x_pincode_user: str | None = Header(default=None)):
    database = require_db()
    owner = owner_id(x_pincode_user)
    files = validate_files(payload.files)
    now = datetime.now(timezone.utc).isoformat()
    await database.projects.update_one(
        {"owner_id": owner, "project_id": payload.project_id},
        {"$set": {"owner_id": owner, "project_id": payload.project_id, "name": payload.name,
                  "files": files, "updated_at": now}},
        upsert=True,
    )
    return {"ok": True, "project_id": payload.project_id, "updated_at": now}

@app.get("/api/projects")
async def list_projects(x_pincode_user: str | None = Header(default=None)):
    database = require_db()
    owner = owner_id(x_pincode_user)
    cursor = database.projects.find({"owner_id": owner}, {"_id": 0, "files": 0})
    return {"projects": await cursor.to_list(length=200)}

@app.get("/api/projects/{project_id}")
async def get_project(project_id: str, x_pincode_user: str | None = Header(default=None)):
    database = require_db()
    owner = owner_id(x_pincode_user)
    project = await database.projects.find_one({"owner_id": owner, "project_id": project_id}, {"_id": 0})
    if not project:
        raise HTTPException(404, "Project not found")
    return project

@app.post("/api/publish")
async def publish_site(payload: PublishRequest, x_pincode_user: str | None = Header(default=None)):
    database = require_db()
    owner = owner_id(x_pincode_user)
    name = clean_site_name(payload.name)
    files = validate_files(payload.files)
    if payload.entry_file not in files:
        raise HTTPException(400, f"Entry file '{payload.entry_file}' was not found.")
    if not payload.entry_file.lower().endswith((".html", ".htm")):
        raise HTTPException(400, "The entry file must be HTML.")
    existing = await database.sites.find_one({"name": name})
    if existing and existing.get("owner_id") != owner:
        suggestions = [f"{name}-site", f"{name}-app", f"{name}-2"]
        raise HTTPException(409, detail={"message": f"{name}.pin is already taken.", "alternatives": suggestions})
    now = datetime.now(timezone.utc).isoformat()
    await database.sites.update_one(
        {"name": name, "owner_id": owner},
        {"$set": {"name": name, "owner_id": owner, "files": files,
                  "entry_file": payload.entry_file, "published_at": now, "updated_at": now}},
        upsert=True,
    )
    return {"ok": True, "url": f"http://{name}.pin", "name": name, "published_at": now,
            "note": "Stored in PinCode cloud. Public .pin resolution requires a configured Pin Browser resolver."}

@app.get("/api/sites/{name}")
async def read_published_site(name: str):
    database = require_db()
    site = await database.sites.find_one({"name": clean_site_name(name)}, {"_id": 0, "owner_id": 0})
    if not site:
        raise HTTPException(404, "Site not found")
    return site

@app.post("/api/ai/fix")
async def ai_fix(payload: dict[str, Any]):
    # Deliberately disabled until a trusted provider and secret are configured.
    if not os.getenv("PINCODE_AI_API_KEY"):
        raise HTTPException(503, "AI is not configured yet. Set PINCODE_AI_API_KEY and implement the provider adapter.")
    raise HTTPException(501, "AI provider adapter is not implemented in this starter.")
