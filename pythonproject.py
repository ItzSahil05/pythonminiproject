import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


# ==========================================
# DATABASE HANDLER (SQLite)
# ==========================================
class Database:
    def __init__(self, db_name="student_records.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                roll_no TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                course TEXT NOT NULL,
                gpa REAL NOT NULL,
                attendance REAL NOT NULL
            )
            """
        )
        self.conn.commit()

    def insert(self, roll_no, name, course, gpa, attendance):
        self.cursor.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?, ?)",
            (roll_no, name, course, gpa, attendance)
        )
        self.conn.commit()

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def update(self, roll_no, name, course, gpa, attendance):
        self.cursor.execute(
            """
            UPDATE students 
            SET name = ?, course = ?, gpa = ?, attendance = ? 
            WHERE roll_no = ?
            """,
            (name, course, gpa, attendance, roll_no)
        )
        self.conn.commit()

    def delete(self, roll_no):
        self.cursor.execute("DELETE FROM students WHERE roll_no = ?", (roll_no,))
        self.conn.commit()

    def search(self, query):
        wildcard = f"%{query}%"
        self.cursor.execute(
            """
            SELECT * FROM students 
            WHERE roll_no LIKE ? OR name LIKE ? OR course LIKE ?
            """,
            (wildcard, wildcard, wildcard)
        )
        return self.cursor.fetchall()


# ==========================================
# MODERN GUI APPLICATION
# ==========================================
class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System — Enterprise Hub")
        self.root.geometry("1080x680")
        self.root.minsize(920, 580)
        self.root.configure(bg="#0b1120")

        self.db = Database()

        # UI Color Tokens
        self.c_bg = "#0b1120"
        self.c_card = "#1e293b"
        self.c_card_border = "#334155"
        self.c_text = "#f8fafc"
        self.c_subtext = "#94a3b8"
        self.c_accent = "#38bdf8"
        self.c_primary = "#2563eb"
        self.c_primary_hover = "#1d4ed8"
        self.c_danger = "#e11d48"
        self.c_danger_hover = "#be123c"
        self.c_success = "#059669"

        # State Variables
        self.var_roll = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_course = tk.StringVar()
        self.var_gpa = tk.StringVar()
        self.var_attendance = tk.StringVar()
        self.var_search = tk.StringVar()

        self.configure_styles()
        self.setup_ui()
        self.load_table_data()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Treeview Styling
        style.configure(
            "Treeview",
            background="#1e293b",
            foreground="#f8fafc",
            fieldbackground="#1e293b",
            rowheight=32,
            font=("Segoe UI", 10),
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background="#334155",
            foreground="#38bdf8",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=6
        )
        style.map(
            "Treeview",
            background=[("selected", "#2563eb")],
            foreground=[("selected", "#ffffff")]
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#475569")]
        )

        # Combobox / Entry styling
        style.configure(
            "TCombobox",
            fieldbackground="#0f172a",
            background="#334155",
            foreground="#f8fafc",
            arrowcolor="#38bdf8",
            padding=5
        )

    def setup_ui(self):
        # 1. Header Bar
        header = tk.Frame(self.root, bg=self.c_card, padx=25, pady=16)
        header.pack(fill="x")

        tk.Label(
            header,
            text="ACADEMIC PORTAL",
            font=("Segoe UI", 15, "bold"),
            fg=self.c_accent,
            bg=self.c_card
        ).pack(side="left")

        tk.Label(
            header,
            text="Student Registry & Analytics Dashboard",
            font=("Segoe UI", 10),
            fg=self.c_subtext,
            bg=self.c_card
        ).pack(side="left", padx=(12, 0), pady=(3, 0))

        # 2. Workspace Body
        body = tk.Frame(self.root, bg=self.c_bg, padx=20, pady=16)
        body.pack(fill="both", expand=True)

        # 3. KPI Metric Cards Row
        kpi_row = tk.Frame(body, bg=self.c_bg)
        kpi_row.pack(fill="x", pady=(0, 16))

        self.card_total = self.create_kpi_card(kpi_row, "TOTAL ENROLLED", "0", "#38bdf8")
        self.card_gpa = self.create_kpi_card(kpi_row, "CLASS AVG GPA", "0.0", "#34d399")
        self.card_risk = self.create_kpi_card(kpi_row, "AT RISK (<75% ATT)", "0", "#f87171")

        # 4. Main Panel Split (Form Left, Table Right)
        panel = tk.Frame(body, bg=self.c_bg)
        panel.pack(fill="both", expand=True)

        # Left Form Card
        form_card = tk.Frame(panel, bg=self.c_card, padx=18, pady=18, width=330, highlightbackground=self.c_card_border, highlightthickness=1)
        form_card.pack(side="left", fill="y", padx=(0, 16))
        form_card.pack_propagate(False)

        tk.Label(
            form_card,
            text="STUDENT RECORD",
            font=("Segoe UI", 11, "bold"),
            fg=self.c_accent,
            bg=self.c_card
        ).pack(anchor="w", pady=(0, 12))

        self.create_form_field(form_card, "Roll Number", self.var_roll)
        self.create_form_field(form_card, "Full Name", self.var_name)
        self.create_combobox_field(
            form_card, "Course Program", self.var_course,
            ["Computer Science", "Information Tech", "Data Science", "Electronics", "Mechanical"]
        )
        self.create_form_field(form_card, "GPA (0.00 - 10.00)", self.var_gpa)
        self.create_form_field(form_card, "Attendance Percentage (%)", self.var_attendance)

        # Action Buttons Grid
        btn_box = tk.Frame(form_card, bg=self.c_card)
        btn_box.pack(fill="x", pady=(18, 0))

        self.btn_add = self.create_action_button(btn_box, "Add Student", self.add_student, self.c_primary, self.c_primary_hover)
        self.btn_add.grid(row=0, column=0, padx=3, pady=3, sticky="ew")

        self.btn_update = self.create_action_button(btn_box, "Update", self.update_student, "#0284c7", "#0369a1")
        self.btn_update.grid(row=0, column=1, padx=3, pady=3, sticky="ew")

        self.btn_delete = self.create_action_button(btn_box, "Delete", self.delete_student, self.c_danger, self.c_danger_hover)
        self.btn_delete.grid(row=1, column=0, padx=3, pady=3, sticky="ew")

        self.btn_clear = self.create_action_button(btn_box, "Reset Form", self.clear_fields, "#475569", "#334155")
        self.btn_clear.grid(row=1, column=1, padx=3, pady=3, sticky="ew")

        btn_box.columnconfigure(0, weight=1)
        btn_box.columnconfigure(1, weight=1)

        # Right Data View Card
        data_card = tk.Frame(panel, bg=self.c_card, padx=16, pady=16, highlightbackground=self.c_card_border, highlightthickness=1)
        data_card.pack(side="right", fill="both", expand=True)

        # Search Bar Strip
        search_strip = tk.Frame(data_card, bg=self.c_card)
        search_strip.pack(fill="x", pady=(0, 12))

        tk.Label(
            search_strip,
            text="Search Records:",
            font=("Segoe UI", 9, "bold"),
            fg=self.c_subtext,
            bg=self.c_card
        ).pack(side="left", padx=(0, 8))

        search_entry = tk.Entry(
            search_strip,
            textvariable=self.var_search,
            font=("Segoe UI", 10),
            bg="#0f172a",
            fg="white",
            insertbackground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.c_card_border
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=4)
        search_entry.bind("<KeyRelease>", lambda e: self.search_student())

        refresh_btn = tk.Button(
            search_strip,
            text="↻ Refresh",
            command=self.load_table_data,
            bg="#334155",
            fg="white",
            font=("Segoe UI", 9),
            relief="flat",
            padx=12,
            pady=3,
            cursor="hand2"
        )
        refresh_btn.pack(side="left")

        # Treeview Container
        table_container = tk.Frame(data_card, bg=self.c_card)
        table_container.pack(fill="both", expand=True)

        columns = ("Roll No", "Name", "Course", "GPA", "Attendance")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("Roll No", text="Roll No", anchor="center")
        self.tree.column("Roll No", width=95, anchor="center")

        self.tree.heading("Name", text="Full Name", anchor="w")
        self.tree.column("Name", width=220, anchor="w")

        self.tree.heading("Course", text="Course Program", anchor="w")
        self.tree.column("Course", width=160, anchor="w")

        self.tree.heading("GPA", text="GPA", anchor="center")
        self.tree.column("GPA", width=80, anchor="center")

        self.tree.heading("Attendance", text="Attendance", anchor="center")
        self.tree.column("Attendance", width=105, anchor="center")

        # Striped table tags
        self.tree.tag_configure("odd", background="#1e293b")
        self.tree.tag_configure("even", background="#162032")

        scroll = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.get_selected_row)

    # ---------------- UI Helper Builders ----------------
    def create_kpi_card(self, parent, title, initial_val, accent_color):
        card = tk.Frame(parent, bg=self.c_card, padx=16, pady=12, highlightbackground=self.c_card_border, highlightthickness=1)
        card.pack(side="left", fill="x", expand=True, padx=4)

        tk.Label(card, text=title, font=("Segoe UI", 8, "bold"), fg=self.c_subtext, bg=self.c_card).pack(anchor="w")
        val_label = tk.Label(card, text=initial_val, font=("Segoe UI", 18, "bold"), fg=accent_color, bg=self.c_card)
        val_label.pack(anchor="w", pady=(2, 0))
        return val_label

    def create_form_field(self, parent, label_text, text_var):
        tk.Label(parent, text=label_text, font=("Segoe UI", 9), fg=self.c_subtext, bg=self.c_card).pack(anchor="w", pady=(6, 2))
        entry = tk.Entry(
            parent,
            textvariable=text_var,
            font=("Segoe UI", 10),
            bg="#0f172a",
            fg="white",
            insertbackground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.c_card_border
        )
        entry.pack(fill="x", ipady=4)

    def create_combobox_field(self, parent, label_text, text_var, options):
        tk.Label(parent, text=label_text, font=("Segoe UI", 9), fg=self.c_subtext, bg=self.c_card).pack(anchor="w", pady=(6, 2))
        combo = ttk.Combobox(parent, textvariable=text_var, values=options, state="readonly", font=("Segoe UI", 10))
        combo.pack(fill="x", ipady=2)
        if options:
            combo.set(options[0])

    def create_action_button(self, parent, text, command, bg_color, hover_color):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg="white",
            activebackground=hover_color,
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            pady=7,
            cursor="hand2"
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
        return btn

    # ---------------- Business Logic & Analytics ----------------
    def refresh_kpis(self, records):
        total = len(records)
        if total == 0:
            self.card_total.config(text="0")
            self.card_gpa.config(text="0.00")
            self.card_risk.config(text="0")
            return

        avg_gpa = sum(float(r[3]) for r in records) / total
        at_risk = sum(1 for r in records if float(r[4]) < 75.0)

        self.card_total.config(text=str(total))
        self.card_gpa.config(text=f"{avg_gpa:.2f}")
        self.card_risk.config(text=str(at_risk))

    def load_table_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        records = self.db.fetch_all()
        for idx, student in enumerate(records):
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert("", "end", values=student, tags=(tag,))
        self.refresh_kpis(records)

    def add_student(self):
        roll = self.var_roll.get().strip()
        name = self.var_name.get().strip()
        course = self.var_course.get()

        try:
            gpa = float(self.var_gpa.get())
            att = float(self.var_attendance.get())
            if not roll or not name:
                raise ValueError
            if not (0.0 <= gpa <= 10.0) or not (0.0 <= att <= 100.0):
                messagebox.showerror("Range Error", "GPA must be 0-10 and Attendance must be 0-100%.")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Please provide valid information for all fields.")
            return

        try:
            self.db.insert(roll, name, course, gpa, att)
            self.load_table_data()
            self.clear_fields()
            messagebox.showinfo("Success", f"Enrolled student: {name}")
        except sqlite3.IntegrityError:
            messagebox.showerror("Conflict", f"Roll Number {roll} already exists.")

    def update_student(self):
        roll = self.var_roll.get().strip()
        if not roll:
            messagebox.showwarning("Selection Required", "Select a record from the table to update.")
            return

        try:
            name = self.var_name.get().strip()
            course = self.var_course.get()
            gpa = float(self.var_gpa.get())
            att = float(self.var_attendance.get())
            self.db.update(roll, name, course, gpa, att)
            self.load_table_data()
            messagebox.showinfo("Success", "Record successfully updated.")
        except ValueError:
            messagebox.showerror("Error", "Invalid numeric values entered.")

    def delete_student(self):
        roll = self.var_roll.get().strip()
        if not roll:
            messagebox.showwarning("Selection Required", "Select a record from the table to delete.")
            return

        if messagebox.askyesno("Confirm Deletion", f"Permanently remove student record {roll}?"):
            self.db.delete(roll)
            self.load_table_data()
            self.clear_fields()

    def get_selected_row(self, event):
        selected = self.tree.focus()
        if selected:
            data = self.tree.item(selected, "values")
            self.var_roll.set(data[0])
            self.var_name.set(data[1])
            self.var_course.set(data[2])
            self.var_gpa.set(data[3])
            self.var_attendance.set(data[4])

    def search_student(self):
        query = self.var_search.get().strip()
        results = self.db.search(query)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for idx, record in enumerate(results):
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert("", "end", values=record, tags=(tag,))
        self.refresh_kpis(results)

    def clear_fields(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_gpa.set("")
        self.var_attendance.set("")
        self.var_search.set("")


if __name__ == "__main__":
    app_window = tk.Tk()
    app = StudentManagementApp(app_window)
    app_window.mainloop()