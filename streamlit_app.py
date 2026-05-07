"""
Chicken Kitchen HR Forms - Streamlit Cloud App
Email verification + QR code access + embedded HR forms + document upload + submit.
"""

import streamlit as st
import streamlit.components.v1 as components
import base64
import random
import string
import smtplib
import datetime
import tempfile
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from io import BytesIO

try:
    import qrcode
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False

# ─── Page Config ───
st.set_page_config(
    page_title="Chicken Kitchen - HR Forms",
    page_icon=":poultry_leg:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit default elements for a cleaner look
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp { background: #2C2C2C; }
[data-testid="stSidebar"] { display: none; }
div.block-container { padding-top: 1rem; padding-bottom: 0; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ───
_defaults = {
    "authenticated": False,
    "verification_code": None,
    "user_email": "",
    "code_sent": False,
    "error_msg": "",
    "submitted": False,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── Paths ───
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "app" / "templates"
WEB_DIR = BASE_DIR / "web"

DEST_EMAIL = "adela@chickenkitchen.com"

# ═══════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════

@st.cache_data
def load_templates_b64():
    """Read all 5 PDF templates and return as base64 strings."""
    mapping = {
        "employee_app": "EmployeeApp_template.pdf",
        "direct_deposit": "DDAuth_template.pdf",
        "w4": "W4_template.pdf",
        "i9": "I9_template.pdf",
        "payroll": "PayrollAction_template.pdf",
    }
    result = {}
    for key, filename in mapping.items():
        fp = TEMPLATES_DIR / filename
        if fp.exists():
            result[key] = base64.b64encode(fp.read_bytes()).decode("ascii")
        else:
            result[key] = ""
    return result


@st.cache_data
def load_web_file(name):
    """Read a web/ file as text."""
    fp = WEB_DIR / name
    return fp.read_text(encoding="utf-8") if fp.exists() else ""


def generate_code():
    return "".join(random.choices(string.digits, k=6))


def send_code_email(recipient, code):
    """Send verification code via Gmail SMTP."""
    try:
        sender = st.secrets["email"]["sender"]
        app_password = st.secrets["email"]["app_password"]

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Chicken Kitchen HR - Verification Code"
        msg["From"] = sender
        msg["To"] = recipient

        html_body = f"""
        <div style="font-family:Arial,sans-serif;max-width:480px;margin:auto;padding:20px;">
          <div style="background:#D32F2F;padding:18px;text-align:center;border-radius:10px 10px 0 0;">
            <h2 style="color:#fff;margin:0;letter-spacing:2px;">CHICKEN KITCHEN</h2>
            <p style="color:#ffcdd2;margin:5px 0 0;font-size:13px;">HR Forms / Formularios RH / Fom RH</p>
          </div>
          <div style="background:#fff;padding:25px;border:1px solid #ddd;border-radius:0 0 10px 10px;">
            <p style="margin:0 0 10px;">Your verification code is / Su codigo de verificacion es / Kod verifikasyon ou a se:</p>
            <div style="background:#f5f5f5;padding:18px;text-align:center;font-size:36px;font-weight:bold;
                        letter-spacing:10px;color:#D32F2F;border-radius:8px;margin:15px 0;">{code}</div>
            <p style="color:#999;font-size:11px;margin:0;">This code is valid for this session only.<br>
               Este codigo es valido solo para esta sesion.<br>
               Kod sa a valab pou sesyon sa a selman.</p>
          </div>
        </div>"""

        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, app_password)
            server.sendmail(sender, recipient, msg.as_string())
        return True
    except Exception as e:
        st.session_state.error_msg = str(e)
        return False


def send_application_email(applicant_name, applicant_email, files):
    """Send the completed application with all attachments to HR."""
    try:
        sender = st.secrets["email"]["sender"]
        app_password = st.secrets["email"]["app_password"]

        msg = MIMEMultipart()
        msg["Subject"] = f"New Employee Application - {applicant_name}"
        msg["From"] = sender
        msg["To"] = DEST_EMAIL
        if applicant_email:
            msg["Reply-To"] = applicant_email

        now = datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")
        body = (
            f"New employee application received.\n\n"
            f"Name: {applicant_name}\n"
            f"Email: {applicant_email}\n"
            f"Date: {now}\n"
            f"Files attached: {len(files)}\n\n"
            f"---\nSent from Chicken Kitchen HR Forms App"
        )
        msg.attach(MIMEText(body, "plain"))

        for f in files:
            f.seek(0)
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition", f'attachment; filename="{f.name}"'
            )
            msg.attach(part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, app_password)
            server.sendmail(sender, DEST_EMAIL, msg.as_string())
        return True
    except Exception as e:
        st.session_state.error_msg = str(e)
        return False


def generate_qr_bytes(url):
    """Generate a QR code PNG as bytes."""
    if not HAS_QRCODE:
        return None
    qr = qrcode.QRCode(version=1, box_size=8, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#D32F2F", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ═══════════════════════════════════════════
# BUILD EMBEDDED HTML
# ═══════════════════════════════════════════

@st.cache_data
def build_hr_component_html():
    """Build a self-contained HTML page with Streamlit component support.

    Includes the Streamlit component shim for bidirectional communication,
    the Documents & Submit tab, and all form/PDF functionality inlined.
    """
    templates = load_templates_b64()
    css = load_web_file("style.css")
    translations_js = load_web_file("translations.js")
    us_data_js = load_web_file("us-data.js")
    pdf_overlay_js = load_web_file("pdf-overlay.js")
    app_js = load_web_file("app.js")

    # Build base64 template data object for JS
    tpl_entries = ",\n    ".join(
        f'{key}: "{b64}"' for key, b64 in templates.items() if b64
    )
    template_data_js = f"const TEMPLATE_DATA = {{\n    {tpl_entries}\n}};"

    # Streamlit component shim - minimal postMessage bridge
    streamlit_shim = """
(function() {
  function sendMsg(type, data) {
    window.parent.postMessage(
      Object.assign({ isStreamlitMessage: true, type: type }, data), "*"
    );
  }
  var Streamlit = {
    RENDER_EVENT: "streamlit:render",
    events: new EventTarget(),
    setComponentReady: function() {
      sendMsg("streamlit:componentReady", { apiVersion: 1 });
    },
    setComponentValue: function(value) {
      sendMsg("streamlit:setComponentValue", { value: value });
    },
    setFrameHeight: function(height) {
      sendMsg("streamlit:setFrameHeight", {
        height: height || document.body.scrollHeight
      });
    }
  };
  window.addEventListener("message", function(event) {
    if (event.data && event.data.type === "streamlit:render") {
      Streamlit.events.dispatchEvent(
        new CustomEvent(Streamlit.RENDER_EVENT, { detail: event.data })
      );
    }
  });
  window.Streamlit = Streamlit;
})();
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chicken Kitchen - HR Forms</title>
  <style>
{css}
  </style>
</head>
<body>

  <!-- Streamlit Component Shim (must load first) -->
  <script>
{streamlit_shim}
  </script>

  <!-- Header -->
  <div class="header">
    <h1 id="headerTitle">CHICKEN KITCHEN - HR FORMS</h1>
    <div class="lang-select">
      <span id="langLabel">Language:</span>
      <select id="langSelect" onchange="switchLanguage(this.value)">
        <option value="en">English</option>
        <option value="es">Espanol</option>
        <option value="ht">Kreyol</option>
      </select>
    </div>
  </div>

  <!-- Main -->
  <div class="main">
    <div class="sidebar" id="sidebar">
      <button data-form="employee_app" onclick="showForm('employee_app')">Employee Application</button>
      <button data-form="direct_deposit" onclick="showForm('direct_deposit')">Direct Deposit</button>
      <button data-form="w4" onclick="showForm('w4')">W-4 (2026)</button>
      <button data-form="i9" onclick="showForm('i9')">I-9 Verification</button>
      <button data-form="payroll" onclick="showForm('payroll')">Payroll Action</button>
      <div style="border-top:1px solid #444;margin:8px 5px;"></div>
      <button data-form="documents" onclick="showForm('documents')" style="color:#4CAF50;">Documents & Submit</button>
    </div>
    <div class="content-wrapper">
      <div class="content" id="content">
        <div class="welcome" id="welcome">
          <span>Select a form from the sidebar to begin.</span>
        </div>
      </div>
      <div class="btn-bar">
        <button class="btn-clear" id="btnClear" onclick="clearForm()">Clear Form</button>
        <button class="btn-preview" id="btnPreview" onclick="previewPDF()">Preview</button>
        <button class="btn-export" id="btnExport" onclick="exportPDF()">Export PDF</button>
      </div>
    </div>
  </div>

  <!-- Preview modal -->
  <div class="preview-overlay" id="previewOverlay" style="display:none">
    <div class="preview-toolbar">
      <button onclick="zoomPreview(-0.15)">-</button>
      <span class="zoom-label" id="zoomLabel">100%</span>
      <button onclick="zoomPreview(0.15)">+</button>
      <span class="title" id="previewFormName"></span>
      <button class="close-btn" onclick="closePreview()">X</button>
    </div>
    <div class="preview-body" id="previewBody"></div>
  </div>

  <!-- External libs (CDN) -->
  <script src="https://unpkg.com/pdf-lib@1.17.1/dist/pdf-lib.min.js"></script>
  <script src="https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.min.js"></script>
  <script>
    pdfjsLib.GlobalWorkerOptions.workerSrc =
      'https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js';
  </script>

  <!-- App scripts (inlined) -->
  <script>
{translations_js}
  </script>
  <script>
{us_data_js}
  </script>
  <script>
{template_data_js}

{pdf_overlay_js}
  </script>
  <script>
{app_js}
  </script>

  <!-- Initialize Streamlit component lifecycle -->
  <script>
    if (window.Streamlit) {{
      window.Streamlit.setComponentReady();
      window.Streamlit.setFrameHeight(880);
    }}
  </script>
</body>
</html>"""


@st.cache_resource
def _get_hr_component():
    """Create and cache the bidirectional HR forms component."""
    comp_dir = Path(tempfile.mkdtemp(prefix="ck_hr_"))
    html_content = build_hr_component_html()
    (comp_dir / "index.html").write_text(html_content, encoding="utf-8")
    return components.declare_component("ck_hr_forms", path=str(comp_dir))


# ═══════════════════════════════════════════
# LOGIN PAGE
# ═══════════════════════════════════════════

def show_login_page():
    app_url = st.secrets.get("app", {}).get(
        "url", "https://your-app.streamlit.app"
    )

    st.markdown("""
    <style>
    .login-box {
        max-width: 460px; margin: 0 auto; background: #fff;
        border-radius: 12px; overflow: hidden;
        box-shadow: 0 4px 24px rgba(0,0,0,0.35);
    }
    .login-hdr {
        background: #D32F2F; padding: 22px; text-align: center;
    }
    .login-hdr h1 { color:#fff; margin:0; font-size:26px; letter-spacing:3px; }
    .login-hdr p  { color:#ffcdd2; margin:6px 0 0; font-size:13px; }
    </style>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div class="login-box">
          <div class="login-hdr">
            <h1>CHICKEN KITCHEN</h1>
            <p>HR Forms / Formularios RH / Fom RH</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # QR code
        qr_bytes = generate_qr_bytes(app_url)
        if qr_bytes:
            _, qr_col, _ = st.columns([1, 1, 1])
            with qr_col:
                st.image(qr_bytes, width=180)
                st.caption("Scan to access / Escanee para acceder")

        st.markdown("---")

        if not st.session_state.code_sent:
            st.markdown(
                "**Enter your email / Ingrese su correo / Antre imel ou**"
            )
            email = st.text_input(
                "Email",
                placeholder="employee@example.com",
                label_visibility="collapsed",
            )
            if st.button(
                "Send Code / Enviar Codigo / Voye Kod",
                type="primary",
                use_container_width=True,
            ):
                if email and "@" in email and "." in email:
                    code = generate_code()
                    st.session_state.verification_code = code
                    st.session_state.user_email = email
                    if send_code_email(email, code):
                        st.session_state.code_sent = True
                        st.rerun()
                    else:
                        st.error(
                            f"Error: {st.session_state.error_msg}"
                        )
                else:
                    st.warning("Please enter a valid email / Ingrese un correo valido")
        else:
            st.markdown(
                f"**Code sent to / Codigo enviado a:**  \n"
                f"`{st.session_state.user_email}`"
            )
            code_input = st.text_input(
                "6-digit code / Codigo de 6 digitos",
                max_chars=6,
                placeholder="000000",
            )
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Verify / Verificar", type="primary", use_container_width=True):
                    if code_input == st.session_state.verification_code:
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error("Invalid code / Codigo invalido")
            with c2:
                if st.button("Resend / Reenviar", use_container_width=True):
                    new_code = generate_code()
                    st.session_state.verification_code = new_code
                    if send_code_email(st.session_state.user_email, new_code):
                        st.success("Code resent / Codigo reenviado")

            if st.button("Back / Volver", use_container_width=True):
                st.session_state.code_sent = False
                st.session_state.verification_code = None
                st.rerun()


# ═══════════════════════════════════════════
# PROCESS COMPONENT SUBMISSION
# ═══════════════════════════════════════════

def _process_submission(data):
    """Receive form PDFs + identity docs from the component and email them."""
    name = data.get("name", "Unknown")
    email = data.get("email", "")
    pdfs = data.get("pdfs", {})
    docs = data.get("docs", {})

    all_files = []
    for filename, b64 in pdfs.items():
        buf = BytesIO(base64.b64decode(b64))
        buf.name = filename
        all_files.append(buf)
    for filename, b64 in docs.items():
        buf = BytesIO(base64.b64decode(b64))
        buf.name = filename
        all_files.append(buf)

    if not all_files:
        st.warning(
            "No files to send / No hay archivos para enviar / "
            "Pa gen fichye pou voye"
        )
        return

    with st.spinner(
        "Sending application to Chicken Kitchen HR... / "
        "Enviando solicitud a RR.HH. ..."
    ):
        success = send_application_email(name, email, all_files)

    if success:
        st.session_state.submitted = True
        st.rerun()
    else:
        st.error(
            f"Error sending / Error al enviar: {st.session_state.error_msg}"
        )


# ═══════════════════════════════════════════
# THANK YOU PAGE
# ═══════════════════════════════════════════

def show_thank_you():
    st.markdown("""
    <div style="text-align:center;padding:80px 20px;background:#fff;border-radius:12px;
                margin:40px auto;max-width:600px;box-shadow:0 4px 20px rgba(0,0,0,0.2);">
      <div style="width:80px;height:80px;border-radius:50%;background:#4CAF50;
                  margin:0 auto 20px;display:flex;align-items:center;justify-content:center;">
        <span style="color:#fff;font-size:40px;font-weight:bold;">&#10003;</span>
      </div>
      <h1 style="color:#4CAF50;margin:0 0 10px;">Thank You!</h1>
      <h2 style="color:#4CAF50;margin:0 0 10px;">Gracias! / Mesi!</h2>
      <p style="color:#555;font-size:16px;margin:15px 0;line-height:1.6;">
        Your application has been submitted successfully.<br>
        Su solicitud ha sido enviada exitosamente.<br>
        Aplikasyon ou a te soumèt avek sikse.
      </p>
      <hr style="margin:20px 40px;border:none;border-top:1px solid #ddd;">
      <p style="color:#999;font-size:13px;">
        We will contact you soon.<br>
        Nos pondremos en contacto pronto.<br>
        Nou pral kontakte ou byento.
      </p>
    </div>
    """, unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if st.button(
            "New Application / Nueva Solicitud",
            use_container_width=True,
        ):
            st.session_state.submitted = False
            st.rerun()


# ═══════════════════════════════════════════
# MAIN HR APP PAGE
# ═══════════════════════════════════════════

def show_hr_app():
    # Logout button top-right
    _, right = st.columns([8, 1])
    with right:
        if st.button("Logout", use_container_width=True):
            for k in _defaults:
                st.session_state[k] = _defaults[k]
            st.rerun()

    st.info(
        "Fill the forms, then click **Documents & Submit** to send. / "
        "Llene los formularios, luego haga clic en **Documents & Submit** para enviar. / "
        "Ranpli fom yo, epi klike sou **Documents & Submit** pou voye."
    )

    # Render the bidirectional HR forms component
    hr_comp = _get_hr_component()
    result = hr_comp(key="hr_forms", default=None, height=880)

    # Handle submission from the component
    if result and isinstance(result, dict) and result.get("action") == "submit":
        submit_id = result.get("submit_id")
        if submit_id != st.session_state.get("last_submit_id"):
            st.session_state.last_submit_id = submit_id
            _process_submission(result)


# ═══════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════

if st.session_state.get("submitted"):
    show_thank_you()
elif st.session_state.authenticated:
    show_hr_app()
else:
    show_login_page()
