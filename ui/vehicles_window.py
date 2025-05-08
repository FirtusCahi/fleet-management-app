import tkinter as tk
from tkinter import ttk, messagebox
import db_utils as root_database
from utils.validation_utils import validate_date
from datetime import datetime

class VehiclesWindow(tk.Toplevel):
    def __init__(self, parent, db_file, lang, reload_callback):
        tk.Toplevel.__init__(self, parent)
        self.title(lang.get("vehicles_title", "Gestion des Véhicules"))
        self.geometry("900x450")
        self.db_file = db_file
        self.lang = lang
        self.reload_callback = reload_callback

        self.create_widgets()
        self.populate_treeview()

    def create_widgets(self):
        # --- Form Frame ---
        form_frame = ttk.LabelFrame(self, text=self.lang.get("vehicle_details", "Détails du Véhicule"), padding=10)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("registration", "Immatriculation:")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.reg_entry = ttk.Entry(form_frame)
        self.reg_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("make", "Marque:")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.make_entry = ttk.Entry(form_frame)
        self.make_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("model", "Modèle:")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.model_entry = ttk.Entry(form_frame)
        self.model_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("year", "Année:")).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.year_entry = ttk.Entry(form_frame)
        self.year_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("revision_date", "Date de révision (AAAA-MM-JJ):")).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.revision_entry = ttk.Entry(form_frame)
        self.revision_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(form_frame, text=self.lang.get("button_today", "Aujourd'hui"), command=lambda: self.revision_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))).grid(row=4, column=2, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("control_date", "Date du contrôle (AAAA-MM-JJ):")).grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.control_entry = ttk.Entry(form_frame)
        self.control_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(form_frame, text=self.lang.get("button_today", "Aujourd'hui"), command=lambda: self.control_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))).grid(row=5, column=2, padx=5, pady=5, sticky="ew")

        self.add_button = ttk.Button(form_frame, text=self.lang.get("button_add", "Ajouter"), command=self.add_vehicle)
        self.add_button.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

        self.delete_button = ttk.Button(form_frame, text=self.lang.get("button_delete", "Supprimer"), command=self.delete_vehicle, state=tk.DISABLED)
        self.delete_button.grid(row=7, column=0, columnspan=2, pady=5, sticky="ew")

        self.update_button = ttk.Button(form_frame, text=self.lang.get("button_update", "Modifier"), command=self.update_vehicle, state=tk.DISABLED)
        self.update_button.grid(row=8, column=0, columnspan=2, pady=5, sticky="ew")

        # --- Treeview Frame ---
        tree_frame = ttk.Frame(self, padding=10)
        tree_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(tree_frame, columns=("id", "registration", "make", "model", "year", "revision_date", "control_date"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("registration", text=self.lang.get("registration", "Immatriculation"))
        self.tree.heading("make", text=self.lang.get("make", "Marque"))
        self.tree.heading("model", text=self.lang.get("model", "Modèle"))
        self.tree.heading("year", text=self.lang.get("year", "Année"))
        self.tree.heading("revision_date", text=self.lang.get("revision_date_short", "Révision"))
        self.tree.heading("control_date", text=self.lang.get("control_date_short", "Contrôle"))

        for col in ["id", "registration", "make", "model", "year", "revision_date", "control_date"]:
            self.tree.column(col, width=100, anchor="center")
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
        ttk.Button(search_frame, text=self.lang.get("button_search", "Rechercher"), command=self.search_vehicles).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def populate_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        vehicles = root_database.list_vehicles(self.db_file)
        for vehicle in vehicles:
            self.tree.insert("", tk.END, values=vehicle)

    def populate_form(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            vehicle_id, registration, make, model, year, revision_date, control_date = self.tree.item(selected_item[0], 'values')
            self.reg_entry.delete(0, tk.END)
            self.reg_entry.insert(0, registration)
            self.make_entry.delete(0, tk.END)
            self.make_entry.insert(0, make)
            self.model_entry.delete(0, tk.END)
            self.model_entry.insert(0, model)
            self.year_entry.delete(0, tk.END)
            self.year_entry.insert(0, year)
            self.revision_entry.delete(0, tk.END)
            self.revision_entry.insert(0, revision_date)
            self.control_entry.delete(0, tk.END)
            self.control_entry.insert(0, control_date)
            self.update_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
            self.selected_id = vehicle_id
        else:
            self.update_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
            self.selected_id = None

    def add_vehicle(self):
        registration = self.reg_entry.get()
        make = self.make_entry.get()
        model = self.model_entry.get()
        year_str = self.year_entry.get()
        revision_date = self.revision_entry.get()
        control_date = self.control_entry.get()

        if not all([registration, make, model]):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_required_fields", "Veuillez remplir tous les champs obligatoires."))
            return

        if year_str and not year_str.isdigit():
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_year", "L'année doit être un nombre."))
            return

        if revision_date and not validate_date(revision_date):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_date_format", "Format de date de révision invalide (AAAA-MM-JJ)."))
            return

        if control_date and not validate_date(control_date):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_date_format", "Format de date de contrôle technique invalide (AAAA-MM-JJ)."))
            return

        try:
            root_database.add_vehicle(self.db_file, registration, make, model, year_str if year_str else None, revision_date if revision_date else None, control_date if control_date else None)
            self.populate_treeview()
            self.reload_callback()
            self.clear_form()
            messagebox.showinfo(self.lang.get("success_title", "Succès"), self.lang.get("vehicle_added", "Véhicule ajouté avec succès."))
        except ValueError as e:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), str(e))
        except Exception as e:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_database_operation", "Erreur lors de l'opération sur la base de données:") + str(e))

    def update_vehicle(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_select_vehicle_update", "Veuillez sélectionner un véhicule à modifier."))
            return

        registration = self.reg_entry.get()
        make = self.make_entry.get()
        model = self.model_entry.get()
        year_str = self.year_entry.get()
        revision_date = self.revision_entry.get()
        control_date = self.control_entry.get()

        if not all([registration, make, model]):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_required_fields", "Veuillez remplir tous les champs obligatoires."))
            return

        if year_str and not year_str.isdigit():
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_year", "L'année doit être un nombre."))
            return

        if revision_date and not validate_date(revision_date):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_date_format", "Format de date de révision invalide (AAAA-MM-JJ)."))
            return

        if control_date and not validate_date(control_date):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_date_format", "Format de date de contrôle technique invalide (AAAA-MM-JJ)."))
            return

        try:
            root_database.update_vehicle(self.db_file, self.selected_id, registration, make, model, year_str if year_str else None, revision_date if revision_date else None, control_date if control_date else None)
            self.populate_treeview()
            self.reload_callback()
            self.clear_form()
            messagebox.showinfo(self.lang.get("success_title", "Succès"), self.lang.get("vehicle_updated", "Véhicule mis à jour avec succès."))
            self.update_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
            self.selected_id = None
        except ValueError as e:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), str(e))
        except Exception as e:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_database_operation", "Erreur lors de l'opération sur la base de données:") + str(e))

    def delete_vehicle(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_select_vehicle_delete", "Veuillez sélectionner un véhicule à supprimer."))
            return

        if messagebox.askyesno(self.lang.get("confirm_delete_title", "Confirmer la suppression"), self.lang.get("confirm_delete_vehicle", "Êtes-vous sûr de vouloir supprimer ce véhicule ?")):
            try:
                root_database.delete_vehicle(self.db_file, self.selected_id)
                self.populate_treeview()
                self.reload_callback()
                self.clear_form()
                messagebox.showinfo(self.lang.get("success_title", "Succès"), self.lang.get("vehicle_deleted", "Véhicule supprimé avec succès."))
                self.update_button.config(state=tk.DISABLED)
                self.delete_button.config(state=tk.DISABLED)
                self.selected_id = None
            except Exception as e:
                messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_database_operation", "Erreur lors de l'opération sur la base de données:") + str(e))

    def clear_form(self):
        self.reg_entry.delete(0, tk.END)
        self.make_entry.delete(0, tk.END)
        self.model_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.revision_entry.delete(0, tk.END)
        self.control_entry.delete(0, tk.END)
        self.update_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)
        self.selected_id = None

    def search_vehicles(self):
        query = self.search_entry.get()
        if query:
            for item in self.tree.get_children():
                self.tree.delete(item)
            vehicles = database.search_vehicles(self.db_file, query)
            for vehicle in vehicles:
                self.tree.insert("", tk.END, values=vehicle)
        else:
            self.populate_treeview()

    def sort_treeview(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        try:
            # Try to sort as numbers if possible
            data.sort(key=lambda item: float(item[0]), reverse=reverse)
        except ValueError:
            # Otherwise sort as strings
            data.sort(key=lambda item: item[0], reverse=reverse)
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))