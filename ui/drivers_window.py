import tkinter as tk
from tkinter import ttk, messagebox
import db_utils as root_database
from utils.validation_utils import validate_date
from datetime import datetime
from utils.excel_utils import import_xls_file, export_xls_file
from utils.print_utils import PrintPreviewDialog
import tkinter.filedialog as filedialog

class DriversWindow(tk.Toplevel):
    def __init__(self, parent, db_file, lang, reload_callback):
        tk.Toplevel.__init__(self, parent)
        self.title(lang.get("drivers_title", "Gestion des Conducteurs"))
        self.geometry("800x400")
        self.db_file = db_file
        self.lang = lang
        self.reload_callback = reload_callback

        self.create_widgets()
        self.populate_treeview()
        self.create_import_export_print_buttons()

    def create_widgets(self):
        # --- Form Frame ---
        form_frame = ttk.LabelFrame(self, text=self.lang.get("driver_details", "Détails du Conducteur"), padding=10)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("name", "Nom:")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("surname", "Prénom:")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.surname_entry = ttk.Entry(form_frame)
        self.surname_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("license_number", "Numéro de permis:")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.license_entry = ttk.Entry(form_frame)
        self.license_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("expiry_date", "Date d'expiration (AAAA-MM-JJ):")).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.expiry_entry = ttk.Entry(form_frame)
        self.expiry_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(form_frame, text=self.lang.get("button_today", "Aujourd'hui"), command=lambda: self.expiry_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))).grid(row=3, column=2, padx=5, pady=5, sticky="ew")

    def create_import_export_print_buttons(self):
        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        import_btn = ttk.Button(button_frame, text=self.lang.get("button_import_excel", "Importer Excel"), command=self.import_drivers)
        import_btn.pack(side="left", padx=5)

        export_btn = ttk.Button(button_frame, text=self.lang.get("button_export_excel", "Exporter Excel"), command=self.export_drivers)
        export_btn.pack(side="left", padx=5)

        print_btn = ttk.Button(button_frame, text=self.lang.get("button_print", "Imprimer"), command=self.print_drivers)
        print_btn.pack(side="left", padx=5)

        ttk.Label(form_frame, text=self.lang.get("name", "Nom:")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("surname", "Prénom:")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.surname_entry = ttk.Entry(form_frame)
        self.surname_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("license_number", "Numéro de permis:")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.license_entry = ttk.Entry(form_frame)
        self.license_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("expiry_date", "Date d'expiration (AAAA-MM-JJ):")).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.expiry_entry = ttk.Entry(form_frame)
        self.expiry_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(form_frame, text=self.lang.get("button_today", "Aujourd'hui"), command=lambda: self.expiry_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))).grid(row=3, column=2, padx=5, pady=5, sticky="ew")

        self.add_button = ttk.Button(form_frame, text=self.lang.get("button_add", "Ajouter"), command=self.add_driver)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        self.update_button = ttk.Button(form_frame, text=self.lang.get("button_update", "Modifier"), command=self.update_driver, state=tk.DISABLED)
        self.update_button.grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")

        self.delete_button = ttk.Button(form_frame, text=self.lang.get("button_delete", "Supprimer"), command=self.delete_driver, state=tk.DISABLED)
        self.delete_button.grid(row=6, column=0, columnspan=2, pady=5, sticky="ew")

        # --- Treeview Frame ---
        tree_frame = ttk.Frame(self, padding=10)
        tree_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(tree_frame, columns=("id", "name", "surname", "license_number", "expiry_date"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text=self.lang.get("name", "Nom"))
        self.tree.heading("surname", text=self.lang.get("surname", "Prénom"))
        self.tree.heading("license_number", text=self.lang.get("license_number", "Numéro de permis"))
        self.tree.heading("expiry_date", text=self.lang.get("expiry_date_short", "Expiration"))

        for col in ["id", "name", "surname", "license_number", "expiry_date"]:
            self.tree.column(col, width=150, anchor="center")
            self.tree.heading(col, command=lambda c=col: self.sort_treeview(c, False))

        self.tree.bind('<<TreeviewSelect>>', self.populate_form)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        search_frame = ttk.LabelFrame(self, text=self.lang.get("search", "Rechercher"), padding=5)
        search_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(search_frame, text=self.lang.get("button_search", "Rechercher"), command=self.search_drivers).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def populate_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        drivers = root_database.list_drivers(self.db_file)
        for driver in drivers:
            self.tree.insert("", tk.END, values=driver)

    def import_drivers(self):
        workbook, error = import_xls_file()
        if error:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), error)
            return
        try:
            sheet = workbook.sheet_by_index(0)
            for row_idx in range(1, sheet.nrows):
                row = sheet.row_values(row_idx)
                # Assuming columns: first_name, last_name, license_number, phone, email
                first_name = row[0]
                last_name = row[1]
                license_number = row[2]
                phone = row[3]
                email = row[4]
                root_database.add_driver(self.db_file, first_name, last_name, license_number, phone, email)
            self.populate_treeview()
            self.reload_callback()
            messagebox.showinfo(self.lang.get("success_title", "Succès"), self.lang.get("import_success", "Importation réussie."))
        except Exception as e:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_import_failed", "Échec de l'importation: ") + str(e))

    def export_drivers(self):
        try:
            data = []
            headers = ["ID", "Prénom", "Nom", "Numéro de permis", "Téléphone", "Email"]
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

    def print_drivers(self):
        try:
            data = []
            headers = ["ID", "Prénom", "Nom", "Numéro de permis", "Téléphone", "Email"]
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
            driver_id, name, surname, license_number, expiry_date = self.tree.item(selected_item[0], 'values')
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, name)
            self.surname_entry.delete(0, tk.END)
            self.surname_entry.insert(0, surname)
            self.license_entry.delete(0, tk.END)
            self.license_entry.insert(0, license_number)
            self.expiry_entry.delete(0, tk.END)
            self.expiry_entry.insert(0, expiry_date)
            self.update_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
            self.selected_id = driver_id
        else:
            self.update_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
            self.selected_id = None

    def add_driver(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        license_number = self.license_entry.get()
        expiry_date = self.expiry_entry.get()

        if not all([name, surname, license_number, expiry_date]):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_required_fields", "Veuillez remplir tous les champs obligatoires."))
            return

        if not validate_date(expiry_date):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_date_format", "Format de date d'expiration invalide (AAAA-MM-JJ)."))
            return

        try:
            root_database.add_driver(self.db_file, name, surname, license_number, expiry_date)
            self.populate_treeview()
            self.reload_callback()
            self.clear_form()
            messagebox.showinfo(self.lang.get("success_title", "Succès"), self.lang.get("driver_added", "Conducteur ajouté avec succès."))
        except ValueError as e:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), str(e))
        except Exception as e:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_database_operation", "Erreur lors de l'opération sur la base de données:") + str(e))

    def update_driver(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_select_driver_update", "Veuillez sélectionner un conducteur à modifier."))
            return

        name = self.name_entry.get()
        surname = self.surname_entry.get()
        license_number = self.license_entry.get()
        expiry_date = self.expiry_entry.get()

        if not all([name, surname, license_number, expiry_date]):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_required_fields", "Veuillez remplir tous les champs obligatoires."))
            return

        if not validate_date(expiry_date):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_date_format", "Format de date d'expiration invalide (AAAA-MM-JJ)."))
            return

        try:
            root_database.update_driver(self.db_file, self.selected_id, name, surname, license_number, expiry_date)
            self.populate_treeview()
            self.reload_callback()
            self.clear_form()
            messagebox.showinfo(self.lang.get("success_title", "Succès"), self.lang.get("driver_updated", "Conducteur mis à jour avec succès."))
            self.update_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
            self.selected_id = None
        except ValueError as e:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), str(e))
        except Exception as e:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_database_operation", "Erreur lors de l'opération sur la base de données:") + str(e))

    def delete_driver(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_select_driver_delete", "Veuillez sélectionner un conducteur à supprimer."))
            return

        if messagebox.askyesno(self.lang.get("confirm_delete_title", "Confirmer la suppression"), self.lang.get("confirm_delete_driver", "Êtes-vous sûr de vouloir supprimer ce conducteur ?")):
            try:
                root_database.delete_driver(self.db_file, self.selected_id)
                self.populate_treeview()
                self.reload_callback()
                self.clear_form()
                messagebox.showinfo(self.lang.get("success_title", "Succès"), self.lang.get("driver_deleted", "Conducteur supprimé avec succès."))
                self.update_button.config(state=tk.DISABLED)
                self.delete_button.config(state=tk.DISABLED)
                self.selected_id = None
            except Exception as e:
                messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_database_operation", "Erreur lors de l'opération sur la base de données:") + str(e))

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.license_entry.delete(0, tk.END)
        self.expiry_entry.delete(0, tk.END)
        self.update_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)
        self.selected_id = None

    def search_drivers(self):
        query = self.search_entry.get()
        if query:
            for item in self.tree.get_children():
                self.tree.delete(item)
            drivers = root_database.search_drivers(self.db_file, query)
            for driver in drivers:
                self.tree.insert("", tk.END, values=driver)
        else:
            self.populate_treeview()

    def sort_treeview(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort(key=lambda item: item[0].lower(), reverse=reverse)
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))