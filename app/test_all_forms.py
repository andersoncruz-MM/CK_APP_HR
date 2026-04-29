"""
Test script: Generate all 5 forms with realistic random data,
export to PDF, render each page to PNG for visual validation.
"""
import os
import sys
import tempfile

# Ensure we can import from app directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pdf_overlay import fill_template

# ── Test data for all 5 forms ──
TEST_DATA = {
    # ═══ EMPLOYEE APPLICATION ═══
    "ea_last_name": "Rodriguez",
    "ea_first_name": "Carlos",
    "ea_mi": "A",
    "ea_date": "04/26/2026",
    "ea_street_address": "2450 SW 8th Street",
    "ea_apt": "Apt 15B",
    "ea_city": "Miami",
    "ea_state": "FL",
    "ea_zip": "33135",
    "ea_phone": "(305) 555-7890",
    "ea_email": "carlos.rodriguez@email.com",
    "ea_ssn": "123-45-6789",
    "ea_date_available": "05/15/2026",
    "ea_desired_salary": "$17/hr",
    "ea_position": "Line Cook",
    "ea_citizen": "yes",
    "ea_authorized": "yes",
    "ea_worked_before": "no",
    "ea_when": "",
    "ea_felony": "no",
    "ea_felony_explain": "",
    # Education
    "ea_hs_name": "Miami Senior High",
    "ea_hs_address": "2450 SW 1st St, Miami FL",
    "ea_hs_from": "2010",
    "ea_hs_to": "2014",
    "ea_hs_graduate": "yes",
    "ea_hs_degree": "High School Diploma",
    "ea_col_name": "Miami Dade College",
    "ea_col_address": "300 NE 2nd Ave, Miami FL",
    "ea_col_from": "2014",
    "ea_col_to": "2016",
    "ea_col_graduate": "yes",
    "ea_col_degree": "AA Culinary Arts",
    "ea_oth_name": "Le Cordon Bleu",
    "ea_oth_address": "521 E Green St, Pasadena CA",
    "ea_oth_from": "2016",
    "ea_oth_to": "2017",
    "ea_oth_graduate": "yes",
    "ea_oth_degree": "Certificate",
    # References
    "ea_ref0_name": "Maria Fernandez",
    "ea_ref0_relationship": "Former Manager",
    "ea_ref0_company": "Pollo Tropical",
    "ea_ref0_phone": "(305) 555-1111",
    "ea_ref0_address": "1800 Biscayne Blvd, Miami FL 33132",
    "ea_ref1_name": "Jose Hernandez",
    "ea_ref1_relationship": "Coworker",
    "ea_ref1_company": "Versailles Restaurant",
    "ea_ref1_phone": "(786) 555-2222",
    "ea_ref1_address": "3555 SW 8th St, Miami FL 33135",
    "ea_ref2_name": "Ana Martinez",
    "ea_ref2_relationship": "Professor",
    "ea_ref2_company": "Miami Dade College",
    "ea_ref2_phone": "(305) 555-3333",
    "ea_ref2_address": "300 NE 2nd Ave, Miami FL 33132",
    # Employment history
    "ea_emp0_company": "Pollo Tropical #127",
    "ea_emp0_phone": "(305) 555-4444",
    "ea_emp0_address": "1800 Biscayne Blvd, Miami FL",
    "ea_emp0_supervisor": "Maria Fernandez",
    "ea_emp0_title": "Prep Cook",
    "ea_emp0_start_salary": "$14/hr",
    "ea_emp0_end_salary": "$16/hr",
    "ea_emp0_responsibilities": "Food prep, cooking, cleaning station",
    "ea_emp0_from": "01/2020",
    "ea_emp0_to": "06/2023",
    "ea_emp0_reason": "Career growth",
    "ea_emp0_contact": "yes",
    "ea_emp1_company": "Versailles Restaurant",
    "ea_emp1_phone": "(786) 555-5555",
    "ea_emp1_address": "3555 SW 8th St, Miami FL",
    "ea_emp1_supervisor": "Pedro Gomez",
    "ea_emp1_title": "Line Cook",
    "ea_emp1_start_salary": "$15/hr",
    "ea_emp1_end_salary": "$17/hr",
    "ea_emp1_responsibilities": "Grill station, entrees, plating",
    "ea_emp1_from": "07/2023",
    "ea_emp1_to": "03/2026",
    "ea_emp1_reason": "Relocation",
    "ea_emp1_contact": "yes",
    "ea_emp2_company": "Flanigan's Seafood",
    "ea_emp2_phone": "(954) 555-6666",
    "ea_emp2_address": "100 E Broward Blvd, Fort Lauderdale FL",
    "ea_emp2_supervisor": "Tom Wilson",
    "ea_emp2_title": "Kitchen Helper",
    "ea_emp2_start_salary": "$12/hr",
    "ea_emp2_end_salary": "$13/hr",
    "ea_emp2_responsibilities": "Dishwashing, prep assistance",
    "ea_emp2_from": "06/2018",
    "ea_emp2_to": "12/2019",
    "ea_emp2_reason": "Seasonal",
    "ea_emp2_contact": "no",
    # Military
    "ea_mil_branch": "U.S. Army",
    "ea_mil_from": "2017",
    "ea_mil_to": "2019",
    "ea_mil_rank": "E-4 Specialist",
    "ea_mil_discharge_type": "Honorable",
    "ea_mil_explain": "",
    # Signature
    "ea_signature": "Carlos A. Rodriguez",
    "ea_sign_date": "04/26/2026",

    # ═══ DIRECT DEPOSIT ═══
    "dd_bank_name": "Chase Bank",
    "dd_fee_accept": "yes",
    "dd_acct1_type": "checking",
    "dd_acct1_routing": "067014822",
    "dd_acct1_number": "9876543210",
    "dd_acct1_amount": "100%",
    "dd_acct2_type": "savings",
    "dd_acct2_routing": "067014999",
    "dd_acct2_number": "1112223334",
    "dd_signature": "Carlos A. Rodriguez",
    "dd_employee_id": "CK-2026-087",
    "dd_print_name": "Carlos A. Rodriguez",
    "dd_date": "04/26/2026",

    # ═══ W-4 ═══
    "w4_first_name": "Carlos A.",
    "w4_last_name": "Rodriguez",
    "w4_ssn": "123-45-6789",
    "w4_address": "2450 SW 8th Street, Apt 15B",
    "w4_city_state_zip": "Miami, FL 33135",
    "w4_filing_status": "single",
    "w4_two_jobs": "False",
    "w4_children": "2",
    "w4_other_deps": "1",
    "w4_other_credits": "0",
    "w4_total_step3": "4900",
    "w4_other_income": "500",
    "w4_deductions": "0",
    "w4_extra_withholding": "25",
    "w4_exempt": "False",
    "w4_signature": "Carlos A. Rodriguez",
    "w4_date": "04/26/2026",
    "w4_employer_name": "Chicken Kitchen LLC, 2390 NW 2nd Ave, Miami FL",
    "w4_first_date": "05/15/2026",
    "w4_ein": "59-1234567",

    # ═══ I-9 ═══
    "i9_last_name": "Rodriguez",
    "i9_first_name": "Carlos",
    "i9_middle_initial": "A",
    "i9_other_names": "N/A",
    "i9_address": "2450 SW 8th Street",
    "i9_apt": "15B",
    "i9_city": "Miami",
    "i9_state": "FL",
    "i9_zip": "33135",
    "i9_dob": "03/15/1996",
    "i9_ssn": "123-45-6789",
    "i9_email": "carlos.rodriguez@email.com",
    "i9_phone": "(305) 555-7890",
    "i9_status": "citizen",
    "i9_uscis": "",
    "i9_i94": "",
    "i9_passport": "",
    "i9_country": "",
    "i9_exp_date": "",
    "i9_employee_sig": "Carlos A. Rodriguez",
    "i9_employee_date": "04/26/2026",
    # Section 2 - List A
    "i9_lista_title": "U.S. Passport",
    "i9_lista_issuing": "U.S. Dept of State",
    "i9_lista_number": "C04567891",
    "i9_lista_exp": "06/20/2030",
    # Section 2 - List B
    "i9_listb_title": "FL Driver License",
    "i9_listb_issuing": "FL DHSMV",
    "i9_listb_number": "R520-123-45-678-0",
    "i9_listb_exp": "03/15/2028",
    # Section 2 - List C
    "i9_listc_title": "Social Security Card",
    "i9_listc_issuing": "SSA",
    "i9_listc_number": "123-45-6789",
    "i9_listc_exp": "N/A",
    # Employer section
    "i9_first_day": "05/15/2026",
    "i9_employer_name": "Chicken Kitchen LLC",
    "i9_employer_sig": "Monica Zamora",
    "i9_employer_date": "05/15/2026",
    "i9_employer_biz": "Chicken Kitchen LLC",
    "i9_employer_addr": "2390 NW 2nd Ave, Miami FL 33127",

    # ═══ PAYROLL ACTION ═══
    "pa_name": "Carlos A. Rodriguez",
    "pa_date_action": "04/26/2026",
    "pa_job_title": "Line Cook",
    "pa_store_name": "CK Brickell",
    "pa_employee_id": "CK-2026-087",
    "pa_supervisor": "Monica Zamora",
    "pa_dob": "03/15/1996",
    "pa_address": "2450 SW 8th Street, Apt 15B",
    "pa_city": "Miami",
    "pa_state": "FL",
    "pa_zip": "33135",
    "pa_rate_of_pay": "17.00",
    "pa_pay_type": "hourly",
    "pa_increase_amount": "",
    "pa_from_title": "",
    "pa_to_title": "",
    "pa_from_store": "",
    "pa_to_store": "",
    "pa_out_from": "",
    "pa_out_to": "",
    "pa_last_date": "",
    "pa_new_hire": "True",
    "pa_rehire": "False",
    "pa_salary_increase": "False",
    "pa_promotion": "False",
    "pa_demotion": "False",
    "pa_transfer": "False",
    "pa_vacation": "False",
    "pa_leave": "False",
    "pa_termination": "False",
    "pa_change_address": "False",
    "pa_other": "False",
    "pa_eligible_rehire": "yes",
    "pa_cause_change": "New hire - starting position as Line Cook",
    "pa_mgr_sig": "Monica Zamora",
    "pa_sup_sig": "Laura Perez",
}


def get_val(key):
    return TEST_DATA.get(key, "")


def main():
    out_dir = os.path.join(tempfile.gettempdir(), "ck_test_all_forms")
    os.makedirs(out_dir, exist_ok=True)

    forms = ["employee_app", "direct_deposit", "w4", "i9", "payroll"]

    for form_key in forms:
        pdf_path = os.path.join(out_dir, f"{form_key}_test.pdf")
        print(f"Generating {form_key}...")
        fill_template(form_key, get_val, pdf_path)
        print(f"  -> {pdf_path}")

    # Render all pages to PNG using PyMuPDF
    try:
        import fitz
        print("\nRendering pages to PNG...")
        for form_key in forms:
            pdf_path = os.path.join(out_dir, f"{form_key}_test.pdf")
            doc = fitz.open(pdf_path)
            for i, page in enumerate(doc):
                pix = page.get_pixmap(dpi=200)
                img_path = os.path.join(out_dir, f"{form_key}_p{i+1}.png")
                pix.save(img_path)
                print(f"  {form_key} page {i+1} -> {img_path}")
            doc.close()
    except ImportError:
        print("\nPyMuPDF (fitz) not installed - skipping PNG render.")
        print("Install with: pip install PyMuPDF")

    print(f"\nAll files in: {out_dir}")


if __name__ == "__main__":
    main()
