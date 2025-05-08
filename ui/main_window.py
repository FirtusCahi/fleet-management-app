import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import db_utils as root_database
from ui.vehicles_window import VehiclesWindow
from ui.drivers_window import DriversWindow
from ui.expenses_window import ExpensesWindow
from ui.missions_window import MissionsWindow
from ui.assignment_window import AssignmentWindow
from ui.about_window import AboutWindow
from reporting.pdf_exporter import export_to_pdf
from reporting.excel_exporter import export_to_excel
from utils.date_utils import calculate_weekends
import pandas as pd
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MainWindow(ttk.Frame):
    def __init__(self, parent, db_file, lang, switch_language_callback):
        ttk.Frame.__init__(self, parent, padding=10)
        self.parent = parent
        self.db_file = db_file
        self.lang = lang
        self.switch_language_callback = switch_language_callback

        self.vehicles_window = None
        self.drivers_window = None
        self.expenses_window = None
        self.missions_window = None
        self.assignment_window = None
        self.about_window = None

        self.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        self.create_widgets()
        self.update_language(self.lang)
        self.load_dashboard_data()

    def update_language(self, lang):
        self.lang = lang
        self.lbl_dashboard.config(text=self.lang.get("dashboard_title", "Tableau de Bord"))
        self.nb_dashboard.tab(self.tab_alerts, text=self.lang.get("dashboard_tab_alerts", "Alertes"))
        self.nb_dashboard.tab(self.tab_overview, text=self.lang.get("dashboard_tab_overview", "Aperçu"))
        self.nb_dashboard.tab(self.tab_assignments, text=self.lang.get("dashboard_tab_assignments", "Affectations Récentes"))
        self.nb_dashboard.tab(self.tab_expenses, text=self.lang.get("dashboard_tab_expenses", "Répartition des Dépenses"))

        self.btn_manage_vehicles.config(text=self.lang.get("menu_vehicles", "Véhicules"))
        self.btn_manage_drivers.config(text=self.lang.get("menu_drivers", "Conducteurs"))
        self.btn_manage_expenses.config(text=self.lang.get("menu_expenses", "Dépenses"))
        self.btn_manage_missions.config(text=self.lang.get("menu_missions", "Missions"))
        self.btn_manage_assignments.config(text=self.lang.get("menu_assignments", "Affectations"))
        self.btn_export.config(text=self.lang.get("button_export", "Exporter"))
        self.btn_print.config(text=self.lang.get("button_print", "Imprimer"))

        # Update labels in overview tab
        self.lbl_total_vehicles.config(text=self.lang.get("overview_total_vehicles", "Total Véhicules:"))
        self.lbl_total_drivers.config(text=self.lang.get("overview_total_drivers", "Total Conducteurs:"))
        self.lbl_total_expenses_overview.config(text=self.lang.get("overview_total_expenses", "Dépenses Totales:"))

        # Update column headers in alerts treeview
        self.tv_alerts.heading("type", text=self.lang.get("alerts_column_type", "Type"))
        self.tv_alerts.heading("item", text=self.lang.get("alerts_column_item", "Élément"))
        self.tv_alerts.heading("date", text=self.lang.get("alerts_column_date", "Date"))

        # Update column headers in assignments treeview
        self.tv_assignments.heading("vehicle", text=self.lang.get("assignments_column_vehicle", "Véhicule"))
        self.tv_assignments.heading("driver", text=self.lang.get("assignments_column_driver", "Conducteur"))
        self.tv_assignments.heading("date", text=self.lang.get("assignments_column_date", "Date d'affectation"))

        self.load_dashboard_data() # Reload data with new language

    def create_widgets(self):
        self.lbl_dashboard = ttk.Label(self, font=("Arial", 16))
        self.lbl_dashboard.grid(row=0, column=0, columnspan=5, pady=10, sticky="ew")

        # Notebook for dashboard tabs
        self.nb_dashboard = ttk.Notebook(self)
        self.nb_dashboard.grid(row=1, column=0, columnspan=5, sticky="nsew")

        # --- Alerts Tab ---
        self.tab_alerts = ttk.Frame(self.nb_dashboard)
        self.tv_alerts = ttk.Treeview(self.tab_alerts, columns=("type", "item", "date"), show="headings")
        self.tv_alerts.column("type", width=200)
        self.tv_alerts.column("item", width=200)
        self.tv_alerts.column("date", width=150)
        self.tv_alerts.grid(row=0, column=0, sticky="nsew")
        scrollbar_alerts_y = ttk.Scrollbar(self.tab_alerts, orient="vertical", command=self.tv_alerts.yview)
        self.tv_alerts.configure(yscrollcommand=scrollbar_alerts_y.set)
        scrollbar_alerts_y.grid(row=0, column=1, sticky="ns")
        self.tab_alerts.columnconfigure(0, weight=1)
        self.tab_alerts.rowconfigure(0, weight=1)
        self.nb_dashboard.add(self.tab_alerts)

        # --- Overview Tab ---
        self.tab_overview = ttk.Frame(self.nb_dashboard)
        ttk.Label(self.tab_overview, text=self.lang.get("overview_statistics", "Statistiques Générales"), font=("Arial", 12)).grid(row=0, column=0, columnspan=2, pady=5, sticky="ew")
        self.lbl_total_vehicles_text = ttk.Label(self.tab_overview)
        self.lbl_total_vehicles_text.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.lbl_total_vehicles = ttk.Label(self.tab_overview, font=("Arial", 10, "bold"))
        self.lbl_total_vehicles.grid(row=1, column=1, padx=5, pady=2, sticky="e")
        self.lbl_total_drivers_text = ttk.Label(self.tab_overview)
        self.lbl_total_drivers_text.grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.lbl_total_drivers = ttk.Label(self.tab_overview, font=("Arial", 10, "bold"))
        self.lbl_total_drivers.grid(row=2, column=1, padx=5, pady=2, sticky="e")
        self.lbl_total_expenses_overview_text = ttk.Label(self.tab_overview)
        self.lbl_total_expenses_overview_text.grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.lbl_total_expenses_overview = ttk.Label(self.tab_overview, font=("Arial", 10, "bold"))
        self.lbl_total_expenses_overview.grid(row=3, column=1, padx=5, pady=2, sticky="e")
        self.nb_dashboard.add(self.tab_overview)

        # --- Recent Assignments Tab ---
        self.tab_assignments = ttk.Frame(self.nb_dashboard)
        self.tv_assignments = ttk.Treeview(self.tab_assignments, columns=("vehicle", "driver", "date"), show="headings")
        self.tv_assignments.column("vehicle", width=150)
        self.tv_assignments.column("driver", width=150)
        self.tv_assignments.column("date", width=100)
        self.tv_assignments.grid(row=0, column=0, sticky="nsew")
        scrollbar_assignments_y = ttk.Scrollbar(self.tab_assignments, orient="vertical", command=self.tv_assignments.yview)
        self.tv_assignments.configure(yscrollcommand=scrollbar_assignments_y.set)
        scrollbar_assignments_y.grid(row=0, column=1, sticky="ns")
        self.tab_assignments.columnconfigure(0, weight=1)
        self.tab_assignments.rowconfigure(0, weight=1)
        self.nb_dashboard.add(self.tab_assignments)

        # --- Expenses Breakdown Tab ---
        self.tab_expenses = ttk.Frame(self.nb_dashboard)
        self.expenses_canvas = tk.Canvas(self.tab_expenses)
        self.expenses_canvas.pack(fill="both", expand=True)
        self.nb_dashboard.add(self.tab_expenses)

        # --- Buttons ---
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=5, pady=10, sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        button_frame.columnconfigure(3, weight=1)
        button_frame.columnconfigure(4, weight=1)

        self.btn_manage_vehicles = ttk.Button(button_frame, command=self.open_vehicles_window)
        self.btn_manage_vehicles.grid(row=0, column=0, padx=5, sticky="ew")

        self.btn_manage_drivers = ttk.Button(button_frame, command=self.open_drivers_window)
        self.btn_manage_drivers.grid(row=0, column=1, padx=5, sticky="ew")

        self.btn_manage_expenses = ttk.Button(button_frame, command=self.open_expenses_window)
        self.btn_manage_expenses.grid(row=0, column=2, padx=5, sticky="ew")

        self.btn_manage_missions = ttk.Button(button_frame, command=self.open_missions_window)
        self.btn_manage_missions.grid(row=0, column=3, padx=5, sticky="ew")

        self.btn_manage_assignments = ttk.Button(button_frame, command=self.open_assignment_window)
        self.btn_manage_assignments.grid(row=0, column=4, padx=5, sticky="ew")

        export_print_frame = ttk.Frame(self)
        export_print_frame.grid(row=3, column=0, columnspan=5, pady=5, sticky="ew")
        export_print_frame.columnconfigure(0, weight=1)
        export_print_frame.columnconfigure(1, weight=1)

        self.btn_export = ttk.Button(export_print_frame, command=self.export_data)
        self.btn_export.grid(row=0, column=0, padx=5, sticky="ew")

        self.btn_print = ttk.Button(export_print_frame, command=self.print_data)
        self.btn_print.grid(row=0, column=1, padx=5, sticky="ew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def load_dashboard_data(self):
        # Load alerts
        for item in self.tv_alerts.get_children():
            self.tv_alerts.delete(item)
        vehicle_alerts = root_database.check_vehicle_alerts(self.db_file)
        driver_alerts = root_database.check_driver_alerts(self.db_file)
        for alert in vehicle_alerts:
            self.tv_alerts.insert("", tk.END, values=(alert['type'], f"{self.lang.get('vehicle', 'Véhicule')} {alert['registration']}", alert['date']))
        for alert in driver_alerts:
            self.tv_alerts.insert("", tk.END, values=(alert['type'], f"{self.lang.get('driver', 'Conducteur')} {alert['name']}", alert['date']))

        # Load overview data
        vehicles = root_database.list_vehicles(self.db_file)
        drivers = root_database.list_drivers(self.db_file)
        total_expenses = root_database.get_total_expenses(self.db_file)
        self.lbl_total_vehicles.config(text=len(vehicles))
        self.lbl_total_drivers.config(text=len(drivers))
        self.lbl_total_expenses_overview.config(text=f"{total_expenses:.2f}")
        self.lbl_total_vehicles_text.config(text=self.lang.get("overview_total_vehicles", "Total Véhicules:"))
        self.lbl_total_drivers_text.config(text=self.lang.get("overview_total_drivers", "Total Conducteurs:"))
        self.lbl_total_expenses_overview_text.config(text=self.lang.get("overview_total_expenses", "Dépenses Totales:"))

        # Load recent assignments
        for item in self.tv_assignments.get_children():
            self.tv_assignments.delete(item)
        assignments = root_database.list_assignments(self.db_file)
        assignments.sort(key=lambda x: datetime.strptime(x[4], '%Y-%m-%d'), reverse=True) # Sort by date
        for assignment in assignments[:5]: # Display the 5 most recent
            self.tv_assignments.insert("", tk.END, values=(assignment[1], f"{assignment[2]} {assignment[3]}", assignment[4]))

        # Load expenses breakdown
        expenses_data = root_database.get_expenses_by_type(self.db_file)
        self.plot_expenses_pie_chart(expenses_data)

    def plot_expenses_pie_chart(self, expenses_data):
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        for widget in self.expenses_canvas.winfo_children():
            widget.destroy()

        if not expenses_data:
            no_data_label = ttk.Label(self.expenses_canvas, text=self.lang.get("expenses_no_data", "Aucune dépense enregistrée."))
            no_data_label.pack(padx=10, pady=10)
            return

        labels = [item[0] for item in expenses_data]
        sizes = [item[1] for item in expenses_data]
        if not sizes:
            no_data_label = ttk.Label(self.expenses_canvas, text=self.lang.get("expenses_no_data", "Aucune dépense enregistrée."))
            no_data_label.pack(padx=10, pady=10)
            return

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title(self.lang.get("expenses_breakdown", "Répartition des Dépenses"))

        canvas = FigureCanvasTkAgg(fig, master=self.expenses_canvas)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)
        canvas.draw()
        plt.close(fig) # Close the matplotlib figure to prevent memory issues

    def open_vehicles_window(self):
        if self.vehicles_window is None or not tk.Toplevel.winfo_exists(self.vehicles_window):
            self.vehicles_window = VehiclesWindow(self.parent, self.db_file, self.lang, self.reload_dashboard)
        else:
            self.vehicles_window.focus()

    def open_drivers_window(self):
        if self.drivers_window is None or not tk.Toplevel.winfo_exists(self.drivers_window):
            self.drivers_window = DriversWindow(self.parent, self.db_file, self.lang, self.reload_dashboard)
        else:
            self.drivers_window.focus()

    def open_expenses_window(self):
        if self.expenses_window is None or not tk.Toplevel.winfo_exists(self.expenses_window):
            self.expenses_window = ExpensesWindow(self.parent, self.db_file, self.lang, self.reload_dashboard)
        else:
            self.expenses_window.focus()

    def open_missions_window(self):
        if self.missions_window is None or not tk.Toplevel.winfo_exists(self.missions_window):
            self.missions_window = MissionsWindow(self.parent, self.db_file, self.lang, self.reload_dashboard)
        else:
            self.missions_window.focus()

    def open_assignment_window(self):
        if self.assignment_window is None or not tk.Toplevel.winfo_exists(self.assignment_window):
            self.assignment_window = AssignmentWindow(self.parent, self.db_file, self.lang, self.reload_dashboard)
        else:
            self.assignment_window.focus()

    def show_about(self):
        if self.about_window is None or not tk.Toplevel.winfo_exists(self.about_window):
            self.about_window = AboutWindow(self.parent, self.lang)
        else:
            self.about_window.focus()

    def export_data(self):
        export_type = tk.messagebox.askquestion(self.lang.get("export_title", "Exporter"), self.lang.get("export_ask_format", "Souhaitez-vous exporter au format Excel ou PDF ?"), icon='question')
        if export_type == 'yes':
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[(self.lang.get("excel_files", "Fichiers Excel"), "*.xlsx")])
            if file_path:
                vehicles = root_database.list_vehicles(self.db_file)
                drivers
                expenses = root_database.list_expenses(self.db_file)
                missions = root_database.list_missions(self.db_file)
                assignments_data = root_database.list_assignments(self.db_file)
                export_to_excel(file_path, vehicles, drivers, expenses, missions, assignments_data, self.lang)
                os.startfile(file_path) # Open the file after saving (Windows only)
        elif export_type == 'no':
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[(self.lang.get("pdf_files", "Fichiers PDF"), "*.pdf")])
            if file_path:
                vehicles = root_database.list_vehicles(self.db_file)
                drivers = root_database.list_drivers(self.db_file)
                expenses = root_database.list_expenses(self.db_file)
                missions = root_database.list_missions(self.db_file)
                assignments_data = root_database.list_assignments(self.db_file)
                export_to_pdf(file_path, vehicles, drivers, expenses, missions, assignments_data, self.lang)
                try:
                    os.startfile(file_path) # Open the file after saving (Windows)
                except AttributeError:
                    import subprocess
                    subprocess.call(['open', file_path]) # Open the file after saving (macOS)
                except FileNotFoundError:
                    tk.messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_pdf_viewer", "Impossible d'ouvrir le fichier PDF. Veuillez vérifier si un lecteur PDF est installé."))

    def print_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[(self.lang.get("pdf_files", "Fichiers PDF"), "*.pdf")])
        if file_path:
            vehicles = database.list_vehicles(self.db_file)
            drivers = database.list_drivers(self.db_file)
            expenses = database.list_expenses(self.db_file)
            missions = database.list_missions(self.db_file)
            assignments_data = database.list_assignments(self.db_file)
            export_to_pdf(file_path, vehicles, drivers, expenses, missions, assignments_data, self.lang, for_print=True)
            try:
                os.startfile(file_path) # Open the file for printing (user can then choose to print)
            except AttributeError:
                import subprocess
                subprocess.call(['open', file_path]) # Open the file for printing (macOS)
            except FileNotFoundError:
                tk.messagebox.showerror(self.lang.get("error_title", "Erreur"), self.lang.get("error_pdf_viewer", "Impossible d'ouvrir le fichier PDF. Veuillez vérifier si un lecteur PDF est installé."))

    def backup_database(self):
        backup_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[(self.lang.get("database_files", "Fichiers de base de données"), "*.db")])
        if backup_path:
            if root_database.backup_database(self.db_file, backup_path):
                tk.messagebox.showinfo(self.lang.get("backup_success_title", "Sauvegarde réussie"), self.lang.get("backup_success_message", "La base de données a été sauvegardée avec succès."))
            else:
                tk.messagebox.showerror(self.lang.get("backup_error_title", "Erreur de sauvegarde"), self.lang.get("backup_error_message", "Une erreur s'est produite lors de la sauvegarde de la base de données."))

    def restore_database(self):
        backup_path = filedialog.askopenfilename(defaultextension=".db", filetypes=[(self.lang.get("database_backup_files", "Fichiers de sauvegarde de la base de données"), "*.db")])
        if backup_path:
            if root_database.restore_database(backup_path, self.db_file):
                tk.messagebox.showinfo(self.lang.get("restore_success_title", "Restauration réussie"), self.lang.get("restore_success_message", "La base de données a été restaurée avec succès. L'application va redémarrer."), )
                self.parent.destroy()
                import main
                main.App()
            else:
                tk.messagebox.showerror(self.lang.get("restore_error_title", "Erreur de restauration"), self.lang.get("restore_error_message", "Une erreur s'est produite lors de la restauration de la base de données."))

    def reload_dashboard(self):
        self.load_dashboard_data()
