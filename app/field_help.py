"""
Field-level help tooltips for all forms.
Each entry: field_key -> {"en": (description, example), "es": (description, example)}
"""

FIELD_TIPS = {
    # ═══════════════════════════════════════
    # EMPLOYEE APPLICATION
    # ═══════════════════════════════════════
    "ea_last_name": {
        "en": ("Your legal last name (family name)", "Garcia"),
        "es": ("Su apellido legal", "Garcia"),
    },
    "ea_first_name": {
        "en": ("Your legal first name", "Maria"),
        "es": ("Su nombre legal", "Maria"),
    },
    "ea_mi": {
        "en": ("Middle initial only", "L"),
        "es": ("Solo la inicial del segundo nombre", "L"),
    },
    "ea_date": {
        "en": ("Today's date in mm/dd/yyyy format", "04/25/2026"),
        "es": ("Fecha de hoy en formato mm/dd/aaaa", "04/25/2026"),
    },
    "ea_street_address": {
        "en": ("Your street number and name", "1250 NW 7th Street"),
        "es": ("Numero y nombre de su calle", "1250 NW 7th Street"),
    },
    "ea_apt": {
        "en": ("Apartment, suite, or unit number", "Apt 302"),
        "es": ("Numero de apartamento o unidad", "Apt 302"),
    },
    "ea_city": {
        "en": ("City where you live", "Miami"),
        "es": ("Ciudad donde vive", "Miami"),
    },
    "ea_state": {
        "en": ("Two-letter state abbreviation", "FL"),
        "es": ("Abreviatura del estado (2 letras)", "FL"),
    },
    "ea_zip": {
        "en": ("5-digit ZIP code", "33125"),
        "es": ("Codigo postal de 5 digitos", "33125"),
    },
    "ea_phone": {
        "en": ("Your phone number with area code", "(305) 555-1234"),
        "es": ("Su numero de telefono con codigo de area", "(305) 555-1234"),
    },
    "ea_email": {
        "en": ("Your email address", "maria@email.com"),
        "es": ("Su correo electronico", "maria@email.com"),
    },
    "ea_ssn": {
        "en": ("Social Security Number (XXX-XX-XXXX)", "123-45-6789"),
        "es": ("Numero de Seguro Social (XXX-XX-XXXX)", "123-45-6789"),
    },
    "ea_date_available": {
        "en": ("Date you can start working", "05/01/2026"),
        "es": ("Fecha en que puede empezar a trabajar", "05/01/2026"),
    },
    "ea_desired_salary": {
        "en": ("Your desired hourly rate or salary", "$16/hr"),
        "es": ("Su tarifa por hora o salario deseado", "$16/hr"),
    },
    "ea_position": {
        "en": ("Job position you are applying for", "Cashier"),
        "es": ("Puesto al que aplica", "Cajero"),
    },

    # ═══════════════════════════════════════
    # DIRECT DEPOSIT
    # ═══════════════════════════════════════
    "dd_acct1_routing": {
        "en": ("9-digit bank routing number from your check", "067014822"),
        "es": ("Numero de ruta bancaria de 9 digitos de su cheque", "067014822"),
    },
    "dd_acct1_number": {
        "en": ("Your bank account number", "1234567890"),
        "es": ("Su numero de cuenta bancaria", "1234567890"),
    },
    "dd_acct1_amount": {
        "en": ("Percentage or fixed dollar amount to deposit", "100% or $500"),
        "es": ("Porcentaje o monto fijo a depositar", "100% o $500"),
    },
    "dd_print_name": {
        "en": ("Print your full legal name clearly", "Maria L. Garcia"),
        "es": ("Escriba su nombre legal completo claramente", "Maria L. Garcia"),
    },
    "dd_employee_id": {
        "en": ("Your employee ID number", "CK-2026-042"),
        "es": ("Su numero de ID de empleado", "CK-2026-042"),
    },

    # ═══════════════════════════════════════
    # W-4 FORM
    # ═══════════════════════════════════════
    "w4_first_name": {
        "en": ("First name and middle initial as shown on SSN card", "Maria L."),
        "es": ("Nombre y segundo nombre como aparece en tarjeta de SSN", "Maria L."),
    },
    "w4_last_name": {
        "en": ("Last name as shown on your Social Security card", "Garcia"),
        "es": ("Apellido como aparece en su tarjeta de Seguro Social", "Garcia"),
    },
    "w4_ssn": {
        "en": ("Your 9-digit Social Security Number", "123-45-6789"),
        "es": ("Su Numero de Seguro Social de 9 digitos", "123-45-6789"),
    },
    "w4_address": {
        "en": ("Your home street address", "1250 NW 7th St, Apt 302"),
        "es": ("Su direccion de casa", "1250 NW 7th St, Apt 302"),
    },
    "w4_city_state_zip": {
        "en": ("City, state abbreviation, and ZIP code", "Miami, FL 33125"),
        "es": ("Ciudad, abreviatura del estado y codigo postal", "Miami, FL 33125"),
    },
    "w4_children": {
        "en": ("Number of qualifying children under 17.\nThe form will calculate: count x $2,200", "2"),
        "es": ("Numero de hijos calificados menores de 17.\nEl formulario calculara: cantidad x $2,200", "2"),
    },
    "w4_other_deps": {
        "en": ("Number of other dependents.\nThe form will calculate: count x $500", "1"),
        "es": ("Numero de otros dependientes.\nEl formulario calculara: cantidad x $500", "1"),
    },
    "w4_other_credits": {
        "en": ("Dollar amount for other credits (if any)", "0"),
        "es": ("Monto en dolares por otros creditos (si aplica)", "0"),
    },
    "w4_total_step3": {
        "en": ("Auto-calculated: (children x $2,200) + (deps x $500) + other credits", "4900"),
        "es": ("Auto-calculado: (hijos x $2,200) + (deps x $500) + otros creditos", "4900"),
    },
    "w4_other_income": {
        "en": ("Other income not from jobs (interest, dividends, retirement)", "500"),
        "es": ("Otros ingresos no de empleos (intereses, dividendos, jubilacion)", "500"),
    },
    "w4_deductions": {
        "en": ("Deductions amount (see Deductions Worksheet on W-4 page 4)", "1000"),
        "es": ("Monto de deducciones (vea la Hoja de Deducciones en pagina 4 del W-4)", "1000"),
    },
    "w4_extra_withholding": {
        "en": ("Additional tax to withhold each pay period", "50"),
        "es": ("Impuesto adicional a retener cada periodo de pago", "50"),
    },
    "w4_employer_name": {
        "en": ("Employer fills this: company name and address", "Chicken Kitchen LLC"),
        "es": ("El empleador llena esto: nombre y direccion de la empresa", "Chicken Kitchen LLC"),
    },
    "w4_first_date": {
        "en": ("First date of employment (mm/dd/yyyy)", "05/01/2026"),
        "es": ("Primera fecha de empleo (mm/dd/aaaa)", "05/01/2026"),
    },
    "w4_ein": {
        "en": ("Employer Identification Number (XX-XXXXXXX)", "59-1234567"),
        "es": ("Numero de Identificacion del Empleador (XX-XXXXXXX)", "59-1234567"),
    },

    # ═══════════════════════════════════════
    # I-9 FORM
    # ═══════════════════════════════════════
    "i9_last_name": {
        "en": ("Your legal last name (family name)", "Garcia"),
        "es": ("Su apellido legal", "Garcia"),
    },
    "i9_first_name": {
        "en": ("Your legal first name (given name)", "Maria"),
        "es": ("Su nombre legal", "Maria"),
    },
    "i9_other_names": {
        "en": ("Any other last names used (maiden name, etc.)", "Garcia Lopez"),
        "es": ("Otros apellidos usados (nombre de soltera, etc.)", "Garcia Lopez"),
    },
    "i9_dob": {
        "en": ("Date of birth in mm/dd/yyyy", "03/15/1996"),
        "es": ("Fecha de nacimiento en mm/dd/aaaa", "03/15/1996"),
    },
    "i9_ssn": {
        "en": ("U.S. Social Security Number (XXX-XX-XXXX)", "123-45-6789"),
        "es": ("Numero de Seguro Social de EE.UU. (XXX-XX-XXXX)", "123-45-6789"),
    },
    "i9_lista_title": {
        "en": ("List A document title (e.g., U.S. Passport, Permanent Resident Card)", "U.S. Passport"),
        "es": ("Titulo del documento Lista A (ej. Pasaporte de EE.UU., Tarjeta de Residente)", "Pasaporte de EE.UU."),
    },
    "i9_listb_title": {
        "en": ("List B document for identity (e.g., Driver's License, State ID)", "FL Driver License"),
        "es": ("Documento Lista B para identidad (ej. Licencia de Conducir)", "Licencia de FL"),
    },
    "i9_listc_title": {
        "en": ("List C document for work authorization (e.g., Social Security Card, Birth Certificate)", "Social Security Card"),
        "es": ("Documento Lista C para autorizacion de trabajo (ej. Tarjeta de Seguro Social)", "Tarjeta de Seguro Social"),
    },

    # ═══════════════════════════════════════
    # PAYROLL ACTION
    # ═══════════════════════════════════════
    "pa_name": {
        "en": ("Employee's full legal name", "Maria L. Garcia"),
        "es": ("Nombre legal completo del empleado", "Maria L. Garcia"),
    },
    "pa_store_name": {
        "en": ("Store or location name", "CK Brickell"),
        "es": ("Nombre de la tienda o ubicacion", "CK Brickell"),
    },
    "pa_rate_of_pay": {
        "en": ("Hourly rate or weekly pay amount", "16.00"),
        "es": ("Tarifa por hora o monto de pago semanal", "16.00"),
    },
    "pa_cause_change": {
        "en": ("Reason for the payroll action", "New hire - starting position"),
        "es": ("Razon de la accion de nomina", "Nueva contratacion - puesto inicial"),
    },
}


def get_tip(field_key, lang="en"):
    """Get tooltip (description, example) for a field. Returns None if no tip."""
    tip = FIELD_TIPS.get(field_key)
    if tip is None:
        return None
    return tip.get(lang, tip.get("en"))
