/**
 * Chicken Kitchen HR Forms - Web App
 * Main application logic: form building, navigation, export
 */

let currentForm = null;
let formValues = {};  // stores all field values
let selectedStore = null;  // {code, name, legal_entity, admin_email, address}

// Store data (from CK_Master_Locations.xlsx)
const CK_STORES = {
  ALT:{name:"Alton",legal_entity:"CK at Alton Road LLC",admin_email:"ckatalton@gmail.com",address:"1509 Alton Rd, Miami, FL 33139"},
  BIR:{name:"Bird & Ludlum",legal_entity:"CK at Bird & Ludum LLC",admin_email:"ckbirdludlum@gmail.com",address:"6786 Bird Rd, Miami, FL 33155"},
  BIS:{name:"Biscayne & 69th",legal_entity:"CK at Buena Vista LLC",admin_email:"buenavista@chickenkitchen.com",address:"6907 Biscayne Blvd, Miami, FL 33138"},
  BLU:{name:"Blue Lagoon",legal_entity:"CK at Blue Lagoon LLC",admin_email:"bluelagoon@chickenkitchen.com",address:"5765 NW 7th St, Miami, FL 33126"},
  COL:{name:"Collins & 71st",legal_entity:"CK at North Beach LLC",admin_email:"northbeach@chickenkitchen.com",address:"7116 Collins Ave, Miami, FL 33141"},
  COU:{name:"Country Walk",legal_entity:"CK at Country Walk LLC",admin_email:"cwalk@chickenkitchen.com",address:"15812 SW 137th Ave, Miami, FL 33175"},
  CRF:{name:"Coral Reef",legal_entity:"CK at So. Dixie LLC",admin_email:"ckcoralreef@hotmail.com",address:"15053 South Dixie Hwy, Miami, FL 33176"},
  CUT:{name:"Cutler Ridge",legal_entity:"CK at Cutler Ridge LLC",admin_email:"cutlerbay@chickenkitchen.com",address:"20527 Old Cutler Rd, Cutler Bay, FL 33189"},
  DAV:{name:"Davie",legal_entity:"CK at Davie LLC",admin_email:"davie@chickenkitchen.com",address:"2319 South University Dr, Davie, FL 33324"},
  DOR:{name:"Doral",legal_entity:"CK at Doral LLC",admin_email:"doral@chickenkitchen.com",address:"9741 NW 41st St, Miami, FL 33178"},
  DWT:{name:"Downtown",legal_entity:"CK at Downtown LLC",admin_email:"downtown@chickenkitchen.com",address:"146 NE 2nd Ave, Miami, FL 33132"},
  FIU:{name:"FIU",legal_entity:"CK at FIU LLC",admin_email:"fiu@chickenkitchen.com",address:"10550 SW 8th St, Miami, FL 33174"},
  FTL:{name:"Ft Lauderdale",legal_entity:"CK at Plaza del Mar LLC",admin_email:"coralridge@chickenkitchen.com",address:"1523 N Federal Hwy, Fort Lauderdale, FL 33304"},
  GAL:{name:"Galloway",legal_entity:"CK at Galloway LLC",admin_email:"galloway@chickenkitchen.com",address:"8732 Sunset Dr, Miami, FL 33173"},
  HAM:{name:"Hammocks",legal_entity:"CK at Hammocks LLC",admin_email:"hammocks@chickenkitchen.com",address:"15738 SW 72nd St, Miami, FL 33193"},
  KBI:{name:"Key Biscayne",legal_entity:"CK at Key Biscayne LLC",admin_email:"keybiscayne@chickenkitchen.com",address:"65 Harbor Dr Space #6, Key Biscayne, FL 33149"},
  KEN:{name:"Kendall",legal_entity:"CK at Kendall Mall LLC",admin_email:"chickenkitchenkendall@gmail.com",address:"9067 SW 107th Ave, Miami, FL 33176"},
  KEY:{name:"Keystone",legal_entity:"CK at Keystone Plaza LLC",admin_email:"keystone@chickenkitchen.com",address:"13521 Biscayne Blvd, North Miami Beach, FL 33183"},
  LEJ:{name:"Lejeune",legal_entity:"CK at Lejeune LLC",admin_email:"lejeune@chickenkitchen.com",address:"400 South Dixie Hwy, Coral Gables, FL 33146"},
  MBE:{name:"Miami Beach",legal_entity:"CK at 41st LLC",admin_email:"41st@chickenkitchen.com",address:"524 Arthur Godfrey Rd, Miami Beach, FL 33140"},
  MGA:{name:"Miami Gardens",legal_entity:"CK at Miami Garders Drive LLC",admin_email:"miagardens@chickenkitchen.com",address:"18515 NE 18th Ave Ste #100, North Miami Beach, FL 33179"},
  MLK:{name:"Miami Lakes",legal_entity:"CK at Miami Lakes LLC",admin_email:"ckmiamilakes@gmail.com",address:"15221 NW 67th Ave, Miami Lakes, FL 33014"},
  NML:{name:"N. Miami Lakes",legal_entity:"CK at North Miami Lakes LLC",admin_email:"NMLakes@chickenkitchen.com",address:"6450 NW 186 St, Hialeah, FL 33015"},
  PCR:{name:"Pinecrest",legal_entity:"CK at Pinecrest LLC",admin_email:"pinecrest@chickenkitchen.com",address:"11403 South Dixie Hwy, Miami, FL 33176"},
  PLA:{name:"Plantation",legal_entity:"CK at Plantation LLC",admin_email:"plantation@chickenkitchen.com",address:"6985 W Broward Blvd, Plantation, FL 33317"},
  PNS:{name:"Pembroke Pines",legal_entity:"CK at Pines LLC",admin_email:"ppines@chickenkitchen.com",address:"2014 N Flamingo Rd, Pembroke Pines, FL 33028"},
  SUN:{name:"Sunset",legal_entity:"CK at Sunset Drive LLC",admin_email:"sunset@chickenkitchen.com",address:"1565 Sunset Dr, Coral Gables, FL 33143"},
  WBR:{name:"West Bird",legal_entity:"CK at Westbird LLC",admin_email:"westbird@chickenkitchen.com",address:"11425 SW 40th St, Miami, FL 33165"},
  WPI:{name:"West Pines",legal_entity:"CK at West Pines LLC",admin_email:"westpines@chickenkitchen.com",address:"17149 Pines Blvd, Pembroke Pines, FL 33027"},
};

function selectStore(code) {
  const store = CK_STORES[code];
  if (!store) return;
  selectedStore = { code, ...store };
  // Auto-fill employer fields in Employee Application
  const addr = store.address;
  setVal('ea_employer_name', store.legal_entity);
  setVal('ea_employer_address', addr);
  // Auto-fill employer fields in I-9 and Payroll
  setVal('i9_employer_biz', store.legal_entity);
  setVal('i9_employer_addr', addr);
  setVal('pa_store_name', 'CK ' + store.name);
  setVal('w4_employer_name', store.legal_entity);
}

// ─── I-9 Document Lists ───
const LIST_A_DOCS = [
  "U.S. Passport", "U.S. Passport Card",
  "Permanent Resident Card (Form I-551)", "Alien Registration Receipt Card (Form I-551)",
  "Foreign Passport with I-551 stamp", "Employment Authorization Document (Form I-766)",
  "Foreign Passport with Form I-94/I-94A"
];
const LIST_B_DOCS = [
  "Driver's License", "State ID Card", "Federal Government ID Card",
  "School ID Card with photograph", "Voter's Registration Card",
  "U.S. Military Card", "U.S. Military Draft Record", "Military Dependent's ID Card",
  "U.S. Coast Guard Merchant Mariner Card", "Native American Tribal Document",
  "Canadian Driver's License"
];
const LIST_C_DOCS = [
  "Social Security Card (unrestricted)", "Birth Certificate (certified copy)",
  "Certification of Birth Abroad (DS-1350)", "Report of Birth Abroad (FS-545)",
  "Certification of Report of Birth (FS-240)", "Native American Tribal Document",
  "U.S. Citizen ID Card (Form I-197)", "Resident Citizen ID Card (Form I-179)",
  "Employment Authorization (DHS issued)"
];

// ─── Helpers ───
function el(id) { return document.getElementById(id); }
function html(tag, attrs = {}, children = []) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'className') e.className = v;
    else if (k === 'innerHTML') e.innerHTML = v;
    else if (k === 'textContent') e.textContent = v;
    else if (k.startsWith('on')) e.addEventListener(k.slice(2).toLowerCase(), v);
    else e.setAttribute(k, v);
  }
  children.forEach(c => { if (typeof c === 'string') e.appendChild(document.createTextNode(c)); else if (c) e.appendChild(c); });
  return e;
}

function getVal(key) {
  // Bank name: if "Other" selected, return custom entry value
  if (key === 'dd_bank_name') {
    const sel = formValues.dd_bank_dropdown || '';
    const otherLabel = t('dd_bank_other');
    if (sel === otherLabel) return formValues.dd_bank_name_other || '';
    return sel;
  }
  // Date dropdown combo
  const mm = formValues[key + '_mm'], dd = formValues[key + '_dd'], yy = formValues[key + '_yy'];
  if (mm !== undefined && dd !== undefined && yy !== undefined) {
    if (mm && dd && yy) return `${mm}/${dd}/${yy}`;
    return '';
  }
  // Phone combo
  const code = formValues[key + '_code'], num = formValues[key + '_num'];
  if (code !== undefined && num !== undefined) {
    if (code && num) return `(${code}) ${num}`;
    return num || '';
  }
  return formValues[key] || '';
}

function setVal(key, value) { formValues[key] = value; }

// ─── Field Builders ───
function buildField(label, key, opts = {}) {
  const g = html('div', { className: 'field-group' });
  g.appendChild(html('label', {}, [label + (opts.required ? ' *' : '')]));
  const inp = html('input', {
    type: opts.type || 'text', placeholder: opts.placeholder || '',
    value: formValues[key] || '',
    className: opts.required ? 'required-field' : '',
  });
  inp.style.width = opts.width || '';
  inp.addEventListener('input', () => setVal(key, inp.value));
  g.appendChild(inp);
  formValues[key] = formValues[key] || '';
  return g;
}

function buildDropdown(label, key, options, opts = {}) {
  const g = html('div', { className: 'field-group' });
  g.appendChild(html('label', {}, [label]));
  const sel = html('select');
  sel.appendChild(html('option', { value: '' }, ['-- Select --']));
  options.forEach(o => {
    const opt = html('option', { value: o }, [o]);
    if (formValues[key] === o) opt.selected = true;
    sel.appendChild(opt);
  });
  sel.addEventListener('change', () => setVal(key, sel.value));
  g.appendChild(sel);
  formValues[key] = formValues[key] || '';
  return g;
}

function buildDateField(label, key, yearStart = 2024, yearEnd = 2035, opts = {}) {
  const g = html('div', { className: 'field-group' });
  const lbl = label + (opts.required ? ' *' : '');
  g.appendChild(html('label', {}, [lbl]));
  const row = html('div', { className: 'date-pick' });

  const months = ['', ...Array.from({length:12}, (_,i) => String(i+1).padStart(2,'0'))];
  const days = ['', ...Array.from({length:31}, (_,i) => String(i+1).padStart(2,'0'))];
  const years = ['', ...Array.from({length: yearEnd-yearStart+1}, (_,i) => String(yearStart+i))];

  function makeSel(values, subkey, w) {
    const s = html('select', { style: `min-width:${w}px` });
    values.forEach(v => {
      const o = html('option', { value: v }, [v || '-']);
      if (formValues[subkey] === v) o.selected = true;
      s.appendChild(o);
    });
    s.addEventListener('change', () => setVal(subkey, s.value));
    formValues[subkey] = formValues[subkey] || '';
    return s;
  }

  row.append(
    html('span', { className: 'lbl' }, ['MM']),
    makeSel(months, key + '_mm', 58),
    html('span', { className: 'sep' }, ['/']),
    html('span', { className: 'lbl' }, ['DD']),
    makeSel(days, key + '_dd', 58),
    html('span', { className: 'sep' }, ['/']),
    html('span', { className: 'lbl' }, ['YYYY']),
    makeSel(years, key + '_yy', 75),
  );
  if (opts.required) { row.style.borderLeft = '3px solid #D32F2F'; row.style.paddingLeft = '6px'; }
  g.appendChild(row);
  return g;
}

function buildYesNo(label, key) {
  const g = html('div', { className: 'field-group' });
  g.appendChild(html('label', {}, [label]));
  const row = html('div', { className: 'yesno' });
  ['yes', 'no'].forEach(v => {
    const id = key + '_' + v;
    const r = html('input', { type: 'radio', name: key, value: v, id });
    if (formValues[key] === v) r.checked = true;
    r.addEventListener('change', () => setVal(key, v));
    row.append(r, html('label', { for: id }, [v === 'yes' ? t('yes') : t('no')]));
  });
  g.appendChild(row);
  formValues[key] = formValues[key] || '';
  return g;
}

function buildCityStateZip(cityKey, stateKey, zipKey) {
  const container = document.createDocumentFragment();
  // City dropdown
  const cityG = html('div', { className: 'field-group' });
  cityG.appendChild(html('label', {}, [t('ea_city')]));
  const citySel = html('select');
  citySel.appendChild(html('option', { value: '' }, ['-- ' + t('ea_city') + ' --']));
  FL_CITIES.forEach(c => {
    const o = html('option', { value: c }, [c]);
    if (formValues[cityKey] === c) o.selected = true;
    citySel.appendChild(o);
  });
  citySel.addEventListener('change', () => {
    setVal(cityKey, citySel.value);
    // Auto-fill ZIP and State
    if (FL_ZIPS[citySel.value]) {
      setVal(zipKey, FL_ZIPS[citySel.value]);
      setVal(stateKey, 'FL');
      // Update the visible fields
      const zipInp = container._zipInput;
      if (zipInp) zipInp.value = FL_ZIPS[citySel.value];
      const stateSel = container._stateSelect;
      if (stateSel) stateSel.value = 'FL';
    }
  });
  cityG.appendChild(citySel);
  formValues[cityKey] = formValues[cityKey] || '';

  // State dropdown
  const stateG = html('div', { className: 'field-group' });
  stateG.appendChild(html('label', {}, [t('ea_state')]));
  const stateSel = html('select');
  stateSel.appendChild(html('option', { value: '' }, ['--']));
  US_STATES.forEach(s => {
    const o = html('option', { value: s }, [s]);
    if ((formValues[stateKey] || 'FL') === s) o.selected = true;
    stateSel.appendChild(o);
  });
  stateSel.addEventListener('change', () => setVal(stateKey, stateSel.value));
  stateG.appendChild(stateSel);
  formValues[stateKey] = formValues[stateKey] || 'FL';

  // ZIP (editable combo - input with datalist)
  const zipG = html('div', { className: 'field-group' });
  zipG.appendChild(html('label', {}, [t('ea_zip')]));
  const zipInp = html('input', { type: 'text', placeholder: '33130', value: formValues[zipKey] || '', style: 'width:100px' });
  zipInp.addEventListener('input', () => setVal(zipKey, zipInp.value));
  zipG.appendChild(zipInp);
  formValues[zipKey] = formValues[zipKey] || '';

  // Store refs for auto-fill
  const row = fieldRow(cityG, stateG);
  const row2 = fieldRow(zipG);
  container.appendChild(row);
  container.appendChild(row2);
  container._zipInput = zipInp;
  container._stateSelect = stateSel;
  return container;
}

function buildRadioGroup(label, key, options) {
  const g = html('div', { className: 'field-group' });
  g.appendChild(html('label', { style: 'font-weight:bold' }, [label]));
  const grp = html('div', { className: 'radio-group', style: 'flex-direction:column;gap:4px;margin-top:4px' });
  options.forEach(([text, value]) => {
    const id = key + '_' + value;
    const r = html('input', { type: 'radio', name: key, value, id });
    if (formValues[key] === value) r.checked = true;
    r.addEventListener('change', () => setVal(key, value));
    grp.append(html('label', { for: id }, [r, document.createTextNode(' ' + text)]));
  });
  g.appendChild(grp);
  formValues[key] = formValues[key] || '';
  return g;
}

function buildCheckbox(label, key) {
  const g = html('div', { style: 'display:flex;align-items:center;gap:5px' });
  const cb = html('input', { type: 'checkbox', id: key });
  if (formValues[key] === 'True') cb.checked = true;
  cb.addEventListener('change', () => setVal(key, cb.checked ? 'True' : 'False'));
  g.append(cb, html('label', { for: key, style: 'font-size:13px;cursor:pointer' }, [label]));
  formValues[key] = formValues[key] || 'False';
  return g;
}

function buildTextarea(label, key, rows = 3) {
  const g = html('div', { className: 'field-group' });
  g.appendChild(html('label', {}, [label]));
  const ta = html('textarea', { rows });
  ta.value = formValues[key] || '';
  ta.addEventListener('input', () => setVal(key, ta.value));
  g.appendChild(ta);
  formValues[key] = formValues[key] || '';
  return g;
}

function buildPhoneField(label, codeKey, numKey) {
  const g = html('div', { className: 'field-group' });
  g.appendChild(html('label', {}, [label]));
  const row = html('div', { className: 'phone-field' });
  const codeInp = html('input', { type: 'text', className: 'code', placeholder: '305', maxlength: '3', value: formValues[codeKey] || '' });
  codeInp.addEventListener('input', () => setVal(codeKey, codeInp.value));
  const numInp = html('input', { type: 'text', className: 'num', placeholder: '555-1234', value: formValues[numKey] || '' });
  numInp.addEventListener('input', () => setVal(numKey, numInp.value));
  row.append(
    document.createTextNode('('), codeInp, document.createTextNode(') '), numInp
  );
  g.appendChild(row);
  formValues[codeKey] = formValues[codeKey] || '';
  formValues[numKey] = formValues[numKey] || '';
  return g;
}

function fieldRow(...fields) {
  const r = html('div', { className: 'field-row' });
  fields.forEach(f => { if (f) r.appendChild(f); });
  return r;
}

function section(titleKey, ...children) {
  const s = html('div', { className: 'section' });
  s.appendChild(html('div', { className: 'section-title' }, [t(titleKey)]));
  children.forEach(c => { if (c) s.appendChild(c); });
  return s;
}

// ═══════════════════════════════════════════
// FORM BUILDERS
// ═══════════════════════════════════════════

function buildEmployeeApp() {
  const c = document.createDocumentFragment();
  // Applicant Info
  c.appendChild(section('ea_applicant_info',
    fieldRow(buildField(t('ea_last_name'), 'ea_last_name'), buildField(t('ea_first_name'), 'ea_first_name')),
    fieldRow(buildField(t('ea_mi'), 'ea_mi', {width:'60px'}), buildField(t('ea_date'), 'ea_date', {placeholder:'mm/dd/yyyy'})),
    fieldRow(buildField(t('ea_street_address'), 'ea_street_address'), buildField(t('ea_apt'), 'ea_apt', {width:'100px'})),
    buildCityStateZip('ea_city', 'ea_state', 'ea_zip'),
    fieldRow(buildPhoneField(t('ea_phone'), 'ea_phone_code', 'ea_phone_num')),
    fieldRow(buildField(t('ea_email'), 'ea_email'), buildField(t('ea_ssn'), 'ea_ssn')),
    fieldRow(buildField(t('ea_date_available'), 'ea_date_available'), buildField(t('ea_desired_salary'), 'ea_desired_salary')),
    fieldRow(buildField(t('ea_position'), 'ea_position')),
    fieldRow(buildYesNo(t('ea_citizen'), 'ea_citizen'), buildYesNo(t('ea_authorized'), 'ea_authorized')),
    fieldRow(buildYesNo(t('ea_worked_before'), 'ea_worked_before'), buildField(t('ea_when'), 'ea_when')),
    fieldRow(buildYesNo(t('ea_felony'), 'ea_felony'), buildField(t('ea_felony_explain'), 'ea_felony_explain')),
  ));
  // Education
  const eduContent = [];
  [['hs', 'ea_high_school'], ['col', 'ea_college'], ['oth', 'ea_other_edu']].forEach(([pfx, lbl]) => {
    if (pfx !== 'hs') eduContent.push(html('hr', { className: 'form-separator' }));
    eduContent.push(
      fieldRow(buildField(t(lbl), `ea_${pfx}_name`), buildField(t('ea_address'), `ea_${pfx}_address`)),
      fieldRow(buildField(t('ea_from'), `ea_${pfx}_from`, {width:'100px'}), buildField(t('ea_to'), `ea_${pfx}_to`, {width:'100px'})),
      fieldRow(buildYesNo(t('ea_graduate'), `ea_${pfx}_graduate`), buildField(t('ea_degree'), `ea_${pfx}_degree`)),
    );
  });
  c.appendChild(section('ea_education', ...eduContent));
  // References
  const refContent = [html('p', { style:'font-size:12px;color:#777;font-style:italic;margin-bottom:8px' }, [t('ea_ref_note')])];
  for (let i = 0; i < 3; i++) {
    if (i > 0) refContent.push(html('hr', { className: 'form-separator' }));
    refContent.push(
      fieldRow(buildField(t('ea_full_name'), `ea_ref${i}_name`), buildField(t('ea_relationship'), `ea_ref${i}_relationship`)),
      fieldRow(buildField(t('ea_company'), `ea_ref${i}_company`), buildPhoneField(t('ea_phone'), `ea_ref${i}_phone_code`, `ea_ref${i}_phone_num`)),
      fieldRow(buildField(t('ea_address'), `ea_ref${i}_address`)),
    );
  }
  c.appendChild(section('ea_references', ...refContent));
  // Employment
  const empContent = [];
  for (let i = 0; i < 3; i++) {
    if (i > 0) empContent.push(html('hr', { className: 'form-separator' }));
    empContent.push(
      fieldRow(buildField(t('ea_company'), `ea_emp${i}_company`), buildPhoneField(t('ea_phone'), `ea_emp${i}_phone_code`, `ea_emp${i}_phone_num`)),
      fieldRow(buildField(t('ea_address'), `ea_emp${i}_address`), buildField(t('ea_supervisor'), `ea_emp${i}_supervisor`)),
      fieldRow(buildField(t('ea_job_title'), `ea_emp${i}_title`), buildField(t('ea_starting_salary'), `ea_emp${i}_start_salary`)),
      fieldRow(buildField(t('ea_ending_salary'), `ea_emp${i}_end_salary`), buildField(t('ea_reason_leaving'), `ea_emp${i}_reason`)),
      fieldRow(buildTextarea(t('ea_responsibilities'), `ea_emp${i}_responsibilities`, 2)),
      fieldRow(buildField(t('ea_from'), `ea_emp${i}_from`, {width:'100px'}), buildField(t('ea_to'), `ea_emp${i}_to`, {width:'100px'})),
      fieldRow(buildYesNo(t('ea_contact_supervisor'), `ea_emp${i}_contact`)),
    );
  }
  c.appendChild(section('ea_prev_employment', ...empContent));
  // Military
  c.appendChild(section('ea_military',
    fieldRow(buildField(t('ea_branch'), 'ea_mil_branch'), buildField(t('ea_from'), 'ea_mil_from', {width:'100px'})),
    fieldRow(buildField(t('ea_to'), 'ea_mil_to', {width:'100px'}), buildField(t('ea_rank_discharge'), 'ea_mil_rank')),
    fieldRow(buildField(t('ea_type_discharge'), 'ea_mil_discharge_type'), buildField(t('ea_other_than_honorable'), 'ea_mil_explain')),
  ));
  // Disclaimer
  c.appendChild(section('ea_disclaimer',
    html('p', { style:'font-size:12px;color:#555;margin-bottom:10px' }, [t('ea_disclaimer_text')]),
    fieldRow(buildField(t('signature'), 'ea_signature'), buildField(t('date'), 'ea_sign_date')),
  ));
  return c;
}

function buildDirectDeposit() {
  const c = document.createDocumentFragment();

  // Bank Name (required dropdown with "Other" option) + $5 Fee notice
  const otherLabel = t('dd_bank_other');
  const bankOptions = [...US_BANKS, otherLabel];
  const bankDrop = buildDropdown(t('dd_bank_name') + ' *', 'dd_bank_dropdown', bankOptions);

  // Hidden text input for custom bank name
  const otherGroup = html('div', { className: 'field-group', style: 'display:none' });
  otherGroup.appendChild(html('label', {}, [t('dd_bank_name') + ':']));
  const otherInp = html('input', { type: 'text', placeholder: t('dd_bank_other'), value: formValues.dd_bank_name_other || '' });
  otherInp.addEventListener('input', () => setVal('dd_bank_name_other', otherInp.value));
  otherGroup.appendChild(otherInp);
  formValues.dd_bank_name_other = formValues.dd_bank_name_other || '';

  // Show/hide other input on dropdown change
  const bankSel = bankDrop.querySelector('select');
  if (bankSel) {
    bankSel.addEventListener('change', () => {
      if (bankSel.value === otherLabel) {
        otherGroup.style.display = '';
      } else {
        otherGroup.style.display = 'none';
      }
    });
    // Restore visibility if "Other" was previously selected
    if (formValues.dd_bank_dropdown === otherLabel) otherGroup.style.display = '';
  }

  const bankSec = section('dd_bank_name',
    fieldRow(bankDrop, otherGroup),
    html('div', { style:'background:#FFF3E0;border-left:4px solid #D32F2F;padding:10px;margin:10px 0;border-radius:4px' }, [
      html('p', { style:'font-weight:bold;color:#D32F2F;margin:0 0 8px 0;font-size:14px' }, [t('dd_fee_notice')]),
    ]),
    buildYesNo(t('dd_fee_accept'), 'dd_fee_accept'),
  );
  c.appendChild(bankSec);

  const acctSection = (num, typeKey, routKey, numKey, amtKey) => {
    const lbl = num === 1 ? 'dd_account1' : 'dd_account2';
    const content = [];
    // Account type radios
    const tg = html('div', { className: 'field-group' });
    tg.appendChild(html('label', {}, [t('dd_account_type')]));
    const rg = html('div', { className: 'radio-group' });
    ['checking', 'savings'].forEach(v => {
      const id = typeKey + '_' + v;
      const r = html('input', { type: 'radio', name: typeKey, value: v, id });
      if ((formValues[typeKey] || 'checking') === v) r.checked = true;
      r.addEventListener('change', () => setVal(typeKey, v));
      rg.append(r, html('label', { for: id }, [t('dd_' + v)]));
    });
    formValues[typeKey] = formValues[typeKey] || 'checking';
    tg.appendChild(rg);
    content.push(tg);
    content.push(fieldRow(buildField(t('dd_routing'), routKey), buildField(t('dd_account_number'), numKey)));
    if (amtKey) content.push(fieldRow(buildField(t('dd_amount'), amtKey)));
    return section(lbl, ...content);
  };
  c.appendChild(acctSection(1, 'dd_acct1_type', 'dd_acct1_routing', 'dd_acct1_number', 'dd_acct1_amount'));
  c.appendChild(acctSection(2, 'dd_acct2_type', 'dd_acct2_routing', 'dd_acct2_number'));
  c.appendChild(section('dd_authorization',
    html('p', { style:'font-size:12px;color:#555;margin-bottom:10px' }, [t('dd_auth_text').replace('{company}', 'Chicken Kitchen')]),
    fieldRow(buildField(t('dd_print_name'), 'dd_print_name'), buildField(t('dd_employee_id'), 'dd_employee_id')),
    fieldRow(buildField(t('signature'), 'dd_signature'), buildField(t('date'), 'dd_date')),
  ));
  return c;
}

function buildW4() {
  const c = document.createDocumentFragment();
  c.appendChild(section('w4_step1',
    fieldRow(buildField(t('w4_first_name'), 'w4_first_name'), buildField(t('w4_last_name'), 'w4_last_name')),
    fieldRow(buildField(t('w4_address'), 'w4_address'), buildField(t('w4_city_state_zip'), 'w4_city_state_zip')),
    fieldRow(buildField(t('w4_ssn'), 'w4_ssn')),
    buildRadioGroup(t('w4_filing_status'), 'w4_filing_status', [
      [t('w4_single'), 'single'], [t('w4_married'), 'married_joint'], [t('w4_head'), 'head_household']
    ]),
  ));
  c.appendChild(section('w4_step2', buildCheckbox(t('w4_step2_check'), 'w4_two_jobs')));
  // Step 3 with auto-calc
  const s3 = section('w4_step3',
    fieldRow(buildField(t('w4_children'), 'w4_children', {type:'number',width:'80px'}), buildField(t('w4_other_dependents'), 'w4_other_deps', {type:'number',width:'80px'})),
    fieldRow(buildField(t('w4_other_credits'), 'w4_other_credits', {width:'120px'}), buildField(t('w4_total_step3'), 'w4_total_step3', {width:'120px'})),
  );
  c.appendChild(s3);
  // Bind auto-calc
  setTimeout(() => {
    ['w4_children', 'w4_other_deps', 'w4_other_credits'].forEach(k => {
      const inp = document.querySelector(`[data-key="${k}"]`);
    });
    document.querySelectorAll('input').forEach(inp => {
      if (['w4_children','w4_other_deps','w4_other_credits'].some(k => formValues[k] !== undefined)) {
        inp.addEventListener('input', calcW4Step3);
      }
    });
  }, 100);

  c.appendChild(section('w4_step4',
    fieldRow(buildField(t('w4_other_income'), 'w4_other_income', {width:'120px'}), buildField(t('w4_deductions'), 'w4_deductions', {width:'120px'})),
    fieldRow(buildField(t('w4_extra_withholding'), 'w4_extra_withholding', {width:'120px'})),
    buildCheckbox(t('w4_exempt'), 'w4_exempt'),
  ));
  c.appendChild(section('w4_step5',
    fieldRow(buildField(t('signature'), 'w4_signature'), buildField(t('date'), 'w4_date')),
  ));
  c.appendChild(section('w4_employer_section',
    fieldRow(buildField(t('w4_employer_name'), 'w4_employer_name'), buildField(t('w4_first_date'), 'w4_first_date')),
    fieldRow(buildField(t('w4_ein'), 'w4_ein')),
  ));
  return c;
}

function calcW4Step3() {
  const c = parseInt(getVal('w4_children')) || 0;
  const d = parseInt(getVal('w4_other_deps')) || 0;
  const cr = parseInt(getVal('w4_other_credits')) || 0;
  const total = c * 2200 + d * 500 + cr;
  setVal('w4_total_step3', total ? String(total) : '');
  // Update the total field display
  document.querySelectorAll('input').forEach(inp => {
    if (inp.closest('.field-group')?.querySelector('label')?.textContent.includes(t('w4_total_step3'))) {
      inp.value = total ? String(total) : '';
    }
  });
}

function buildI9() {
  const c = document.createDocumentFragment();
  // Section 1
  c.appendChild(section('i9_section1',
    fieldRow(buildField(t('i9_last_name'), 'i9_last_name'), buildField(t('i9_first_name'), 'i9_first_name')),
    fieldRow(buildField(t('i9_middle_initial'), 'i9_middle_initial', {width:'60px'}), buildField(t('i9_other_last_names'), 'i9_other_names')),
    fieldRow(buildField(t('i9_address'), 'i9_address'), buildField(t('i9_apt'), 'i9_apt', {width:'80px'})),
    buildCityStateZip('i9_city', 'i9_state', 'i9_zip'),
    fieldRow(buildDateField(t('i9_dob'), 'i9_dob', 1940, 2010)),
    fieldRow(buildField(t('i9_ssn'), 'i9_ssn'), buildField(t('i9_email'), 'i9_email')),
    fieldRow(buildPhoneField(t('i9_phone'), 'i9_phone_code', 'i9_phone_num')),
    html('p', { style:'font-size:11px;color:#666;font-style:italic;margin:8px 0' }, [t('i9_attestation_notice')]),
    buildRadioGroup(t('i9_citizenship'), 'i9_status', [
      [t('i9_citizen'), 'citizen'], [t('i9_noncitizen_national'), 'noncitizen_national'],
      [t('i9_permanent_resident'), 'permanent_resident'], [t('i9_alien_authorized'), 'alien_authorized'],
    ]),
    fieldRow(buildField(t('i9_uscis_number'), 'i9_uscis'), buildField(t('i9_i94_number'), 'i9_i94')),
    fieldRow(buildField(t('i9_passport_number'), 'i9_passport'), buildField(t('i9_country_issuance'), 'i9_country')),
    fieldRow(buildDateField(t('i9_exp_date'), 'i9_exp_date', 2024, 2040)),
    fieldRow(buildField(t('signature'), 'i9_employee_sig'), buildDateField(t('date'), 'i9_employee_date', 2024, 2030)),
  ));

  // Section 2 - List A
  const sec2 = section('i9_section2',
    html('h4', { style:'color:#D32F2F;margin-bottom:8px' }, [t('i9_list_a')]),
    fieldRow(buildDropdown(t('i9_doc_title'), 'i9_lista_title', LIST_A_DOCS), buildField(t('i9_issuing_authority'), 'i9_lista_issuing')),
    fieldRow(buildField(t('i9_doc_number'), 'i9_lista_number'), buildDateField(t('i9_exp_date_doc'), 'i9_lista_exp', 2024, 2040)),
    html('hr', { className: 'form-separator' }),
  );

  // Lists B + C side by side
  const listsBC = html('div', { className: 'lists-bc' });
  const colB = html('div', { className: 'list-col' });
  colB.append(
    html('h4', {}, [t('i9_list_b')]),
    buildDropdown(t('i9_doc_title'), 'i9_listb_title', LIST_B_DOCS),
    buildField(t('i9_issuing_authority'), 'i9_listb_issuing'),
    buildField(t('i9_doc_number'), 'i9_listb_number'),
    buildDateField(t('i9_exp_date_doc'), 'i9_listb_exp', 2024, 2040),
  );
  const colC = html('div', { className: 'list-col' });
  colC.append(
    html('h4', {}, [t('i9_list_c')]),
    buildDropdown(t('i9_doc_title'), 'i9_listc_title', LIST_C_DOCS),
    buildField(t('i9_issuing_authority'), 'i9_listc_issuing'),
    buildField(t('i9_doc_number'), 'i9_listc_number'),
    buildDateField(t('i9_exp_date_doc'), 'i9_listc_exp', 2024, 2040),
  );
  listsBC.append(colB, colC);
  sec2.appendChild(listsBC);
  sec2.appendChild(html('hr', { className: 'form-separator' }));

  // Employer required fields
  sec2.appendChild(html('p', { className: 'required-note' }, ['* ' + t('i9_required_fields_title')]));
  sec2.append(
    fieldRow(buildDateField(t('i9_first_day_label'), 'i9_first_day', 2024, 2030, {required:true}),
             buildField(t('i9_employer_name_title_label'), 'i9_employer_name', {required:true})),
    fieldRow(buildField(t('i9_employer_sig_label'), 'i9_employer_sig', {required:true}),
             buildDateField(t('i9_today_date_label'), 'i9_employer_date', 2024, 2030, {required:true})),
    fieldRow(buildField(t('i9_employer_biz_label'), 'i9_employer_biz', {required:true}),
             buildField(t('i9_employer_addr_label'), 'i9_employer_addr', {required:true})),
  );
  c.appendChild(sec2);
  return c;
}

function buildPayroll() {
  const c = document.createDocumentFragment();
  c.appendChild(section('pa_employee_info',
    fieldRow(buildField(t('pa_name'), 'pa_name'), buildField(t('pa_date_action'), 'pa_date_action')),
    fieldRow(buildField(t('pa_job_title'), 'pa_job_title'), buildField(t('pa_store_name'), 'pa_store_name')),
    fieldRow(buildField(t('pa_employee_id'), 'pa_employee_id'), buildField(t('pa_supervisor'), 'pa_supervisor')),
    fieldRow(buildField(t('pa_dob'), 'pa_dob')),
  ));
  // Action checkboxes
  const actSec = section('pa_action_type');
  const grid = html('div', { className: 'action-grid' });
  ['pa_new_hire','pa_rehire','pa_salary_increase','pa_promotion','pa_demotion',
   'pa_transfer','pa_vacation','pa_leave','pa_termination','pa_change_address','pa_other'
  ].forEach(k => grid.appendChild(buildCheckbox(t(k), k)));
  actSec.appendChild(grid);
  c.appendChild(actSec);
  // Details
  c.appendChild(section('pa_details',
    fieldRow(buildField(t('pa_address'), 'pa_address')),
    buildCityStateZip('pa_city', 'pa_state', 'pa_zip'),
    fieldRow(buildField(t('pa_rate_of_pay'), 'pa_rate_of_pay', {width:'120px'}), buildField(t('pa_increase_amount'), 'pa_increase_amount', {width:'120px'})),
    fieldRow(buildField(t('pa_from_title'), 'pa_from_title'), buildField(t('pa_to_title'), 'pa_to_title')),
    fieldRow(buildField(t('pa_from_store'), 'pa_from_store'), buildField(t('pa_to_store'), 'pa_to_store')),
    fieldRow(buildField(t('pa_out_from'), 'pa_out_from'), buildField(t('pa_out_to'), 'pa_out_to')),
    fieldRow(buildField(t('pa_last_date_worked'), 'pa_last_date'), buildYesNo(t('pa_eligible_rehire'), 'pa_eligible_rehire')),
    buildTextarea(t('pa_cause_change'), 'pa_cause_change', 3),
    fieldRow(buildField(t('pa_store_mgr_sig'), 'pa_mgr_sig'), buildField(t('pa_supervisor_sig'), 'pa_sup_sig')),
  ));
  return c;
}

// ═══════════════════════════════════════════
// DOCUMENTS & SUBMIT
// ═══════════════════════════════════════════

// Track uploaded documents in memory
let uploadedDocs = {};

function buildDocuments() {
  const c = document.createDocumentFragment();

  // Store selection
  const storeSec = section('doc_store_selection');
  const storeLabel = html('label', { style:'font-weight:600;display:block;margin-bottom:6px;' },
    [t('doc_select_store') || 'Select store / Seleccione tienda / Chwazi magazen *']);
  storeSec.appendChild(storeLabel);
  const storeSel = html('select', { style:'width:100%;padding:8px;font-size:14px;border-radius:6px;border:2px solid #D32F2F;' });
  storeSel.appendChild(html('option', { value:'' }, ['-- ' + (t('doc_select_store') || 'Select store') + ' --']));
  Object.keys(CK_STORES).sort((a,b) => CK_STORES[a].name.localeCompare(CK_STORES[b].name)).forEach(code => {
    const s = CK_STORES[code];
    const opt = html('option', { value: code }, [s.name + ' — ' + s.address]);
    if (selectedStore && selectedStore.code === code) opt.selected = true;
    storeSel.appendChild(opt);
  });
  const storeInfo = html('div', { id:'storeInfoBox', style:'margin-top:8px;padding:10px;background:#E8F5E9;border-radius:6px;display:' + (selectedStore ? 'block' : 'none') + ';' });
  if (selectedStore) {
    storeInfo.innerHTML = '<strong>' + selectedStore.legal_entity + '</strong><br>' + selectedStore.address;
  }
  storeSel.addEventListener('change', () => {
    selectStore(storeSel.value);
    if (selectedStore) {
      storeInfo.style.display = 'block';
      storeInfo.innerHTML = '<strong>' + selectedStore.legal_entity + '</strong><br>' + selectedStore.address;
    } else {
      storeInfo.style.display = 'none';
    }
  });
  storeSec.appendChild(storeSel);
  storeSec.appendChild(storeInfo);
  c.appendChild(storeSec);

  // Applicant info
  c.appendChild(section('doc_applicant_info',
    fieldRow(buildField(t('doc_full_name'), 'doc_name'), buildField(t('doc_email'), 'doc_email')),
    fieldRow(buildField(t('doc_phone_label'), 'doc_phone')),
  ));

  // Document upload section
  const docSec = section('doc_upload_title');

  // Checklist header
  docSec.appendChild(html('p', { style:'font-size:12px;color:#777;font-style:italic;margin-bottom:12px' },
    [t('doc_upload_instructions')]));

  const docTypes = [
    ['doc_photo_id', 'doc_photo_id_label'],
    ['doc_drivers_license', 'doc_drivers_license_label'],
    ['doc_ssn_card', 'doc_ssn_card_label'],
    ['doc_work_auth', 'doc_work_auth_label'],
    ['doc_void_check', 'doc_void_check_label'],
    ['doc_other', 'doc_other_label'],
  ];

  docTypes.forEach(([key, labelKey]) => {
    const row = html('div', { className: 'doc-upload-row' });

    const label = html('label', { className: 'doc-upload-label' }, [t(labelKey)]);
    row.appendChild(label);

    const inputWrap = html('div', { className: 'doc-upload-input' });

    const fileInput = html('input', { type: 'file', accept: 'image/*,.pdf', id: 'file_' + key });
    fileInput.addEventListener('change', function() {
      const file = this.files[0];
      if (file) {
        uploadedDocs[key] = file;
        statusSpan.textContent = file.name;
        statusSpan.style.color = '#4CAF50';
      }
    });
    inputWrap.appendChild(fileInput);

    const statusSpan = html('span', { className: 'doc-file-status' }, [t('doc_no_file')]);
    if (uploadedDocs[key]) {
      statusSpan.textContent = uploadedDocs[key].name;
      statusSpan.style.color = '#4CAF50';
    }
    inputWrap.appendChild(statusSpan);

    row.appendChild(inputWrap);
    docSec.appendChild(row);
    docSec.appendChild(html('hr', { className: 'form-separator' }));
  });

  c.appendChild(docSec);

  // Signature pad
  const sigSec = section('doc_signature_section');
  const sigContainer = html('div', { id: 'signaturePadContainer' });
  sigSec.appendChild(sigContainer);
  c.appendChild(sigSec);

  // Initialize signature pad after DOM insert
  setTimeout(() => { initSignaturePad('signaturePadContainer'); }, 50);

  // Submit button section
  const submitSec = section('doc_submit_section',
    html('p', { style:'font-size:13px;color:#555;margin-bottom:15px;line-height:1.5' }, [t('doc_submit_instructions')]),
  );

  const submitBtn = html('button', {
    className: 'btn-submit-app',
    textContent: t('doc_submit_btn'),
    onClick: submitApplication,
  });
  submitSec.appendChild(submitBtn);

  c.appendChild(submitSec);
  return c;
}

// ─── Streamlit Detection ───
function isStreamlit() {
  try { return window.parent !== window && typeof window.Streamlit !== 'undefined'; }
  catch(e) { return false; }
}

// Check if a form has any filled data
function formHasData(formKey) {
  const prefixes = {
    employee_app: 'ea_', direct_deposit: 'dd_',
    w4: 'w4_', i9: 'i9_', payroll: 'pa_'
  };
  const prefix = prefixes[formKey];
  if (!prefix) return false;
  for (const [key, val] of Object.entries(formValues)) {
    if (key.startsWith(prefix) && val && typeof val === 'string' && val.trim() !== '') {
      return true;
    }
  }
  return false;
}

// Generate all filled form PDFs and send to Streamlit for email delivery
async function submitToStreamlit() {
  const name = getVal('doc_name');
  const email = getVal('doc_email');

  if (!name || !name.trim()) {
    alert(t('doc_name_required'));
    return;
  }

  const submitBtn = document.querySelector('.btn-submit-app');
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Generating PDFs... / Generando PDFs...';
  }

  try {
    const formKeys = ['employee_app', 'direct_deposit', 'w4', 'i9', 'payroll'];
    const names = {
      employee_app: 'Employee_Application', direct_deposit: 'Direct_Deposit',
      w4: 'W4_Form_2026', i9: 'I9_Form', payroll: 'Payroll_Action'
    };
    const today = new Date().toISOString().slice(0,10).replace(/-/g,'');
    const pdfs = {};

    formValues._lang = currentLang;

    const signatureDataUrl = typeof getSignatureBase64 === 'function' ? getSignatureBase64() : '';

    for (const key of formKeys) {
      if (formHasData(key)) {
        try {
          const pdfBytes = await generatePDF(key, getVal, signatureDataUrl);
          const bytes = new Uint8Array(pdfBytes);
          let binary = '';
          const chunk = 8192;
          for (let i = 0; i < bytes.length; i += chunk) {
            binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
          }
          pdfs[names[key] + '_' + today + '.pdf'] = btoa(binary);
        } catch (e) {
          console.error('Error generating PDF for ' + key + ':', e);
        }
      }
    }

    // Collect uploaded identity documents as base64
    const docs = {};
    const docKeys = Object.keys(uploadedDocs);
    for (let d = 0; d < docKeys.length; d++) {
      const file = uploadedDocs[docKeys[d]];
      const b64 = await new Promise(function(resolve) {
        const reader = new FileReader();
        reader.onload = function() { resolve(reader.result.split(',')[1]); };
        reader.readAsDataURL(file);
      });
      docs[file.name] = b64;
    }

    if (Object.keys(pdfs).length === 0 && Object.keys(docs).length === 0) {
      alert('Please fill at least one form or upload documents.\n' +
            'Por favor llene al menos un formulario o cargue documentos.');
      return;
    }

    window.Streamlit.setComponentValue({
      action: 'submit',
      submit_id: Date.now(),
      name: name,
      email: email,
      store_code: selectedStore ? selectedStore.code : '',
      signature_b64: signatureDataUrl,
      pdfs: pdfs,
      docs: docs
    });

  } catch (e) {
    alert('Error: ' + e.message);
    console.error(e);
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = t('doc_submit_btn');
    }
  }
}

async function submitApplication() {
  // If running inside Streamlit, use bidirectional component API
  if (isStreamlit()) {
    return submitToStreamlit();
  }

  const name = getVal('doc_name');
  const email = getVal('doc_email');
  const phone = getVal('doc_phone');

  if (!name.trim()) {
    alert(t('doc_name_required'));
    return;
  }
  if (!selectedStore) {
    alert(t('doc_store_required') || 'Please select a store / Seleccione una tienda');
    return;
  }
  if (!hasSignature()) {
    alert(t('doc_signature_required') || 'Please sign / Por favor firme / Tanpri siyen');
    return;
  }

  const submitBtn = document.querySelector('.btn-submit-app');
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting... / Enviando...';
  }

  try {
    const signatureDataUrl = getSignatureBase64();
    const formKeys = ['employee_app', 'direct_deposit', 'w4', 'i9', 'payroll'];
    const names = {
      employee_app: 'Employee_Application', direct_deposit: 'Direct_Deposit',
      w4: 'W4_Form_2026', i9: 'I9_Form', payroll: 'Payroll_Action'
    };
    const today = new Date().toISOString().slice(0,10).replace(/-/g,'');
    const pdfs = {};

    formValues._lang = currentLang;

    for (const key of formKeys) {
      if (formHasData(key)) {
        try {
          const pdfBytes = await generatePDF(key, getVal, signatureDataUrl);
          const bytes = new Uint8Array(pdfBytes);
          let binary = '';
          const chunk = 8192;
          for (let i = 0; i < bytes.length; i += chunk) {
            binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
          }
          pdfs[names[key] + '_' + today + '.pdf'] = btoa(binary);
        } catch (e) {
          console.error('Error generating PDF for ' + key + ':', e);
        }
      }
    }

    // Collect uploaded identity documents as base64
    const docs = {};
    for (const [dKey, file] of Object.entries(uploadedDocs)) {
      const b64 = await new Promise(resolve => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result.split(',')[1]);
        reader.readAsDataURL(file);
      });
      docs[file.name] = b64;
    }

    if (Object.keys(pdfs).length === 0 && Object.keys(docs).length === 0) {
      alert('Please fill at least one form or upload documents.\nPor favor llene al menos un formulario.');
      return;
    }

    // Submit to API
    const resp = await fetch('/api/apply', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email, name, phone,
        store_code: selectedStore.code,
        signature_b64: signatureDataUrl,
        pdfs, docs,
      }),
    });

    if (!resp.ok) {
      const err = await resp.json().catch(() => ({}));
      throw new Error(err.detail || 'Server error');
    }

    showThankYou();
  } catch (e) {
    alert('Error: ' + e.message);
    console.error(e);
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = t('doc_submit_btn');
    }
  }
}

function showThankYou() {
  currentForm = null;
  const content = el('content');
  content.innerHTML = '';

  // Deactivate sidebar buttons
  document.querySelectorAll('.sidebar button').forEach(b => b.classList.remove('active'));

  const ty = html('div', { style: 'display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;padding:40px;text-align:center;' });

  const circle = html('div', { style: 'width:80px;height:80px;border-radius:50%;background:#4CAF50;display:flex;align-items:center;justify-content:center;margin-bottom:20px;' });
  circle.appendChild(html('span', { style: 'color:#fff;font-size:40px;font-weight:bold;' }, ['\u2713']));
  ty.appendChild(circle);

  ty.appendChild(html('h1', { style: 'color:#4CAF50;margin:0 0 10px;' }, [t('doc_thank_title')]));
  ty.appendChild(html('p', { style: 'color:#555;font-size:16px;line-height:1.6;margin:10px 0;' }, [t('doc_thank_msg')]));
  ty.appendChild(html('p', { style: 'color:#999;font-size:13px;margin-top:15px;' }, [t('doc_thank_contact')]));

  const newBtn = html('button', {
    style: 'margin-top:25px;background:#D32F2F;color:#fff;border:none;padding:12px 30px;border-radius:6px;font-size:14px;font-weight:bold;cursor:pointer;',
    textContent: t('doc_new_application'),
    onClick: function() {
      uploadedDocs = {};
      Object.keys(formValues).forEach(k => { formValues[k] = ''; });
      showForm('employee_app');
    }
  });
  ty.appendChild(newBtn);

  content.appendChild(ty);
}

// ═══════════════════════════════════════════
// NAVIGATION
// ═══════════════════════════════════════════

const FORM_BUILDERS = {
  employee_app: buildEmployeeApp,
  direct_deposit: buildDirectDeposit,
  w4: buildW4,
  i9: buildI9,
  payroll: buildPayroll,
  documents: buildDocuments,
};

const FORM_TITLES = {
  employee_app: 'ea_title', direct_deposit: 'dd_title',
  w4: 'w4_title', i9: 'i9_title', payroll: 'pa_title',
  documents: 'doc_title'
};

function showForm(formKey) {
  currentForm = formKey;
  const content = el('content');
  content.innerHTML = '';

  // Title bar
  const titleBar = html('div', { className: 'form-title' });
  titleBar.appendChild(html('h2', {}, [t(FORM_TITLES[formKey])]));
  content.appendChild(titleBar);

  // Build form
  content.appendChild(FORM_BUILDERS[formKey]());

  // Update sidebar
  document.querySelectorAll('.sidebar button').forEach(b => {
    b.classList.toggle('active', b.dataset.form === formKey);
  });

  // Hide export/preview buttons on Documents tab
  const isDoc = formKey === 'documents';
  el('btnExport').style.display = isDoc ? 'none' : '';
  el('btnPreview').style.display = isDoc ? 'none' : '';
  el('btnClear').style.display = isDoc ? 'none' : '';

  content.scrollTop = 0;
}

function clearForm() {
  if (!currentForm) return;
  // Clear only values for current form prefix
  Object.keys(formValues).forEach(k => { formValues[k] = ''; });
  showForm(currentForm);
}

// ─── Language ───
function switchLanguage(lang) {
  currentLang = lang;
  const titleMap = { en: 'CHICKEN KITCHEN - HR FORMS', es: 'CHICKEN KITCHEN - FORMULARIOS RR.HH.', ht: 'CHICKEN KITCHEN - FOM RH' };
  el('headerTitle').textContent = titleMap[lang] || titleMap.en;
  el('langLabel').textContent = t('language');
  el('btnExport').textContent = t('export_pdf');
  el('btnPreview').textContent = t('preview_btn');
  el('btnClear').textContent = t('clear_form');
  // Sidebar
  document.querySelectorAll('.sidebar button').forEach(b => {
    b.textContent = t('form_' + b.dataset.form);
  });
  if (currentForm) showForm(currentForm);
  else el('welcome').querySelector('span').textContent = t('select_form');
}

// ─── I-9 Section 1 Validation (all fields except email) ───
function validateI9Section1() {
  if (currentForm !== 'i9') return true;
  const required = {
    i9_last_name: t('i9_last_name'),
    i9_first_name: t('i9_first_name'),
    i9_middle_initial: t('i9_middle_initial'),
    i9_other_names: t('i9_other_last_names'),
    i9_address: t('i9_address'),
    i9_apt: t('i9_apt'),
    i9_ssn: t('i9_ssn'),
    i9_employee_sig: t('signature'),
  };
  const missing = [];
  for (const [key, label] of Object.entries(required)) {
    if (!getVal(key).trim()) missing.push('  - ' + label);
  }
  // City/State/ZIP
  if (!getVal('i9_city').trim()) missing.push('  - ' + t('i9_city'));
  if (!getVal('i9_state').trim()) missing.push('  - ' + t('i9_state'));
  if (!getVal('i9_zip').trim()) missing.push('  - ' + t('i9_zip'));
  // DOB date
  if (!getVal('i9_dob').trim()) missing.push('  - ' + t('i9_dob'));
  // Employee date
  if (!getVal('i9_employee_date').trim()) missing.push('  - ' + t('date'));
  // Phone
  if (!getVal('i9_phone').trim()) missing.push('  - ' + t('i9_phone'));
  // Citizenship status
  if (!getVal('i9_status').trim()) missing.push('  - ' + t('i9_citizenship'));

  if (missing.length) {
    alert(t('i9_section1_required_title') + '\n\n' + t('i9_section1_required_msg') + '\n\n' + missing.join('\n'));
    return false;
  }
  return true;
}

// ─── I-9 Section 2 Validation ───
function validateI9() {
  if (currentForm !== 'i9') return true;
  const required = {
    i9_first_day: t('i9_first_day_label'),
    i9_employer_name: t('i9_employer_name_title_label'),
    i9_employer_sig: t('i9_employer_sig_label'),
    i9_employer_date: t('i9_today_date_label'),
    i9_employer_biz: t('i9_employer_biz_label'),
    i9_employer_addr: t('i9_employer_addr_label'),
  };
  const missing = [];
  for (const [key, label] of Object.entries(required)) {
    if (!getVal(key).trim()) missing.push('  - ' + label);
  }
  if (missing.length) {
    alert(t('i9_required_fields_msg') + '\n\n' + missing.join('\n'));
    return false;
  }
  return true;
}

// ─── Direct Deposit Validation ───
function validateDD() {
  if (currentForm !== 'direct_deposit') return true;
  const missing = [];
  if (!getVal('dd_bank_name').trim()) missing.push('  - ' + t('dd_bank_name'));
  if (missing.length) {
    alert(t('i9_required_fields_title') + '\n\n' + missing.join('\n'));
    return false;
  }
  return true;
}

// ═══════════════════════════════════════════
// PDF EXPORT & PREVIEW
// ═══════════════════════════════════════════

async function exportPDF() {
  if (!currentForm) { alert(t('select_form')); return; }
  if (!validateI9Section1()) return;
  if (!validateI9()) return;
  if (!validateDD()) return;
  // Store language for PDF overlay
  formValues._lang = currentLang;
  try {
    const sigUrl = typeof getSignatureBase64 === 'function' ? getSignatureBase64() : '';
    const pdfBytes = await generatePDF(currentForm, getVal, sigUrl);
    const blob = new Blob([pdfBytes], { type: 'application/pdf' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    const today = new Date().toISOString().slice(0,10).replace(/-/g,'');
    const names = { employee_app:'Employee_Application', direct_deposit:'Direct_Deposit', w4:'W4_Form_2026', i9:'I9_Form', payroll:'Payroll_Action' };
    a.href = url;
    a.download = `${names[currentForm]}_${today}.pdf`;
    a.click();
    URL.revokeObjectURL(url);
  } catch (e) {
    alert(t('pdf_error') + ': ' + e.message);
    console.error(e);
  }
}

let previewZoom = 1.0;

async function previewPDF() {
  if (!currentForm) { alert(t('select_form')); return; }
  formValues._lang = currentLang;
  try {
    const sigUrl = typeof getSignatureBase64 === 'function' ? getSignatureBase64() : '';
    const pdfBytes = await generatePDF(currentForm, getVal, sigUrl);
    previewZoom = 1.0;
    el('zoomLabel').textContent = '100%';
    el('previewFormName').textContent = t(FORM_TITLES[currentForm]);
    el('previewOverlay').style.display = 'flex';
    await renderPreview(pdfBytes);
  } catch (e) {
    alert(t('pdf_error') + ': ' + e.message);
    console.error(e);
  }
}

async function renderPreview(pdfBytes) {
  const body = el('previewBody');
  body.innerHTML = '';
  const loadingTask = pdfjsLib.getDocument({ data: pdfBytes });
  const pdf = await loadingTask.promise;
  for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const viewport = page.getViewport({ scale: 1.5 * previewZoom });
    body.appendChild(html('div', { className: 'page-label' }, [`${t('preview_page')} ${i}`]));
    const canvas = html('canvas');
    canvas.width = viewport.width;
    canvas.height = viewport.height;
    const ctx = canvas.getContext('2d');
    await page.render({ canvasContext: ctx, viewport }).promise;
    body.appendChild(canvas);
  }
  // Store bytes for zoom
  body._pdfBytes = pdfBytes;
}

async function zoomPreview(delta) {
  previewZoom = Math.max(0.3, Math.min(2.5, previewZoom + delta));
  el('zoomLabel').textContent = Math.round(previewZoom * 100) + '%';
  const bytes = el('previewBody')._pdfBytes;
  if (bytes) await renderPreview(bytes);
}

function closePreview() {
  el('previewOverlay').style.display = 'none';
  el('previewBody').innerHTML = '';
}

// ─── Init ───
document.addEventListener('DOMContentLoaded', () => {
  switchLanguage('en');
});
