"""
Chicken Kitchen HR — Supabase database client (REST API via httpx).
No SDK dependency — uses Supabase PostgREST API directly.
"""

import os
import secrets
from datetime import datetime, timezone
import httpx

_url = ""
_key = ""
_headers = {}


def _init():
    global _url, _key, _headers
    if _url:
        return
    _url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    _key = os.environ.get("SUPABASE_KEY", "")
    if not _url or not _key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
    _headers = {
        "apikey": _key,
        "Authorization": f"Bearer {_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def _rest(path: str) -> str:
    _init()
    return f"{_url}/rest/v1/{path}"


# ── Generic helpers ──

def _select(table: str, params: dict) -> list[dict]:
    _init()
    resp = httpx.get(_rest(table), headers=_headers, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def _insert(table: str, data: dict) -> dict:
    _init()
    resp = httpx.post(_rest(table), headers=_headers, json=data, timeout=15)
    resp.raise_for_status()
    rows = resp.json()
    return rows[0] if rows else data


def _update(table: str, data: dict, params: dict) -> list[dict]:
    _init()
    resp = httpx.patch(_rest(table), headers=_headers, json=data, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


# ── Verifications ──

def save_verification(email: str, code: str, ip: str = "") -> dict:
    return _insert("verifications", {"email": email, "code": code, "ip_address": ip})


def check_verification(email: str, code: str) -> dict | None:
    rows = _select("verifications", {
        "select": "*",
        "email": f"eq.{email}",
        "code": f"eq.{code}",
        "verified_at": "is.null",
        "order": "sent_at.desc",
        "limit": "1",
    })
    if not rows:
        return None
    row = rows[0]
    _update("verifications",
        {"verified_at": datetime.now(timezone.utc).isoformat()},
        {"id": f"eq.{row['id']}"},
    )
    return row


# ── Applications ──

def create_application(
    email: str, name: str, phone: str,
    store_code: str, store_name: str, signature_b64: str,
) -> dict:
    admin_token = secrets.token_urlsafe(32)
    return _insert("applications", {
        "email": email, "name": name, "phone": phone,
        "store_code": store_code, "store_name": store_name,
        "signature_b64": signature_b64, "admin_token": admin_token,
    })


def get_application(app_id: str) -> dict | None:
    rows = _select("applications", {"select": "*", "id": f"eq.{app_id}", "limit": "1"})
    return rows[0] if rows else None


def get_application_by_token(token: str) -> dict | None:
    rows = _select("applications", {"select": "*", "admin_token": f"eq.{token}", "limit": "1"})
    return rows[0] if rows else None


def get_pending_applications(store_code: str) -> list[dict]:
    return _select("applications", {
        "select": "id,email,name,phone,store_name,created_at,status",
        "store_code": f"eq.{store_code}",
        "status": "eq.pending",
        "order": "created_at.desc",
    })


def approve_application(app_id: str, approved_by: str) -> dict | None:
    rows = _update("applications", {
        "status": "approved",
        "approved_at": datetime.now(timezone.utc).isoformat(),
        "approved_by": approved_by,
    }, {"id": f"eq.{app_id}", "status": "eq.pending"})
    return rows[0] if rows else None


# ── Documents ──

def save_document(application_id: str, filename: str, doc_type: str, file_b64: str) -> dict:
    return _insert("documents", {
        "application_id": application_id,
        "filename": filename, "doc_type": doc_type, "file_b64": file_b64,
    })


def get_documents(application_id: str) -> list[dict]:
    return _select("documents", {
        "select": "id,filename,doc_type,file_b64,created_at",
        "application_id": f"eq.{application_id}",
    })
