import tkinter as tk
from tkinter import ttk, messagebox
from ui.main_window import MainWindow
from utils.error_logger import setup_logger
import logging
import json
import os

APP_NAME = "Gestion de Flotte"
VERSION = "1.0"
DATABASE_FILE = "fleet_data.db"
LOG_FILE = "app.log"
LANG_DIR = "lang"
DEFAULT_LANG = "fr"

logger = setup_logger(LOG_FILE)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1200x700")
        self.minsize(800, 500)

        self.lang = self.load_language(DEFAULT_LANG)
        self.database_file = DATABASE_FILE

        import db_utils as root_database
        root_database.create_tables(self.database_file)

        self.main_window = MainWindow(self, self.database_file, self.lang, self.switch_language)
        self.config(menu=self.create_menu())

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_language(self, lang_code):
        try:
            # Corrected path to the language files within the "translations" subdirectory
            filepath = os.path.join('lang', 'translations', f"{lang_code}.json")
            logger.debug(f"Loading language file: {filepath}")
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Fichier de langue '{filepath}' non trouvé.")
            if lang_code != DEFAULT_LANG:  # Prevent recursion if default lang file is missing
                return self.load_language(DEFAULT_LANG)  # Fallback
            else:
                return {}  # Return empty dict to avoid error, and continue execution.
        except json.JSONDecodeError:
            logger.error(f"Erreur de décodage JSON dans '{filepath}'.")
            if lang_code != DEFAULT_LANG:  # Prevent recursion if default lang file has invalid JSON
                return self.load_language(DEFAULT_LANG)  # Fallback
            else:
                return {}  # Return empty dict to avoid error, and continue execution.

    def switch_language(self, lang_code):
        self.lang = self.load_language(lang_code)
        self.main_window.update_language(self.lang)
        self.config(menu=self.create_menu())  # Recreate menu for translation

    def create_menu(self):
        menubar = tk.Menu(self)

        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label=self.lang.get("menu_file_backup", "Sauvegarder"), command=self.main_window.backup_database)
        file_menu.add_command(label=self.lang.get("menu_file_restore", "Restaurer"), command=self.main_window.restore_database)
        file_menu.add_separator()
        file_menu.add_command(label=self.lang.get("menu_file_exit", "Quitter"), command=self.quit)
        menubar.add_cascade(label=self.lang.get("menu_file", "Fichier"), menu=file_menu)

        # Menu Affichage
        view_menu = tk.Menu(menubar, tearoff=0)
        lang_menu = tk.Menu(view_menu, tearoff=0)
        lang_menu.add_command(label="Français", command=lambda: self.switch_language("fr"))
        lang_menu.add_command(label="العربية", command=lambda: self.switch_language("ar"))
        view_menu.add_cascade(label=self.lang.get("menu_view_language", "Langue"), menu=lang_menu)
        menubar.add_cascade(label=self.lang.get("menu_view", "Affichage"), menu=view_menu)

        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label=self.lang.get("menu_help_about", "À propos"), command=self.main_window.show_about)
        menubar.add_cascade(label=self.lang.get("menu_help", "Aide"), menu=help_menu)

        return menubar

    def on_closing(self):
        if messagebox.askokcancel(self.lang.get("dialog_quit_title", "Quitter"), self.lang.get("dialog_quit_message", "Voulez-vous vraiment quitter l'application ?")):
            self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()