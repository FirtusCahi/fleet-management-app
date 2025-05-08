import tkinter as tk
from tkinter import ttk, messagebox
import db_utils as root_database
from utils.validation_utils import validate_date
from datetime import datetime
from utils.excel_utils import import_xls_file, export_xls_file
from utils.print_utils import PrintPreviewDialog
import tkinter.filedialog as filedialog

class ExpensesWindow(tk.Toplevel):
    def __init__(self, parent, db_file, lang, reload_callback):
        tk.Toplevel.__init__(self, parent)
        self.title(lang.get("expenses_title", "Gestion des Dépenses"))
        self.geometry("900x450")
        self.db_file = db_file
        self.lang = lang
        self.reload_callback = reload_callback

        self.vehicles = root_database.list_vehicles(self.db_file)
        self.vehicle_dict = {f"{v[1]} ({v[2]})": v[0] for v in self.vehicles} # Registration (Model) : ID

        self.create_widgets()
        self.populate_treeview()
        self.create_import_export_print_buttons()

    def create_widgets(self):
        # --- Form Frame ---
        form_frame = ttk.LabelFrame(self, text=self.lang.get("expense_details", "Détails de la Dépense"), padding=10)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    def create_import_export_print_buttons(self):
        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        import_btn = ttk.Button(button_frame, text=self.lang.get("button_import_excel", "Importer Excel"), command=self.import_expenses)
        import_btn.pack(side="left", padx=5)

        export_btn = ttk.Button(button_frame, text=self.lang.get("button_export_excel", "Exporter Excel"), command=self.export_expenses)
        export_btn.pack(side="left", padx=5)

        print_btn = ttk.Button(button_frame, text=self.lang.get("button_print", "Imprimer"), command=self.print_expenses)
        print_btn.pack(side="left", padx=5)

        ttk.Label(form_frame, text=self.lang.get("vehicle", "Véhicule:")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.vehicle_combo = ttk.Combobox(form_frame, values=list(self.vehicle_dict.keys()))
        self.vehicle_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("date", "Date (AAAA-MM-JJ):")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(form_frame, text=self.lang.get("button_today", "Aujourd'hui"), command=lambda: self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))).grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("type", "Type:")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.type_entry = ttk.Entry(form_frame)
        self.type_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("amount", "Montant:")).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(form_frame)
        self.amount_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("description", "Description:")).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.description_entry = ttk.Entry(form_frame)
        self.description_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("mileage", "Kilométrage:")).grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.mileage_entry = ttk.Entry(form_frame)
        self.mileage_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("liters", "Litres:")).grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.liters_entry = ttk.Entry(form_frame)
        self.liters_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        self.add_button = ttk.Button(form_frame, text=self.lang.get("button_add", "Ajouter"), command=self.add_expense)
        self.add_button.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")

        self.update_button = ttk.Button(form_frame, text=self.lang.get("button_update", "Modifier"), command=self.update_expense, state=tk.DISABLED)
        self.update_button.grid(row=8, column=0, columnspan=2, pady=5, sticky="ew")

        self.delete_button = ttk.Button(form_frame, text=self.lang.get("button_delete", "Supprimer"), command=self.delete_expense, state=tk.DISABLED)
        self.delete_button.grid(row=9, column=0, columnspan=2, pady=5, sticky="ew")

        # --- Treeview Frame ---
        tree_frame = ttk.Frame(self, padding=10)
        tree_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(tree_frame, columns=("id", "vehicle_reg", "date", "type", "amount", "description", "mileage", "liters"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("vehicle_reg", text=self.lang.get("vehicle", "Véhicule"))
        self.tree.heading("date", text=self.lang.get("date", "Date"))
        self.tree.heading("type", text=self.lang.get("type", "Type"))
        self.tree.heading("amount", text=self.lang.get("amount", "Montant"))
        self.tree.heading("description", text=self.lang.get("description", "Description"))
        self.tree.heading("mileage", text=self.lang.get("mileage", "Kilométrage"))
        self.tree.heading("liters", text=self.lang.get("liters", "Litres"))

        for col in ["id", "vehicle_reg", "date", "type", "amount", "description", "mileage", "liters"]:
            self.tree.column(col, width=100, anchor="center")
            self.tree.heading(col, command=lambda c=col: self.sort_treeview(c, False))

        self.tree.bind('<<TreeviewSelect>>', self.populate_form)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def populate_treeview(self, vehicle_id=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        expenses = root_database.list_expenses(self.db_file, vehicle_id)
        for expense in expenses:
            vehicle = root_database.get_vehicle(self.db_file, expense[1])
            vehicle_reg = vehicle[1] if vehicle else self.lang.get("unknown", "Inconnu")
            self.tree.insert("", tk.END, values=(expense[0], vehicle_reg, expense[2], expense[3], expense[4], expense[5], expense[6], expense[7]))

    def import_expenses(self):
        workbook, error = import_xls_file()
        if error:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), error)
            return
        try:
            sheet = workbook.sheet_by_index(0)
            for row_idx in range(1, sheet.nrows):
                row = sheet.row_values(row_idx)
                # Assuming columns: vehicle_reg, date, type, amount, description, mileage, liters
                vehicle_reg = row[0]
                vehicle_id = None
                for key, val in self.vehicle_dict.items():
                    if vehicle_reg == key:
                        vehicle_id = val
                        break
                if vehicle_id is None:
                    continue  # skip unknown vehicle
                date = row[1]
                type = row[2]
                amount = float(row[3]) if row[3] else 0.0
                description = row[4]
                mileage = int(row[5]) if row[5] else None
                liters = float(row[6]) if row[6] else None
                root_database.add_expense(self.db_file, vehicle_id, date, type, amount, description, mileage, liters)
            self.populate_treeview()
            self.reload_callback()
            messagebox.showinfo(self.lang.get("success_title", "Succès"), self.lang.get("import_success", "Importation réussie."))
        except Exception as e:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_import_failed", "Échec de l'importation: ") + str(e))

    def export_expenses(self):
        try:
            data = []
            headers = ["ID", "Véhicule", "Date", "Type", "Montant", "Description", "Kilométrage", "Litres"]
            for item in self.tree.get_children():
                values = self.tree.item(item, "values")
                data.append(values)
            error = export_xls_file(data, headers)
            if error:
                messagebox.showerror(self.lang.get("error_title", "Erreur"), error)
            else:
                messagebox.showinfo(self.lang.get("success_title", "Succès"), self.lang.get("export_success", "Exportation réussie."))
        except Exception as e:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_export_failed", "Échec de l'exportation: ") + str(e))

    def print_expenses(self):
        try:
            data = []
            headers = ["ID", "Véhicule", "Date", "Type", "Montant", "Description", "Kilométrage", "Litres"]
            for item in self.tree.get_children():
                values = self.tree.item(item, "values")
                data.append(values)
            preview = PrintPreviewDialog(self, data, headers, title=self.lang.get("print_preview_title", "Aperçu avant impression"))
            preview.grab_set()
        except Exception as e:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_print_failed", "Échec de l'impression: ") + str(e))

    def populate_form(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            expense_id, vehicle_reg, date, type, amount, description, mileage, liters = self.tree.item(selected_item[0], 'values')
            vehicle_id = self.vehicle_dict.get(vehicle_reg)
            if vehicle_id is not None:
                for key, val in self.vehicle_dict.items():
                    if val == vehicle_id:
                        self.vehicle_combo.set(key)
                        break
            else:
                self.vehicle_combo.set("")
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, date)
            self.type_entry.delete(0, tk.END)
            self.type_entry.insert(0, type)
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, amount)
            self.description_entry.delete(0, tk.END)
            self.description_entry.insert(0, description)
            self.mileage_entry.delete(0, tk.END)
            self.mileage_entry.insert(0, mileage)
            self.liters_entry.delete(0, tk.END)
            self.liters_entry.insert(0, liters)
            self.update_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
            self.selected_id = int(expense_id)
        else:
            self.update_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
            self.selected_id = None

    def add_expense(self):
        selected_vehicle = self.vehicle_combo.get()
        vehicle_id = self.vehicle_dict.get(selected_vehicle)
        date = self.date_entry.get()
        type = self.type_entry.get()
        amount_str = self.amount_entry.get()
        description = self.description_entry.get()
        mileage_str = self.mileage_entry.get()
        liters_str = self.liters_entry.get()

        if not all([selected_vehicle, date, type, amount_str]):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_required_fields", "Veuillez remplir tous les champs obligatoires."))
            return

        if not validate_date(date):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_date_format", "Format de date invalide (AAAA-MM-JJ)."))
            return

        try:
            amount = float(amount_str) if amount_str else 0.0
            mileage = int(mileage_str) if mileage_str else None
            liters = float(liters_str) if liters_str else None

            root_database.add_expense(self.db_file, vehicle_id, date, type, amount, description, mileage, liters)
            self.populate_treeview()
            self.reload_callback()
            self.clear_form()
            messagebox.showinfo(self.lang.get("success_title", "Succès"), self.lang.get("expense_added", "Dépense ajoutée avec succès."))
        except ValueError:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_number", "Montant, kilométrage ou litres invalides."))
        except Exception as e:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_database_operation", "Erreur lors de l'opération sur la base de données:") + str(e))

    def update_expense(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_select_expense_update", "Veuillez sélectionner une dépense à modifier."))
            return

        selected_vehicle = self.vehicle_combo.get()
        vehicle_id = self.vehicle_dict.get(selected_vehicle)
        date = self.date_entry.get()
        type = self.type_entry.get()
        amount_str = self.amount_entry.get()
        description = self.description_entry.get()
        mileage_str = self.mileage_entry.get()
        liters_str = self.liters_entry.get()

        if not all([selected_vehicle, date, type, amount_str]):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_required_fields", "Veuillez remplir tous les champs obligatoires."))
            return

        if not validate_date(date):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_date_format", "Format de date invalide (AAAA-MM-JJ)."))
            return

        try:
            amount = float(amount_str) if amount_str else 0.0
            mileage = int(mileage_str) if mileage_str else None
            liters = float(liters_str) if liters_str else None

            root_database.update_expense(self.db_file, self.selected_id, vehicle_id, date, type, amount, description, mileage, liters)
            self.populate_treeview()
            self.reload_callback()
            self.clear_form()
            messagebox.showinfo(self.lang.get("success_title", "Succès"), self.lang.get("expense_updated", "Dépense mise à jour avec succès."))
            self.update_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
            self.selected_id = None
        except ValueError:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_number", "Montant, kilométrage ou litres invalides."))
        except Exception as e:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_database_operation", "Erreur lors de l'opération sur la base de données:") + str(e))

    def delete_expense(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_select_expense_delete", "Veuillez sélectionner une dépense à supprimer."))
            return

        if messagebox.askyesno(self.lang.get("confirm_delete_title", "Confirmer la suppression"), self.lang.get("confirm_delete_expense", "Êtes-vous sûr de vouloir supprimer cette dépense ?")):
            try:
                root_database.delete_expense(self.db_file, self.selected_id)
                self.populate_treeview()
                self.reload_callback()
                self.clear_form()
                messagebox.showinfo(self.lang.get("success_title", "Succès"), self.lang.get("expense_deleted", "Dépense supprimée avec succès."))
                self.update_button.config(state=tk.DISABLED)
                self.delete_button.config(state=tk.DISABLED)
                self.selected_id = None
            except Exception as e:
                messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_database_operation", "Erreur lors de l'opération sur la base de données:") + str(e))

    def clear_form(self):
        self.vehicle_combo.set("")
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.mileage_entry.delete(0, tk.END)
        self.liters_entry.delete(0, tk.END)
        self.update_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)
        self.selected_id = None

    def sort_treeview(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        try:
            if col == "amount" or col == "mileage" or col == "liters":
                data.sort(key=lambda item: float(item[0]) if item[0] else float('-inf'), reverse=reverse)
            else:
                data.sort(key=lambda item: item[0].lower(), reverse=reverse)
        except ValueError:
            data.sort(key=lambda item: item[0].lower(), reverse=reverse)
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))