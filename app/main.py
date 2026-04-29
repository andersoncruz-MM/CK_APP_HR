"""
Chicken Kitchen - HR Forms Application
Main entry point with GUI for filling, exporting, and printing HR forms.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import datetime

from translations import TRANSLATIONS, t
from pdf_overlay import fill_template
from field_help import get_tip
from us_data import US_STATES, FL_CITIES, FL_ZIPS, US_BANKS

# ─── Color Palette ───
BG_DARK = "#2C2C2C"
BG_SIDEBAR = "#1E1E1E"
BG_CONTENT = "#FFFFFF"
BG_HEADER = "#D32F2F"      # Chicken Kitchen red
BG_SECTION = "#F5F5F5"
FG_WHITE = "#FFFFFF"
FG_DARK = "#333333"
FG_LABEL = "#555555"
ACCENT = "#D32F2F"
ACCENT_HOVER = "#B71C1C"
BTN_GREEN = "#4CAF50"
BTN_BLUE = "#2196F3"
BORDER_COLOR = "#DDDDDD"


class ScrollableFrame(ttk.Frame):
    """A frame with a vertical scrollbar."""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg=BG_CONTENT, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas, style="Content.TFrame")

        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self._bind_mousewheel(self.canvas)
        self._bind_mousewheel(self.inner)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _bind_mousewheel(self, widget):
        widget.bind("<MouseWheel>", self._on_mousewheel)
        widget.bind("<Enter>", lambda e: self._bind_all_mousewheel())
        widget.bind("<Leave>", lambda e: self._unbind_all_mousewheel())

    def _bind_all_mousewheel(self):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_all_mousewheel(self):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def scroll_to_top(self):
        self.canvas.yview_moveto(0)


class CKApp(tk.Tk):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.lang = "en"
        self.current_form = None
        self.form_widgets = {}  # key -> widget mapping for each form
        self.form_data = {}     # stores all entry/var references per form

        self.title(t("app_title", self.lang))
        self.geometry("1100x750")
        self.minsize(900, 600)
        self.configure(bg=BG_DARK)

        self._setup_styles()
        self._build_header()
        self._build_sidebar()
        self._build_content_area()
        self._show_welcome()

    # ─── Styles ───
    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("Sidebar.TFrame", background=BG_SIDEBAR)
        self.style.configure("Content.TFrame", background=BG_CONTENT)
        self.style.configure("Header.TFrame", background=BG_HEADER)

        self.style.configure("Sidebar.TButton",
                             background=BG_SIDEBAR, foreground=FG_WHITE,
                             font=("Segoe UI", 10), padding=(10, 12),
                             borderwidth=0, relief="flat")
        self.style.map("Sidebar.TButton",
                        background=[("active", "#444444"), ("pressed", ACCENT)])

        self.style.configure("Active.Sidebar.TButton",
                             background=ACCENT, foreground=FG_WHITE,
                             font=("Segoe UI", 10, "bold"), padding=(10, 12))

        self.style.configure("Section.TLabelframe",
                             background=BG_SECTION, foreground=FG_DARK,
                             font=("Segoe UI", 11, "bold"), padding=10)
        self.style.configure("Section.TLabelframe.Label",
                             background=BG_SECTION, foreground=ACCENT,
                             font=("Segoe UI", 11, "bold"))

        self.style.configure("Field.TLabel",
                             background=BG_CONTENT, foreground=FG_LABEL,
                             font=("Segoe UI", 9))
        self.style.configure("SectionBg.TLabel",
                             background=BG_SECTION, foreground=FG_LABEL,
                             font=("Segoe UI", 9))

        self.style.configure("Export.TButton",
                             background=BTN_GREEN, foreground=FG_WHITE,
                             font=("Segoe UI", 11, "bold"), padding=(20, 8))
        self.style.map("Export.TButton",
                        background=[("active", "#388E3C")])

        self.style.configure("Clear.TButton",
                             background=BTN_BLUE, foreground=FG_WHITE,
                             font=("Segoe UI", 11, "bold"), padding=(20, 8))
        self.style.map("Clear.TButton",
                        background=[("active", "#1976D2")])

    # ─── Header ───
    def _build_header(self):
        self.header = tk.Frame(self, bg=BG_HEADER, height=60)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        self.title_label = tk.Label(self.header,
                                     text="  CHICKEN KITCHEN - HR FORMS",
                                     bg=BG_HEADER, fg=FG_WHITE,
                                     font=("Segoe UI", 16, "bold"),
                                     anchor="w")
        self.title_label.pack(side="left", padx=15)

        lang_frame = tk.Frame(self.header, bg=BG_HEADER)
        lang_frame.pack(side="right", padx=20)

        self.lang_label = tk.Label(lang_frame, text=t("language", self.lang),
                                    bg=BG_HEADER, fg=FG_WHITE,
                                    font=("Segoe UI", 10))
        self.lang_label.pack(side="left", padx=(0, 8))

        self.lang_var = tk.StringVar(value="English")
        self.lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var,
                                        values=["English", "Espanol", "Kreyol"],
                                        state="readonly", width=12,
                                        font=("Segoe UI", 10))
        self.lang_combo.pack(side="left")
        self.lang_combo.bind("<<ComboboxSelected>>", self._on_language_change)

    # ─── Sidebar ───
    def _build_sidebar(self):
        self.sidebar = tk.Frame(self, bg=BG_SIDEBAR, width=180)
        self.sidebar.pack(fill="y", side="left")
        self.sidebar.pack_propagate(False)

        self.sidebar_buttons = {}
        forms = [
            ("form_employee_app", self._show_employee_app),
            ("form_direct_deposit", self._show_direct_deposit),
            ("form_w4", self._show_w4),
            ("form_i9", self._show_i9),
            ("form_payroll", self._show_payroll),
        ]

        for key, cmd in forms:
            btn = tk.Button(self.sidebar,
                            text=t(key, self.lang),
                            bg=BG_SIDEBAR, fg=FG_WHITE,
                            activebackground="#444444", activeforeground=FG_WHITE,
                            font=("Segoe UI", 9), relief="flat",
                            bd=0, pady=14, padx=10, anchor="w",
                            cursor="hand2",
                            command=cmd)
            btn.pack(fill="x", padx=2, pady=1)
            self.sidebar_buttons[key] = btn

        # Separator + Documents & Submit button
        sep = tk.Frame(self.sidebar, bg="#444444", height=1)
        sep.pack(fill="x", padx=8, pady=6)
        doc_btn = tk.Button(self.sidebar,
                            text=t("form_documents", self.lang),
                            bg=BG_SIDEBAR, fg="#4CAF50",
                            activebackground="#444444", activeforeground="#4CAF50",
                            font=("Segoe UI", 9, "bold"), relief="flat",
                            bd=0, pady=14, padx=10, anchor="w",
                            cursor="hand2",
                            command=self._show_documents)
        doc_btn.pack(fill="x", padx=2, pady=1)
        self.sidebar_buttons["form_documents"] = doc_btn

    def _set_active_sidebar(self, active_key):
        for key, btn in self.sidebar_buttons.items():
            if key == active_key:
                btn.configure(bg=ACCENT, font=("Segoe UI", 9, "bold"))
            else:
                btn.configure(bg=BG_SIDEBAR, font=("Segoe UI", 9))

    # ─── Content Area ───
    def _build_content_area(self):
        self.content_wrapper = tk.Frame(self, bg=BG_CONTENT)
        self.content_wrapper.pack(fill="both", expand=True, side="left")

        self.scroll_frame = ScrollableFrame(self.content_wrapper)
        self.scroll_frame.pack(fill="both", expand=True)

        # Bottom button bar
        self.btn_bar = tk.Frame(self.content_wrapper, bg="#EEEEEE", height=55)
        self.btn_bar.pack(fill="x", side="bottom")
        self.btn_bar.pack_propagate(False)

        self.export_btn = tk.Button(self.btn_bar, text=t("export_pdf", self.lang),
                                     bg=BTN_GREEN, fg=FG_WHITE,
                                     font=("Segoe UI", 11, "bold"),
                                     relief="flat", padx=25, pady=6,
                                     cursor="hand2",
                                     command=self._export_pdf)
        self.export_btn.pack(side="right", padx=15, pady=10)

        self.preview_btn = tk.Button(self.btn_bar, text=t("preview_btn", self.lang),
                                      bg="#FF9800", fg=FG_WHITE,
                                      font=("Segoe UI", 11, "bold"),
                                      relief="flat", padx=25, pady=6,
                                      cursor="hand2",
                                      command=self._preview_pdf)
        self.preview_btn.pack(side="right", padx=5, pady=10)

        self.clear_btn = tk.Button(self.btn_bar, text=t("clear_form", self.lang),
                                    bg=BTN_BLUE, fg=FG_WHITE,
                                    font=("Segoe UI", 11, "bold"),
                                    relief="flat", padx=25, pady=6,
                                    cursor="hand2",
                                    command=self._clear_form)
        self.clear_btn.pack(side="right", padx=5, pady=10)

    def _show_welcome(self):
        self._clear_content()
        frame = self.scroll_frame.inner
        lbl = tk.Label(frame, text=t("select_form", self.lang),
                        bg=BG_CONTENT, fg=FG_LABEL,
                        font=("Segoe UI", 14))
        lbl.pack(expand=True, pady=100)

    def _clear_content(self):
        for w in self.scroll_frame.inner.winfo_children():
            w.destroy()
        self.form_widgets = {}
        self.form_data = {}

    # ─── Language Change ───
    def _on_language_change(self, event=None):
        sel = self.lang_var.get()
        self.lang = "es" if sel == "Espanol" else "ht" if sel == "Kreyol" else "en"
        self.title(t("app_title", self.lang))
        title_map = {"en": "  CHICKEN KITCHEN - HR FORMS",
                     "es": "  CHICKEN KITCHEN - FORMULARIOS RR.HH.",
                     "ht": "  CHICKEN KITCHEN - FOM RH"}
        self.title_label.config(text=title_map.get(self.lang, title_map["en"]))
        self.lang_label.config(text=t("language", self.lang))
        self.export_btn.config(text=t("export_pdf", self.lang))
        self.preview_btn.config(text=t("preview_btn", self.lang))
        self.clear_btn.config(text=t("clear_form", self.lang))

        for key, btn in self.sidebar_buttons.items():
            btn.config(text=t(key, self.lang))

        # Reload current form
        if self.current_form:
            saved = self._save_form_values()
            form_map = {
                "employee_app": self._show_employee_app,
                "direct_deposit": self._show_direct_deposit,
                "w4": self._show_w4,
                "i9": self._show_i9,
                "payroll": self._show_payroll,
                "documents": self._show_documents,
            }
            form_map[self.current_form]()
            self._restore_form_values(saved)
        else:
            self._show_welcome()

    def _save_form_values(self):
        """Save current form field values before rebuilding."""
        saved = {}
        for key, widget in self.form_widgets.items():
            if isinstance(widget, tk.Entry):
                saved[key] = widget.get()
            elif isinstance(widget, tk.Text):
                saved[key] = widget.get("1.0", "end-1c")
            elif isinstance(widget, ttk.Combobox):
                saved[key] = widget.get()
            elif isinstance(widget, tk.StringVar):
                saved[key] = widget.get()
            elif isinstance(widget, tk.BooleanVar):
                saved[key] = widget.get()
            elif isinstance(widget, tk.IntVar):
                saved[key] = widget.get()
        return saved

    def _restore_form_values(self, saved):
        """Restore saved values into rebuilt form."""
        for key, val in saved.items():
            widget = self.form_widgets.get(key)
            if widget is None:
                continue
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
                widget.insert(0, val)
            elif isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
                widget.insert("1.0", val)
            elif isinstance(widget, ttk.Combobox):
                widget.set(val)
            elif isinstance(widget, (tk.StringVar, tk.BooleanVar, tk.IntVar)):
                widget.set(val)

    # ═══════════════════════════════════════════════
    # HELPER: Build form fields
    # ═══════════════════════════════════════════════
    def _add_section(self, parent, title_key):
        """Add a section header."""
        lf = tk.LabelFrame(parent, text=f"  {t(title_key, self.lang)}  ",
                            bg=BG_SECTION, fg=ACCENT,
                            font=("Segoe UI", 11, "bold"),
                            padx=12, pady=10, bd=1, relief="groove")
        lf.pack(fill="x", padx=15, pady=(10, 5))
        return lf

    def _show_instructions(self, form_key):
        """Show a dialog with instructions for filling the current form."""
        instructions = {
            "employee_app": {
                "en": (
                    "EMPLOYEE APPLICATION - Instructions\n\n"
                    "1. Fill in all your personal information (name, address, phone, email).\n"
                    "2. Enter your Social Security Number, desired salary and position.\n"
                    "3. Answer all Yes/No questions honestly.\n"
                    "4. Complete the Education section with school names and dates.\n"
                    "5. Provide 3 professional references with contact info.\n"
                    "6. List your previous employment history (up to 3 jobs).\n"
                    "7. Fill in Military Service if applicable.\n"
                    "8. Sign and date at the bottom.\n\n"
                    "When finished, click 'Export PDF' to save."
                ),
                "es": (
                    "SOLICITUD DE EMPLEO - Instrucciones\n\n"
                    "1. Complete toda su informacion personal (nombre, direccion, telefono, email).\n"
                    "2. Ingrese su Numero de Seguro Social, salario deseado y puesto.\n"
                    "3. Responda todas las preguntas Si/No honestamente.\n"
                    "4. Complete la seccion de Educacion con nombres de escuelas y fechas.\n"
                    "5. Proporcione 3 referencias profesionales con informacion de contacto.\n"
                    "6. Liste su historial de empleo anterior (hasta 3 trabajos).\n"
                    "7. Complete el Servicio Militar si aplica.\n"
                    "8. Firme y feche al final.\n\n"
                    "Al terminar, haga clic en 'Exportar PDF' para guardar."
                ),
            },
            "direct_deposit": {
                "en": (
                    "DIRECT DEPOSIT AUTHORIZATION - Instructions\n\n"
                    "1. Select your Account 1 type (Checking or Savings).\n"
                    "2. Enter the Bank Routing Number (ABA) - 9 digits from your check.\n"
                    "3. Enter your Account Number.\n"
                    "4. Enter the percentage or dollar amount to deposit.\n"
                    "5. If you have a second account, fill Account 2 (remainder goes here).\n"
                    "6. Sign, print your name, enter your Employee ID and date.\n\n"
                    "IMPORTANT: Attach a voided check for each account."
                ),
                "es": (
                    "AUTORIZACION DE DEPOSITO DIRECTO - Instrucciones\n\n"
                    "1. Seleccione el tipo de Cuenta 1 (Corriente o Ahorros).\n"
                    "2. Ingrese el Numero de Ruta Bancaria (ABA) - 9 digitos de su cheque.\n"
                    "3. Ingrese su Numero de Cuenta.\n"
                    "4. Ingrese el porcentaje o monto en dolares a depositar.\n"
                    "5. Si tiene una segunda cuenta, complete la Cuenta 2 (el resto va aqui).\n"
                    "6. Firme, escriba su nombre, ingrese su ID de empleado y fecha.\n\n"
                    "IMPORTANTE: Adjunte un cheque anulado por cada cuenta."
                ),
            },
            "w4": {
                "en": (
                    "W-4 FORM (2026) - Instructions\n\n"
                    "Step 1: Enter your personal information and filing status.\n"
                    "Step 2: Check the box ONLY if you have two jobs total.\n"
                    "Step 3: Enter number of qualifying children (x$2,200) and other dependents (x$500).\n"
                    "Step 4: Enter other income, deductions, and extra withholding if applicable.\n"
                    "Step 5: Sign and date the form.\n\n"
                    "Employer section is filled by your employer.\n"
                    "Use the IRS estimator at www.irs.gov/W4App for accuracy."
                ),
                "es": (
                    "FORMULARIO W-4 (2026) - Instrucciones\n\n"
                    "Paso 1: Ingrese su informacion personal y estado civil para declarar.\n"
                    "Paso 2: Marque la casilla SOLO si tiene dos empleos en total.\n"
                    "Paso 3: Ingrese numero de hijos calificados (x$2,200) y otros dependientes (x$500).\n"
                    "Paso 4: Ingrese otros ingresos, deducciones y retencion adicional si aplica.\n"
                    "Paso 5: Firme y feche el formulario.\n\n"
                    "La seccion del empleador la llena su empleador.\n"
                    "Use el estimador del IRS en www.irs.gov/W4App para mayor precision."
                ),
            },
            "i9": {
                "en": (
                    "I-9 FORM - Instructions\n\n"
                    "Section 1 (Employee):\n"
                    "1. Fill in your full legal name, address, date of birth, SSN.\n"
                    "2. Enter your email and phone number.\n"
                    "3. Select your citizenship/immigration status.\n"
                    "4. If alien authorized, enter USCIS#, I-94#, or passport info.\n"
                    "5. Sign and date.\n\n"
                    "Section 2 (Employer):\n"
                    "1. Enter documents from List A, OR List B + List C.\n"
                    "2. Enter employee's first day of employment.\n"
                    "3. Employer signs and dates.\n\n"
                    "Must be completed within 3 business days of hire."
                ),
                "es": (
                    "FORMULARIO I-9 - Instrucciones\n\n"
                    "Seccion 1 (Empleado):\n"
                    "1. Ingrese su nombre legal completo, direccion, fecha de nacimiento, SSN.\n"
                    "2. Ingrese su email y numero de telefono.\n"
                    "3. Seleccione su estado de ciudadania/inmigracion.\n"
                    "4. Si es extranjero autorizado, ingrese USCIS#, I-94#, o info de pasaporte.\n"
                    "5. Firme y feche.\n\n"
                    "Seccion 2 (Empleador):\n"
                    "1. Ingrese documentos de Lista A, O Lista B + Lista C.\n"
                    "2. Ingrese el primer dia de empleo del empleado.\n"
                    "3. El empleador firma y fecha.\n\n"
                    "Debe completarse dentro de 3 dias habiles de la contratacion."
                ),
            },
            "payroll": {
                "en": (
                    "PAYROLL ACTION FORM - Instructions\n\n"
                    "1. Enter employee name, date, job title, store, ID, and supervisor.\n"
                    "2. Check the applicable action(s): New Hire, Rehire, Salary Increase, etc.\n"
                    "3. Fill in address if Change of Address.\n"
                    "4. Enter Rate of Pay and select Hourly or Weekly.\n"
                    "5. For transfers: fill From/To Job Title and Store Location.\n"
                    "6. For leave: fill Will Be Out From/To dates.\n"
                    "7. For termination: fill Last Date Worked and Eligible for Rehire.\n"
                    "8. Enter Cause for Change.\n"
                    "9. Store Manager and Supervisor must sign."
                ),
                "es": (
                    "FORMULARIO DE ACCION DE NOMINA - Instrucciones\n\n"
                    "1. Ingrese nombre del empleado, fecha, puesto, tienda, ID y supervisor.\n"
                    "2. Marque la(s) accion(es) aplicables: Nueva Contratacion, Aumento, etc.\n"
                    "3. Complete la direccion si es Cambio de Direccion.\n"
                    "4. Ingrese la Tasa de Pago y seleccione Por Hora o Semanal.\n"
                    "5. Para transferencias: complete De/A Puesto y Ubicacion de Tienda.\n"
                    "6. Para licencias: complete las fechas Desde/Hasta.\n"
                    "7. Para terminacion: complete Ultima Fecha Trabajada y Elegible para Recontratacion.\n"
                    "8. Ingrese la Causa del Cambio.\n"
                    "9. El Gerente y Supervisor deben firmar."
                ),
            },
        }
        text = instructions.get(form_key, {}).get(self.lang, "")
        if text:
            win = tk.Toplevel(self)
            title = t("instructions_title", self.lang)
            win.title(title)
            win.geometry("520x420")
            win.resizable(False, False)
            win.configure(bg=BG_CONTENT)
            win.transient(self)
            win.grab_set()

            tk.Label(win, text="?", bg=BG_HEADER, fg=FG_WHITE,
                     font=("Segoe UI", 18, "bold"), width=3).pack(
                side="top", anchor="ne", padx=0, pady=0)

            txt_frame = tk.Frame(win, bg=BG_CONTENT)
            txt_frame.pack(fill="both", expand=True, padx=20, pady=(5, 10))

            txt = tk.Text(txt_frame, font=("Segoe UI", 10), wrap="word",
                          bg=BG_CONTENT, fg=FG_DARK, relief="flat",
                          highlightthickness=0, padx=10, pady=10)
            txt.insert("1.0", text)
            txt.config(state="disabled")
            txt.pack(fill="both", expand=True)

            tk.Button(win, text="OK", command=win.destroy,
                      bg=ACCENT, fg=FG_WHITE, font=("Segoe UI", 10, "bold"),
                      relief="flat", padx=30, pady=5, cursor="hand2"
                      ).pack(pady=(0, 15))

    def _add_phone_field(self, parent, label_key, code_key, number_key, row, col=0, bg=None):
        """Add a phone field with separate area code indicator and number."""
        bg = bg or parent.cget("bg")
        lbl = tk.Label(parent, text=t(label_key, self.lang),
                        bg=bg, fg=FG_LABEL, font=("Segoe UI", 9), anchor="w")
        lbl.grid(row=row, column=col * 2, sticky="w", padx=(5, 3), pady=3)

        frame = tk.Frame(parent, bg=bg)
        frame.grid(row=row, column=col * 2 + 1, sticky="ew", padx=(0, 10), pady=3)

        tk.Label(frame, text="(", bg=bg, font=("Segoe UI", 10)).pack(side="left")
        code_entry = tk.Entry(frame, font=("Segoe UI", 10), width=4,
                               relief="solid", bd=1, justify="center")
        code_entry.pack(side="left", padx=1)
        tk.Label(frame, text=")", bg=bg, font=("Segoe UI", 10)).pack(side="left")

        num_entry = tk.Entry(frame, font=("Segoe UI", 10), width=20,
                              relief="solid", bd=1)
        num_entry.pack(side="left", padx=(5, 0))

        self.form_widgets[code_key] = code_entry
        self.form_widgets[number_key] = num_entry
        return code_entry, num_entry

    def _show_field_tip(self, field_key):
        """Show a tooltip popup for a specific field."""
        tip = get_tip(field_key, self.lang)
        if not tip:
            return
        desc, example = tip
        win = tk.Toplevel(self)
        win.overrideredirect(True)
        win.configure(bg="#333333")

        # Position near mouse
        x = self.winfo_pointerx() + 10
        y = self.winfo_pointery() + 10
        win.geometry(f"+{x}+{y}")

        inner = tk.Frame(win, bg="#FFFDE7", padx=12, pady=8, highlightbackground="#333",
                          highlightthickness=1)
        inner.pack()

        tk.Label(inner, text=desc, bg="#FFFDE7", fg="#333333",
                 font=("Segoe UI", 9), wraplength=280, justify="left").pack(anchor="w")
        ex_label = "Example" if self.lang == "en" else "Ejemplo"
        tk.Label(inner, text=f"{ex_label}: {example}", bg="#FFFDE7", fg="#1565C0",
                 font=("Segoe UI", 9, "bold"), wraplength=280, justify="left"
                 ).pack(anchor="w", pady=(4, 0))

        # Auto-close after 4 seconds or on click
        win.bind("<Button-1>", lambda e: win.destroy())
        win.after(4000, lambda: win.destroy() if win.winfo_exists() else None)

    def _add_field(self, parent, label_key, field_key, row, col=0,
                   colspan=1, width=30, bg=None):
        """Add a label + entry field, with optional ? tooltip button."""
        bg = bg or parent.cget("bg")

        # Label frame with optional ? button
        tip = get_tip(field_key, self.lang)
        if tip:
            lbl_frame = tk.Frame(parent, bg=bg)
            lbl_frame.grid(row=row, column=col * 2, sticky="w", padx=(5, 3), pady=3)
            tk.Label(lbl_frame, text=t(label_key, self.lang),
                      bg=bg, fg=FG_LABEL, font=("Segoe UI", 9), anchor="w").pack(side="left")
            tip_btn = tk.Label(lbl_frame, text=" ?", bg=bg, fg="#FF9800",
                                font=("Segoe UI", 8, "bold"), cursor="hand2")
            tip_btn.pack(side="left")
            tip_btn.bind("<Button-1>", lambda e, k=field_key: self._show_field_tip(k))
        else:
            tk.Label(parent, text=t(label_key, self.lang),
                      bg=bg, fg=FG_LABEL, font=("Segoe UI", 9), anchor="w"
                      ).grid(row=row, column=col * 2, sticky="w", padx=(5, 3), pady=3)

        entry = tk.Entry(parent, font=("Segoe UI", 10), width=width,
                          relief="solid", bd=1)
        entry.grid(row=row, column=col * 2 + 1, columnspan=colspan,
                    sticky="ew", padx=(0, 10), pady=3)

        self.form_widgets[field_key] = entry
        return entry

    def _add_dropdown(self, parent, label_key, field_key, options, row, col=0,
                      width=30, bg=None):
        """Add a label + dropdown (Combobox) with predefined options."""
        bg = bg or parent.cget("bg")
        tk.Label(parent, text=t(label_key, self.lang),
                 bg=bg, fg=FG_LABEL, font=("Segoe UI", 9), anchor="w"
                 ).grid(row=row, column=col * 2, sticky="w", padx=(5, 3), pady=3)

        combo = ttk.Combobox(parent, font=("Segoe UI", 10), width=width,
                             values=options, state="readonly")
        combo.grid(row=row, column=col * 2 + 1, sticky="ew", padx=(0, 10), pady=3)
        combo.set("")
        self.form_widgets[field_key] = combo
        return combo

    def _add_date_field(self, parent, label_key, field_key, row, col=0,
                        year_start=2024, year_end=2035, bg=None):
        """Add a date field with 3 dropdowns: MM / DD / YYYY."""
        bg = bg or parent.cget("bg")
        tk.Label(parent, text=t(label_key, self.lang),
                 bg=bg, fg=FG_LABEL, font=("Segoe UI", 9), anchor="w"
                 ).grid(row=row, column=col * 2, sticky="w", padx=(5, 3), pady=3)

        frame = tk.Frame(parent, bg=bg)
        frame.grid(row=row, column=col * 2 + 1, sticky="w", padx=(0, 10), pady=3)

        months = [""] + [f"{i:02d}" for i in range(1, 13)]
        days = [""] + [f"{i:02d}" for i in range(1, 32)]
        years = [""] + [str(y) for y in range(year_start, year_end + 1)]

        tk.Label(frame, text="MM", bg=bg, fg="#999", font=("Segoe UI", 7)).pack(side="left", padx=(0, 1))
        mm = ttk.Combobox(frame, values=months, width=4, state="readonly",
                          font=("Segoe UI", 10))
        mm.pack(side="left")
        mm.set("")
        tk.Label(frame, text=" / ", bg=bg, font=("Segoe UI", 11, "bold")).pack(side="left")

        tk.Label(frame, text="DD", bg=bg, fg="#999", font=("Segoe UI", 7)).pack(side="left", padx=(0, 1))
        dd = ttk.Combobox(frame, values=days, width=4, state="readonly",
                          font=("Segoe UI", 10))
        dd.pack(side="left")
        dd.set("")
        tk.Label(frame, text=" / ", bg=bg, font=("Segoe UI", 11, "bold")).pack(side="left")

        tk.Label(frame, text="YYYY", bg=bg, fg="#999", font=("Segoe UI", 7)).pack(side="left", padx=(0, 1))
        yy = ttk.Combobox(frame, values=years, width=6, state="readonly",
                          font=("Segoe UI", 10))
        yy.pack(side="left")
        yy.set("")

        # Store sub-widgets for auto-combine in _get_val
        self.form_widgets[field_key + "_mm"] = mm
        self.form_widgets[field_key + "_dd"] = dd
        self.form_widgets[field_key + "_yy"] = yy

    def _add_city_state_zip(self, parent, city_key, state_key, zip_key, row, bg=None):
        """Add City dropdown + State dropdown + ZIP dropdown on one row.
        Auto-fills ZIP when city is selected (for FL cities)."""
        bg = bg or parent.cget("bg")

        # City
        tk.Label(parent, text=t("ea_city", self.lang),
                 bg=bg, fg=FG_LABEL, font=("Segoe UI", 9), anchor="w"
                 ).grid(row=row, column=0, sticky="w", padx=(5, 3), pady=3)
        city_combo = ttk.Combobox(parent, font=("Segoe UI", 10), width=20,
                                  values=FL_CITIES, state="readonly")
        city_combo.grid(row=row, column=1, sticky="ew", padx=(0, 10), pady=3)
        city_combo.set(self.form_widgets.get(city_key, "") if isinstance(
            self.form_widgets.get(city_key), str) else "")
        self.form_widgets[city_key] = city_combo

        # State
        tk.Label(parent, text=t("ea_state", self.lang),
                 bg=bg, fg=FG_LABEL, font=("Segoe UI", 9), anchor="w"
                 ).grid(row=row, column=2, sticky="w", padx=(5, 3), pady=3)
        state_combo = ttk.Combobox(parent, font=("Segoe UI", 10), width=6,
                                   values=US_STATES, state="readonly")
        state_combo.grid(row=row, column=3, sticky="w", padx=(0, 10), pady=3)
        state_combo.set("FL")
        self.form_widgets[state_key] = state_combo

        # ZIP (next row)
        tk.Label(parent, text=t("ea_zip", self.lang),
                 bg=bg, fg=FG_LABEL, font=("Segoe UI", 9), anchor="w"
                 ).grid(row=row + 1, column=0, sticky="w", padx=(5, 3), pady=3)
        zip_combo = ttk.Combobox(parent, font=("Segoe UI", 10), width=10)
        zip_combo.grid(row=row + 1, column=1, sticky="w", padx=(0, 10), pady=3)
        self.form_widgets[zip_key] = zip_combo

        # Auto-fill: when city changes, set ZIP and State=FL
        def _on_city_change(event=None):
            city = city_combo.get()
            if city in FL_ZIPS:
                zip_combo.delete(0, tk.END)
                zip_combo.insert(0, FL_ZIPS[city])
                state_combo.set("FL")

        city_combo.bind("<<ComboboxSelected>>", _on_city_change)

    def _add_yes_no(self, parent, label_key, field_key, row, col=0, bg=None):
        """Add a label + Yes/No radio buttons."""
        bg = bg or parent.cget("bg")
        lbl = tk.Label(parent, text=t(label_key, self.lang),
                        bg=bg, fg=FG_LABEL, font=("Segoe UI", 9), anchor="w")
        lbl.grid(row=row, column=col * 2, sticky="w", padx=(5, 3), pady=3)

        var = tk.StringVar(value="")
        frame = tk.Frame(parent, bg=bg)
        frame.grid(row=row, column=col * 2 + 1, sticky="w", padx=(0, 10), pady=3)

        rb_yes = tk.Radiobutton(frame, text=t("yes", self.lang), variable=var,
                                 value="yes", bg=bg, font=("Segoe UI", 9),
                                 activebackground=bg)
        rb_yes.pack(side="left", padx=(0, 10))
        rb_no = tk.Radiobutton(frame, text=t("no", self.lang), variable=var,
                                value="no", bg=bg, font=("Segoe UI", 9),
                                activebackground=bg)
        rb_no.pack(side="left")

        self.form_widgets[field_key] = var
        return var

    def _add_radio_group(self, parent, label_key, field_key, options, row, bg=None):
        """Add a group of radio buttons."""
        bg = bg or parent.cget("bg")
        lbl = tk.Label(parent, text=t(label_key, self.lang),
                        bg=bg, fg=FG_LABEL, font=("Segoe UI", 9, "bold"), anchor="w")
        lbl.grid(row=row, column=0, columnspan=4, sticky="w", padx=(5, 3), pady=(8, 2))

        var = tk.StringVar(value="")
        for i, (opt_key, opt_val) in enumerate(options):
            rb = tk.Radiobutton(parent, text=t(opt_key, self.lang), variable=var,
                                 value=opt_val, bg=bg, font=("Segoe UI", 9),
                                 activebackground=bg, anchor="w")
            rb.grid(row=row + 1 + i, column=0, columnspan=4, sticky="w", padx=(20, 3), pady=1)

        self.form_widgets[field_key] = var
        return var

    def _add_checkbox(self, parent, label_key, field_key, row, col=0, bg=None):
        """Add a checkbox."""
        bg = bg or parent.cget("bg")
        var = tk.BooleanVar(value=False)
        cb = tk.Checkbutton(parent, text=t(label_key, self.lang), variable=var,
                             bg=bg, font=("Segoe UI", 9), activebackground=bg,
                             anchor="w")
        cb.grid(row=row, column=col * 2, columnspan=2, sticky="w", padx=(5, 3), pady=3)
        self.form_widgets[field_key] = var
        return var

    def _add_text(self, parent, label_key, field_key, row, height=3, bg=None):
        """Add a label + multiline text box."""
        bg = bg or parent.cget("bg")
        lbl = tk.Label(parent, text=t(label_key, self.lang),
                        bg=bg, fg=FG_LABEL, font=("Segoe UI", 9), anchor="w")
        lbl.grid(row=row, column=0, sticky="nw", padx=(5, 3), pady=3)

        txt = tk.Text(parent, font=("Segoe UI", 10), height=height,
                       relief="solid", bd=1, wrap="word")
        txt.grid(row=row, column=1, columnspan=3, sticky="ew", padx=(0, 10), pady=3)
        self.form_widgets[field_key] = txt
        return txt

    # ═══════════════════════════════════════════════
    # FORM 1: EMPLOYEE APPLICATION
    # ═══════════════════════════════════════════════
    def _show_employee_app(self):
        self._clear_content()
        self.current_form = "employee_app"
        self._set_active_sidebar("form_employee_app")
        frame = self.scroll_frame.inner

        # Title + Instructions button
        title_frame = tk.Frame(frame, bg=BG_CONTENT)
        title_frame.pack(fill="x", padx=15, pady=(15, 5))
        tk.Label(title_frame, text=t("ea_title", self.lang), bg=BG_CONTENT, fg=FG_DARK,
                 font=("Segoe UI", 14, "bold")).pack(side="left", expand=True)
        tk.Button(title_frame, text=t("instructions_btn", self.lang),
                  bg="#FF9800", fg=FG_WHITE, font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=12, pady=3, cursor="hand2",
                  command=lambda: self._show_instructions("employee_app")
                  ).pack(side="right")

        # ── Applicant Info ──
        sec = self._add_section(frame, "ea_applicant_info")
        sec.columnconfigure(1, weight=1)
        sec.columnconfigure(3, weight=1)

        self._add_field(sec, "ea_last_name", "ea_last_name", 0, 0)
        self._add_field(sec, "ea_first_name", "ea_first_name", 0, 1)
        self._add_field(sec, "ea_mi", "ea_mi", 1, 0, width=8)
        self._add_field(sec, "ea_date", "ea_date", 1, 1)
        self._add_field(sec, "ea_street_address", "ea_street_address", 2, 0)
        self._add_field(sec, "ea_apt", "ea_apt", 2, 1, width=12)
        self._add_city_state_zip(sec, "ea_city", "ea_state", "ea_zip", 3)
        self._add_phone_field(sec, "ea_phone", "ea_phone_code", "ea_phone_num", 4, 1)
        self._add_field(sec, "ea_email", "ea_email", 5, 0)
        self._add_field(sec, "ea_ssn", "ea_ssn", 5, 1)
        self._add_field(sec, "ea_date_available", "ea_date_available", 6, 0)
        self._add_field(sec, "ea_desired_salary", "ea_desired_salary", 6, 1)
        self._add_field(sec, "ea_position", "ea_position", 7, 0, colspan=3)

        self._add_yes_no(sec, "ea_citizen", "ea_citizen", 8, 0)
        self._add_yes_no(sec, "ea_authorized", "ea_authorized", 8, 1)
        self._add_yes_no(sec, "ea_worked_before", "ea_worked_before", 9, 0)
        self._add_field(sec, "ea_when", "ea_when", 9, 1)
        self._add_yes_no(sec, "ea_felony", "ea_felony", 10, 0)
        self._add_field(sec, "ea_felony_explain", "ea_felony_explain", 10, 1)

        # ── Education ──
        sec2 = self._add_section(frame, "ea_education")
        sec2.columnconfigure(1, weight=1)
        sec2.columnconfigure(3, weight=1)

        for i, prefix in enumerate(["hs", "col", "oth"]):
            label_key = {"hs": "ea_high_school", "col": "ea_college", "oth": "ea_other_edu"}[prefix]
            row_base = i * 3
            self._add_field(sec2, label_key, f"ea_{prefix}_name", row_base, 0)
            self._add_field(sec2, "ea_address", f"ea_{prefix}_address", row_base, 1)
            self._add_field(sec2, "ea_from", f"ea_{prefix}_from", row_base + 1, 0, width=12)
            self._add_field(sec2, "ea_to", f"ea_{prefix}_to", row_base + 1, 1, width=12)
            self._add_yes_no(sec2, "ea_graduate", f"ea_{prefix}_graduate", row_base + 2, 0)
            self._add_field(sec2, "ea_degree", f"ea_{prefix}_degree", row_base + 2, 1)

        # ── References ──
        sec3 = self._add_section(frame, "ea_references")
        sec3.columnconfigure(1, weight=1)
        sec3.columnconfigure(3, weight=1)

        tk.Label(sec3, text=t("ea_ref_note", self.lang), bg=BG_SECTION,
                 fg=FG_LABEL, font=("Segoe UI", 9, "italic")).grid(
            row=0, column=0, columnspan=4, sticky="w", padx=5, pady=(0, 5))

        for i in range(3):
            row_base = 1 + i * 3
            self._add_field(sec3, "ea_full_name", f"ea_ref{i}_name", row_base, 0)
            self._add_field(sec3, "ea_relationship", f"ea_ref{i}_relationship", row_base, 1)
            self._add_field(sec3, "ea_company", f"ea_ref{i}_company", row_base + 1, 0)
            self._add_phone_field(sec3, "ea_phone", f"ea_ref{i}_phone_code", f"ea_ref{i}_phone_num", row_base + 1, 1)
            self._add_field(sec3, "ea_address", f"ea_ref{i}_address", row_base + 2, 0, colspan=3)

        # ── Previous Employment ──
        sec4 = self._add_section(frame, "ea_prev_employment")
        sec4.columnconfigure(1, weight=1)
        sec4.columnconfigure(3, weight=1)

        for i in range(3):
            row_base = i * 7
            if i > 0:
                ttk.Separator(sec4, orient="horizontal").grid(
                    row=row_base - 1, column=0, columnspan=4, sticky="ew", pady=8)
            self._add_field(sec4, "ea_company", f"ea_emp{i}_company", row_base, 0)
            self._add_phone_field(sec4, "ea_phone", f"ea_emp{i}_phone_code", f"ea_emp{i}_phone_num", row_base, 1)
            self._add_field(sec4, "ea_address", f"ea_emp{i}_address", row_base + 1, 0)
            self._add_field(sec4, "ea_supervisor", f"ea_emp{i}_supervisor", row_base + 1, 1)
            self._add_field(sec4, "ea_job_title", f"ea_emp{i}_title", row_base + 2, 0)
            self._add_field(sec4, "ea_starting_salary", f"ea_emp{i}_start_salary", row_base + 2, 1, width=15)
            self._add_field(sec4, "ea_ending_salary", f"ea_emp{i}_end_salary", row_base + 3, 0, width=15)
            self._add_field(sec4, "ea_reason_leaving", f"ea_emp{i}_reason", row_base + 3, 1)
            self._add_text(sec4, "ea_responsibilities", f"ea_emp{i}_responsibilities", row_base + 4, height=2)
            self._add_field(sec4, "ea_from", f"ea_emp{i}_from", row_base + 5, 0, width=12)
            self._add_field(sec4, "ea_to", f"ea_emp{i}_to", row_base + 5, 1, width=12)
            self._add_yes_no(sec4, "ea_contact_supervisor", f"ea_emp{i}_contact", row_base + 6, 0)

        # ── Military ──
        sec5 = self._add_section(frame, "ea_military")
        sec5.columnconfigure(1, weight=1)
        sec5.columnconfigure(3, weight=1)
        self._add_field(sec5, "ea_branch", "ea_mil_branch", 0, 0)
        self._add_field(sec5, "ea_from", "ea_mil_from", 0, 1, width=12)
        self._add_field(sec5, "ea_to", "ea_mil_to", 1, 0, width=12)
        self._add_field(sec5, "ea_rank_discharge", "ea_mil_rank", 1, 1)
        self._add_field(sec5, "ea_type_discharge", "ea_mil_discharge_type", 2, 0)
        self._add_field(sec5, "ea_other_than_honorable", "ea_mil_explain", 2, 1)

        # ── Disclaimer ──
        sec6 = self._add_section(frame, "ea_disclaimer")
        sec6.columnconfigure(1, weight=1)
        sec6.columnconfigure(3, weight=1)
        tk.Label(sec6, text=t("ea_disclaimer_text", self.lang), bg=BG_SECTION,
                 fg=FG_DARK, font=("Segoe UI", 9), wraplength=700,
                 justify="left").grid(row=0, column=0, columnspan=4, sticky="w", padx=5, pady=5)
        self._add_field(sec6, "signature", "ea_signature", 1, 0)
        self._add_field(sec6, "date", "ea_sign_date", 1, 1)

        self.scroll_frame.scroll_to_top()

    # ═══════════════════════════════════════════════
    # FORM 2: DIRECT DEPOSIT
    # ═══════════════════════════════════════════════
    def _show_direct_deposit(self):
        self._clear_content()
        self.current_form = "direct_deposit"
        self._set_active_sidebar("form_direct_deposit")
        frame = self.scroll_frame.inner

        # Title + Instructions button
        title_frame = tk.Frame(frame, bg=BG_CONTENT)
        title_frame.pack(fill="x", padx=15, pady=(15, 5))
        tk.Label(title_frame, text=t("dd_title", self.lang), bg=BG_CONTENT, fg=FG_DARK,
                 font=("Segoe UI", 14, "bold")).pack(side="left", expand=True)
        tk.Button(title_frame, text=t("instructions_btn", self.lang),
                  bg="#FF9800", fg=FG_WHITE, font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=12, pady=3, cursor="hand2",
                  command=lambda: self._show_instructions("direct_deposit")
                  ).pack(side="right")

        # Instructions
        tk.Label(frame, text=t("dd_instructions", self.lang), bg=BG_CONTENT,
                 fg=FG_LABEL, font=("Segoe UI", 9, "italic"),
                 wraplength=700, justify="left").pack(padx=20, pady=(0, 10))

        # Bank Name (required dropdown with "Other" option) + $5 Fee
        sec_bank = self._add_section(frame, "dd_bank_name")
        sec_bank.columnconfigure(1, weight=1)
        sec_bank.columnconfigure(3, weight=1)

        bg_bank = sec_bank.cget("bg")
        other_label = t("dd_bank_other", self.lang)  # "Other (write)" etc.
        bank_options = list(US_BANKS) + [other_label]
        self._add_dropdown(sec_bank, "dd_bank_name", "dd_bank_dropdown", bank_options, 0, 0)

        # Hidden entry for custom bank name (shown when "Other" selected)
        other_entry = tk.Entry(sec_bank, font=("Segoe UI", 10), width=30)
        other_entry.grid(row=0, column=3, sticky="ew", padx=(0, 10), pady=3)
        other_entry.grid_remove()  # hidden by default
        self.form_widgets["dd_bank_name_other"] = other_entry

        # Show/hide other entry on dropdown change
        combo = self.form_widgets.get("dd_bank_dropdown")
        def _on_bank_change(event=None):
            val = combo.get() if combo else ""
            if val == other_label:
                other_entry.grid()
            else:
                other_entry.grid_remove()
        if combo:
            combo.bind("<<ComboboxSelected>>", _on_bank_change)

        # Virtual key: dd_bank_name returns the actual printable name
        # (either the dropdown value or the custom entry)
        class _BankNameProxy:
            """Returns dropdown value or custom entry, never the 'Other' hint."""
            def get(self):
                sel = combo.get() if combo else ""
                if sel == other_label:
                    return other_entry.get()
                return sel
        self.form_widgets["dd_bank_name"] = _BankNameProxy()

        # $5 Fee Notice
        bg_fee = sec_bank.cget("bg")
        fee_frame = tk.Frame(sec_bank, bg=bg_fee)
        fee_frame.grid(row=1, column=0, columnspan=4, sticky="w", padx=5, pady=(8, 3))
        tk.Label(fee_frame, text=t("dd_fee_notice", self.lang),
                 bg=bg_fee, fg="#D32F2F", font=("Segoe UI", 10, "bold")
                 ).pack(side="left", padx=(0, 15))

        fee_var = tk.StringVar(value="")
        fee_rf = tk.Frame(sec_bank, bg=bg_fee)
        fee_rf.grid(row=2, column=0, columnspan=4, sticky="w", padx=5, pady=3)
        tk.Label(fee_rf, text=t("dd_fee_accept", self.lang),
                 bg=bg_fee, fg=FG_DARK, font=("Segoe UI", 9)
                 ).pack(side="left", padx=(0, 10))
        tk.Radiobutton(fee_rf, text=t("yes", self.lang), variable=fee_var,
                        value="yes", bg=bg_fee, font=("Segoe UI", 9)).pack(side="left", padx=(0, 8))
        tk.Radiobutton(fee_rf, text=t("no", self.lang), variable=fee_var,
                        value="no", bg=bg_fee, font=("Segoe UI", 9)).pack(side="left")
        self.form_widgets["dd_fee_accept"] = fee_var

        # Account 1
        sec1 = self._add_section(frame, "dd_account1")
        sec1.columnconfigure(1, weight=1)
        sec1.columnconfigure(3, weight=1)

        bg = sec1.cget("bg")
        lbl = tk.Label(sec1, text=t("dd_account_type", self.lang), bg=bg,
                        fg=FG_LABEL, font=("Segoe UI", 9))
        lbl.grid(row=0, column=0, sticky="w", padx=(5, 3), pady=3)

        var1 = tk.StringVar(value="checking")
        rf = tk.Frame(sec1, bg=bg)
        rf.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=3)
        tk.Radiobutton(rf, text=t("dd_checking", self.lang), variable=var1,
                        value="checking", bg=bg, font=("Segoe UI", 9)).pack(side="left", padx=(0, 10))
        tk.Radiobutton(rf, text=t("dd_savings", self.lang), variable=var1,
                        value="savings", bg=bg, font=("Segoe UI", 9)).pack(side="left")
        self.form_widgets["dd_acct1_type"] = var1

        self._add_field(sec1, "dd_routing", "dd_acct1_routing", 1, 0)
        self._add_field(sec1, "dd_account_number", "dd_acct1_number", 1, 1)
        self._add_field(sec1, "dd_amount", "dd_acct1_amount", 2, 0)

        # Account 2
        sec2 = self._add_section(frame, "dd_account2")
        sec2.columnconfigure(1, weight=1)
        sec2.columnconfigure(3, weight=1)

        bg2 = sec2.cget("bg")
        lbl2 = tk.Label(sec2, text=t("dd_account_type", self.lang), bg=bg2,
                          fg=FG_LABEL, font=("Segoe UI", 9))
        lbl2.grid(row=0, column=0, sticky="w", padx=(5, 3), pady=3)

        var2 = tk.StringVar(value="checking")
        rf2 = tk.Frame(sec2, bg=bg2)
        rf2.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=3)
        tk.Radiobutton(rf2, text=t("dd_checking", self.lang), variable=var2,
                        value="checking", bg=bg2, font=("Segoe UI", 9)).pack(side="left", padx=(0, 10))
        tk.Radiobutton(rf2, text=t("dd_savings", self.lang), variable=var2,
                        value="savings", bg=bg2, font=("Segoe UI", 9)).pack(side="left")
        self.form_widgets["dd_acct2_type"] = var2

        self._add_field(sec2, "dd_routing", "dd_acct2_routing", 1, 0)
        self._add_field(sec2, "dd_account_number", "dd_acct2_number", 1, 1)

        # Authorization
        sec3 = self._add_section(frame, "dd_authorization")
        sec3.columnconfigure(1, weight=1)
        sec3.columnconfigure(3, weight=1)

        auth_text = t("dd_auth_text", self.lang).format(company="Chicken Kitchen")
        tk.Label(sec3, text=auth_text, bg=BG_SECTION,
                 fg=FG_DARK, font=("Segoe UI", 9), wraplength=700,
                 justify="left").grid(row=0, column=0, columnspan=4, sticky="w", padx=5, pady=5)

        self._add_field(sec3, "dd_print_name", "dd_print_name", 1, 0)
        self._add_field(sec3, "dd_employee_id", "dd_employee_id", 1, 1)
        self._add_field(sec3, "signature", "dd_signature", 2, 0)
        self._add_field(sec3, "date", "dd_date", 2, 1)

        self.scroll_frame.scroll_to_top()

    # ═══════════════════════════════════════════════
    # FORM 3: W-4
    # ═══════════════════════════════════════════════
    def _show_w4(self):
        self._clear_content()
        self.current_form = "w4"
        self._set_active_sidebar("form_w4")
        frame = self.scroll_frame.inner

        # Title + Instructions button
        title_frame = tk.Frame(frame, bg=BG_CONTENT)
        title_frame.pack(fill="x", padx=15, pady=(15, 5))
        tk.Label(title_frame, text=t("w4_title", self.lang), bg=BG_CONTENT, fg=FG_DARK,
                 font=("Segoe UI", 14, "bold")).pack(side="left", expand=True)
        tk.Button(title_frame, text=t("instructions_btn", self.lang),
                  bg="#FF9800", fg=FG_WHITE, font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=12, pady=3, cursor="hand2",
                  command=lambda: self._show_instructions("w4")
                  ).pack(side="right")

        # Step 1
        sec1 = self._add_section(frame, "w4_step1")
        sec1.columnconfigure(1, weight=1)
        sec1.columnconfigure(3, weight=1)
        self._add_field(sec1, "w4_first_name", "w4_first_name", 0, 0)
        self._add_field(sec1, "w4_last_name", "w4_last_name", 0, 1)
        self._add_field(sec1, "w4_address", "w4_address", 1, 0)
        self._add_field(sec1, "w4_city_state_zip", "w4_city_state_zip", 1, 1)
        self._add_field(sec1, "w4_ssn", "w4_ssn", 2, 0)

        self._add_radio_group(sec1, "w4_filing_status", "w4_filing_status", [
            ("w4_single", "single"),
            ("w4_married", "married_joint"),
            ("w4_head", "head_household"),
        ], 3)

        # Step 2
        sec2 = self._add_section(frame, "w4_step2")
        sec2.columnconfigure(1, weight=1)
        self._add_checkbox(sec2, "w4_step2_check", "w4_two_jobs", 0, 0)

        # Step 3
        sec3 = self._add_section(frame, "w4_step3")
        sec3.columnconfigure(1, weight=1)
        sec3.columnconfigure(3, weight=1)
        self._add_field(sec3, "w4_children", "w4_children", 0, 0, width=10)
        self._add_field(sec3, "w4_other_dependents", "w4_other_deps", 0, 1, width=10)
        self._add_field(sec3, "w4_other_credits", "w4_other_credits", 1, 0, width=15)
        self._add_field(sec3, "w4_total_step3", "w4_total_step3", 1, 1, width=15)

        # Auto-calculate Step 3 total when children/deps/credits change
        def _calc_step3(*args):
            try:
                c = int(self._get_val("w4_children") or "0")
                d = int(self._get_val("w4_other_deps") or "0")
                cr = int(self._get_val("w4_other_credits") or "0")
                total = c * 2200 + d * 500 + cr
                total_entry = self.form_widgets.get("w4_total_step3")
                if total_entry:
                    total_entry.delete(0, tk.END)
                    total_entry.insert(0, str(total) if total else "")
            except (ValueError, TypeError):
                pass

        for fk in ["w4_children", "w4_other_deps", "w4_other_credits"]:
            w = self.form_widgets.get(fk)
            if w:
                w.bind("<KeyRelease>", _calc_step3)

        # Step 4
        sec4 = self._add_section(frame, "w4_step4")
        sec4.columnconfigure(1, weight=1)
        sec4.columnconfigure(3, weight=1)
        self._add_field(sec4, "w4_other_income", "w4_other_income", 0, 0, width=15)
        self._add_field(sec4, "w4_deductions", "w4_deductions", 0, 1, width=15)
        self._add_field(sec4, "w4_extra_withholding", "w4_extra_withholding", 1, 0, width=15)
        self._add_checkbox(sec4, "w4_exempt", "w4_exempt", 2, 0)

        # Step 5
        sec5 = self._add_section(frame, "w4_step5")
        sec5.columnconfigure(1, weight=1)
        sec5.columnconfigure(3, weight=1)
        self._add_field(sec5, "signature", "w4_signature", 0, 0)
        self._add_field(sec5, "date", "w4_date", 0, 1)

        # Employer section
        sec6 = self._add_section(frame, "w4_employer_section")
        sec6.columnconfigure(1, weight=1)
        sec6.columnconfigure(3, weight=1)
        self._add_field(sec6, "w4_employer_name", "w4_employer_name", 0, 0)
        self._add_field(sec6, "w4_first_date", "w4_first_date", 0, 1)
        self._add_field(sec6, "w4_ein", "w4_ein", 1, 0)

        self.scroll_frame.scroll_to_top()

    # ═══════════════════════════════════════════════
    # FORM 4: I-9
    # ═══════════════════════════════════════════════
    def _show_i9(self):
        self._clear_content()
        self.current_form = "i9"
        self._set_active_sidebar("form_i9")
        frame = self.scroll_frame.inner

        # Title + Instructions button
        title_frame = tk.Frame(frame, bg=BG_CONTENT)
        title_frame.pack(fill="x", padx=15, pady=(15, 5))
        tk.Label(title_frame, text=t("i9_title", self.lang), bg=BG_CONTENT, fg=FG_DARK,
                 font=("Segoe UI", 14, "bold")).pack(side="left", expand=True)
        tk.Button(title_frame, text=t("instructions_btn", self.lang),
                  bg="#FF9800", fg=FG_WHITE, font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=12, pady=3, cursor="hand2",
                  command=lambda: self._show_instructions("i9")
                  ).pack(side="right")

        # Section 1
        sec1 = self._add_section(frame, "i9_section1")
        sec1.columnconfigure(1, weight=1)
        sec1.columnconfigure(3, weight=1)

        self._add_field(sec1, "i9_last_name", "i9_last_name", 0, 0)
        self._add_field(sec1, "i9_first_name", "i9_first_name", 0, 1)
        self._add_field(sec1, "i9_middle_initial", "i9_middle_initial", 1, 0, width=8)
        self._add_field(sec1, "i9_other_last_names", "i9_other_names", 1, 1)
        self._add_field(sec1, "i9_address", "i9_address", 2, 0)
        self._add_field(sec1, "i9_apt", "i9_apt", 2, 1, width=10)
        self._add_city_state_zip(sec1, "i9_city", "i9_state", "i9_zip", 3)
        self._add_date_field(sec1, "i9_dob", "i9_dob", 4, 1,
                             year_start=1940, year_end=2010)
        self._add_field(sec1, "i9_ssn", "i9_ssn", 5, 0)
        self._add_field(sec1, "i9_email", "i9_email", 5, 1)
        self._add_phone_field(sec1, "i9_phone", "i9_phone_code", "i9_phone_num", 6, 0)

        # Attestation notice
        tk.Label(sec1, text=t("i9_attestation_notice", self.lang), bg=BG_SECTION,
                 fg=FG_DARK, font=("Segoe UI", 8, "italic"), wraplength=700,
                 justify="left").grid(row=7, column=0, columnspan=4, sticky="w", padx=5, pady=(10, 5))

        self._add_radio_group(sec1, "i9_citizenship", "i9_status", [
            ("i9_citizen", "citizen"),
            ("i9_noncitizen_national", "noncitizen_national"),
            ("i9_permanent_resident", "permanent_resident"),
            ("i9_alien_authorized", "alien_authorized"),
        ], 8)

        self._add_field(sec1, "i9_uscis_number", "i9_uscis", 13, 0)
        self._add_field(sec1, "i9_i94_number", "i9_i94", 13, 1)
        self._add_field(sec1, "i9_passport_number", "i9_passport", 14, 0)
        self._add_field(sec1, "i9_country_issuance", "i9_country", 14, 1)
        self._add_date_field(sec1, "i9_exp_date", "i9_exp_date", 15, 0,
                             year_start=2024, year_end=2040)

        self._add_field(sec1, "signature", "i9_employee_sig", 16, 0)
        self._add_date_field(sec1, "date", "i9_employee_date", 16, 1,
                             year_start=2024, year_end=2030)

        # Section 2
        sec2 = self._add_section(frame, "i9_section2")
        sec2.columnconfigure(1, weight=1)
        sec2.columnconfigure(3, weight=1)

        # ── Dropdown options from I-9 Lists of Acceptable Documents (Page 5) ──
        list_a_docs = [
            "U.S. Passport",
            "U.S. Passport Card",
            "Permanent Resident Card (Form I-551)",
            "Alien Registration Receipt Card (Form I-551)",
            "Foreign Passport with I-551 stamp",
            "Employment Authorization Document (Form I-766)",
            "Foreign Passport with Form I-94/I-94A",
        ]
        list_b_docs = [
            "Driver's License",
            "State ID Card",
            "Federal Government ID Card",
            "School ID Card with photograph",
            "Voter's Registration Card",
            "U.S. Military Card",
            "U.S. Military Draft Record",
            "Military Dependent's ID Card",
            "U.S. Coast Guard Merchant Mariner Card",
            "Native American Tribal Document",
            "Canadian Driver's License",
        ]
        list_c_docs = [
            "Social Security Card (unrestricted)",
            "Birth Certificate (certified copy)",
            "Certification of Birth Abroad (DS-1350)",
            "Report of Birth Abroad (FS-545)",
            "Certification of Report of Birth (FS-240)",
            "Native American Tribal Document",
            "U.S. Citizen ID Card (Form I-197)",
            "Resident Citizen ID Card (Form I-179)",
            "Employment Authorization (DHS issued)",
        ]

        # List A - Dropdown for document title
        tk.Label(sec2, text=t("i9_list_a", self.lang), bg=BG_SECTION,
                 fg=ACCENT, font=("Segoe UI", 10, "bold")).grid(
            row=0, column=0, columnspan=4, sticky="w", padx=5, pady=(5, 3))

        self._add_dropdown(sec2, "i9_doc_title", "i9_lista_title", list_a_docs, 1, 0)
        self._add_field(sec2, "i9_issuing_authority", "i9_lista_issuing", 1, 1)
        self._add_field(sec2, "i9_doc_number", "i9_lista_number", 2, 0)
        self._add_date_field(sec2, "i9_exp_date_doc", "i9_lista_exp", 2, 1,
                             year_start=2024, year_end=2040)

        ttk.Separator(sec2, orient="horizontal").grid(
            row=3, column=0, columnspan=4, sticky="ew", pady=8)

        # List B - Dropdown for document title
        tk.Label(sec2, text=t("i9_list_b", self.lang), bg=BG_SECTION,
                 fg=ACCENT, font=("Segoe UI", 10, "bold")).grid(
            row=4, column=0, columnspan=2, sticky="w", padx=5, pady=(5, 3))
        # List C - Dropdown for document title
        tk.Label(sec2, text=t("i9_list_c", self.lang), bg=BG_SECTION,
                 fg=ACCENT, font=("Segoe UI", 10, "bold")).grid(
            row=4, column=2, columnspan=2, sticky="w", padx=5, pady=(5, 3))

        self._add_dropdown(sec2, "i9_doc_title", "i9_listb_title", list_b_docs, 5, 0)
        self._add_dropdown(sec2, "i9_doc_title", "i9_listc_title", list_c_docs, 5, 1)
        self._add_field(sec2, "i9_issuing_authority", "i9_listb_issuing", 6, 0)
        self._add_field(sec2, "i9_issuing_authority", "i9_listc_issuing", 6, 1)
        self._add_field(sec2, "i9_doc_number", "i9_listb_number", 7, 0)
        self._add_field(sec2, "i9_doc_number", "i9_listc_number", 7, 1)
        self._add_date_field(sec2, "i9_exp_date_doc", "i9_listb_exp", 8, 0,
                             year_start=2024, year_end=2040)
        self._add_date_field(sec2, "i9_exp_date_doc", "i9_listc_exp", 8, 1,
                             year_start=2024, year_end=2040)

        ttk.Separator(sec2, orient="horizontal").grid(
            row=9, column=0, columnspan=4, sticky="ew", pady=8)

        # ── Employer fields (required *) ──
        tk.Label(sec2, text="* " + t("i9_required_fields_title", self.lang),
                 bg=BG_SECTION, fg="#D32F2F", font=("Segoe UI", 8, "bold")
                 ).grid(row=10, column=0, columnspan=4, sticky="w", padx=5, pady=(5, 2))

        self._add_date_field(sec2, "i9_first_day_label", "i9_first_day", 11, 0,
                             year_start=2024, year_end=2030)
        self._add_field(sec2, "i9_employer_name_title_label", "i9_employer_name", 11, 1)
        self._add_field(sec2, "i9_employer_sig_label", "i9_employer_sig", 12, 0)
        self._add_date_field(sec2, "i9_today_date_label", "i9_employer_date", 12, 1,
                             year_start=2024, year_end=2030)
        self._add_field(sec2, "i9_employer_biz_label", "i9_employer_biz", 13, 0)
        self._add_field(sec2, "i9_employer_addr_label", "i9_employer_addr", 13, 1)

        # Mark required fields with red asterisk
        for fk in ["i9_first_day", "i9_employer_name", "i9_employer_sig",
                    "i9_employer_date", "i9_employer_biz", "i9_employer_addr"]:
            w = self.form_widgets.get(fk)
            if w and isinstance(w, tk.Entry):
                w.config(highlightbackground="#D32F2F", highlightcolor="#D32F2F",
                         highlightthickness=1)

        self.scroll_frame.scroll_to_top()

    # ═══════════════════════════════════════════════
    # FORM 5: PAYROLL ACTION
    # ═══════════════════════════════════════════════
    def _show_payroll(self):
        self._clear_content()
        self.current_form = "payroll"
        self._set_active_sidebar("form_payroll")
        frame = self.scroll_frame.inner

        # Title + Instructions button
        title_frame = tk.Frame(frame, bg=BG_CONTENT)
        title_frame.pack(fill="x", padx=15, pady=(15, 5))
        tk.Label(title_frame, text=t("pa_title", self.lang), bg=BG_CONTENT, fg=FG_DARK,
                 font=("Segoe UI", 14, "bold")).pack(side="left", expand=True)
        tk.Button(title_frame, text=t("instructions_btn", self.lang),
                  bg="#FF9800", fg=FG_WHITE, font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=12, pady=3, cursor="hand2",
                  command=lambda: self._show_instructions("payroll")
                  ).pack(side="right")

        # Employee Info
        sec1 = self._add_section(frame, "pa_employee_info")
        sec1.columnconfigure(1, weight=1)
        sec1.columnconfigure(3, weight=1)

        self._add_field(sec1, "pa_name", "pa_name", 0, 0)
        self._add_field(sec1, "pa_date_action", "pa_date_action", 0, 1)
        self._add_field(sec1, "pa_job_title", "pa_job_title", 1, 0)
        self._add_field(sec1, "pa_store_name", "pa_store_name", 1, 1)
        self._add_field(sec1, "pa_employee_id", "pa_employee_id", 2, 0)
        self._add_field(sec1, "pa_supervisor", "pa_supervisor", 2, 1)
        self._add_field(sec1, "pa_dob", "pa_dob", 3, 0)

        # Action Type
        sec2 = self._add_section(frame, "pa_action_type")
        sec2.columnconfigure(1, weight=1)
        sec2.columnconfigure(3, weight=1)

        actions = [
            "pa_new_hire", "pa_rehire", "pa_salary_increase", "pa_promotion",
            "pa_demotion", "pa_transfer", "pa_vacation", "pa_leave",
            "pa_termination", "pa_change_address", "pa_other"
        ]
        bg = sec2.cget("bg")
        for i, act_key in enumerate(actions):
            var = tk.BooleanVar(value=False)
            cb = tk.Checkbutton(sec2, text=t(act_key, self.lang), variable=var,
                                 bg=bg, font=("Segoe UI", 9), activebackground=bg)
            row_i = i // 3
            col_i = i % 3
            cb.grid(row=row_i, column=col_i, sticky="w", padx=(10, 5), pady=2)
            self.form_widgets[act_key] = var

        # Details
        sec3 = self._add_section(frame, "pa_details")
        sec3.columnconfigure(1, weight=1)
        sec3.columnconfigure(3, weight=1)

        self._add_field(sec3, "pa_address", "pa_address", 0, 0)
        self._add_city_state_zip(sec3, "pa_city", "pa_state", "pa_zip", 1)

        # Rate of pay with radio
        self._add_field(sec3, "pa_rate_of_pay", "pa_rate_of_pay", 2, 0, width=15)
        bg3 = sec3.cget("bg")
        pay_var = tk.StringVar(value="hourly")
        pay_frame = tk.Frame(sec3, bg=bg3)
        pay_frame.grid(row=2, column=3, sticky="w", padx=(0, 10), pady=3)
        tk.Radiobutton(pay_frame, text=t("pa_hourly", self.lang), variable=pay_var,
                        value="hourly", bg=bg3, font=("Segoe UI", 9)).pack(side="left", padx=(0, 8))
        tk.Radiobutton(pay_frame, text=t("pa_weekly", self.lang), variable=pay_var,
                        value="weekly", bg=bg3, font=("Segoe UI", 9)).pack(side="left")
        self.form_widgets["pa_pay_type"] = pay_var

        self._add_field(sec3, "pa_increase_amount", "pa_increase_amount", 3, 0, width=15)
        self._add_field(sec3, "pa_from_title", "pa_from_title", 4, 0)
        self._add_field(sec3, "pa_to_title", "pa_to_title", 4, 1)
        self._add_field(sec3, "pa_from_store", "pa_from_store", 5, 0)
        self._add_field(sec3, "pa_to_store", "pa_to_store", 5, 1)
        self._add_field(sec3, "pa_out_from", "pa_out_from", 6, 0)
        self._add_field(sec3, "pa_out_to", "pa_out_to", 6, 1)
        self._add_field(sec3, "pa_last_date_worked", "pa_last_date", 7, 0)
        self._add_yes_no(sec3, "pa_eligible_rehire", "pa_eligible_rehire", 7, 1)
        self._add_text(sec3, "pa_cause_change", "pa_cause_change", 8, height=3)
        self._add_field(sec3, "pa_store_mgr_sig", "pa_mgr_sig", 9, 0)
        self._add_field(sec3, "pa_supervisor_sig", "pa_sup_sig", 9, 1)

        self.scroll_frame.scroll_to_top()

    # ═══════════════════════════════════════════════
    # CLEAR FORM
    # ═══════════════════════════════════════════════
    # ═══════════════════════════════════════════════
    # DOCUMENTS & SUBMIT
    # ═══════════════════════════════════════════════

    def _show_documents(self):
        self.current_form = "documents"
        self._set_active_sidebar("form_documents")
        self._clear_content()
        frame = self.scroll_frame.inner

        # Initialize attached files dict
        if not hasattr(self, '_attached_files'):
            self._attached_files = {}

        # Title
        title = tk.Label(frame, text=t("doc_title", self.lang),
                         bg=BG_CONTENT, fg=FG_DARK,
                         font=("Segoe UI", 14, "bold"))
        title.pack(padx=15, pady=(10, 5), anchor="w")

        # Applicant info section
        info_lf = self._add_section(frame, "doc_applicant_info")

        row1 = tk.Frame(info_lf, bg=BG_SECTION)
        row1.pack(fill="x", padx=5, pady=2)
        self._add_entry_field(row1, "doc_name", t("doc_full_name", self.lang), side="left")
        self._add_entry_field(row1, "doc_email", t("doc_email", self.lang), side="left")

        row2 = tk.Frame(info_lf, bg=BG_SECTION)
        row2.pack(fill="x", padx=5, pady=2)
        self._add_entry_field(row2, "doc_phone", t("doc_phone_label", self.lang), side="left")

        # Documents upload section
        doc_lf = self._add_section(frame, "doc_upload_title")

        doc_types = [
            ("doc_photo_id", t("doc_photo_id", self.lang)),
            ("doc_drivers_license", t("doc_drivers_license", self.lang)),
            ("doc_ssn_card", t("doc_ssn_card", self.lang)),
            ("doc_work_auth", t("doc_work_auth", self.lang)),
            ("doc_void_check", t("doc_void_check", self.lang)),
            ("doc_other", t("doc_other", self.lang)),
        ]

        for doc_key, doc_label in doc_types:
            row = tk.Frame(doc_lf, bg=BG_SECTION)
            row.pack(fill="x", padx=5, pady=4)

            lbl = tk.Label(row, text=doc_label, bg=BG_SECTION, fg=FG_DARK,
                           font=("Segoe UI", 9), width=30, anchor="w")
            lbl.pack(side="left", padx=(0, 10))

            browse_btn = tk.Button(row, text=t("doc_browse", self.lang),
                                   bg="#FF9800", fg=FG_WHITE,
                                   font=("Segoe UI", 8, "bold"),
                                   relief="flat", padx=10, cursor="hand2",
                                   command=lambda k=doc_key: self._browse_document(k))
            browse_btn.pack(side="left", padx=(0, 8))

            status_var = tk.StringVar(value=self._attached_files.get(doc_key, {}).get(
                "name", t("doc_no_file", self.lang)))
            status_lbl = tk.Label(row, textvariable=status_var, bg=BG_SECTION,
                                  fg="#4CAF50" if doc_key in self._attached_files else FG_LABEL,
                                  font=("Segoe UI", 8, "italic"))
            status_lbl.pack(side="left", fill="x", expand=True)

            self.form_widgets[doc_key + "_status"] = status_var
            self.form_widgets[doc_key + "_label"] = status_lbl

            sep = tk.Frame(doc_lf, bg=BORDER_COLOR, height=1)
            sep.pack(fill="x", padx=10, pady=2)

        # Submit section
        submit_lf = self._add_section(frame, "doc_submit_section")

        note = tk.Label(submit_lf,
                        text=t("doc_submit_instructions" if "doc_submit_instructions" in TRANSLATIONS else "doc_submit_btn", self.lang),
                        bg=BG_SECTION, fg=FG_LABEL, font=("Segoe UI", 9),
                        wraplength=500, justify="left")
        note.pack(padx=5, pady=(0, 10), anchor="w")

        # Destination label
        dest_lbl = tk.Label(submit_lf,
                           text="adela@chickenkitchen.com",
                           bg=BG_SECTION, fg=ACCENT,
                           font=("Segoe UI", 10, "bold"))
        dest_lbl.pack(padx=5, pady=(0, 10))

        submit_btn = tk.Button(submit_lf,
                               text=t("doc_submit_btn", self.lang),
                               bg="#4CAF50", fg=FG_WHITE,
                               font=("Segoe UI", 12, "bold"),
                               relief="flat", padx=30, pady=10,
                               cursor="hand2",
                               command=self._submit_application)
        submit_btn.pack(padx=5, pady=10)

        self.scroll_frame.scroll_to_top()

    def _add_entry_field(self, parent, key, label, side="left"):
        """Helper to add a labeled entry field."""
        grp = tk.Frame(parent, bg=BG_SECTION)
        grp.pack(side=side, fill="x", expand=True, padx=5, pady=2)
        lbl = tk.Label(grp, text=label, bg=BG_SECTION, fg=FG_LABEL,
                       font=("Segoe UI", 9))
        lbl.pack(anchor="w")
        entry = tk.Entry(grp, font=("Segoe UI", 10), relief="solid", bd=1)
        entry.pack(fill="x", pady=(0, 2))
        self.form_widgets[key] = entry
        return entry

    def _browse_document(self, doc_key):
        """Open file dialog to select a document."""
        filepath = filedialog.askopenfilename(
            title=t("doc_browse", self.lang),
            filetypes=[
                ("All supported", "*.pdf;*.jpg;*.jpeg;*.png;*.gif;*.bmp;*.tiff"),
                ("PDF files", "*.pdf"),
                ("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp;*.tiff"),
                ("All files", "*.*"),
            ]
        )
        if filepath:
            filename = os.path.basename(filepath)
            self._attached_files[doc_key] = {"path": filepath, "name": filename}
            # Update status label
            status_var = self.form_widgets.get(doc_key + "_status")
            status_lbl = self.form_widgets.get(doc_key + "_label")
            if status_var:
                status_var.set(filename)
            if status_lbl:
                status_lbl.configure(fg="#4CAF50")

    def _submit_application(self):
        """Send application email with all attached documents."""
        name = self.form_widgets.get("doc_name")
        name_val = name.get().strip() if name else ""
        email = self.form_widgets.get("doc_email")
        email_val = email.get().strip() if email else ""
        phone = self.form_widgets.get("doc_phone")
        phone_val = phone.get().strip() if phone else ""

        if not name_val:
            messagebox.showwarning("", t("doc_name_required", self.lang))
            return

        # Confirm
        if not messagebox.askyesno(
            t("doc_submit_btn", self.lang),
            t("doc_submit_confirm", self.lang)
        ):
            return

        # Prompt for Gmail credentials if not already set
        if not hasattr(self, '_smtp_sender') or not self._smtp_sender:
            self._prompt_email_config()
            if not hasattr(self, '_smtp_sender') or not self._smtp_sender:
                return

        try:
            import smtplib as _smtp
            from email.mime.multipart import MIMEMultipart as _MM
            from email.mime.text import MIMEText as _MT
            from email.mime.base import MIMEBase as _MB
            from email import encoders as _enc

            msg = _MM()
            msg["Subject"] = f"New Employee Application - {name_val}"
            msg["From"] = self._smtp_sender
            msg["To"] = "adela@chickenkitchen.com"
            if email_val:
                msg["Reply-To"] = email_val

            now = datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")
            body = (
                f"New employee application received.\n\n"
                f"Name: {name_val}\n"
                f"Email: {email_val}\n"
                f"Phone: {phone_val}\n"
                f"Date: {now}\n"
                f"Files attached: {len(self._attached_files)}\n\n"
                f"---\nSent from Chicken Kitchen HR Forms Desktop App"
            )
            msg.attach(_MT(body, "plain"))

            # Attach all files
            for doc_key, info in self._attached_files.items():
                filepath = info["path"]
                if os.path.exists(filepath):
                    with open(filepath, "rb") as f:
                        part = _MB("application", "octet-stream")
                        part.set_payload(f.read())
                    _enc.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f'attachment; filename="{info["name"]}"'
                    )
                    msg.attach(part)

            with _smtp.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self._smtp_sender, self._smtp_password)
                server.sendmail(self._smtp_sender, "adela@chickenkitchen.com",
                                msg.as_string())

            self._show_thank_you()

        except Exception as e:
            messagebox.showerror(
                t("doc_send_error", self.lang),
                str(e)
            )

    def _prompt_email_config(self):
        """Prompt for Gmail SMTP credentials."""
        dialog = tk.Toplevel(self)
        dialog.title(t("doc_email_config_title", self.lang))
        dialog.geometry("400x250")
        dialog.configure(bg=BG_CONTENT)
        dialog.transient(self)
        dialog.grab_set()

        tk.Label(dialog, text=t("doc_email_config_msg", self.lang),
                 bg=BG_CONTENT, fg=FG_DARK, font=("Segoe UI", 9),
                 wraplength=360, justify="left").pack(padx=20, pady=(15, 10))

        f1 = tk.Frame(dialog, bg=BG_CONTENT)
        f1.pack(fill="x", padx=20, pady=3)
        tk.Label(f1, text="Gmail:", bg=BG_CONTENT, fg=FG_LABEL,
                 font=("Segoe UI", 9), width=12, anchor="w").pack(side="left")
        sender_entry = tk.Entry(f1, font=("Segoe UI", 10), width=30)
        sender_entry.pack(side="left", fill="x", expand=True)

        f2 = tk.Frame(dialog, bg=BG_CONTENT)
        f2.pack(fill="x", padx=20, pady=3)
        tk.Label(f2, text="App Password:", bg=BG_CONTENT, fg=FG_LABEL,
                 font=("Segoe UI", 9), width=12, anchor="w").pack(side="left")
        pass_entry = tk.Entry(f2, font=("Segoe UI", 10), width=30, show="*")
        pass_entry.pack(side="left", fill="x", expand=True)

        def on_ok():
            s = sender_entry.get().strip()
            p = pass_entry.get().strip()
            if s and p:
                self._smtp_sender = s
                self._smtp_password = p
                dialog.destroy()
            else:
                messagebox.showwarning("", "Please fill both fields.")

        tk.Button(dialog, text="OK", bg=BTN_GREEN, fg=FG_WHITE,
                  font=("Segoe UI", 10, "bold"), relief="flat",
                  padx=30, pady=5, cursor="hand2",
                  command=on_ok).pack(pady=15)

        dialog.wait_window()

    def _show_thank_you(self):
        """Show thank you screen after successful submission."""
        self.current_form = None
        self._clear_content()
        frame = self.scroll_frame.inner

        # Deactivate sidebar
        for key, btn in self.sidebar_buttons.items():
            btn.configure(bg=BG_SIDEBAR, font=("Segoe UI", 9))

        spacer = tk.Frame(frame, bg=BG_CONTENT, height=60)
        spacer.pack()

        # Green checkmark circle
        circle = tk.Canvas(frame, width=80, height=80, bg=BG_CONTENT,
                           highlightthickness=0)
        circle.create_oval(5, 5, 75, 75, fill="#4CAF50", outline="")
        circle.create_text(40, 40, text="\u2713", fill="white",
                           font=("Segoe UI", 36, "bold"))
        circle.pack(pady=(0, 15))

        tk.Label(frame, text=t("doc_thank_title", self.lang),
                 bg=BG_CONTENT, fg="#4CAF50",
                 font=("Segoe UI", 22, "bold")).pack()

        tk.Label(frame, text=t("doc_thank_msg", self.lang),
                 bg=BG_CONTENT, fg=FG_DARK,
                 font=("Segoe UI", 11), wraplength=450,
                 justify="center").pack(pady=15)

        tk.Label(frame, text=t("doc_thank_contact", self.lang),
                 bg=BG_CONTENT, fg=FG_LABEL,
                 font=("Segoe UI", 10)).pack(pady=(0, 20))

        tk.Button(frame, text=t("form_employee_app", self.lang).replace("\n", " "),
                  bg=ACCENT, fg=FG_WHITE,
                  font=("Segoe UI", 10, "bold"), relief="flat",
                  padx=20, pady=8, cursor="hand2",
                  command=self._show_employee_app).pack()

    def _clear_form(self):
        for key, widget in self.form_widgets.items():
            if isinstance(widget, ttk.Combobox):
                widget.set("")
            elif isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
            elif isinstance(widget, tk.StringVar):
                widget.set("")
            elif isinstance(widget, tk.BooleanVar):
                widget.set(False)
            elif isinstance(widget, tk.IntVar):
                widget.set(0)

    # ═══════════════════════════════════════════════
    # PREVIEW PDF
    # ═══════════════════════════════════════════════
    def _preview_pdf(self):
        """Generate and display a live preview of the filled form."""
        if not self.current_form:
            messagebox.showwarning("", t("select_form", self.lang))
            return

        # Store language for PDF overlay
        self.form_widgets["_lang"] = tk.StringVar(value=self.lang)

        try:
            import fitz  # PyMuPDF
            from PIL import Image, ImageTk
        except ImportError:
            messagebox.showerror("", t("preview_error", self.lang))
            return

        # Generate temp PDF
        import tempfile
        tmp_path = os.path.join(tempfile.gettempdir(), "_ck_preview.pdf")

        try:
            fill_template(self.current_form, self._get_val, tmp_path)
        except Exception as e:
            messagebox.showerror(t("preview_error", self.lang), str(e))
            return

        # Render PDF pages to images
        try:
            doc = fitz.open(tmp_path)
        except Exception as e:
            messagebox.showerror(t("preview_error", self.lang), str(e))
            return

        page_images = []
        dpi = 150
        for page in doc:
            pix = page.get_pixmap(dpi=dpi)
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            page_images.append(img)
        doc.close()

        try:
            os.unlink(tmp_path)
        except OSError:
            pass

        # ── Build preview window ──
        win = tk.Toplevel(self)
        win.title(t("preview_title", self.lang))
        win.geometry("750x900")
        win.minsize(500, 400)
        win.configure(bg="#444444")
        win.transient(self)

        # Toolbar
        toolbar = tk.Frame(win, bg="#333333", height=40)
        toolbar.pack(fill="x", side="top")
        toolbar.pack_propagate(False)

        win._zoom = [1.0]  # mutable zoom level

        def _rebuild_images(zoom):
            """Resize images and redraw canvas."""
            for widget in inner.winfo_children():
                widget.destroy()
            win._photo_refs = []
            for i, img in enumerate(page_images):
                target_w = int(img.width * zoom)
                target_h = int(img.height * zoom)
                img_r = img.resize((target_w, target_h), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img_r)
                win._photo_refs.append(photo)

                # Page label
                pg_text = f"{t('preview_page', self.lang)} {i + 1}"
                tk.Label(inner, text=pg_text, bg="#444444", fg="#CCCCCC",
                         font=("Segoe UI", 9)).pack(pady=(8, 2))
                tk.Label(inner, image=photo, bg="#444444",
                         borderwidth=2, relief="solid").pack(padx=10, pady=(0, 5))

            inner.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.yview_moveto(0)

        def _zoom_in():
            win._zoom[0] = min(win._zoom[0] + 0.15, 2.5)
            zoom_lbl.config(text=f"{int(win._zoom[0]*100)}%")
            _rebuild_images(win._zoom[0])

        def _zoom_out():
            win._zoom[0] = max(win._zoom[0] - 0.15, 0.3)
            zoom_lbl.config(text=f"{int(win._zoom[0]*100)}%")
            _rebuild_images(win._zoom[0])

        tk.Button(toolbar, text=" - ", command=_zoom_out,
                  bg="#555555", fg=FG_WHITE, font=("Segoe UI", 12, "bold"),
                  relief="flat", padx=8, cursor="hand2").pack(side="left", padx=(10, 2), pady=5)
        zoom_lbl = tk.Label(toolbar, text="100%", bg="#333333", fg=FG_WHITE,
                            font=("Segoe UI", 10), width=5)
        zoom_lbl.pack(side="left", padx=2)
        tk.Button(toolbar, text=" + ", command=_zoom_in,
                  bg="#555555", fg=FG_WHITE, font=("Segoe UI", 12, "bold"),
                  relief="flat", padx=8, cursor="hand2").pack(side="left", padx=2, pady=5)

        form_names = {
            "employee_app": "Employee Application",
            "direct_deposit": "Direct Deposit",
            "w4": "W-4 (2026)",
            "i9": "I-9",
            "payroll": "Payroll Action",
        }
        tk.Label(toolbar, text=f"  {form_names.get(self.current_form, '')}",
                 bg="#333333", fg="#AAAAAA", font=("Segoe UI", 10)).pack(side="left", padx=10)

        # Scrollable canvas for page images
        canvas = tk.Canvas(win, bg="#444444", highlightthickness=0)
        scrollbar = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)

        inner = tk.Frame(canvas, bg="#444444")
        canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Mouse wheel scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # Auto-fit to window width
        def _auto_fit():
            win.update_idletasks()
            if page_images:
                avail_w = canvas.winfo_width() - 30
                if avail_w > 50:
                    win._zoom[0] = avail_w / page_images[0].width
                    zoom_lbl.config(text=f"{int(win._zoom[0]*100)}%")
                    _rebuild_images(win._zoom[0])

        win.after(100, _auto_fit)

    # ═══════════════════════════════════════════════
    # EXPORT PDF
    # ═══════════════════════════════════════════════
    def _get_val(self, key):
        widget = self.form_widgets.get(key)
        if widget is not None:
            if isinstance(widget, ttk.Combobox):
                return widget.get()
            elif isinstance(widget, tk.Entry):
                return widget.get()
            elif isinstance(widget, tk.Text):
                return widget.get("1.0", "end-1c")
            elif isinstance(widget, (tk.StringVar, tk.BooleanVar, tk.IntVar)):
                return str(widget.get())
            elif hasattr(widget, 'get'):
                return str(widget.get())
            return ""
        # Auto-combine date dropdowns (MM/DD/YYYY)
        mm_w = self.form_widgets.get(key + "_mm")
        dd_w = self.form_widgets.get(key + "_dd")
        yy_w = self.form_widgets.get(key + "_yy")
        if mm_w is not None and dd_w is not None and yy_w is not None:
            mm = mm_w.get().strip()
            dd = dd_w.get().strip()
            yy = yy_w.get().strip()
            if mm and dd and yy:
                return f"{mm}/{dd}/{yy}"
            return ""
        # Auto-combine phone code + number fields for PDF export
        code_w = self.form_widgets.get(key + "_code")
        num_w = self.form_widgets.get(key + "_num")
        if code_w is not None and num_w is not None:
            code = code_w.get().strip()
            num = num_w.get().strip()
            if code and num:
                return f"({code}) {num}"
            elif num:
                return num
            elif code:
                return f"({code})"
        return ""

    def _validate_i9_section1(self):
        """Validate required I-9 Section 1 fields. Returns True if OK."""
        if self.current_form != "i9":
            return True

        required = {
            "i9_last_name": t("i9_last_name", self.lang),
            "i9_first_name": t("i9_first_name", self.lang),
            "i9_middle_initial": t("i9_middle_initial", self.lang),
            "i9_other_names": t("i9_other_last_names", self.lang),
            "i9_address": t("i9_address", self.lang),
            "i9_apt": t("i9_apt", self.lang),
            "i9_ssn": t("i9_ssn", self.lang),
            "i9_employee_sig": t("signature", self.lang),
        }
        missing = []
        for key, label in required.items():
            val = self._get_val(key).strip()
            if not val:
                missing.append(f"  - {label}")

        # City/State/ZIP (dropdown-based)
        for key, label in [("i9_city", t("i9_city", self.lang)),
                           ("i9_state", t("i9_state", self.lang)),
                           ("i9_zip", t("i9_zip", self.lang))]:
            val = self._get_val(key).strip()
            if not val:
                missing.append(f"  - {label}")

        # DOB date dropdown
        for key, label in [("i9_dob", t("i9_dob", self.lang))]:
            mm = self.form_widgets.get(key + "_mm")
            dd = self.form_widgets.get(key + "_dd")
            yy = self.form_widgets.get(key + "_yy")
            if mm and dd and yy:
                if not (mm.get() and dd.get() and yy.get()):
                    missing.append(f"  - {label}")
            else:
                val = self._get_val(key).strip()
                if not val:
                    missing.append(f"  - {label}")

        # Employee date
        for key, label in [("i9_employee_date", t("date", self.lang))]:
            mm = self.form_widgets.get(key + "_mm")
            dd = self.form_widgets.get(key + "_dd")
            yy = self.form_widgets.get(key + "_yy")
            if mm and dd and yy:
                if not (mm.get() and dd.get() and yy.get()):
                    missing.append(f"  - {label}")

        # Phone (code + num)
        phone_val = self._get_val("i9_phone").strip()
        if not phone_val:
            missing.append(f"  - {t('i9_phone', self.lang)}")

        # Citizenship status (radio)
        status = self._get_val("i9_status").strip()
        if not status:
            missing.append(f"  - {t('i9_citizenship', self.lang)}")

        if missing:
            msg = t("i9_section1_required_msg", self.lang).format(
                fields="\n".join(missing))
            messagebox.showwarning(t("i9_section1_required_title", self.lang), msg)
            return False
        return True

    def _validate_dd(self):
        """Validate required Direct Deposit fields. Returns True if OK."""
        if self.current_form != "direct_deposit":
            return True

        missing = []
        bank_name = self._get_val("dd_bank_name").strip()
        if not bank_name:
            missing.append(f"  - {t('dd_bank_name', self.lang)}")

        if missing:
            msg = t("i9_required_fields_msg", self.lang).format(
                fields="\n".join(missing))
            messagebox.showwarning(t("i9_required_fields_title", self.lang), msg)
            return False
        return True

    def _validate_i9_section2(self):
        """Validate required I-9 Section 2 fields. Returns True if OK."""
        if self.current_form != "i9":
            return True

        required = {
            "i9_first_day": t("i9_first_day_label", self.lang),
            "i9_employer_name": t("i9_employer_name_title_label", self.lang),
            "i9_employer_sig": t("i9_employer_sig_label", self.lang),
            "i9_employer_date": t("i9_today_date_label", self.lang),
            "i9_employer_biz": t("i9_employer_biz_label", self.lang),
            "i9_employer_addr": t("i9_employer_addr_label", self.lang),
        }
        missing = []
        for key, label in required.items():
            val = self._get_val(key).strip()
            if not val:
                missing.append(f"  - {label}")

        # For date dropdowns, check all 3 parts are selected
        for key, label in [("i9_first_day", t("i9_first_day_label", self.lang)),
                           ("i9_employer_date", t("i9_today_date_label", self.lang))]:
            mm = self.form_widgets.get(key + "_mm")
            dd = self.form_widgets.get(key + "_dd")
            yy = self.form_widgets.get(key + "_yy")
            if mm and dd and yy:
                if mm.get() and dd.get() and yy.get():
                    pass  # Complete date - OK
                elif mm.get() or dd.get() or yy.get():
                    # Partially filled date
                    incomplete = "mm/dd/yyyy" if self.lang == "en" else "mm/dd/aaaa"
                    missing.append(f"  - {label} ({incomplete})")

        if missing:
            msg = t("i9_required_fields_msg", self.lang).format(
                fields="\n".join(missing))
            messagebox.showwarning(t("i9_required_fields_title", self.lang), msg)
            return False
        return True

    def _export_pdf(self):
        if not self.current_form:
            messagebox.showwarning("", t("select_form", self.lang))
            return

        # Store language for PDF overlay
        self.form_widgets["_lang"] = tk.StringVar(value=self.lang)

        # Validate required fields before export
        if not self._validate_i9_section1():
            return
        if not self._validate_i9_section2():
            return
        if not self._validate_dd():
            return

        form_names = {
            "employee_app": "Employee_Application",
            "direct_deposit": "Direct_Deposit_Authorization",
            "w4": "W4_Form_2026",
            "i9": "I9_Form",
            "payroll": "Payroll_Action_Form",
        }
        default_name = form_names.get(self.current_form, "form")
        today = datetime.date.today().strftime("%Y%m%d")
        default_filename = f"{default_name}_{today}.pdf"

        filepath = filedialog.asksaveasfilename(
            title=t("save_pdf_title", self.lang),
            defaultextension=".pdf",
            initialfile=default_filename,
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if not filepath:
            return

        try:
            fill_template(self.current_form, self._get_val, filepath)
            messagebox.showinfo("", t("pdf_saved", self.lang))
            os.startfile(filepath)
        except Exception as e:
            import traceback
            err_detail = traceback.format_exc()
            messagebox.showerror(t("pdf_error", self.lang),
                                 f"{e}\n\n{err_detail}")



def main():
    app = CKApp()
    app.mainloop()


if __name__ == "__main__":
    main()
