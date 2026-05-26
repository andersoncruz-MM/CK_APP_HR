/**
 * PDF Overlay Module - Web version
 * Mirrors app/pdf_overlay.py coordinates exactly.
 * Uses pdf-lib to overlay text on original PDF templates.
 */

const TEMPLATE_FILES = {
  employee_app: '../app/templates/EmployeeApp_template.pdf',
  direct_deposit: '../app/templates/DDAuth_template.pdf',
  w4: '../app/templates/W4_template.pdf',
  i9: '../app/templates/I9_template.pdf',
  payroll: '../app/templates/PayrollAction_template.pdf',
};

const FILL_COLOR_RGB = [0.05, 0.05, 0.35];
const CHECK_COLOR_RGB = [0.1, 0.1, 0.6];

// Signature placement coordinates per form {pageIdx: {x, y, width, height}}
const SIGNATURE_COORDS = {
  employee_app: { page: 1, x: 96, y: 120, w: 150, h: 30 },
  direct_deposit: { page: 0, x: 149, y: 60, w: 150, h: 30 },
  w4: { page: 0, x: 200, y: 72, w: 150, h: 30 },
  i9: { page: 0, x: 130, y: 416, w: 150, h: 30 },
  payroll: { page: 0, x: 142, y: 183, w: 130, h: 25 },
};

async function generatePDF(formKey, gv, signatureDataUrl) {
  const { PDFDocument, rgb, StandardFonts } = PDFLib;

  // Use inlined base64 templates (Streamlit) or fetch from file (standalone)
  let tplBytes;
  if (typeof TEMPLATE_DATA !== 'undefined' && TEMPLATE_DATA[formKey]) {
    const _b64 = TEMPLATE_DATA[formKey];
    const _raw = atob(_b64);
    const _arr = new Uint8Array(_raw.length);
    for (let i = 0; i < _raw.length; i++) _arr[i] = _raw.charCodeAt(i);
    tplBytes = _arr.buffer;
  } else {
    const tplUrl = TEMPLATE_FILES[formKey];
    tplBytes = await fetch(tplUrl).then(r => r.arrayBuffer());
  }
  const pdfDoc = await PDFDocument.load(tplBytes);
  const font = await pdfDoc.embedFont(StandardFonts.Helvetica);
  const fillColor = rgb(...FILL_COLOR_RGB);
  const checkColor = rgb(...CHECK_COLOR_RGB);

  // Embed signature image if provided
  let sigImage = null;
  if (signatureDataUrl && signatureDataUrl.startsWith('data:image/png')) {
    const sigB64 = signatureDataUrl.split(',')[1];
    const sigRaw = atob(sigB64);
    const sigArr = new Uint8Array(sigRaw.length);
    for (let i = 0; i < sigRaw.length; i++) sigArr[i] = sigRaw.charCodeAt(i);
    sigImage = await pdfDoc.embedPng(sigArr);
  }

  const generators = {
    employee_app: fillEmployeeApp,
    direct_deposit: fillDirectDeposit,
    w4: fillW4,
    i9: fillI9,
    payroll: fillPayroll,
  };

  const pageData = generators[formKey](gv);
  const pages = pdfDoc.getPages();

  for (const [pageIdx, data] of Object.entries(pageData)) {
    const page = pages[parseInt(pageIdx)];
    if (!page) continue;
    const { fields = [], checks = [], blanks = [] } = data;

    // Draw white blanking rectangles
    for (const [bx, by, bw, bh] of blanks) {
      page.drawRectangle({ x: bx, y: by, width: bw, height: bh,
        color: rgb(1, 1, 1), borderWidth: 0 });
    }

    // Draw text fields
    for (const [x, y, text, fs] of fields) {
      if (!text) continue;
      page.drawText(String(text), { x, y, size: fs, font, color: fillColor });
    }

    // Draw checkmarks
    for (const [cx, cy] of checks) {
      const sz = 8;
      page.drawLine({
        start: { x: cx, y: cy }, end: { x: cx + sz * 0.35, y: cy - sz * 0.4 },
        thickness: 1.5, color: checkColor
      });
      page.drawLine({
        start: { x: cx + sz * 0.35, y: cy - sz * 0.4 }, end: { x: cx + sz, y: cy + sz * 0.6 },
        thickness: 1.5, color: checkColor
      });
    }
  }

  // Draw signature image on the correct page
  if (sigImage && SIGNATURE_COORDS[formKey]) {
    const sc = SIGNATURE_COORDS[formKey];
    const targetPage = pages[sc.page];
    if (targetPage) {
      targetPage.drawImage(sigImage, { x: sc.x, y: sc.y, width: sc.w, height: sc.h });
    }
  }

  return await pdfDoc.save();
}

// ═══════════════════════════════════════════
// EMPLOYEE APPLICATION - Same coordinates as Python
// ═══════════════════════════════════════════
function fillEmployeeApp(gv) {
  const S = 9;
  const p1fields = [
    [105, 620, gv('ea_last_name'), S], [292, 620, gv('ea_first_name'), S],
    [431, 620, gv('ea_mi'), S], [482, 620, gv('ea_date'), 8],
    [95, 602, gv('ea_street_address'), S], [480, 602, gv('ea_apt'), 8],
    [78, 578, gv('ea_city'), S], [295, 578, gv('ea_state'), S], [429, 578, gv('ea_zip'), S],
    [88, 557, gv('ea_phone'), S], [306, 557, gv('ea_email'), 8],
    [99, 539, gv('ea_date_available'), 8], [289, 539, gv('ea_ssn'), S], [428, 539, gv('ea_desired_salary'), S],
    [128, 518, gv('ea_position'), S],
    [364, 474, gv('ea_when'), 8], [335, 456, gv('ea_felony_explain'), 8],
  ];
  const c1 = [];
  // Checkbox positions from PyMuPDF get_drawings() - exact □ rectangle coords
  // Citizen: YES□ x=241.4 y=495.9, NO□ x=278.9 y=495.9
  if (gv('ea_citizen')==='yes') c1.push([242,496]); else if (gv('ea_citizen')==='no') c1.push([279,496]);
  // Authorized: YES□ x=493.5, NO□ x=535.5
  if (gv('ea_authorized')==='yes') c1.push([494,496]); else if (gv('ea_authorized')==='no') c1.push([536,496]);
  // Worked before: YES□ x=241.4 y=475.0, NO□ x=278.9
  if (gv('ea_worked_before')==='yes') c1.push([242,475]); else if (gv('ea_worked_before')==='no') c1.push([279,475]);
  // Felony: YES□ x=241.4 y=454.3, NO□ x=278.9
  if (gv('ea_felony')==='yes') c1.push([242,454]); else if (gv('ea_felony')==='no') c1.push([279,454]);

  // Education
  const eduData = [
    ['hs', 405, 381], ['col', 363, 339], ['oth', 317, 297]
  ];
  const othAddrY = 321;
  for (const [pfx, yName, yFrom] of eduData) {
    const addrY = pfx === 'oth' ? othAddrY : yName;
    p1fields.push(
      [90, yName, gv(`ea_${pfx}_name`), 8], [300, addrY, gv(`ea_${pfx}_address`), 8],
      [83, yFrom, gv(`ea_${pfx}_from`), 8], [143, yFrom, gv(`ea_${pfx}_to`), 8],
      [375, yFrom, gv(`ea_${pfx}_degree`), 8],
    );
    // Graduate: YES□ x=281.9, NO□ x=319.5 (from get_drawings)
    if (gv(`ea_${pfx}_graduate`)==='yes') c1.push([282, yFrom+1]);
    else if (gv(`ea_${pfx}_graduate`)==='no') c1.push([320, yFrom+1]);
  }

  // References
  const blanks1 = [];
  const refsY = [[229,208,187],[166,145,125],[104,83,62]];
  for (let i = 0; i < 3; i++) {
    const [yN, yC, yA] = refsY[i];
    p1fields.push(
      [103, yN, gv(`ea_ref${i}_name`), 8], [375, yN, gv(`ea_ref${i}_relationship`), 8],
      [100, yC, gv(`ea_ref${i}_company`), 8], [355, yC, gv(`ea_ref${i}_phone`), 8],
      [95, yA, gv(`ea_ref${i}_address`), 8],
    );
    if (gv(`ea_ref${i}_phone`)) blanks1.push([355, yC-3, 45, 14]);
  }

  // Page 2 - Employers
  const p2fields = [];
  const c2 = [];
  const blanks2 = [];
  const empY = [709, 577, 444];
  for (let i = 0; i < 3; i++) {
    const yb = empY[i];
    let startSal = gv(`ea_emp${i}_start_salary`);
    if (startSal.startsWith('$')) startSal = startSal.slice(1);
    let endSal = gv(`ea_emp${i}_end_salary`);
    if (endSal.startsWith('$')) endSal = endSal.slice(1);
    p2fields.push(
      [96, yb, gv(`ea_emp${i}_company`), 8], [369, yb, gv(`ea_emp${i}_phone`), 8],
      [91, yb-22, gv(`ea_emp${i}_address`), 8], [370, yb-22, gv(`ea_emp${i}_supervisor`), 8],
      [93, yb-44, gv(`ea_emp${i}_title`), 8], [337, yb-44, startSal, 8], [472, yb-44, endSal, 8],
      [116, yb-66, gv(`ea_emp${i}_responsibilities`), 7],
      [81, yb-88, gv(`ea_emp${i}_from`), 8], [143, yb-88, gv(`ea_emp${i}_to`), 8],
      [265, yb-88, gv(`ea_emp${i}_reason`), 8],
    );
    if (gv(`ea_emp${i}_phone`)) blanks2.push([367, yb-3, 40, 14]);
    // Contact: YES□ x=303 NO□ x=345.4 (from get_drawings, yb-109)
    if (gv(`ea_emp${i}_contact`)==='yes') c2.push([303, yb-109]);
    else if (gv(`ea_emp${i}_contact`)==='no') c2.push([346, yb-109]);
  }
  p2fields.push(
    [87, 279, gv('ea_mil_branch'), S], [400, 279, gv('ea_mil_from'), 8], [455, 279, gv('ea_mil_to'), 8],
    [127, 257, gv('ea_mil_rank'), S], [446, 257, gv('ea_mil_discharge_type'), S],
    [175, 235, gv('ea_mil_explain'), 8],
    [96, 129, gv('ea_signature'), S], [428, 129, gv('ea_sign_date'), S],
  );

  return {
    0: { fields: p1fields, checks: c1, blanks: blanks1 },
    1: { fields: p2fields, checks: c2, blanks: blanks2 },
  };
}

// ═══════════════════════════════════════════
// DIRECT DEPOSIT
// ═══════════════════════════════════════════
function fillDirectDeposit(gv) {
  const S = 10;
  // Language-specific labels for $5 fee notice
  const lang = gv('_lang') || 'en';
  const _fee = {
    en: ['Bank Name:', 'A $5.00 fee will be charged for direct deposit.', 'I accept:', 'YES', 'NO'],
    es: ['Nombre del Banco:', 'Se cobrara un cargo de $5.00 por deposito directo.', 'Acepto:', 'SI', 'NO'],
    ht: ['Non Bank la:', 'Yo pral chaje $5.00 pou depo direk.', 'Mwen aksepte:', 'WI', 'NON'],
  };
  const [bankLbl, feeTxt, acceptLbl, yesLbl, noLbl] = _fee[lang] || _fee.en;

  const fields = [
    // Bank name (in the voided check area)
    [38, 380, bankLbl, 7],
    [155, 380, gv('dd_bank_name'), 9],
    // $5 Fee notice (selected language only)
    [38, 360, feeTxt, 7],
    [38, 345, acceptLbl, 7],
    [175, 345, yesLbl, 7],
    [235, 345, noLbl, 7],
    // Account 1
    [220, 530, gv('dd_acct1_routing'), S], [125, 508, gv('dd_acct1_number'), S],
    [333, 486, gv('dd_acct1_amount'), S],
    // Account 2
    [220, 425, gv('dd_acct2_routing'), S], [125, 403, gv('dd_acct2_number'), S],
    [116, 174, 'Chicken Kitchen', S],
    [149, 68, gv('dd_signature'), S], [438, 68, gv('dd_employee_id'), S],
    [101, 46, gv('dd_print_name'), S], [389, 46, gv('dd_date'), S],
  ];
  const checks = [];
  if (gv('dd_acct1_type')==='checking') checks.push([157,548]);
  else if (gv('dd_acct1_type')==='savings') checks.push([257,548]);
  if (gv('dd_acct2_type')==='checking') checks.push([157,443]);
  else if (gv('dd_acct2_type')==='savings') checks.push([257,443]);
  // $5 Fee acceptance
  if (gv('dd_fee_accept')==='yes') checks.push([210,345]);
  else if (gv('dd_fee_accept')==='no') checks.push([250,345]);
  return { 0: { fields, checks } };
}

// ═══════════════════════════════════════════
// W-4
// ═══════════════════════════════════════════
function fillW4(gv) {
  const S = 10;
  const safeInt = v => parseInt(v) || 0;
  const safeMoney = v => { const n = parseInt(v) || 0; return n ? String(n) : ''; };
  const childrenCount = safeInt(gv('w4_children'));
  const otherDeps = safeInt(gv('w4_other_deps'));
  const childrenAmt = childrenCount ? String(childrenCount * 2200) : '';
  const otherDepsAmt = otherDeps ? String(otherDeps * 500) : '';
  const otherCredits = safeMoney(gv('w4_other_credits'));
  let total3 = gv('w4_total_step3');
  if (!total3) { const calc = childrenCount*2200 + otherDeps*500 + safeInt(otherCredits); total3 = calc ? String(calc) : ''; }

  const fields = [
    [100, 688, gv('w4_first_name'), S], [280, 688, gv('w4_last_name'), S], [480, 688, gv('w4_ssn'), 9],
    [100, 664, gv('w4_address'), S], [100, 640, gv('w4_city_state_zip'), S],
    [420, 301, childrenAmt, S], [420, 289, otherDepsAmt, S], [515, 265, total3, S],
    [515, 229, safeMoney(gv('w4_other_income')), S],
    [515, 193, safeMoney(gv('w4_deductions')), S],
    [515, 175, safeMoney(gv('w4_extra_withholding')), S],
    [200, 80, gv('w4_signature'), S], [485, 80, gv('w4_date'), 9],
    [100, 52, gv('w4_employer_name'), 7], [400, 52, gv('w4_first_date'), 8], [478, 52, gv('w4_ein'), 8],
  ];
  const checks = [];
  const st = gv('w4_filing_status');
  // W-4 checkboxes from get_drawings: x=115.2, sizes 8x8
  // Filing: single y=626, married y=614, head y=602.2
  if (st==='single') checks.push([115,626]);
  else if (st==='married_joint') checks.push([115,614]);
  else if (st==='head_household') checks.push([115,602]);
  // Two jobs: x=564 y=380 (8x8)
  if (gv('w4_two_jobs')==='True') checks.push([564,380]);
  // Exempt: x=564 y=129.5
  if (gv('w4_exempt')==='True') checks.push([564,130]);
  return { 0: { fields, checks } };
}

// ═══════════════════════════════════════════
// I-9
// ═══════════════════════════════════════════
function fillI9(gv) {
  const S = 9;
  const LB_X = 290, LC_X = 445;
  // SSN boxes
  const ssnCx = [155.4,166.6,178.3,190.1,201.8,213.6,225.3,237.1,249.0];
  const ssnY = 556;
  const ssnRaw = (gv('i9_ssn')||'').replace(/-/g,'').replace(/ /g,'');
  const ssnFields = [];
  for (let i = 0; i < ssnCx.length; i++) {
    const d = i < ssnRaw.length ? ssnRaw[i] : '';
    if (d) ssnFields.push([ssnCx[i]-3, ssnY, d, 9]);
  }

  const fields = [
    [42,608,gv('i9_last_name'),S], [204,608,gv('i9_first_name'),S],
    [348,608,gv('i9_middle_initial'),S], [420,608,gv('i9_other_names'),8],
    [42,582,gv('i9_address'),8], [234,582,gv('i9_apt'),S],
    [306,582,gv('i9_city'),S], [462,582,gv('i9_state'),S], [510,582,gv('i9_zip'),S],
    [42,556,gv('i9_dob'),S], [264,556,gv('i9_email'),8], [456,556,gv('i9_phone'),S],
    [250,457,gv('i9_uscis'),8], [340,457,gv('i9_i94'),8],
    [455,457,gv('i9_passport'),8], [455,445,gv('i9_country'),8],
    [300,486,gv('i9_exp_date'),8],
    [130,424,gv('i9_employee_sig'),S], [430,424,gv('i9_employee_date'),S],
    [125,343,gv('i9_lista_title'),8], [125,325,gv('i9_lista_issuing'),8],
    [125,307,gv('i9_lista_number'),8], [125,289,gv('i9_lista_exp'),8],
    [LB_X,343,gv('i9_listb_title'),7], [LB_X,325,gv('i9_listb_issuing'),7],
    [LB_X,307,gv('i9_listb_number'),7], [LB_X,289,gv('i9_listb_exp'),7],
    [LC_X,343,gv('i9_listc_title'),7], [LC_X,325,gv('i9_listc_issuing'),7],
    [LC_X,307,gv('i9_listc_number'),7], [LC_X,289,gv('i9_listc_exp'),7],
    [462,120,gv('i9_first_day'),8],
    [38,93,gv('i9_employer_name'),7], [294,93,gv('i9_employer_sig'),7], [490,93,gv('i9_employer_date'),7],
    [38,60,gv('i9_employer_biz'),7], [246,60,gv('i9_employer_addr'),6],
    ...ssnFields,
  ];
  const checks = [];
  const st = gv('i9_status');
  // I-9 citizenship checkboxes from get_drawings: x=181.9, 9x9
  if (st==='citizen') checks.push([182,524]);
  else if (st==='noncitizen_national') checks.push([182,512]);
  else if (st==='permanent_resident') checks.push([182,500]);
  else if (st==='alien_authorized') checks.push([182,488]);
  return { 0: { fields, checks } };
}

// ═══════════════════════════════════════════
// PAYROLL ACTION
// ═══════════════════════════════════════════
function fillPayroll(gv) {
  const S = 10;
  const fields = [
    [124,593,gv('pa_name'),S], [329,593,gv('pa_date_action'),S],
    [89,576,gv('pa_job_title'),S], [333,576,gv('pa_store_name'),S],
    [104,555,gv('pa_employee_id'),S], [330,555,gv('pa_supervisor'),S],
    [82,535,gv('pa_dob'),S],
    [259,514,gv('pa_address'),8], [258,493,gv('pa_city'),8],
    [258,472,gv('pa_state'),8], [258,452,gv('pa_zip'),8],
    [293,420,gv('pa_rate_of_pay'),S], [299,400,gv('pa_increase_amount'),S],
    [286,379,gv('pa_from_title'),8], [446,379,gv('pa_to_title'),8],
    [289,358,gv('pa_from_store'),8], [418,358,gv('pa_to_store'),8],
    [291,337,gv('pa_out_from'),8], [419,337,gv('pa_out_to'),8],
    [121,317,gv('pa_last_date'),S],
    [142,191,gv('pa_mgr_sig'),S], [129,170,gv('pa_sup_sig'),S],
  ];
  const actionMap = {
    pa_new_hire:493, pa_rehire:483, pa_salary_increase:472, pa_promotion:462,
    pa_demotion:452, pa_transfer:441, pa_vacation:431, pa_leave:420,
    pa_termination:410, pa_change_address:400, pa_other:389,
  };
  for (const [key, yPos] of Object.entries(actionMap)) {
    if (gv(key)==='True') fields.push([155, yPos, 'X', 11]);
  }
  const cause = gv('pa_cause_change');
  if (cause) {
    cause.split('\n').slice(0,3).forEach((line, j) => {
      fields.push([121, 270 - j*12, line.slice(0,70), 8]);
    });
  }
  const checks = [];
  if (gv('pa_pay_type')==='hourly') checks.push([342,422]);
  else if (gv('pa_pay_type')==='weekly') checks.push([438,422]);
  if (gv('pa_eligible_rehire')==='yes') checks.push([120,297]);
  else if (gv('pa_eligible_rehire')==='no') checks.push([216,297]);
  return { 0: { fields, checks } };
}
