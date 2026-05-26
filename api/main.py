"""
Chicken Kitchen HR — FastAPI Backend.
Serves the web frontend and provides API endpoints for:
  - Email verification
  - Application submission
  - Admin review & approval
"""

import os
import random
import string
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr

from api.store_data import STORES, get_store, get_store_choices
from api import database as db
from api import email_service as email

app = FastAPI(title="Chicken Kitchen HR", docs_url="/api/docs")

# ─── Static files (served at root so relative CSS/JS paths work) ───
WEB_DIR = Path(__file__).resolve().parent.parent / "web"


@app.get("/")
async def root():
    return RedirectResponse("/web/index.html")


# Mount AFTER the root route so /api/* routes take priority
app.mount("/web", StaticFiles(directory=str(WEB_DIR)), name="web")


# ─── Models ───

class VerifySendReq(BaseModel):
    email: EmailStr

class VerifyCheckReq(BaseModel):
    email: EmailStr
    code: str

class ApplyReq(BaseModel):
    email: EmailStr
    name: str
    phone: str = ""
    store_code: str
    signature_b64: str
    pdfs: dict[str, str]       # {filename: base64}
    docs: dict[str, str] = {}  # {filename: base64}

class ApproveReq(BaseModel):
    approved_by: str


# ─── Endpoints ───

@app.get("/api/stores")
async def list_stores():
    """Return store list for dropdown."""
    return get_store_choices()


@app.get("/api/store/{code}")
async def store_detail(code: str):
    """Return full store info for auto-fill."""
    store = get_store(code)
    if not store:
        raise HTTPException(404, "Store not found")
    return store


@app.post("/api/verify/send")
async def verify_send(req: VerifySendReq, request: Request):
    """Generate and send 6-digit verification code."""
    code = "".join(random.choices(string.digits, k=6))
    ip = request.client.host if request.client else ""
    db.save_verification(req.email, code, ip)
    try:
        email.send_verification_code(req.email, code)
    except Exception as e:
        raise HTTPException(500, f"Email error: {e}")
    return {"ok": True, "message": "Code sent"}


@app.post("/api/verify/check")
async def verify_check(req: VerifyCheckReq):
    """Validate verification code."""
    row = db.check_verification(req.email, req.code)
    if not row:
        raise HTTPException(400, "Invalid or expired code")
    return {"ok": True, "email": req.email}


@app.post("/api/apply")
async def apply(req: ApplyReq, request: Request):
    """Submit full application: save to DB, send emails."""
    store = get_store(req.store_code)
    if not store:
        raise HTTPException(400, "Invalid store code")

    # Save application
    application = db.create_application(
        email=req.email,
        name=req.name,
        phone=req.phone,
        store_code=req.store_code,
        store_name=store["name"],
        signature_b64=req.signature_b64,
    )
    app_id = application["id"]
    admin_token = application["admin_token"]

    # Save all documents (PDFs + identity docs)
    all_docs = []
    for filename, b64 in req.pdfs.items():
        doc = db.save_document(app_id, filename, "form_pdf", b64)
        all_docs.append({"filename": filename, "file_b64": b64})
    for filename, b64 in req.docs.items():
        doc = db.save_document(app_id, filename, "identity_doc", b64)
        all_docs.append({"filename": filename, "file_b64": b64})

    # Build review link for admin
    base_url = os.environ.get("APP_BASE_URL", str(request.base_url).rstrip("/"))
    review_link = f"{base_url}/web/admin.html?token={admin_token}"

    # Send emails
    try:
        email.send_applicant_pending(req.email, req.name, store["name"])
    except Exception:
        pass  # non-blocking — applicant already sees thank-you screen

    try:
        email.send_admin_review(
            admin_email=store["admin_email"],
            store_name=store["name"],
            applicant_name=req.name,
            applicant_email=req.email,
            applicant_phone=req.phone,
            review_link=review_link,
            documents=all_docs,
        )
    except Exception:
        pass  # non-blocking

    return {"ok": True, "application_id": app_id}


@app.get("/api/admin/review")
async def admin_review(token: str):
    """Get application details for admin review page."""
    application = db.get_application_by_token(token)
    if not application:
        raise HTTPException(404, "Application not found or invalid token")

    documents = db.get_documents(application["id"])

    return {
        "application": {
            "id": application["id"],
            "name": application["name"],
            "email": application["email"],
            "phone": application["phone"],
            "store_code": application["store_code"],
            "store_name": application["store_name"],
            "status": application["status"],
            "created_at": application["created_at"],
            "signature_b64": application["signature_b64"],
        },
        "documents": [
            {"id": d["id"], "filename": d["filename"], "doc_type": d["doc_type"]}
            for d in documents
        ],
    }


@app.get("/api/admin/document/{doc_id}")
async def admin_get_document(doc_id: str, token: str):
    """Download a specific document (verified via admin token)."""
    application = db.get_application_by_token(token)
    if not application:
        raise HTTPException(403, "Invalid token")

    documents = db.get_documents(application["id"])
    doc = next((d for d in documents if d["id"] == doc_id), None)
    if not doc:
        raise HTTPException(404, "Document not found")

    return {"filename": doc["filename"], "file_b64": doc["file_b64"]}


@app.post("/api/admin/approve/{app_id}")
async def admin_approve(app_id: str, req: ApproveReq, token: str):
    """Approve application and notify HR (Adela)."""
    application = db.get_application_by_token(token)
    if not application or application["id"] != app_id:
        raise HTTPException(403, "Invalid token")

    if application["status"] != "pending":
        raise HTTPException(400, f"Application already {application['status']}")

    updated = db.approve_application(app_id, req.approved_by)
    if not updated:
        raise HTTPException(500, "Failed to approve")

    # Get all documents to attach in HR email
    documents = db.get_documents(app_id)
    doc_list = [{"filename": d["filename"], "file_b64": d["file_b64"]} for d in documents]

    try:
        email.send_hr_approved(
            store_name=application["store_name"],
            approved_by=req.approved_by,
            applicant_name=application["name"],
            applicant_email=application["email"],
            documents=doc_list,
        )
    except Exception:
        pass  # logged but non-blocking

    return {"ok": True, "status": "approved"}
