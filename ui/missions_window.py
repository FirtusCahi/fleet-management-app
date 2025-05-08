import tkinter as tk
from tkinter import ttk, messagebox
import db_utils as root_database
from utils.validation_utils import validate_date
from utils.date_utils import calculate_weekends
from datetime import datetime, timedelta

class MissionsWindow(tk.Toplevel):
    def __init__(self, parent, db_file, lang, reload_callback):
        tk.Toplevel.__init__(self, parent)
        self.title(lang.get("missions_title", "Gestion des Missions"))
        self.geometry("900x450")
        self.db_file = db_file
        self.lang = lang
        self.reload_callback = reload_callback

        self.drivers = root_database.list_drivers(self.db_file)
        self.driver_dict = {f"{d[1]} {d[2]}": d[0] for d in self.drivers} # Name Surname : ID

        self.create_widgets()
        self.populate_treeview()
        self.create_import_export_print_buttons()

    def create_widgets(self):
        # --- Form Frame ---
        form_frame = ttk.LabelFrame(self, text=self.lang.get("mission_details", "Détails de la Mission"), padding=10)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    def create_import_export_print_buttons(self):
        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        import_btn = ttk.Button(button_frame, text=self.lang.get("button_import_excel", "Importer Excel"), command=self.import_missions)
        import_btn.pack(side="left", padx=5)

        export_btn = ttk.Button(button_frame, text=self.lang.get("button_export_excel", "Exporter Excel"), command=self.export_missions)
        export_btn.pack(side="left", padx=5)

        print_btn = ttk.Button(button_frame, text=self.lang.get("button_print", "Imprimer"), command=self.print_missions)
        print_btn.pack(side="left", padx=5)

        ttk.Label(form_frame, text=self.lang.get("driver", "Conducteur:")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.driver_combo = ttk.Combobox(form_frame, values=list(self.driver_dict.keys()))
        self.driver_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("start_date", "Date de début (AAAA-MM-JJ):")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.start_date_entry = ttk.Entry(form_frame)
        self.start_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(form_frame, text=self.lang.get("button_today", "Aujourd'hui"), command=lambda: self.start_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))).grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("end_date", "Date de fin (AAAA-MM-JJ):")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.end_date_entry = ttk.Entry(form_frame)
        self.end_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(form_frame, text=self.lang.get("button_today", "Aujourd'hui"), command=lambda: self.end_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))).grid(row=2, column=2, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("destination", "Destination:")).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.destination_entry = ttk.Entry(form_frame)
        self.destination_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("duration", "Durée (jours):")).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.duration_entry = ttk.Entry(form_frame)
        self.duration_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("meals", "Nombre de repas:")).grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.meals_entry = ttk.Entry(form_frame)
        self.meals_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("nights", "Nombre de nuitées:")).grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.nights_entry = ttk.Entry(form_frame)
        self.nights_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("weekends", "Nombre de week-ends:")).grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.weekends_entry = ttk.Entry(form_frame, state='readonly')
        self.weekends_entry.grid(row=7, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(form_frame, text=self.lang.get("button_calculate", "Calculer"), command=self.calculate_weekends).grid(row=7, column=2, padx=5, pady=5, sticky="ew")

    def create_import_export_print_buttons(self):
        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        import_btn = ttk.Button(button_frame, text=self.lang.get("button_import_excel", "Importer Excel"), command=self.import_missions)
        import_btn.pack(side="left", padx=5)

        export_btn = ttk.Button(button_frame, text=self.lang.get("button_export_excel", "Exporter Excel"), command=self.export_missions)
        export_btn.pack(side="left", padx=5)

        print_btn = ttk.Button(button_frame, text=self.lang.get("button_print", "Imprimer"), command=self.print_missions)
        print_btn.pack(side="left", padx=5)

        ttk.Label(form_frame, text=self.lang.get("driver", "Conducteur:")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.driver_combo = ttk.Combobox(form_frame, values=list(self.driver_dict.keys()))
        self.driver_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("start_date", "Date de début (AAAA-MM-JJ):")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.start_date_entry = ttk.Entry(form_frame)
        self.start_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(form_frame, text=self.lang.get("button_today", "Aujourd'hui"), command=lambda: self.start_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))).grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("end_date", "Date de fin (AAAA-MM-JJ):")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.end_date_entry = ttk.Entry(form_frame)
        self.end_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(form_frame, text=self.lang.get("button_today", "Aujourd'hui"), command=lambda: self.end_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))).grid(row=2, column=2, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("destination", "Destination:")).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.destination_entry = ttk.Entry(form_frame)
        self.destination_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("duration", "Durée (jours):")).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.duration_entry = ttk.Entry(form_frame)
        self.duration_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("meals", "Nombre de repas:")).grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.meals_entry = ttk.Entry(form_frame)
        self.meals_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("nights", "Nombre de nuitées:")).grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.nights_entry = ttk.Entry(form_frame)
        self.nights_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text=self.lang.get("weekends", "Nombre de week-ends:")).grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.weekends_entry = ttk.Entry(form_frame, state='readonly')
        self.weekends_entry.grid(row=7, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(form_frame, text=self.lang.get("button_calculate", "Calculer"), command=self.calculate_weekends).grid(row=7, column=2, padx=5, pady=5, sticky="ew")

        self.add_button = ttk.Button(form_frame, text=self.lang.get("button_add", "Ajouter"), command=self.add_mission)
        self.add_button.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")

        self.update_button = ttk.Button(form_frame, text=self.lang.get("button_update", "Modifier"), command=self.update_mission, state=tk.DISABLED)
        self.update_button.grid(row=9, column=0, columnspan=2, pady=5, sticky="ew")

        self.delete_button = ttk.Button(form_frame, text=self.lang.get("button_delete", "Supprimer"), command=self.delete_mission, state=tk.DISABLED)
        self.delete_button.grid(row=10, column=0, columnspan=2, pady=5, sticky="ew")

        # --- Treeview Frame ---
        tree_frame = ttk.Frame(self, padding=10)
        tree_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(tree_frame, columns=("id", "driver_name", "start_date", "end_date", "destination", "duration", "meals", "nights", "weekends"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("driver_name", text=self.lang.get("driver", "Conducteur"))
        self.tree.heading("start_date", text=self.lang.get("start_date_short", "Début"))
        self.tree.heading("end_date", text=self.lang.get("end_date_short", "Fin"))
        self.tree.heading("destination", text=self.lang.get("destination", "Destination"))
        self.tree.heading("duration", text=self.lang.get("duration_short", "Durée"))
        self.tree.heading("meals", text=self.lang.get("meals_short", "Repas"))
        self.tree.heading("nights", text=self.lang.get("nights_short", "Nuits"))
        self.tree.heading("weekends", text=self.lang.get("weekends_short", "WE"))

        for col in ["id", "driver_name", "start_date", "end_date", "destination", "duration", "meals", "nights", "weekends"]:
            self.tree.column(col, width=100, anchor="center")
            self.tree.heading(col, command=lambda c=col: self.sort_treeview(c, False))

        self.tree.bind('<<TreeviewSelect>>', self.populate_form)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def populate_treeview(self, driver_id=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        missions = root_database.list_missions(self.db_file, driver_id)
        for mission in missions:
            driver = root_database.get_driver(self.db_file, mission[1])
            driver_name = f"{driver[1]} {driver[2]}" if driver else self.lang.get("unknown", "Inconnu")
            self.tree.insert("", tk.END, values=(mission[0], driver_name, mission[2], mission[3], mission[4], mission[5], mission[6], mission[7], mission[8]))

    def populate_form(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            mission_id, driver_name, start_date, end_date, destination, duration, meals, nights, weekends = self.tree.item(selected_item[0], 'values')
            driver_id = self.driver_dict.get(driver_name)
            if driver_id is not None:
                for key, val in self.driver_dict.items():
                    if val == driver_id:
                        self.driver_combo.set(key)
                        break
            else:
                self.driver_combo.set("")
            self.start_date_entry.delete(0, tk.END)
            self.start_date_entry.insert(0, start_date)
            self.end_date_entry.delete(0, tk.END)
            self.end_date_entry.insert(0, end_date)
            self.destination_entry.delete(0, tk.END)
            self.destination_entry.insert(0, destination)
            self.duration_entry.delete(0, tk.END)
            self.duration_entry.insert(0, duration)
            self.meals_entry.delete(0, tk.END)
            self.meals_entry.insert(0, meals)
            self.nights_entry.delete(0, tk.END)
            self.nights_entry.insert(0, nights)
            self.weekends_entry.delete(0, tk.END)
            self.weekends_entry.insert(0, weekends)
            self.update_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
            self.selected_id = int(mission_id)
        else:
            self.update_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
            self.selected_id = None

    def add_mission(self):
        selected_driver = self.driver_combo.get()
        driver_id = self.driver_dict.get(selected_driver)
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        destination = self.destination_entry.get()
        duration_str = self.duration_entry.get()
        meals_str = self.meals_entry.get()
        nights_str = self.nights_entry.get()
        weekends_str = self.weekends_entry.get()

        if not all([selected_driver, start_date, end_date, destination]):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_required_fields", "Veuillez remplir les champs obligatoires."))
            return

        if not validate_date(start_date) or not validate_date(end_date):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_date_format", "Format de date invalide (AAAA-MM-JJ)."))
            return

        try:
            duration = int(duration_str) if duration_str else None
            meals = int(meals_str) if meals_str else None
            nights = int(nights_str) if nights_str else None
            weekends = int(weekends_str) if weekends_str else 0

            root_database.add_mission(self.db_file, driver_id, start_date, end_date, destination, duration, meals, nights, weekends)
            self.populate_treeview()
            self.reload_callback()
            self.clear_form()
            messagebox.showinfo(self.lang.get("success_title", "Succès"), self.lang.get("mission_added", "Mission ajoutée avec succès."))
        except ValueError:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_number", "Durée, nombre de repas ou nombre de nuitées invalides."))
        except Exception as e:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_database_operation", "Erreur lors de l'opération sur la base de données:") + str(e))

    def update_mission(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_select_mission_update", "Veuillez sélectionner une mission à modifier."))
            return

        selected_driver = self.driver_combo.get()
        driver_id = self.driver_dict.get(selected_driver)
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        destination = self.destination_entry.get()
        duration_str = self.duration_entry.get()
        meals_str = self.meals_entry.get()
        nights_str = self.nights_entry.get()
        weekends_str = self.weekends_entry.get()

        if not all([selected_driver, start_date, end_date, destination]):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_required_fields", "Veuillez remplir les champs obligatoires."))
            return

        if not validate_date(start_date) or not validate_date(end_date):
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_date_format", "Format de date invalide (AAAA-MM-JJ)."))
            return

        try:
            duration = int(duration_str) if duration_str else None
            meals = int(meals_str) if meals_str else None
            nights = int(nights_str) if nights_str else None
            weekends = int(weekends_str) if weekends_str else 0

            root_database.update_mission(self.db_file, self.selected_id, driver_id, start_date, end_date, destination, duration, meals, nights, weekends)
            self.populate_treeview()
            self.reload_callback()
            self.clear_form()
            messagebox.showinfo(self.lang.get("success_title", "Succès"), self.lang.get("mission_updated", "Mission mise à jour avec succès."))
            self.update_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
            self.selected_id = None
        except ValueError:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_number", "Durée, nombre de repas ou nombre de nuitées invalides."))
        except Exception as e:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_database_operation", "Erreur lors de l'opération sur la base de données:") + str(e))

    def delete_mission(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_select_mission_delete", "Veuillez sélectionner une mission à supprimer."))
            return

        if messagebox.askyesno(self.lang.get("confirm_delete_title", "Confirmer la suppression"), self.lang.get("confirm_delete_mission", "Êtes-vous sûr de vouloir supprimer cette mission ?")):
            try:
                root_database.delete_mission(self.db_file, self.selected_id)
                self.populate_treeview()
                self.reload_callback()
                self.clear_form()
                messagebox.showinfo(self.lang.get("success_title", "Succès"), self.lang.get("mission_deleted", "Mission supprimée avec succès."))
                self.update_button.config(state=tk.DISABLED)
                self.delete_button.config(state=tk.DISABLED)
                self.selected_id = None
            except Exception as e:
                messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_database_operation", "Erreur lors de l'opération sur la base de données:") + str(e))

    def clear_form(self):
        self.driver_combo.set("")
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.destination_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.meals_entry.delete(0, tk.END)
        self.nights_entry.delete(0, tk.END)
        self.weekends_entry.delete(0, tk.END)
        self.update_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)
        self.selected_id = None

    def calculate_weekends(self):
        start_date_str = self.start_date_entry.get()
        end_date_str = self.end_date_entry.get()
        if validate_date(start_date_str) and validate_date(end_date_str):
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            weekends = calculate_weekends(start_date, end_date)
            self.weekends_entry.delete(0, tk.END)
            self.weekends_entry.insert(0, str(weekends))
        else:
            messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_invalid_date_format", "Format de date invalide pour calculer les week-ends (AAAA-MM-JJ)."))

    def sort_treeview(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        try:
            if col == "duration" or col == "meals" or col == "nights" or col == "weekends":
                data.sort(key=lambda item: int(item[0]) if item[0] else float('-inf'), reverse=reverse)
            else:
                data.sort(key=lambda item: item[0].lower(), reverse=reverse)
        except ValueError:
            data.sort(key=lambda item: item[0].lower(), reverse=reverse)
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))