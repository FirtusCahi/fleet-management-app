import tkinter as tk
from tkinter import ttk

class AboutWindow(tk.Toplevel):
    def __init__(self, parent, lang):
        tk.Toplevel.__init__(self, parent)
        self.title(lang.get("about_title", "À Propos"))
        self.geometry("300x150")
        self.lang = lang
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text=self.lang.get("app_name", "Gestionnaire de Flotte"), font=("Arial", 14)).pack(pady=10)
        ttk.Label(self, text=self.lang.get("version", "Version:") + " 1.0").pack(pady=5)
        ttk.Label(self, text=self.lang.get("author", "Auteur:") + " Votre Nom").pack(pady=5)
        ttk.Button(self, text=self.lang.get("button_close", "Fermer"), command=self.destroy).pack(pady=10)