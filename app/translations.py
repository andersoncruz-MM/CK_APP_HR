"""
Translations module for CK HR Forms Application.
All UI text in English, Spanish, and Haitian Creole.
"""

TRANSLATIONS = {
    # ── App-level ──
    "app_title": {
        "en": "Chicken Kitchen - HR Forms",
        "es": "Chicken Kitchen - Formularios de RR.HH.",
        "ht": "Chicken Kitchen - Fom RH"
    },
    "language": {"en": "Language", "es": "Idioma", "ht": "Lang"},
    "export_pdf": {"en": "Export PDF", "es": "Exportar PDF", "ht": "Ekspote PDF"},
    "clear_form": {"en": "Clear Form", "es": "Limpiar Formulario", "ht": "Efase Fom"},
    "save_pdf_title": {"en": "Save PDF", "es": "Guardar PDF", "ht": "Anrejistre PDF"},
    "pdf_saved": {"en": "PDF saved successfully!", "es": "PDF guardado exitosamente!", "ht": "PDF anrejistre avek siksè!"},
    "pdf_error": {"en": "Error saving PDF", "es": "Error al guardar PDF", "ht": "Erè pandan anrejistreman PDF"},
    "yes": {"en": "YES", "es": "SI", "ht": "WI"},
    "no": {"en": "NO", "es": "NO", "ht": "NON"},
    "date_format_hint": {"en": "(mm/dd/yyyy)", "es": "(mm/dd/aaaa)", "ht": "(mm/jj/aaaa)"},
    "instructions_title": {"en": "Instructions", "es": "Instrucciones", "ht": "Enstriksyon"},
    "instructions_btn": {"en": "? Instructions", "es": "? Instrucciones", "ht": "? Enstriksyon"},
    "area_code": {"en": "Area Code", "es": "Cod. Area", "ht": "Kòd Zòn"},
    "signature": {"en": "Signature", "es": "Firma", "ht": "Siyati"},
    "date": {"en": "Date", "es": "Fecha", "ht": "Dat"},
    "select_form": {"en": "Select a form from the left panel", "es": "Seleccione un formulario del panel izquierdo", "ht": "Chwazi yon fom nan panno agoch la"},
    "company_name": {"en": "Chicken Kitchen", "es": "Chicken Kitchen", "ht": "Chicken Kitchen"},
    "page": {"en": "Page", "es": "Pagina", "ht": "Paj"},

    # ── Form names (sidebar) ──
    "form_employee_app": {
        "en": "Employee\nApplication",
        "es": "Solicitud de\nEmpleo",
        "ht": "Aplikasyon\nAnplwaye"
    },
    "form_direct_deposit": {
        "en": "Direct Deposit\nAuthorization",
        "es": "Autorizacion de\nDeposito Directo",
        "ht": "Otorizasyon\nDepo Dirèk"
    },
    "form_w4": {
        "en": "W-4 Form\n(2026)",
        "es": "Formulario W-4\n(2026)",
        "ht": "Fom W-4\n(2026)"
    },
    "form_i9": {
        "en": "I-9 Form",
        "es": "Formulario I-9",
        "ht": "Fom I-9"
    },
    "form_payroll": {
        "en": "Payroll\nAction Form",
        "es": "Formulario de\nAccion de Nomina",
        "ht": "Fom Aksyon\nPeman"
    },

    # ═══════════════════════════════════════════════
    # FORM 1: EMPLOYEE APPLICATION
    # ═══════════════════════════════════════════════
    "ea_title": {
        "en": "Employee Application",
        "es": "Solicitud de Empleo",
        "ht": "Aplikasyon Anplwaye"
    },

    # Applicant Information
    "ea_applicant_info": {"en": "Applicant Information", "es": "Informacion del Solicitante", "ht": "Enfòmasyon sou Aplikan an"},
    "ea_last_name": {"en": "Last Name", "es": "Apellido", "ht": "Siyati"},
    "ea_first_name": {"en": "First Name", "es": "Nombre", "ht": "Non"},
    "ea_mi": {"en": "M.I.", "es": "Inicial", "ht": "Inisyal"},
    "ea_date": {"en": "Date", "es": "Fecha", "ht": "Dat"},
    "ea_street_address": {"en": "Street Address", "es": "Direccion", "ht": "Adrès Ri"},
    "ea_apt": {"en": "Apartment/Unit #", "es": "Apto/Unidad #", "ht": "Apatman/Inite #"},
    "ea_city": {"en": "City", "es": "Ciudad", "ht": "Vil"},
    "ea_state": {"en": "State", "es": "Estado", "ht": "Eta"},
    "ea_zip": {"en": "ZIP", "es": "Codigo Postal", "ht": "Kòd Postal"},
    "ea_phone": {"en": "Phone", "es": "Telefono", "ht": "Telefòn"},
    "ea_email": {"en": "E-mail Address", "es": "Correo Electronico", "ht": "Adrès Imèl"},
    "ea_date_available": {"en": "Date Available", "es": "Fecha Disponible", "ht": "Dat Disponib"},
    "ea_ssn": {"en": "Social Security No.", "es": "No. de Seguro Social", "ht": "No. Sekirite Sosyal"},
    "ea_desired_salary": {"en": "Desired Salary", "es": "Salario Deseado", "ht": "Salè Ou Vle"},
    "ea_position": {"en": "Position Applied for", "es": "Puesto Solicitado", "ht": "Pòs Ou Aplike Pou"},
    "ea_citizen": {
        "en": "Are you a citizen of the United States?",
        "es": "Es usted ciudadano de los Estados Unidos?",
        "ht": "Èske ou se yon sitwayen Etazini?"
    },
    "ea_authorized": {
        "en": "If no, are you authorized to work in the U.S.?",
        "es": "Si no, esta autorizado para trabajar en EE.UU.?",
        "ht": "Si non, èske ou gen otorizasyon pou travay nan Etazini?"
    },
    "ea_worked_before": {
        "en": "Have you ever worked for this company?",
        "es": "Ha trabajado anteriormente para esta empresa?",
        "ht": "Èske ou te janm travay pou konpayi sa a?"
    },
    "ea_when": {"en": "If so, when?", "es": "Si es asi, cuando?", "ht": "Si wi, kilè?"},
    "ea_felony": {
        "en": "Have you ever been convicted of a felony?",
        "es": "Ha sido condenado por un delito grave?",
        "ht": "Èske yo te janm kondane ou pou yon krim grav?"
    },
    "ea_felony_explain": {"en": "If yes, explain", "es": "Si es asi, explique", "ht": "Si wi, esplike"},

    # Education
    "ea_education": {"en": "Education", "es": "Educacion", "ht": "Edikasyon"},
    "ea_high_school": {"en": "High School", "es": "Escuela Secundaria", "ht": "Lekòl Segondè"},
    "ea_college": {"en": "College", "es": "Universidad", "ht": "Inivèsite"},
    "ea_other_edu": {"en": "Other", "es": "Otro", "ht": "Lòt"},
    "ea_address": {"en": "Address", "es": "Direccion", "ht": "Adrès"},
    "ea_from": {"en": "From", "es": "Desde", "ht": "Depi"},
    "ea_to": {"en": "To", "es": "Hasta", "ht": "Jiska"},
    "ea_graduate": {"en": "Did you graduate?", "es": "Se graduo?", "ht": "Èske ou te gradye?"},
    "ea_degree": {"en": "Degree", "es": "Titulo", "ht": "Diplòm"},

    # References
    "ea_references": {"en": "References", "es": "Referencias", "ht": "Referans"},
    "ea_ref_note": {
        "en": "Please list three professional references.",
        "es": "Por favor indique tres referencias profesionales.",
        "ht": "Tanpri bay twa referans pwofesyonèl."
    },
    "ea_full_name": {"en": "Full Name", "es": "Nombre Completo", "ht": "Non Konplè"},
    "ea_relationship": {"en": "Relationship", "es": "Relacion", "ht": "Relasyon"},
    "ea_company": {"en": "Company", "es": "Empresa", "ht": "Konpayi"},

    # Previous Employment
    "ea_prev_employment": {"en": "Previous Employment", "es": "Empleo Anterior", "ht": "Travay Anvan"},
    "ea_supervisor": {"en": "Supervisor", "es": "Supervisor", "ht": "Sipèvizè"},
    "ea_job_title": {"en": "Job Title", "es": "Puesto", "ht": "Tit Travay"},
    "ea_starting_salary": {"en": "Starting Salary", "es": "Salario Inicial", "ht": "Salè Kòmansman"},
    "ea_ending_salary": {"en": "Ending Salary", "es": "Salario Final", "ht": "Salè Final"},
    "ea_responsibilities": {"en": "Responsibilities", "es": "Responsabilidades", "ht": "Responsablite"},
    "ea_reason_leaving": {"en": "Reason for Leaving", "es": "Razon de Salida", "ht": "Rezon Ou Te Kite"},
    "ea_contact_supervisor": {
        "en": "May we contact your previous supervisor for a reference?",
        "es": "Podemos contactar a su supervisor anterior como referencia?",
        "ht": "Èske nou ka kontakte ansyen sipèvizè ou pou yon referans?"
    },

    # Military
    "ea_military": {"en": "Military Service", "es": "Servicio Militar", "ht": "Sèvis Militè"},
    "ea_branch": {"en": "Branch", "es": "Rama", "ht": "Branch"},
    "ea_rank_discharge": {"en": "Rank at Discharge", "es": "Rango al Ser Dado de Baja", "ht": "Grad lè Ou Te Kite"},
    "ea_type_discharge": {"en": "Type of Discharge", "es": "Tipo de Baja", "ht": "Tip Liberasyon"},
    "ea_other_than_honorable": {
        "en": "If other than honorable, explain",
        "es": "Si no fue honorable, explique",
        "ht": "Si li pa te onorab, esplike"
    },

    # Disclaimer
    "ea_disclaimer": {"en": "Disclaimer and Signature", "es": "Declaracion y Firma", "ht": "Deklarasyon ak Siyati"},
    "ea_disclaimer_text": {
        "en": "I certify that my answers are true and complete to the best of my knowledge.\nIf this application leads to employment, I understand that false or misleading information in my application or interview may result in my release.",
        "es": "Certifico que mis respuestas son verdaderas y completas a mi mejor saber.\nSi esta solicitud conduce a empleo, entiendo que informacion falsa o enganosa en mi solicitud o entrevista puede resultar en mi despido.",
        "ht": "Mwen sètifye ke repons mwen yo vrè epi konplè dapre sa mwen konnen.\nSi aplikasyon sa a mennen nan yon travay, mwen konprann ke fo enfòmasyon oswa enfòmasyon ki twonpe nan aplikasyon mwen oswa entèvyou mwen ka lakòz revokasyon mwen."
    },

    # ═══════════════════════════════════════════════
    # FORM 2: DIRECT DEPOSIT AUTHORIZATION
    # ═══════════════════════════════════════════════
    "dd_title": {
        "en": "Employee Direct Deposit Authorization Form",
        "es": "Formulario de Autorizacion de Deposito Directo",
        "ht": "Fom Otorizasyon Depo Dirèk Anplwaye"
    },
    "dd_instructions": {
        "en": "Employee: Fill out and return to your employer.\nEmployer: Save for your files only. Do not send this form to Intuit.",
        "es": "Empleado: Complete y devuelva a su empleador.\nEmpleador: Guarde solo para sus archivos. No envie este formulario a Intuit.",
        "ht": "Anplwaye: Ranpli epi retounen bay anplwayè ou.\nAnplwayè: Konsève pou dosye ou sèlman. Pa voye fom sa a bay Intuit."
    },
    "dd_account1": {"en": "Account 1", "es": "Cuenta 1", "ht": "Kont 1"},
    "dd_account2": {"en": "Account 2 (remainder deposited here)", "es": "Cuenta 2 (el resto se deposita aqui)", "ht": "Kont 2 (rès la depoze la a)"},
    "dd_account_type": {"en": "Account Type", "es": "Tipo de Cuenta", "ht": "Tip Kont"},
    "dd_checking": {"en": "Checking", "es": "Corriente", "ht": "Kont Kouran"},
    "dd_savings": {"en": "Savings", "es": "Ahorros", "ht": "Epay"},
    "dd_routing": {"en": "Bank Routing Number (ABA)", "es": "Numero de Ruta Bancaria (ABA)", "ht": "Nimewo Routaj Bank (ABA)"},
    "dd_account_number": {"en": "Account Number", "es": "Numero de Cuenta", "ht": "Nimewo Kont"},
    "dd_amount": {
        "en": "Percentage or dollar amount to deposit",
        "es": "Porcentaje o monto en dolares a depositar",
        "ht": "Pousantaj oswa montan an dola pou depoze"
    },
    "dd_authorization": {"en": "Authorization", "es": "Autorizacion", "ht": "Otorizasyon"},
    "dd_auth_text": {
        "en": "This authorizes {company} (the \"Company\") to send credit entries (and appropriate debit and adjustment entries), electronically or by any other commercially accepted method, to my account(s) indicated above. This authorizes the financial institution holding the Account to post all such entries. I agree that the ACH transactions authorized herein shall comply with all applicable U.S. Law. This authorization will be in effect until the Company receives a written termination notice from myself and has a reasonable opportunity to act on it.",
        "es": "Esto autoriza a {company} (la \"Empresa\") a enviar entradas de credito (y entradas de debito y ajuste apropiadas), electronicamente o por cualquier otro metodo comercialmente aceptado, a mi(s) cuenta(s) indicada(s) arriba. Esto autoriza a la institucion financiera que mantiene la Cuenta a registrar todas dichas entradas. Acepto que las transacciones ACH autorizadas aqui cumpliran con todas las leyes aplicables de EE.UU. Esta autorizacion estara vigente hasta que la Empresa reciba un aviso de terminacion por escrito de mi parte y tenga una oportunidad razonable para actuar al respecto.",
        "ht": "Sa a otorize {company} (\"Konpayi a\") pou voye antre kredi (ak antre debi ak ajisteman apwopriye), pa vwa elektwonik oswa pa nenpòt lòt metòd komèsyalman aksepte, nan kont mwen yo ki endike anwo a. Sa a otorize enstitisyon finansyè ki kenbe Kont lan pou anrejistre tout antre sa yo. Mwen dakò ke tranzaksyon ACH ki otorize la a dwe konfòme ak tout lwa ameriken ki aplikab. Otorizasyon sa a ap rete an vigè jiskaske Konpayi a resevwa yon avi tèminasyon alekri nan men mwen epi li gen yon opòtinite rezonab pou aji sou li."
    },
    "dd_company_name_field": {"en": "Company Name", "es": "Nombre de la Empresa", "ht": "Non Konpayi"},
    "dd_employee_id": {"en": "Employee ID #", "es": "ID de Empleado #", "ht": "ID Anplwaye #"},
    "dd_print_name": {"en": "Print Name", "es": "Nombre en Letra de Molde", "ht": "Ekri Non"},

    # DD Bank Name
    "dd_bank_name": {"en": "Bank Name", "es": "Nombre del Banco", "ht": "Non Bank la"},

    # DD $5 Fee
    "dd_fee_notice": {
        "en": "A $5.00 fee will be charged for direct deposit.",
        "es": "Se cobrara un cargo de $5.00 por deposito directo.",
        "ht": "Yo pral chaje $5.00 pou depo dirèk."
    },
    "dd_fee_accept": {
        "en": "I accept the $5.00 direct deposit fee",
        "es": "Acepto el cargo de $5.00 por deposito directo",
        "ht": "Mwen aksepte frè $5.00 pou depo dirèk la"
    },
    "dd_bank_other": {
        "en": "Other (write)",
        "es": "Otro (escriba)",
        "ht": "Lòt (ekri)"
    },

    # ═══════════════════════════════════════════════
    # FORM 3: W-4 (2026)
    # ═══════════════════════════════════════════════
    "w4_title": {
        "en": "Form W-4 - Employee's Withholding Certificate (2026)",
        "es": "Formulario W-4 - Certificado de Retenciones del Empleado (2026)",
        "ht": "Fom W-4 - Sètifika Retansyon Anplwaye a (2026)"
    },
    "w4_step1": {"en": "Step 1: Personal Information", "es": "Paso 1: Informacion Personal", "ht": "Etap 1: Enfòmasyon Pèsonèl"},
    "w4_first_name": {"en": "First name and middle initial", "es": "Nombre y segundo nombre", "ht": "Non ak inisyal dezyèm non"},
    "w4_last_name": {"en": "Last name", "es": "Apellido", "ht": "Siyati"},
    "w4_address": {"en": "Address", "es": "Direccion", "ht": "Adrès"},
    "w4_city_state_zip": {"en": "City or town, state, and ZIP code", "es": "Ciudad, estado y codigo postal", "ht": "Vil oswa bouk, eta, ak kòd postal"},
    "w4_ssn": {"en": "Social Security Number", "es": "Numero de Seguro Social", "ht": "Nimewo Sekirite Sosyal"},
    "w4_filing_status": {"en": "Filing Status", "es": "Estado Civil para Declarar", "ht": "Estati Deklarasyon"},
    "w4_single": {"en": "Single or Married filing separately", "es": "Soltero o Casado declarando por separado", "ht": "Selibatè oswa Marye k ap deklare apa"},
    "w4_married": {
        "en": "Married filing jointly or Qualifying surviving spouse",
        "es": "Casado declarando en conjunto o Conyuge sobreviviente calificado",
        "ht": "Marye k ap deklare ansanm oswa Konjwen sivivan ki kalifye"
    },
    "w4_head": {
        "en": "Head of household",
        "es": "Jefe de familia",
        "ht": "Chèf kay"
    },

    "w4_step2": {"en": "Step 2: Multiple Jobs or Spouse Works", "es": "Paso 2: Multiples Empleos o Conyuge Trabaja", "ht": "Etap 2: Plizyè Travay oswa Konjwen Travay"},
    "w4_step2_check": {
        "en": "Check here if there are only two jobs total (you may also check the box on the W-4 for the other job)",
        "es": "Marque aqui si solo hay dos empleos en total (tambien puede marcar la casilla en el W-4 del otro empleo)",
        "ht": "Tcheke la a si gen sèlman de travay antou (ou ka tcheke bwat la tou sou W-4 lòt travay la)"
    },

    "w4_step3": {"en": "Step 3: Claim Dependents", "es": "Paso 3: Reclamar Dependientes", "ht": "Etap 3: Reklame Depandan"},
    "w4_children": {
        "en": "Number of qualifying children under age 17 (x $2,200)",
        "es": "Numero de hijos calificados menores de 17 anos (x $2,200)",
        "ht": "Kantite timoun ki kalifye ki gen mwens pase 17 an (x $2,200)"
    },
    "w4_other_dependents": {
        "en": "Number of other dependents (x $500)",
        "es": "Numero de otros dependientes (x $500)",
        "ht": "Kantite lòt depandan (x $500)"
    },
    "w4_other_credits": {"en": "Amount for other credits", "es": "Monto por otros creditos", "ht": "Montan pou lòt kredi"},
    "w4_total_step3": {"en": "Total (Step 3)", "es": "Total (Paso 3)", "ht": "Total (Etap 3)"},

    "w4_step4": {"en": "Step 4: Other Adjustments", "es": "Paso 4: Otros Ajustes", "ht": "Etap 4: Lòt Ajisteman"},
    "w4_other_income": {
        "en": "4(a) Other income (not from jobs)",
        "es": "4(a) Otros ingresos (no de empleos)",
        "ht": "4(a) Lòt revni (pa soti nan travay)"
    },
    "w4_deductions": {
        "en": "4(b) Deductions",
        "es": "4(b) Deducciones",
        "ht": "4(b) Dediksyon"
    },
    "w4_extra_withholding": {
        "en": "4(c) Extra withholding per pay period",
        "es": "4(c) Retencion adicional por periodo de pago",
        "ht": "4(c) Retansyon anplis pa peryòd peman"
    },
    "w4_exempt": {
        "en": "Exempt from withholding (check if applicable)",
        "es": "Exento de retenciones (marque si aplica)",
        "ht": "Egzante de retansyon (tcheke si sa aplike)"
    },

    "w4_step5": {"en": "Step 5: Sign Here", "es": "Paso 5: Firme Aqui", "ht": "Etap 5: Siyen Isit la"},
    "w4_employer_section": {"en": "Employers Only", "es": "Solo para Empleadores", "ht": "Pou Anplwayè Sèlman"},
    "w4_employer_name": {"en": "Employer's name and address", "es": "Nombre y direccion del empleador", "ht": "Non ak adrès anplwayè a"},
    "w4_first_date": {"en": "First date of employment", "es": "Primera fecha de empleo", "ht": "Premye dat travay"},
    "w4_ein": {"en": "Employer Identification Number (EIN)", "es": "Numero de Identificacion del Empleador (EIN)", "ht": "Nimewo Idantifikasyon Anplwayè (EIN)"},

    # ═══════════════════════════════════════════════
    # FORM 4: I-9
    # ═══════════════════════════════════════════════
    "i9_title": {
        "en": "Form I-9 - Employment Eligibility Verification",
        "es": "Formulario I-9 - Verificacion de Elegibilidad de Empleo",
        "ht": "Fom I-9 - Verifikasyon Elijibilite pou Travay"
    },
    "i9_section1": {"en": "Section 1: Employee Information and Attestation", "es": "Seccion 1: Informacion y Declaracion del Empleado", "ht": "Seksyon 1: Enfòmasyon ak Deklarasyon Anplwaye"},
    "i9_last_name": {"en": "Last Name (Family Name)", "es": "Apellido", "ht": "Siyati (Non Fanmi)"},
    "i9_first_name": {"en": "First Name (Given Name)", "es": "Nombre", "ht": "Non (Non Batèm)"},
    "i9_middle_initial": {"en": "Middle Initial", "es": "Inicial del Segundo Nombre", "ht": "Inisyal Dezyèm Non"},
    "i9_other_last_names": {"en": "Other Last Names Used (if any)", "es": "Otros Apellidos Usados (si aplica)", "ht": "Lòt Siyati Itilize (si genyen)"},
    "i9_address": {"en": "Address (Street Number and Name)", "es": "Direccion (Numero y Nombre de la Calle)", "ht": "Adrès (Nimewo ak Non Ri)"},
    "i9_apt": {"en": "Apt. Number", "es": "No. de Apto.", "ht": "No. Apatman"},
    "i9_city": {"en": "City or Town", "es": "Ciudad", "ht": "Vil oswa Bouk"},
    "i9_state": {"en": "State", "es": "Estado", "ht": "Eta"},
    "i9_zip": {"en": "ZIP Code", "es": "Codigo Postal", "ht": "Kòd Postal"},
    "i9_dob": {"en": "Date of Birth (mm/dd/yyyy)", "es": "Fecha de Nacimiento (mm/dd/aaaa)", "ht": "Dat Nesans (mm/jj/aaaa)"},
    "i9_ssn": {"en": "U.S. Social Security Number", "es": "Numero de Seguro Social de EE.UU.", "ht": "Nimewo Sekirite Sosyal Etazini"},
    "i9_email": {"en": "Employee's Email Address", "es": "Correo Electronico del Empleado", "ht": "Adrès Imèl Anplwaye a"},
    "i9_phone": {"en": "Employee's Telephone Number", "es": "Numero de Telefono del Empleado", "ht": "Nimewo Telefòn Anplwaye a"},

    "i9_citizenship": {"en": "Citizenship / Immigration Status", "es": "Ciudadania / Estado Migratorio", "ht": "Sitwayènte / Estati Imigrasyon"},
    "i9_citizen": {"en": "A citizen of the United States", "es": "Ciudadano de los Estados Unidos", "ht": "Yon sitwayen Etazini"},
    "i9_noncitizen_national": {
        "en": "A noncitizen national of the United States",
        "es": "Nacional no ciudadano de los Estados Unidos",
        "ht": "Yon nasyonal ki pa sitwayen Etazini"
    },
    "i9_permanent_resident": {
        "en": "A lawful permanent resident",
        "es": "Residente permanente legal",
        "ht": "Yon rezidan pèmanan legal"
    },
    "i9_alien_authorized": {
        "en": "An alien authorized to work",
        "es": "Extranjero autorizado para trabajar",
        "ht": "Yon etranje ki gen otorizasyon pou travay"
    },
    "i9_uscis_number": {"en": "USCIS or A-Number", "es": "Numero USCIS o A-", "ht": "Nimewo USCIS oswa A-"},
    "i9_i94_number": {"en": "Form I-94 Admission Number", "es": "Numero de Admision del Formulario I-94", "ht": "Nimewo Admisyon Fom I-94"},
    "i9_passport_number": {"en": "Foreign Passport Number", "es": "Numero de Pasaporte Extranjero", "ht": "Nimewo Paspò Etranje"},
    "i9_country_issuance": {"en": "Country of Issuance", "es": "Pais de Emision", "ht": "Peyi ki Bay li"},
    "i9_exp_date": {"en": "Expiration Date", "es": "Fecha de Vencimiento", "ht": "Dat Ekspirasyon"},

    "i9_section2": {"en": "Section 2: Employer Review and Verification", "es": "Seccion 2: Revision y Verificacion del Empleador", "ht": "Seksyon 2: Revizyon ak Verifikasyon Anplwayè"},
    "i9_list_a": {"en": "List A - Identity and Employment Authorization", "es": "Lista A - Identidad y Autorizacion de Empleo", "ht": "Lis A - Idantite ak Otorizasyon Travay"},
    "i9_list_b": {"en": "List B - Identity", "es": "Lista B - Identidad", "ht": "Lis B - Idantite"},
    "i9_list_c": {"en": "List C - Employment Authorization", "es": "Lista C - Autorizacion de Empleo", "ht": "Lis C - Otorizasyon Travay"},
    "i9_doc_title": {"en": "Document Title", "es": "Titulo del Documento", "ht": "Tit Dokiman"},
    "i9_issuing_authority": {"en": "Issuing Authority", "es": "Autoridad Emisora", "ht": "Otorite ki Bay li"},
    "i9_doc_number": {"en": "Document Number", "es": "Numero de Documento", "ht": "Nimewo Dokiman"},
    "i9_exp_date_doc": {"en": "Expiration Date (if any)", "es": "Fecha de Vencimiento (si aplica)", "ht": "Dat Ekspirasyon (si genyen)"},
    "i9_first_day": {"en": "Employee's First Day of Employment", "es": "Primer Dia de Empleo del Empleado", "ht": "Premye Jou Travay Anplwaye a"},
    "i9_employer_name": {"en": "Last Name, First Name and Title of Employer", "es": "Apellido, Nombre y Titulo del Empleador", "ht": "Siyati, Non ak Tit Anplwayè a"},
    "i9_employer_signature": {"en": "Employer Signature", "es": "Firma del Empleador", "ht": "Siyati Anplwayè a"},
    "i9_employer_business": {"en": "Employer's Business Name", "es": "Nombre de la Empresa del Empleador", "ht": "Non Biznis Anplwayè a"},
    "i9_employer_address": {"en": "Employer's Business Address", "es": "Direccion de la Empresa del Empleador", "ht": "Adrès Biznis Anplwayè a"},

    "i9_attestation_notice": {
        "en": "I am aware that federal law provides for imprisonment and/or fines for false statements, or the use of false documents, in connection with the completion of this form.",
        "es": "Estoy consciente de que la ley federal preve prision y/o multas por declaraciones falsas, o el uso de documentos falsos, en relacion con la completacion de este formulario.",
        "ht": "Mwen konnen ke lwa federal la prevwa prizon ak/oswa amann pou fo deklarasyon, oswa itilizasyon fo dokiman, an rapò ak ranpli fom sa a."
    },

    # I-9 Section 1 required fields validation
    "i9_section1_required_title": {"en": "Required Fields - Section 1", "es": "Campos Obligatorios - Seccion 1", "ht": "Chan Obligatwa - Seksyon 1"},
    "i9_section1_required_msg": {
        "en": "The following Section 1 fields are required:\n\n{fields}\n\nPlease fill them before exporting.",
        "es": "Los siguientes campos de la Seccion 1 son obligatorios:\n\n{fields}\n\nPor favor completelos antes de exportar.",
        "ht": "Chan sa yo nan Seksyon 1 obligatwa:\n\n{fields}\n\nTanpri ranpli yo anvan ou ekspòte."
    },

    # ═══════════════════════════════════════════════
    # FORM 5: PAYROLL ACTION FORM
    # ═══════════════════════════════════════════════
    "pa_title": {"en": "Payroll Action Form", "es": "Formulario de Accion de Nomina", "ht": "Fom Aksyon Peman"},
    "pa_employee_info": {"en": "Employee Information", "es": "Informacion del Empleado", "ht": "Enfòmasyon Anplwaye"},
    "pa_name": {"en": "Name of Employee", "es": "Nombre del Empleado", "ht": "Non Anplwaye a"},
    "pa_date_action": {"en": "Date of Action", "es": "Fecha de Accion", "ht": "Dat Aksyon"},
    "pa_job_title": {"en": "Job Title", "es": "Puesto de Trabajo", "ht": "Tit Travay"},
    "pa_store_name": {"en": "Store Name", "es": "Nombre de la Tienda", "ht": "Non Magazen"},
    "pa_employee_id": {"en": "Employee ID", "es": "ID de Empleado", "ht": "ID Anplwaye"},
    "pa_supervisor": {"en": "Supervisor", "es": "Supervisor", "ht": "Sipèvizè"},
    "pa_dob": {"en": "Date of Birth", "es": "Fecha de Nacimiento", "ht": "Dat Nesans"},

    "pa_action_type": {"en": "Payroll Action", "es": "Accion de Nomina", "ht": "Aksyon Peman"},
    "pa_new_hire": {"en": "New Hire", "es": "Nueva Contratacion", "ht": "Nouvo Anplwaye"},
    "pa_rehire": {"en": "Rehire", "es": "Recontratacion", "ht": "Re-anboche"},
    "pa_salary_increase": {"en": "Salary Increase", "es": "Aumento de Salario", "ht": "Ogmantasyon Salè"},
    "pa_promotion": {"en": "Promotion", "es": "Promocion", "ht": "Pwomosyon"},
    "pa_demotion": {"en": "Demotion", "es": "Descenso", "ht": "Desann Grad"},
    "pa_transfer": {"en": "Transfer", "es": "Transferencia", "ht": "Transfè"},
    "pa_vacation": {"en": "Vacation", "es": "Vacaciones", "ht": "Vakans"},
    "pa_leave": {"en": "Leave of Absence", "es": "Licencia de Ausencia", "ht": "Konje"},
    "pa_termination": {"en": "Termination", "es": "Terminacion", "ht": "Tèminasyon"},
    "pa_change_address": {"en": "Change of Address", "es": "Cambio de Direccion", "ht": "Chanjman Adrès"},
    "pa_other": {"en": "Other", "es": "Otro", "ht": "Lòt"},

    "pa_details": {"en": "Details", "es": "Detalles", "ht": "Detay"},
    "pa_address": {"en": "Address", "es": "Direccion", "ht": "Adrès"},
    "pa_city": {"en": "City", "es": "Ciudad", "ht": "Vil"},
    "pa_state": {"en": "State", "es": "Estado", "ht": "Eta"},
    "pa_zip": {"en": "ZIP", "es": "Codigo Postal", "ht": "Kòd Postal"},
    "pa_rate_of_pay": {"en": "Rate of Pay", "es": "Tasa de Pago", "ht": "To Peman"},
    "pa_hourly": {"en": "Hourly", "es": "Por Hora", "ht": "Pa Lè"},
    "pa_weekly": {"en": "Weekly", "es": "Semanal", "ht": "Pa Semèn"},
    "pa_increase_amount": {"en": "Amount of Increase", "es": "Monto del Aumento", "ht": "Montan Ogmantasyon"},
    "pa_from_title": {"en": "From (Job Title)", "es": "De (Puesto)", "ht": "Soti (Tit Travay)"},
    "pa_to_title": {"en": "To (Job Title)", "es": "A (Puesto)", "ht": "Ale (Tit Travay)"},
    "pa_from_store": {"en": "From (Store Location)", "es": "De (Ubicacion de Tienda)", "ht": "Soti (Kote Magazen)"},
    "pa_to_store": {"en": "To (Store Location)", "es": "A (Ubicacion de Tienda)", "ht": "Ale (Kote Magazen)"},
    "pa_out_from": {"en": "Will Be Out From", "es": "Estara Fuera Desde", "ht": "Ap Deyò Depi"},
    "pa_out_to": {"en": "To", "es": "Hasta", "ht": "Jiska"},
    "pa_last_date_worked": {"en": "Last Date Worked", "es": "Ultima Fecha Trabajada", "ht": "Dènye Dat Travay"},
    "pa_eligible_rehire": {"en": "Eligible for Rehire", "es": "Elegible para Recontratacion", "ht": "Elijib pou Re-anboche"},
    "pa_cause_change": {"en": "Cause For Change", "es": "Causa del Cambio", "ht": "Kòz Chanjman an"},
    "pa_store_mgr_sig": {"en": "Store Manager Signature", "es": "Firma del Gerente de Tienda", "ht": "Siyati Manadjè Magazen"},
    "pa_supervisor_sig": {"en": "Supervisor Signature", "es": "Firma del Supervisor", "ht": "Siyati Sipèvizè"},
    # I-9 Section 2 required field alerts
    "i9_required_fields_title": {"en": "Required Fields", "es": "Campos Obligatorios", "ht": "Chan Obligatwa"},
    "i9_required_fields_msg": {
        "en": "The following Section 2 fields are required:\n\n{fields}\n\nPlease fill them before exporting.",
        "es": "Los siguientes campos de la Seccion 2 son obligatorios:\n\n{fields}\n\nPor favor completelos antes de exportar.",
        "ht": "Chan sa yo nan Seksyon 2 obligatwa:\n\n{fields}\n\nTanpri ranpli yo anvan ou ekspòte."
    },
    "i9_first_day_label": {"en": "First Day of Employment (mm/dd/yyyy)", "es": "Primer Dia de Empleo (mm/dd/aaaa)", "ht": "Premye Jou Travay (mm/jj/aaaa)"},
    "i9_employer_name_title_label": {"en": "Last Name, First Name and Title of Employer or Authorized Rep.", "es": "Apellido, Nombre y Titulo del Empleador o Rep. Autorizado", "ht": "Siyati, Non ak Tit Anplwayè oswa Rep. Otorize"},
    "i9_employer_sig_label": {"en": "Signature of Employer or Authorized Rep.", "es": "Firma del Empleador o Rep. Autorizado", "ht": "Siyati Anplwayè oswa Rep. Otorize"},
    "i9_today_date_label": {"en": "Today's Date (mm/dd/yyyy)", "es": "Fecha de Hoy (mm/dd/aaaa)", "ht": "Dat Jodi a (mm/jj/aaaa)"},
    "i9_employer_biz_label": {"en": "Employer's Business or Organization Name", "es": "Nombre de la Empresa u Organizacion del Empleador", "ht": "Non Biznis oswa Òganizasyon Anplwayè a"},
    "i9_employer_addr_label": {"en": "Employer's Address, City, State, ZIP", "es": "Direccion del Empleador, Ciudad, Estado, ZIP", "ht": "Adrès Anplwayè a, Vil, Eta, Kòd Postal"},
    # Preview
    "preview_btn": {"en": "Preview", "es": "Vista Previa", "ht": "Apèsi"},
    "preview_title": {"en": "Form Preview", "es": "Vista Previa del Formulario", "ht": "Apèsi Fom"},
    "preview_generating": {"en": "Generating preview...", "es": "Generando vista previa...", "ht": "Ap jenere apèsi..."},
    "preview_page": {"en": "Page", "es": "Pagina", "ht": "Paj"},
    "preview_error": {"en": "Could not generate preview", "es": "No se pudo generar la vista previa", "ht": "Pa t kapab jenere apèsi a"},
    "preview_zoom_in": {"en": "Zoom +", "es": "Zoom +", "ht": "Zoom +"},
    "preview_zoom_out": {"en": "Zoom -", "es": "Zoom -", "ht": "Zoom -"},
    # ── Documents & Submit ──
    "form_documents": {"en": "Documents\n& Submit", "es": "Documentos\ny Enviar", "ht": "Dokiman\n& Soumèt"},
    "doc_title": {"en": "DOCUMENTS & SUBMIT APPLICATION", "es": "DOCUMENTOS Y ENVIAR SOLICITUD", "ht": "DOKIMAN & SOUMÈT APLIKASYON"},
    "doc_applicant_info": {"en": "Applicant Information", "es": "Informacion del Solicitante", "ht": "Enfòmasyon Aplikan"},
    "doc_full_name": {"en": "Full Name", "es": "Nombre Completo", "ht": "Non Konplè"},
    "doc_email": {"en": "Email", "es": "Correo Electronico", "ht": "Imèl"},
    "doc_phone_label": {"en": "Phone", "es": "Telefono", "ht": "Telefòn"},
    "doc_upload_title": {"en": "Upload Documents", "es": "Cargar Documentos", "ht": "Telechaje Dokiman"},
    "doc_photo_id": {"en": "Photo ID (front & back)", "es": "ID con Foto (frente y reverso)", "ht": "ID ak Foto (devan & dèyè)"},
    "doc_drivers_license": {"en": "Driver's License / State ID", "es": "Licencia de Conducir / ID Estatal", "ht": "Lisans Kondwi / ID Eta"},
    "doc_ssn_card": {"en": "Social Security Card", "es": "Tarjeta de Seguro Social", "ht": "Kat Sekirite Sosyal"},
    "doc_work_auth": {"en": "Work Authorization Document", "es": "Documento de Autorizacion de Trabajo", "ht": "Dokiman Otorizasyon Travay"},
    "doc_void_check": {"en": "Void Check (for Direct Deposit)", "es": "Cheque Anulado (para Deposito Directo)", "ht": "Chèk Anile (pou Depo Dirèk)"},
    "doc_other": {"en": "Other Supporting Documents", "es": "Otros Documentos de Soporte", "ht": "Lòt Dokiman Sipò"},
    "doc_browse": {"en": "Browse...", "es": "Examinar...", "ht": "Chèche..."},
    "doc_no_file": {"en": "No file selected", "es": "Ningun archivo", "ht": "Pa gen fichye"},
    "doc_submit_instructions": {"en": "When you have filled all forms and uploaded your documents, click the button below to send your application to Chicken Kitchen HR.", "es": "Cuando haya llenado todos los formularios y cargado sus documentos, haga clic en el boton para enviar su solicitud a RH de Chicken Kitchen.", "ht": "Lè ou fin ranpli tout fomilè yo epi telechaje dokiman ou yo, klike sou bouton an pou voye aplikasyon ou bay RH Chicken Kitchen."},
    "doc_submit_section": {"en": "Submit Application", "es": "Enviar Solicitud", "ht": "Soumèt Aplikasyon"},
    "doc_submit_btn": {"en": "SUBMIT APPLICATION", "es": "ENVIAR SOLICITUD", "ht": "SOUMÈT APLIKASYON"},
    "doc_submit_confirm": {"en": "Send application with all documents to adela@chickenkitchen.com?", "es": "Enviar solicitud con todos los documentos a adela@chickenkitchen.com?", "ht": "Voye aplikasyon ak tout dokiman nan adela@chickenkitchen.com?"},
    "doc_sending": {"en": "Sending application...", "es": "Enviando solicitud...", "ht": "Ap voye aplikasyon..."},
    "doc_send_error": {"en": "Error sending application", "es": "Error al enviar solicitud", "ht": "Erè pandan voye aplikasyon"},
    "doc_name_required": {"en": "Please enter your full name.", "es": "Ingrese su nombre completo.", "ht": "Tanpri antre non konplè ou."},
    "doc_thank_title": {"en": "Thank You!", "es": "Gracias!", "ht": "Mèsi!"},
    "doc_thank_msg": {"en": "Your application has been submitted successfully.\nSu solicitud ha sido enviada exitosamente.\nAplikasyon ou a te soumèt avèk siksè.", "es": "Su solicitud ha sido enviada exitosamente.\nYour application has been submitted.\nAplikasyon ou a soumèt.", "ht": "Aplikasyon ou a soumèt avèk siksè.\nYour application has been submitted.\nSu solicitud ha sido enviada."},
    "doc_thank_contact": {"en": "We will contact you soon.", "es": "Nos pondremos en contacto pronto.", "ht": "Nou pral kontakte ou byento."},
    "doc_email_config_title": {"en": "Email Configuration", "es": "Configuracion de Correo", "ht": "Konfigirasyon Imèl"},
    "doc_email_config_msg": {"en": "Enter Gmail credentials to send applications.\nThis is saved for this session only.", "es": "Ingrese credenciales de Gmail para enviar.\nSolo se guarda para esta sesion.", "ht": "Antre done Gmail pou voye aplikasyon.\nSa anrejistre pou sesyon sa a sèlman."},
}


def t(key, lang="en"):
    """Get translation for a key in the given language."""
    entry = TRANSLATIONS.get(key, {})
    return entry.get(lang, entry.get("en", f"[{key}]"))
