import tkinter as tk
from tkinter import ttk, messagebox
import employee as ops

# ── Colour palette ──────────────────────────────────────────────────────────
BG       = "#1E1E2E"
PANEL    = "#2A2A3E"
ACCENT   = "#7C3AED"
ACCENT2  = "#A855F7"
SUCCESS  = "#10B981"
DANGER   = "#EF4444"
WARNING  = "#F59E0B"
TEXT     = "#E2E8F0"
MUTED    = "#94A3B8"
ENTRY_BG = "#313148"
TREE_BG  = "#252535"
TREE_SEL = "#5B21B6"
HDR_BG   = "#3B1FA8"

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_LABEL = ("Segoe UI", 10)
FONT_BOLD  = ("Segoe UI", 10, "bold")
FONT_SMALL = ("Segoe UI", 9)
FONT_ENTRY = ("Consolas", 10)


class EmployeeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Employee Management System")
        self.geometry("1150x700")
        self.resizable(True, True)
        self.configure(bg=BG)
        self.minsize(900, 580)
        self._selected_empno = None
        self._build_ui()
        self.load_table()

    # ─────────────────────────────────────────────────────────────────────────
    #  UI BUILD
    # ─────────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=ACCENT, pady=10)
        header.pack(fill="x")
        tk.Label(header, text="👔  Employee Management System",
                 font=FONT_TITLE, bg=ACCENT, fg="white").pack(side="left", padx=20)

        # Main container
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True, padx=16, pady=12)

        self._build_form(container)
        self._build_table(container)

    # ─────────────────────────────────────────────────────────────────────────
    #  LEFT FORM
    # ─────────────────────────────────────────────────────────────────────────
    def _build_form(self, parent):
        form = tk.Frame(parent, bg=PANEL, padx=20, pady=18)
        form.pack(side="left", fill="y", padx=(0, 12))
        form.pack_propagate(False)
        form.configure(width=310)

        tk.Label(form, text="Employee Details",
                 font=FONT_BOLD, bg=PANEL, fg=ACCENT2).grid(
                     row=0, column=0, columnspan=2, pady=(0, 14), sticky="w")

        fields = [
            ("Emp No (auto)",  "empno"),
            ("Full Name",      "empname"),
            ("Designation",    "empdesig"),
            ("Department",     "empdept"),
            ("Salary (₹)",     "salary"),
            ("Phone",          "phone"),
        ]

        self.vars = {}
        self.entries = {}
        for i, (label, key) in enumerate(fields, start=1):
            tk.Label(form, text=label, font=FONT_LABEL,
                     bg=PANEL, fg=MUTED).grid(
                         row=i*2-1, column=0, columnspan=2,
                         sticky="w", pady=(6, 1))
            var = tk.StringVar()
            ent = tk.Entry(form, textvariable=var,
                           font=FONT_ENTRY, bg=ENTRY_BG, fg=TEXT,
                           insertbackground=TEXT, relief="flat", bd=6)
            ent.grid(row=i*2, column=0, columnspan=2, sticky="ew", ipady=4)
            self.vars[key]    = var
            self.entries[key] = ent

        # Emp No is read-only (auto assigned)
        self.entries["empno"].config(state="readonly")
        form.grid_columnconfigure(0, weight=1)

        # Search
        sep = tk.Frame(form, bg=ACCENT, height=1)
        sep.grid(row=13, column=0, columnspan=2, sticky="ew", pady=14)

        tk.Label(form, text="🔍  Search", font=FONT_BOLD,
                 bg=PANEL, fg=ACCENT2).grid(row=14, column=0, columnspan=2,
                                             sticky="w", pady=(0, 4))
        self.search_var = tk.StringVar()
        se = tk.Entry(form, textvariable=self.search_var,
                      font=FONT_ENTRY, bg=ENTRY_BG, fg=TEXT,
                      insertbackground=TEXT, relief="flat", bd=6)
        se.grid(row=15, column=0, columnspan=2, sticky="ew", ipady=4)
        se.bind("<KeyRelease>", lambda e: self.search_records())

        # ── Action Buttons ────────────────────────────────────────────────
        btn_frame = tk.Frame(form, bg=PANEL)
        btn_frame.grid(row=16, column=0, columnspan=2, pady=(18, 0), sticky="ew")
        btn_frame.columnconfigure((0, 1), weight=1)

        # INSERT button
        tk.Button(btn_frame, text="➕  INSERT",
                  font=FONT_BOLD, bg=SUCCESS, fg="white",
                  activebackground="#0e9e6e", relief="flat", bd=0,
                  pady=8, cursor="hand2",
                  command=self.insert_record).grid(
                      row=0, column=0, columnspan=2,
                      sticky="ew", padx=3, pady=3)

        # UPDATE button
        tk.Button(btn_frame, text="✏️  UPDATE",
                  font=FONT_BOLD, bg=WARNING, fg="white",
                  activebackground="#d97706", relief="flat", bd=0,
                  pady=8, cursor="hand2",
                  command=self.update_record).grid(
                      row=1, column=0, sticky="ew", padx=3, pady=3)

        # DELETE button  ← clearly visible large red button
        tk.Button(btn_frame, text="🗑️  DELETE",
                  font=FONT_BOLD, bg=DANGER, fg="white",
                  activebackground="#b91c1c", relief="flat", bd=0,
                  pady=8, cursor="hand2",
                  command=self.delete_record).grid(
                      row=1, column=1, sticky="ew", padx=3, pady=3)

        # CLEAR button
        tk.Button(btn_frame, text="🧹  CLEAR FORM",
                  font=FONT_BOLD, bg=MUTED, fg="white",
                  activebackground="#64748b", relief="flat", bd=0,
                  pady=8, cursor="hand2",
                  command=self.clear_form).grid(
                      row=2, column=0, columnspan=2,
                      sticky="ew", padx=3, pady=3)

        # REFRESH button
        tk.Button(btn_frame, text="🔄  REFRESH TABLE",
                  font=FONT_BOLD, bg=ACCENT, fg="white",
                  activebackground="#6d28d9", relief="flat", bd=0,
                  pady=8, cursor="hand2",
                  command=self.load_table).grid(
                      row=3, column=0, columnspan=2,
                      sticky="ew", padx=3, pady=3)

        # Helper label below buttons
        tk.Label(form,
                 text="💡 Click a row first, then UPDATE or DELETE",
                 font=("Segoe UI", 8), bg=PANEL, fg=MUTED,
                 wraplength=260).grid(row=17, column=0, columnspan=2,
                                      sticky="w", pady=(8, 0))

    # ─────────────────────────────────────────────────────────────────────────
    #  RIGHT TABLE
    # ─────────────────────────────────────────────────────────────────────────
    def _build_table(self, parent):
        frame = tk.Frame(parent, bg=BG)
        frame.pack(side="left", fill="both", expand=True)

        tk.Label(frame, text="All Employees",
                 font=FONT_BOLD, bg=BG, fg=MUTED).pack(anchor="w", pady=(0, 6))

        cols = ("Emp No", "Name", "Designation", "Department", "Salary", "Phone")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                        background=TREE_BG, foreground=TEXT,
                        fieldbackground=TREE_BG, rowheight=30,
                        font=FONT_SMALL, borderwidth=0)
        style.configure("Custom.Treeview.Heading",
                        background=HDR_BG, foreground="white",
                        font=FONT_BOLD, relief="flat")
        style.map("Custom.Treeview",
                  background=[("selected", TREE_SEL)],
                  foreground=[("selected", "white")])

        tree_frame = tk.Frame(frame, bg=BG)
        tree_frame.pack(fill="both", expand=True)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")

        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings",
                                 style="Custom.Treeview",
                                 yscrollcommand=vsb.set,
                                 xscrollcommand=hsb.set)
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        col_widths = [70, 160, 150, 140, 110, 120]
        for col, w in zip(cols, col_widths):
            self.tree.heading(col, text=col,
                              command=lambda c=col: self._sort_tree(c, False))
            self.tree.column(col, width=w, anchor="center", minwidth=60)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(frame, textvariable=self.status_var,
                 font=FONT_SMALL, bg=PANEL, fg=MUTED,
                 anchor="w", padx=10, pady=5).pack(fill="x", pady=(6, 0))

    # ─────────────────────────────────────────────────────────────────────────
    #  HELPERS
    # ─────────────────────────────────────────────────────────────────────────
    def _set_status(self, msg, ok=True):
        prefix = "  ✔  " if ok else "  ✘  "
        self.status_var.set(prefix + msg)

    def _validate_form(self, need_empno=False):
        name   = self.vars["empname"].get().strip()
        desig  = self.vars["empdesig"].get().strip()
        dept   = self.vars["empdept"].get().strip()
        salary = self.vars["salary"].get().strip()
        phone  = self.vars["phone"].get().strip()
        empno  = self.vars["empno"].get().strip()

        if not all([name, desig, dept, salary, phone]):
            raise ValueError("All fields are required.")
        try:
            sal = float(salary)
            if sal < 0:
                raise ValueError
        except ValueError:
            raise ValueError("Salary must be a valid positive number.")
        if not phone.isdigit() or len(phone) < 7:
            raise ValueError("Phone must contain digits only (min 7 digits).")
        if need_empno and not empno:
            raise ValueError("Please click a row in the table first.")

        return (int(empno) if need_empno else None), name, desig, dept, sal, phone

    # ─────────────────────────────────────────────────────────────────────────
    #  CRUD OPERATIONS
    # ─────────────────────────────────────────────────────────────────────────

    # ── INSERT ────────────────────────────────────────────────────────────────
    def insert_record(self):
        try:
            _, name, desig, dept, salary, phone = self._validate_form()
            empno = ops.insert_employee(name, desig, dept, salary, phone)
            self._set_status(f"Employee '{name}' inserted successfully! (Emp No: {empno})")
            self.clear_form()
            self.load_table()
        except ValueError as e:
            messagebox.showwarning("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # ── UPDATE ────────────────────────────────────────────────────────────────
    def update_record(self):
        empno_s = self.vars["empno"].get().strip()
        if not empno_s:
            messagebox.showwarning("No Record Selected",
                                   "Please click a row in the table to select an employee first.")
            return
        try:
            empno, name, desig, dept, salary, phone = self._validate_form(need_empno=True)
            if not messagebox.askyesno("Confirm Update",
                                       f"Update details for Emp No {empno}?"):
                return
            success = ops.update_employee(empno, name, desig, dept, salary, phone)
            if success:
                self._set_status(f"Emp No {empno} updated successfully.")
                self.load_table()
            else:
                messagebox.showwarning("Not Found", f"No employee with Emp No {empno}.")
        except ValueError as e:
            messagebox.showwarning("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # ── DELETE ────────────────────────────────────────────────────────────────
    def delete_record(self):
        empno_s = self.vars["empno"].get().strip()

        # Check if a row is selected
        if not empno_s:
            messagebox.showwarning(
                "No Record Selected",
                "Please click a row in the table to select an employee first.\n\n"
                "Steps:\n"
                "1. Click any employee row in the table\n"
                "2. Their details will appear in the form\n"
                "3. Then click the DELETE button"
            )
            return

        empno    = int(empno_s)
        emp_name = self.vars["empname"].get().strip()

        # Confirm before deleting
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to DELETE this employee?\n\n"
            f"  Emp No   : {empno}\n"
            f"  Name     : {emp_name}\n\n"
            f"This action CANNOT be undone!"
        )
        if not confirm:
            return

        try:
            success = ops.delete_employee(empno)
            if success:
                messagebox.showinfo("Deleted",
                                    f"Employee '{emp_name}' (Emp No: {empno}) "
                                    f"has been deleted successfully.")
                self._set_status(f"Emp No {empno} ({emp_name}) deleted.", ok=False)
                self.clear_form()
                self.load_table()
            else:
                messagebox.showwarning("Not Found",
                                       f"No employee found with Emp No {empno}.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # ── LOAD TABLE ────────────────────────────────────────────────────────────
    def load_table(self, rows=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if rows is None:
            rows = ops.fetch_all_employees()
        for i, row in enumerate(rows):
            tag = "odd" if i % 2 == 0 else "even"
            self.tree.insert("", "end", values=(
                row[0], row[1], row[2], row[3],
                f"Rs.{float(row[4]):,.2f}", row[5]
            ), tags=(tag,))
        self.tree.tag_configure("odd",  background=TREE_BG)
        self.tree.tag_configure("even", background="#2D2D44")
        self._set_status(f"{len(rows)} employee record(s) loaded.")

    # ── SEARCH ────────────────────────────────────────────────────────────────
    def search_records(self):
        keyword = self.search_var.get().strip()
        rows = ops.search_employees(keyword) if keyword else ops.fetch_all_employees()
        self.load_table(rows)

    # ── ROW SELECT ────────────────────────────────────────────────────────────
    def on_row_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        if not values:
            return
        row = ops.fetch_employee_by_id(int(values[0]))
        if row:
            self.vars["empno"].set(row[0])
            self.vars["empname"].set(row[1])
            self.vars["empdesig"].set(row[2])
            self.vars["empdept"].set(row[3])
            self.vars["salary"].set(row[4])
            self.vars["phone"].set(row[5])
            self._set_status(f"Selected: {row[1]} (Emp No: {row[0]})")

    # ── CLEAR FORM ────────────────────────────────────────────────────────────
    def clear_form(self):
        for key, var in self.vars.items():
            var.set("")
        self._selected_empno = None

    # ── SORT TABLE ────────────────────────────────────────────────────────────
    def _sort_tree(self, col, descending):
        data = [(self.tree.set(item, col), item)
                for item in self.tree.get_children("")]
        try:
            data.sort(
                key=lambda x: float(x[0].replace("Rs.", "").replace(",", "")),
                reverse=descending)
        except ValueError:
            data.sort(reverse=descending)
        for i, (_, item) in enumerate(data):
            self.tree.move(item, "", i)
        self.tree.heading(col,
                          command=lambda: self._sort_tree(col, not descending))