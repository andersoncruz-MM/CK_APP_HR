"""
Chicken Kitchen HR — Supabase database client.
Handles all CRUD operations for verifications, applications, and documents.
"""

import os
import secrets
from datetime import datetime, timezone
from supabase import create_client, Client


def _get_client() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_KEY"]
    return create_client(url, key)


db: Client | None = None


def get_db() -> Client:
    global db
    if db is None:
        db = _get_client()
    return db


# ── Verifications ──

def save_verification(email: str, code: str, ip: str = "") -> dict:
    return (
        get_db()
        .table("verifications")
        .insert({"email": email, "code": code, "ip_address": ip})
        .execute()
        .data[0]
    )


def check_verification(email: str, code: str) -> dict | None:
    """Find the most recent unverified code for this email. Return row or None."""
    rows = (
        get_db()
        .table("verifications")
        .select("*")
        .eq("email", email)
        .eq("code", code)
        .is_("verified_at", "null")
        .order("sent_at", desc=True)
        .limit(1)
        .execute()
        .data
    )
    if not rows:
        return None
    row = rows[0]
    # Mark as verified
    get_db().table("verifications").update(
        {"verified_at": datetime.now(timezone.utc).isoformat()}
    ).eq("id", row["id"]).execute()
    return row


# ── Applications ──

def create_application(
    email: str,
    name: str,
    phone: str,
    store_code: str,
    store_name: str,
    signature_b64: str,
) -> dict:
    admin_token = secrets.token_urlsafe(32)
    return (
        get_db()
        .table("applications")
        .insert({
            "email": email,
            "name": name,
            "phone": phone,
            "store_code": store_code,
            "store_name": store_name,
            "signature_b64": signature_b64,
            "admin_token": admin_token,
        })
        .execute()
        .data[0]
    )


def get_application(app_id: str) -> dict | None:
    rows = (
        get_db()
        .table("applications")
        .select("*")
        .eq("id", app_id)
        .limit(1)
        .execute()
        .data
    )
    return rows[0] if rows else None


def get_application_by_token(token: str) -> dict | None:
    rows = (
        get_db()
        .table("applications")
        .select("*")
        .eq("admin_token", token)
        .limit(1)
        .execute()
        .data
    )
    return rows[0] if rows else None


def get_pending_applications(store_code: str) -> list[dict]:
    return (
        get_db()
        .table("applications")
        .select("id, email, name, phone, store_name, created_at, status")
        .eq("store_code", store_code)
        .eq("status", "pending")
        .order("created_at", desc=True)
        .execute()
        .data
    )


def approve_application(app_id: str, approved_by: str) -> dict | None:
    rows = (
        get_db()
        .table("applications")
        .update({
            "status": "approved",
            "approved_at": datetime.now(timezone.utc).isoformat(),
            "approved_by": approved_by,
        })
        .eq("id", app_id)
        .eq("status", "pending")
        .execute()
        .data
    )
    return rows[0] if rows else None


# ── Documents ──

def save_document(application_id: str, filename: str, doc_type: str, file_b64: str) -> dict:
    return (
        get_db()
        .table("documents")
        .insert({
            "application_id": application_id,
            "filename": filename,
            "doc_type": doc_type,
            "file_b64": file_b64,
        })
        .execute()
        .data[0]
    )


def get_documents(application_id: str) -> list[dict]:
    return (
        get_db()
        .table("documents")
        .select("id, filename, doc_type, file_b64, created_at")
        .eq("application_id", application_id)
        .execute()
        .data
    )
