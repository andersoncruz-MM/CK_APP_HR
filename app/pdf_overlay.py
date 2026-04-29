"""
PDF Overlay Module - Fills original PDF templates with form data.
Uses reportlab to create a single combined overlay (text + checks) per page,
then merges it onto the original template using pypdf.
"""

import os
import sys
from io import BytesIO

from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    from PyPDF2 import PdfReader, PdfWriter


def get_templates_dir():
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "templates")


TEMPLATE_FILES = {
    "employee_app": "EmployeeApp_template.pdf",
    "direct_deposit": "DDAuth_template.pdf",
    "w4": "W4_template.pdf",
    "i9": "I9_template.pdf",
    "payroll": "PayrollAction_template.pdf",
}

FILL_COLOR = Color(0.05, 0.05, 0.35)
CHECK_COLOR = Color(0.1, 0.1, 0.6)


def _build_overlay_page(page_width, page_height, fields, checks, blanks=None):
    has_content = any(item[2] for item in fields) or checks or blanks
    if not has_content:
        return None

    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))

    # Draw white blanking rectangles first (to cover template text)
    if blanks:
        c.setFillColorRGB(1, 1, 1)
        for bx, by, bw, bh in blanks:
            c.rect(bx, by, bw, bh, fill=1, stroke=0)

    for x, y, text, fs in fields:
        if not text:
            continue
        c.setFont("Helvetica", fs)
        c.setFillColor(FILL_COLOR)
        c.drawString(x, y, str(text))

    if checks:
        c.setStrokeColor(CHECK_COLOR)
        c.setLineWidth(1.5)
        for cx, cy in checks:
            size = 8
            c.line(cx, cy, cx + size * 0.35, cy - size * 0.4)
            c.line(cx + size * 0.35, cy - size * 0.4, cx + size, cy + size * 0.6)

    c.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]


def fill_template(form_key, get_val, output_path):
    tpl_dir = get_templates_dir()
    tpl_path = os.path.join(tpl_dir, TEMPLATE_FILES[form_key])

    reader = PdfReader(tpl_path)
    writer = PdfWriter()

    generators = {
        "employee_app": _fill_employee_app,
        "direct_deposit": _fill_direct_deposit,
        "w4": _fill_w4,
        "i9": _fill_i9,
        "payroll": _fill_payroll,
    }

    page_data = generators[form_key](get_val, reader)

    for i, page in enumerate(reader.pages):
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)
        if i in page_data:
            data = page_data[i]
            fields = data[0]
            checks = data[1]
            blanks = data[2] if len(data) > 2 else None
            overlay = _build_overlay_page(w, h, fields, checks, blanks)
            if overlay is not None:
                page.merge_page(overlay)
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)


# ═══════════════════════════════════════════════════════════════
# EMPLOYEE APPLICATION  (3 pages, 612x792)
# PyMuPDF coords: label_y is baseline from BOTTOM of page
# Value placed on same y as label, x after label ends
# ═══════════════════════════════════════════════════════════════
def _fill_employee_app(gv, reader):
    S = 9  # font size

    # ── Page 1 ──
    # PyMuPDF precise positions: label x1 (end) + gap for value placement
    p1 = [
        # Last Name x1=103, First x1=290, M.I. x1=429, Date x1=480
        (105, 620, gv("ea_last_name"), S),
        (292, 620, gv("ea_first_name"), S),
        (431, 620, gv("ea_mi"), S),
        (482, 620, gv("ea_date"), 8),
        # Street Address y=602, Apt/Unit (after "Apartment/Unit" label x1=478)
        (95, 602, gv("ea_street_address"), S),
        (480, 602, gv("ea_apt"), 8),
        # City x1=76, State x1=293, ZIP x1=428 at y=578
        (78, 578, gv("ea_city"), S),
        (295, 578, gv("ea_state"), S),
        (429, 578, gv("ea_zip"), S),
        # Phone x1=86 y=557, Email x1=304 y=557
        (88, 557, gv("ea_phone"), S),
        (306, 557, gv("ea_email"), 8),
        # Date Available x1=97, SSN x1=287, Desired Salary x1=427 at y=539
        (99, 539, gv("ea_date_available"), 8),
        (289, 539, gv("ea_ssn"), S),
        (428, 539, gv("ea_desired_salary"), S),
        # Position Applied for x1=126 y=518
        (128, 518, gv("ea_position"), S),
        # If so when? x1=362 y=474
        (364, 474, gv("ea_when"), 8),
        # If yes explain x1=333 y=456
        (335, 456, gv("ea_felony_explain"), 8),
    ]

    c1 = []
    # Checkbox positions from PyMuPDF get_drawings() - exact □ rectangle coords
    # Citizen: YES□ x=241.4 y=495.9, NO□ x=278.9 y=495.9 (7.3x7.3)
    if gv("ea_citizen") == "yes":    c1.append((242, 496))
    elif gv("ea_citizen") == "no":   c1.append((279, 496))
    # Authorized: YES□ x=493.5, NO□ x=535.5
    if gv("ea_authorized") == "yes":    c1.append((494, 496))
    elif gv("ea_authorized") == "no":   c1.append((536, 496))
    # Worked before: YES□ x=241.4 y=475.0, NO□ x=278.9
    if gv("ea_worked_before") == "yes":  c1.append((242, 475))
    elif gv("ea_worked_before") == "no": c1.append((279, 475))
    # Felony: YES□ x=241.4 y=454.3, NO□ x=278.9
    if gv("ea_felony") == "yes":    c1.append((242, 454))
    elif gv("ea_felony") == "no":   c1.append((279, 454))

    # Education - High School
    # PyMuPDF: "High" x1=79 y=407, "Addres" x1=289 y=407, fill line y=405
    p1 += [
        (90, 405, gv("ea_hs_name"), 8),
        (300, 405, gv("ea_hs_address"), 8),  # x=300: gap after "Addres" x1=289
        # From x1=81 y=381, To x1=142, Degree x1=373
        (83, 381, gv("ea_hs_from"), 8),
        (143, 381, gv("ea_hs_to"), 8),
        (375, 381, gv("ea_hs_degree"), 8),
    ]
    # Graduate: YES□ x=281.9 y=382.3, NO□ x=319.5 y=382.3
    if gv("ea_hs_graduate") == "yes":  c1.append((282, 382))
    elif gv("ea_hs_graduate") == "no": c1.append((320, 382))

    # College - "Colleg" x1=83 y=365, "Addres" x1=289 y=365
    p1 += [
        (90, 363, gv("ea_col_name"), 8),
        (300, 363, gv("ea_col_address"), 8),  # x=300: gap after "Addres"
        (83, 339, gv("ea_col_from"), 8),
        (143, 339, gv("ea_col_to"), 8),
        (375, 339, gv("ea_col_degree"), 8),
    ]
    # College graduate: YES□ x=281.9 y=340.6, NO□ x=319.5
    if gv("ea_col_graduate") == "yes":  c1.append((282, 341))
    elif gv("ea_col_graduate") == "no": c1.append((320, 341))

    # Other - "Other" x1=84 y=319, "Addres" x1=289 y=323 (different y!)
    p1 += [
        (90, 317, gv("ea_oth_name"), 8),
        (300, 321, gv("ea_oth_address"), 8),  # x=300, y=321 aligned with "Addres" y=323
        (83, 297, gv("ea_oth_from"), 8),
        (143, 297, gv("ea_oth_to"), 8),
        (375, 297, gv("ea_oth_degree"), 8),
    ]
    # Other graduate: YES□ x=281.9 y=298.9, NO□ x=319.5
    if gv("ea_oth_graduate") == "yes":  c1.append((282, 299))
    elif gv("ea_oth_graduate") == "no": c1.append((320, 299))

    # ── References ──
    # PyMuPDF: FullName y, Company y, Address y (from template labels)
    # "Phone (           )" template text needs blanking to avoid duplicate parens
    refs_y = [(229, 208, 187), (166, 145, 125), (104, 83, 62)]
    blanks1 = []
    for i, (y_name, y_comp, y_addr) in enumerate(refs_y):
        p1 += [
            (103, y_name, gv(f"ea_ref{i}_name"), 8),
            (375, y_name, gv(f"ea_ref{i}_relationship"), 8),
            (100, y_comp, gv(f"ea_ref{i}_company"), 8),
            (355, y_comp, gv(f"ea_ref{i}_phone"), 8),
            (95, y_addr, gv(f"ea_ref{i}_address"), 8),
        ]
        # Blank template "(           )" for phone (after "Phone " text, x=355)
        if gv(f"ea_ref{i}_phone"):
            blanks1.append((355, y_comp - 3, 45, 14))

    # ── Page 2 ── Previous Employment
    # PyMuPDF: Company y=709, Phone "(   )" x=369-405, Address y=687
    # "$" standalone at x=328 (starting) and x=463 (ending)
    p2 = []
    c2 = []
    blanks2 = []
    emp_y = [709, 577, 444]
    for i, yb in enumerate(emp_y):
        # Strip leading "$" from salary (template already has "$")
        start_sal = gv(f"ea_emp{i}_start_salary")
        if start_sal.startswith("$"):
            start_sal = start_sal[1:]
        end_sal = gv(f"ea_emp{i}_end_salary")
        if end_sal.startswith("$"):
            end_sal = end_sal[1:]

        p2 += [
            (96, yb, gv(f"ea_emp{i}_company"), 8),
            (369, yb, gv(f"ea_emp{i}_phone"), 8),       # inside template "(   )"
            (91, yb - 22, gv(f"ea_emp{i}_address"), 8),
            (370, yb - 22, gv(f"ea_emp{i}_supervisor"), 8),
            (93, yb - 44, gv(f"ea_emp{i}_title"), 8),
            (337, yb - 44, start_sal, 8),                # after template "$"
            (472, yb - 44, end_sal, 8),                  # after template "$"
            (116, yb - 66, gv(f"ea_emp{i}_responsibilities"), 7),
            (81, yb - 88, gv(f"ea_emp{i}_from"), 8),
            (143, yb - 88, gv(f"ea_emp{i}_to"), 8),
            (265, yb - 88, gv(f"ea_emp{i}_reason"), 8),
        ]
        # Blank template "(   )" for phone
        if gv(f"ea_emp{i}_phone"):
            blanks2.append((367, yb - 3, 40, 14))
        # Contact: YES□ x=303 NO□ x=345.4 (from get_drawings)
        # emp0 yb=709: boxes at y=599.9 → yb-109.1
        # emp1 yb=577: boxes at y=467.5 → yb-109.5
        # emp2 yb=444: boxes at y=335.2 → yb-108.8
        if gv(f"ea_emp{i}_contact") == "yes":    c2.append((303, yb - 109))
        elif gv(f"ea_emp{i}_contact") == "no":   c2.append((346, yb - 109))

    # Military: Branch x1=85 y=279, From x1=399, To x1=453
    p2 += [
        (87, 279, gv("ea_mil_branch"), S),
        (400, 279, gv("ea_mil_from"), 8),
        (455, 279, gv("ea_mil_to"), 8),
        # Rank at Discharge x1=125 y=257, Type of Discharge x1=444
        (127, 257, gv("ea_mil_rank"), S),
        (446, 257, gv("ea_mil_discharge_type"), S),
        # If other than honorable x1=173 y=235
        (175, 235, gv("ea_mil_explain"), 8),
        # Signature x1=95 y=129, Date x1=427
        (96, 129, gv("ea_signature"), S),
        (428, 129, gv("ea_sign_date"), S),
    ]

    return {0: (p1, c1, blanks1), 1: (p2, c2, blanks2)}


# ═══════════════════════════════════════════════════════════════
# DIRECT DEPOSIT  (1 page, 612x792)
# PyMuPDF precise positions used
# ═══════════════════════════════════════════════════════════════
def _fill_direct_deposit(gv, reader):
    S = 10
    # PyMuPDF precise positions:
    # Account 1 type: Checking x=170 y=546, Savings x=270 y=546
    # Bank routing x1=217 y=524, Account number x1=123 y=502
    # Percentage x1=331 y=480
    # Account 2: type y=441, routing y=419, account y=397
    # Signature x1=147 y=62, Employee ID x1=436 y=62
    # Print name x1=99 y=40, Date x1=387 y=40
    # Language-specific labels for $5 fee notice
    lang = gv("_lang") or "en"
    _fee = {
        "en": ("Bank Name:", "A $5.00 fee will be charged for direct deposit.", "I accept:", "YES", "NO"),
        "es": ("Nombre del Banco:", "Se cobrara un cargo de $5.00 por deposito directo.", "Acepto:", "SI", "NO"),
        "ht": ("Non Bank la:", "Yo pral chaje $5.00 pou depo direk.", "Mwen aksepte:", "WI", "NON"),
    }
    bank_lbl, fee_txt, accept_lbl, yes_lbl, no_lbl = _fee.get(lang, _fee["en"])

    fields = [
        # Bank name (in the voided check area)
        (38, 380, bank_lbl, 7),
        (155, 380, gv("dd_bank_name"), 9),
        # $5 Fee notice (selected language only)
        (38, 360, fee_txt, 7),
        (38, 345, accept_lbl, 7),
        (175, 345, yes_lbl, 7),
        (235, 345, no_lbl, 7),
        # Account 1 - values on fill lines (above labels)
        (220, 530, gv("dd_acct1_routing"), S),
        (125, 508, gv("dd_acct1_number"), S),
        (333, 486, gv("dd_acct1_amount"), S),
        # Account 2
        (220, 425, gv("dd_acct2_routing"), S),
        (125, 403, gv("dd_acct2_number"), S),
        # Authorization "This authorizes ___" y=168
        (116, 174, "Chicken Kitchen", S),
        # Authorized signature x1=147, Employee ID# x1=436 at y=68
        (149, 68, gv("dd_signature"), S),
        (438, 68, gv("dd_employee_id"), S),
        # Print name x1=99, Date x1=387 at y=46
        (101, 46, gv("dd_print_name"), S),
        (389, 46, gv("dd_date"), S),
    ]

    checks = []
    # Checking checkbox before "Checking" at x=170, Savings at x=270
    if gv("dd_acct1_type") == "checking":  checks.append((157, 548))
    elif gv("dd_acct1_type") == "savings": checks.append((257, 548))
    # Account 2
    if gv("dd_acct2_type") == "checking":  checks.append((157, 443))
    elif gv("dd_acct2_type") == "savings": checks.append((257, 443))
    # $5 Fee acceptance YES/NO checkmark
    if gv("dd_fee_accept") == "yes":   checks.append((210, 345))
    elif gv("dd_fee_accept") == "no":  checks.append((250, 345))

    return {0: (fields, checks)}


# ═══════════════════════════════════════════════════════════════
# W-4 FORM (2026) - Page 1 only fillable
# ═══════════════════════════════════════════════════════════════
def _fill_w4(gv, reader):
    S = 10

    # Auto-calculate Step 3 dollar amounts from counts
    def _safe_int(val):
        try:
            return int(val)
        except (ValueError, TypeError):
            return 0

    def _safe_money(val):
        try:
            v = int(float(val))
            return str(v) if v else ""
        except (ValueError, TypeError):
            return ""

    children_count = _safe_int(gv("w4_children"))
    other_deps_count = _safe_int(gv("w4_other_deps"))
    children_amount = str(children_count * 2200) if children_count else ""
    other_deps_amount = str(other_deps_count * 500) if other_deps_count else ""
    other_credits = _safe_money(gv("w4_other_credits"))

    # Auto-calculate total for Step 3
    total_3 = gv("w4_total_step3")
    if not total_3:
        calc = (children_count * 2200) + (other_deps_count * 500) + _safe_int(other_credits)
        total_3 = str(calc) if calc else ""

    # PyMuPDF precise positions for W-4 2026
    # Step 3: "$" at x=411.5 for 3(a)/3(b), "$" at x=505.1 for total
    # Step 4: "$" at x=505.1 for 4(a),4(b),4(c)
    # Signature at y=80, Employer at y=57
    fields = [
        # Step 1: Personal Info
        (100, 688, gv("w4_first_name"), S),
        (280, 688, gv("w4_last_name"), S),
        (480, 688, gv("w4_ssn"), 9),
        (100, 664, gv("w4_address"), S),
        (100, 640, gv("w4_city_state_zip"), S),
        # Step 3: dollar amounts right-aligned in box (after "$" at x=411/505)
        (420, 301, children_amount, S),       # 3(a) after $ at x=411
        (420, 289, other_deps_amount, S),     # 3(b) after $ at x=411
        (515, 265, total_3, S),               # total after $ at x=505
        # Step 4: amounts after "$" at x=505
        (515, 229, _safe_money(gv("w4_other_income")), S),
        (515, 193, _safe_money(gv("w4_deductions")), S),
        (515, 175, _safe_money(gv("w4_extra_withholding")), S),
        # Step 5: Signature y=80, Date y=80
        (200, 80, gv("w4_signature"), S),
        (485, 80, gv("w4_date"), 9),
        # Employer section: fill line at y=57
        (100, 52, gv("w4_employer_name"), 7),
        (400, 52, gv("w4_first_date"), 8),
        (478, 52, gv("w4_ein"), 8),
    ]

    checks = []
    status = gv("w4_filing_status")
    # W-4 checkboxes from get_drawings: x=115.2, sizes 8x8
    # Filing: single y=626, married y=614, head y=602.2
    if status == "single":          checks.append((115, 626))
    elif status == "married_joint":  checks.append((115, 614))
    elif status == "head_household": checks.append((115, 602))
    # Two jobs: x=564 y=380 (8x8)
    if gv("w4_two_jobs") == "True":  checks.append((564, 380))
    # Exempt: x=564 y=129.5
    if gv("w4_exempt") == "True":    checks.append((564, 130))

    return {0: (fields, checks)}


# ═══════════════════════════════════════════════════════════════
# I-9 FORM - Page 1
# ═══════════════════════════════════════════════════════════════
def _fill_i9(gv, reader):
    S = 9

    # ── SSN individual digit boxes ──
    # Box rect: y_bottom=554, y_top=566. Center y for text ≈ 556
    # 9 boxes with center_x positions:
    ssn_box_cx = [155.4, 166.6, 178.3, 190.1, 201.8, 213.6, 225.3, 237.1, 249.0]
    ssn_y = 556
    ssn_raw = gv("i9_ssn").replace("-", "").replace(" ", "")
    ssn_fields = []
    for i, cx in enumerate(ssn_box_cx):
        digit = ssn_raw[i] if i < len(ssn_raw) else ""
        if digit:
            ssn_fields.append((cx - 3, ssn_y, digit, 9))

    # ── Section 2 column positions (from PyMuPDF) ──
    # List A: x=38-265, List B: x=267-430, List C: x=430-576
    # Document rows (measured from labels):
    #   Doc Title at y≈355, Issuing at y≈337, Doc# at y≈319, Exp at y≈301
    # List A has multiple doc slots; rows below first doc start at y≈283

    # List B column starts at x≈290 (after List A OR divider)
    # List C column starts at x≈445 (after List B AND divider)
    LB_X = 290   # List B fill start
    LC_X = 445   # List C fill start

    fields = [
        # Section 1: Personal info
        (42, 608, gv("i9_last_name"), S),
        (204, 608, gv("i9_first_name"), S),
        (348, 608, gv("i9_middle_initial"), S),
        (420, 608, gv("i9_other_names"), 8),
        (42, 582, gv("i9_address"), 8),
        (234, 582, gv("i9_apt"), S),
        (306, 582, gv("i9_city"), S),
        (462, 582, gv("i9_state"), S),
        (510, 582, gv("i9_zip"), S),
        (42, 556, gv("i9_dob"), S),
        # SSN digits added separately below
        (264, 556, gv("i9_email"), 8),
        (456, 556, gv("i9_phone"), S),
        # USCIS/I-94/passport
        (250, 457, gv("i9_uscis"), 8),
        (340, 457, gv("i9_i94"), 8),
        (455, 457, gv("i9_passport"), 8),
        (455, 445, gv("i9_country"), 8),
        (300, 486, gv("i9_exp_date"), 8),
        # Employee signature
        (130, 424, gv("i9_employee_sig"), S),
        (430, 424, gv("i9_employee_date"), S),
        # Section 2: PyMuPDF labels at y=347,329,311,293
        # List A (x≈120, after label ends ~x=122)
        (125, 343, gv("i9_lista_title"), 8),
        (125, 325, gv("i9_lista_issuing"), 8),
        (125, 307, gv("i9_lista_number"), 8),
        (125, 289, gv("i9_lista_exp"), 8),
        # List B (x≈290, middle column)
        (LB_X, 343, gv("i9_listb_title"), 7),
        (LB_X, 325, gv("i9_listb_issuing"), 7),
        (LB_X, 307, gv("i9_listb_number"), 7),
        (LB_X, 289, gv("i9_listb_exp"), 7),
        # List C (x≈445, right column)
        (LC_X, 343, gv("i9_listc_title"), 7),
        (LC_X, 325, gv("i9_listc_issuing"), 7),
        (LC_X, 307, gv("i9_listc_number"), 7),
        (LC_X, 289, gv("i9_listc_exp"), 7),
        # Employer section: First Day at x=462 y=120
        (462, 120, gv("i9_first_day"), 8),
        # Employer name/sig/date at y=93 (fill line below labels at y=100)
        (38, 93, gv("i9_employer_name"), 7),
        (294, 93, gv("i9_employer_sig"), 7),
        (490, 93, gv("i9_employer_date"), 7),
        # Business name/address at y=60 (fill line below labels at y=67)
        (38, 60, gv("i9_employer_biz"), 7),
        (246, 60, gv("i9_employer_addr"), 6),
    ] + ssn_fields  # Add individual SSN digits

    checks = []
    status = gv("i9_status")
    # I-9 citizenship checkboxes from get_drawings: x=181.9, 9x9
    if status == "citizen":              checks.append((182, 524))
    elif status == "noncitizen_national": checks.append((182, 512))
    elif status == "permanent_resident":  checks.append((182, 500))
    elif status == "alien_authorized":    checks.append((182, 488))

    return {0: (fields, checks)}


# ═══════════════════════════════════════════════════════════════
# PAYROLL ACTION FORM  (1 page, 595.3x841.9)
# PyMuPDF precise positions used
# ═══════════════════════════════════════════════════════════════
def _fill_payroll(gv, reader):
    S = 10
    # PyMuPDF precise positions (page size 595.3 x 841.9):
    # Name x1=122 y=593, Date x1=327 y=593
    # Job x1=87 y=576, Store x1=331 y=576
    # EmpID x1=102 y=555, Supervisor x1=328 y=555
    # DOB x1=80 y=535
    fields = [
        (124, 593, gv("pa_name"), S),
        (329, 593, gv("pa_date_action"), S),
        (89, 576, gv("pa_job_title"), S),
        (333, 576, gv("pa_store_name"), S),
        (104, 555, gv("pa_employee_id"), S),
        (330, 555, gv("pa_supervisor"), S),
        (82, 535, gv("pa_dob"), S),
        # Address x1=257 y=514, City x1=257 y=493, State x1=257 y=472, Zip x1=256 y=452
        (259, 514, gv("pa_address"), 8),
        (258, 493, gv("pa_city"), 8),
        (258, 472, gv("pa_state"), 8),
        (258, 452, gv("pa_zip"), 8),
        # Rate of Pay: $ x1=291 y=420, Hourly x=354, Weekly x=450
        (293, 420, gv("pa_rate_of_pay"), S),
        # Amount of Increase x1=297 y=400
        (299, 400, gv("pa_increase_amount"), S),
        # From (Job Title) x1=284 y=379, To (Job Title) x1=444
        (286, 379, gv("pa_from_title"), 8),
        (446, 379, gv("pa_to_title"), 8),
        # From (Store Loc) x1=287 y=358, To x1=416
        (289, 358, gv("pa_from_store"), 8),
        (418, 358, gv("pa_to_store"), 8),
        # Will Be Out From x1=290 y=337, To x1=418
        (291, 337, gv("pa_out_from"), 8),
        (419, 337, gv("pa_out_to"), 8),
        # Last Date Worked x1=119 y=317
        (121, 317, gv("pa_last_date"), S),
        # Store Manager Signature x1=140 y=191
        (142, 191, gv("pa_mgr_sig"), S),
        # Supervisor Signature x1=127 y=170
        (129, 170, gv("pa_sup_sig"), S),
    ]

    # Action checkboxes X marks - "Mark with X" column at x≈160
    # PyMuPDF y positions for each action label
    action_map = {
        "pa_new_hire": 493, "pa_rehire": 483, "pa_salary_increase": 472,
        "pa_promotion": 462, "pa_demotion": 452, "pa_transfer": 441,
        "pa_vacation": 431, "pa_leave": 420, "pa_termination": 410,
        "pa_change_address": 400, "pa_other": 389,
    }
    for key, y_pos in action_map.items():
        if gv(key) == "True":
            fields.append((155, y_pos, "X", 11))

    # Cause for change x1=119 y=275
    cause = gv("pa_cause_change")
    if cause:
        for j, line in enumerate(cause.split("\n")[:3]):
            fields.append((121, 270 - j * 12, line[:70], 8))

    checks = []
    # Hourly at x=354 y=420, Weekly at x=450
    if gv("pa_pay_type") == "hourly":   checks.append((342, 422))
    elif gv("pa_pay_type") == "weekly": checks.append((438, 422))
    # Eligible for Rehire: Yes x=132 y=295, No x=228
    if gv("pa_eligible_rehire") == "yes":    checks.append((120, 297))
    elif gv("pa_eligible_rehire") == "no":   checks.append((216, 297))

    return {0: (fields, checks)}
