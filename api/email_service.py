"""
Chicken Kitchen HR — Email service.
Centralised email sending for all flows:
  1. Verification code to applicant
  2. "Application pending" to applicant
  3. "Review needed" to store admin
  4. "Application approved" to Adela (HR)
"""

import os
import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

DEST_HR = "adela@chickenkitchen.com"


def _smtp_send(to: str, msg: MIMEMultipart):
    sender = os.environ["SMTP_SENDER"]
    password = os.environ["SMTP_PASSWORD"]
    msg["From"] = sender
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, to, msg.as_string())


def _attach_b64(msg: MIMEMultipart, filename: str, data_b64: str):
    part = MIMEBase("application", "octet-stream")
    part.set_payload(base64.b64decode(data_b64))
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
    msg.attach(part)


# ── 1. Verification Code ──

def send_verification_code(to_email: str, code: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Chicken Kitchen HR - Verification Code"
    msg["To"] = to_email

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:480px;margin:auto;padding:20px;">
      <div style="background:#D32F2F;padding:18px;text-align:center;border-radius:10px 10px 0 0;">
        <h2 style="color:#fff;margin:0;letter-spacing:2px;">CHICKEN KITCHEN</h2>
        <p style="color:#ffcdd2;margin:5px 0 0;font-size:13px;">HR Forms / Formularios RH / Fom RH</p>
      </div>
      <div style="background:#fff;padding:25px;border:1px solid #ddd;border-radius:0 0 10px 10px;">
        <p style="margin:0 0 10px;">Your verification code / Su codigo de verificacion / Kod verifikasyon ou:</p>
        <div style="background:#f5f5f5;padding:18px;text-align:center;font-size:36px;font-weight:bold;
                    letter-spacing:10px;color:#D32F2F;border-radius:8px;margin:15px 0;">{code}</div>
        <p style="color:#999;font-size:11px;margin:0;">
          This code is valid for this session only.<br>
          Este codigo es valido solo para esta sesion.<br>
          Kod sa a valab pou sesyon sa a selman.</p>
      </div>
    </div>"""

    msg.attach(MIMEText(html, "html"))
    _smtp_send(to_email, msg)


# ── 2. Application Pending (to applicant) ──

def send_applicant_pending(to_email: str, applicant_name: str, store_name: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Chicken Kitchen - Application Received / Solicitud Recibida"
    msg["To"] = to_email

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:520px;margin:auto;padding:20px;">
      <div style="background:#D32F2F;padding:18px;text-align:center;border-radius:10px 10px 0 0;">
        <h2 style="color:#fff;margin:0;letter-spacing:2px;">CHICKEN KITCHEN</h2>
        <p style="color:#ffcdd2;margin:5px 0 0;font-size:13px;">HR Department</p>
      </div>
      <div style="background:#fff;padding:25px;border:1px solid #ddd;border-radius:0 0 10px 10px;">
        <h3 style="color:#333;margin:0 0 15px;">Hello {applicant_name},</h3>
        <p style="color:#555;line-height:1.6;">
          Your application for <strong>Chicken Kitchen — {store_name}</strong> has been received
          and is <strong>pending review</strong> by the store administrator.<br><br>
          Su solicitud para <strong>Chicken Kitchen — {store_name}</strong> ha sido recibida
          y esta <strong>en espera de revision</strong> por el administrador de la tienda.<br><br>
          Aplikasyon ou pou <strong>Chicken Kitchen — {store_name}</strong> te resevwa
          e li <strong>ap tann revizyon</strong> pa administratè magazen an.
        </p>
        <div style="background:#FFF3E0;padding:12px;border-radius:6px;margin:15px 0;border-left:4px solid #FF9800;">
          <p style="margin:0;color:#E65100;font-size:13px;">
            We will contact you once your application is reviewed.<br>
            Le contactaremos una vez que su solicitud sea revisada.<br>
            Nou pral kontakte ou yon fwa aplikasyon ou revize.
          </p>
        </div>
        <p style="color:#999;font-size:11px;margin:15px 0 0;">
          &mdash; Chicken Kitchen HR Team</p>
      </div>
    </div>"""

    msg.attach(MIMEText(html, "html"))
    _smtp_send(to_email, msg)


# ── 3. Review Needed (to store admin) ──

def send_admin_review(
    admin_email: str,
    store_name: str,
    applicant_name: str,
    applicant_email: str,
    applicant_phone: str,
    review_link: str,
    documents: list[dict],
):
    msg = MIMEMultipart()
    msg["Subject"] = f"[ACTION REQUIRED] New Applicant: {applicant_name} — {store_name}"
    msg["To"] = admin_email

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:560px;margin:auto;padding:20px;">
      <div style="background:#D32F2F;padding:18px;text-align:center;border-radius:10px 10px 0 0;">
        <h2 style="color:#fff;margin:0;letter-spacing:2px;">CHICKEN KITCHEN</h2>
        <p style="color:#ffcdd2;margin:5px 0 0;font-size:13px;">Personnel Review Required</p>
      </div>
      <div style="background:#fff;padding:25px;border:1px solid #ddd;border-radius:0 0 10px 10px;">
        <h3 style="color:#D32F2F;margin:0 0 15px;">New Application Pending Your Review</h3>

        <table style="width:100%;border-collapse:collapse;margin:10px 0;">
          <tr><td style="padding:6px 10px;color:#777;width:120px;">Name:</td>
              <td style="padding:6px 10px;font-weight:bold;">{applicant_name}</td></tr>
          <tr><td style="padding:6px 10px;color:#777;">Email:</td>
              <td style="padding:6px 10px;">{applicant_email}</td></tr>
          <tr><td style="padding:6px 10px;color:#777;">Phone:</td>
              <td style="padding:6px 10px;">{applicant_phone or 'N/A'}</td></tr>
          <tr><td style="padding:6px 10px;color:#777;">Store:</td>
              <td style="padding:6px 10px;">{store_name}</td></tr>
          <tr><td style="padding:6px 10px;color:#777;">Documents:</td>
              <td style="padding:6px 10px;">{len(documents)} attached</td></tr>
        </table>

        <div style="text-align:center;margin:25px 0;">
          <a href="{review_link}"
             style="background:#D32F2F;color:#fff;padding:14px 40px;border-radius:6px;
                    text-decoration:none;font-weight:bold;font-size:15px;display:inline-block;">
            REVIEW &amp; APPROVE
          </a>
        </div>

        <p style="color:#999;font-size:11px;margin:15px 0 0;text-align:center;">
          Click the button above or paste this link in your browser:<br>
          <a href="{review_link}" style="color:#999;">{review_link}</a>
        </p>
      </div>
    </div>"""

    msg.attach(MIMEText(html, "html"))

    for doc in documents:
        _attach_b64(msg, doc["filename"], doc["file_b64"])

    _smtp_send(admin_email, msg)


# ── 4. Approved (to Adela / HR) ──

def send_hr_approved(
    store_name: str,
    approved_by: str,
    applicant_name: str,
    applicant_email: str,
    documents: list[dict],
):
    msg = MIMEMultipart()
    msg["Subject"] = f"[APPROVED] {applicant_name} — {store_name}"
    msg["To"] = DEST_HR
    msg["Reply-To"] = applicant_email

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:520px;margin:auto;padding:20px;">
      <div style="background:#4CAF50;padding:18px;text-align:center;border-radius:10px 10px 0 0;">
        <h2 style="color:#fff;margin:0;letter-spacing:2px;">APPLICATION APPROVED</h2>
        <p style="color:#C8E6C9;margin:5px 0 0;font-size:13px;">Chicken Kitchen HR</p>
      </div>
      <div style="background:#fff;padding:25px;border:1px solid #ddd;border-radius:0 0 10px 10px;">
        <p style="color:#555;line-height:1.6;">
          The store administrator of <strong>{store_name}</strong> has approved
          the application of <strong>{applicant_name}</strong>.
        </p>
        <table style="width:100%;border-collapse:collapse;margin:10px 0;">
          <tr><td style="padding:6px 10px;color:#777;width:130px;">Applicant:</td>
              <td style="padding:6px 10px;font-weight:bold;">{applicant_name}</td></tr>
          <tr><td style="padding:6px 10px;color:#777;">Email:</td>
              <td style="padding:6px 10px;">{applicant_email}</td></tr>
          <tr><td style="padding:6px 10px;color:#777;">Store:</td>
              <td style="padding:6px 10px;">{store_name}</td></tr>
          <tr><td style="padding:6px 10px;color:#777;">Approved by:</td>
              <td style="padding:6px 10px;">{approved_by}</td></tr>
          <tr><td style="padding:6px 10px;color:#777;">Documents:</td>
              <td style="padding:6px 10px;">{len(documents)} attached</td></tr>
        </table>
        <p style="color:#999;font-size:11px;margin:15px 0 0;">
          &mdash; Chicken Kitchen HR Forms App</p>
      </div>
    </div>"""

    msg.attach(MIMEText(html, "html"))

    for doc in documents:
        _attach_b64(msg, doc["filename"], doc["file_b64"])

    _smtp_send(DEST_HR, msg)
