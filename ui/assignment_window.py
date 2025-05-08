import tkinter as tk
from tkinter import ttk, messagebox
import db_utils as root_database
from datetime import datetime

class AssignmentWindow(tk.Toplevel):
    def __init__(self, parent, db_file, lang, reload_callback):
        tk.Toplevel.__init__(self, parent)
        self.title(lang.get("assignments_title", "Gestion des Affectations"))
        self.geometry("700x400")
        self.db_file = db_file
        self.lang = lang
        self.reload_callback = reload_callback

        self.vehicles = root_database.list_vehicles(self.db_file)
        self.vehicle_dict = {v[1]: v[0] for v in self.vehicles} # Registration : ID

        self.drivers = root_database.list_drivers(self.db_file)
        self.driver_dict = {f"{d[1]} {d[2]}": d[0] for d in self.drivers} # Name Surname : ID

        self.create_widgets()
        self.populate_treeview()

    def create_widgets(self):
        # --- Form Frame ---
        form_frame = ttk.LabelFrame(self, text=self.lang.get("assignment_details", "Détails de l'Affectation"), padding=10)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("vehicle", "Véhicule:")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.vehicle_combo = ttk.Combobox(form_frame, values=list(self.vehicle_dict.keys()))
        self.vehicle_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("driver", "Conducteur:")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.driver_combo = ttk.Combobox(form_frame, values=list(self.driver_dict.keys()))
        self.driver_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("assignment_date", "Date d'affectation (AAAA-MM-JJ):")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(form_frame, text=self.lang.get("button_today", "Aujourd'hui"), command=lambda: self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))).grid(row=2, column=2, padx=5, pady=5, sticky="ew")

        self.assign_button = ttk.Button(form_frame, text=self.lang.get("button_assign", "Affecter"), command=self.assign_vehicle)
        self.assign_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        self.delete_button = ttk.Button(form_frame, text=self.lang.get("button_delete", "Supprimer l'affectation"), command=self.delete_assignment, state=tk.DISABLED)
        self.delete_button.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

        # --- Treeview Frame ---
        tree_frame = ttk.Frame(self, padding=10)
        tree_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(tree_frame, columns=("id", "vehicle_reg", "driver_name", "assignment_date"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("vehicle_reg", text=self.lang.get("vehicle", "Véhicule"))
        self.tree.heading("driver_name", text=self.lang.get("driver", "Conducteur"))
        self.tree.heading("assignment_date", text=self.lang.get("assignment_date_short", "Date"))

        for col in ["id", "vehicle_reg", "driver_name", "assignment_date"]:
            self.tree.column(col, width=150, anchor="center")
            self.tree.heading(col, command=lambda c=col: self.sort_treeview(c, False))

        self.tree.bind('<<TreeviewSelect>>', self.populate_form)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def populate_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        assignments = database.list_assignments(self.db_file)
        for assignment in assignments:
            self.tree.insert("", tk.END, values=assignment)

    def populate_form(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            assignment_id, vehicle_reg, driver_name_parts, assignment_date = self.tree.item(selected_item[0], 'values')
            driver_name = f"{driver_name_parts[0]} {driver_name_parts[1]}"
            self.vehicle_combo.set(vehicle_reg)
            self.driver_combo.set(driver_name)
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, assignment_date)
            self.delete_button.config(state=tk.NORMAL)
            self.selected_id = assignment_id
        else:
            self.delete_button.config(state=tk.DISABLED)
            self.selected_id = None

    def assign_vehicle(self):
        selected_vehicle = self.vehicle_combo.get()
        vehicle_id = self.vehicle_dict.get(selected_vehicle)
        selected_driver = self.driver_combo.get()
        driver_id = self.driver_dict.get(selected_driver)
        assignment_date = self.date_entry.get()

        if not all([selected_vehicle, selected_driver, assignment_date]):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_required_fields", "Veuillez remplir tous les champs."))
            return

        if not vehicle_id or not driver_id:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_selection", "Véhicule ou conducteur invalide."))
            return

        if not self.validate_date(assignment_date):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_date_format", "Format de date invalide (AAAA-MM-JJ)."))
            return

        try:
            root_database.assign_vehicle_to_driver(self.db_file, vehicle_id, driver_id, assignment_date)
            self.populate_treeview()
            self.reload_callback()
            self.clear_form()
            messagebox.showinfo(self.lang.get("success_title", "Succès"), self.lang.get("assignment_added", "Véhicule affecté au conducteur avec succès."))
        except ValueError as e:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), str(e))
        except Exception as e:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_database_operation", "Erreur lors de l'opération sur la base de données:") + str(e))

    def delete_assignment(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_select_assignment_delete", "Veuillez sélectionner une affectation à supprimer."))
            return

        if messagebox.askyesno(self.lang.get("confirm_delete_title", "Confirmer la suppression"), self.lang.get("confirm_delete_assignment", "Êtes-vous sûr de vouloir supprimer cette affectation ?")):
            try:
                root_database.delete_assignment(self.db_file, self.selected_id)
                self.populate_treeview()
                self.reload_callback()
                self.clear_form()
                messagebox.showinfo(self.lang.get("success_title", "Succès"), self.lang.get("assignment_deleted", "Affectation supprimée avec succès."))
                self.delete_button.config(state=tk.DISABLED)
                self.selected_id = None
            except Exception as e:
                messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_database_operation", "Erreur lors de l'opération sur la base de données:") + str(e))

    def clear_form(self):
        self.vehicle_combo.set("")
        self.driver_combo.set("")
        self.date_entry.delete(0, tk.END)
        self.delete_button.config(state=tk.DISABLED)
        self.selected_id = None

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def sort_treeview(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort(key=lambda item: item[0].lower(), reverse=reverse)
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))