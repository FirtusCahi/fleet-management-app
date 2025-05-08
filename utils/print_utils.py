import tkinter as tk
from tkinter import Toplevel, Frame, Button, Label, Radiobutton, IntVar, Scrollbar, Canvas, messagebox
from tkinter import filedialog
import tempfile
import os
import platform
import subprocess

class PrintPreviewDialog(Toplevel):
    def __init__(self, parent, data, headers, title="Print Preview"):
        super().__init__(parent)
        self.title(title)
        self.geometry("800x600")
        self.data = data
        self.headers = headers
        self.orientation = IntVar(value=0)  # 0: Portrait, 1: Landscape

        self.create_widgets()
        self.render_preview()

    def create_widgets(self):
        control_frame = Frame(self)
        control_frame.pack(side="top", fill="x")

        Label(control_frame, text="Orientation:").pack(side="left", padx=5)
        Radiobutton(control_frame, text="Portrait", variable=self.orientation, value=0, command=self.render_preview).pack(side="left")
        Radiobutton(control_frame, text="Landscape", variable=self.orientation, value=1, command=self.render_preview).pack(side="left")

        Button(control_frame, text="Print", command=self.print_data).pack(side="right", padx=5)
        Button(control_frame, text="Close", command=self.destroy).pack(side="right")

        # Canvas for preview
        self.canvas = Canvas(self, bg="white")
        self.canvas.pack(side="top", fill="both", expand=True)

        # Scrollbars
        self.v_scroll = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.h_scroll.pack(side="bottom", fill="x")

        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        self.preview_frame = Frame(self.canvas, bg="white")
        self.canvas.create_window((0,0), window=self.preview_frame, anchor="nw")

        self.preview_frame.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def render_preview(self):
        # Clear previous preview
        for widget in self.preview_frame.winfo_children():
            widget.destroy()

        # Render headers
        for col_index, header in enumerate(self.headers):
            lbl = Label(self.preview_frame, text=header, borderwidth=1, relief="solid", width=15, bg="#d3d3d3")
            lbl.grid(row=0, column=col_index, sticky="nsew")

        # Render data rows
        for row_index, row in enumerate(self.data, start=1):
            for col_index, cell in enumerate(row):
                lbl = Label(self.preview_frame, text=str(cell), borderwidth=1, relief="solid", width=15)
                lbl.grid(row=row_index, column=col_index, sticky="nsew")

        # Adjust column weights
        for col_index in range(len(self.headers)):
            self.preview_frame.grid_columnconfigure(col_index, weight=1)

    def print_data(self):
        # Export preview data to a temporary file for printing
        try:
            import xlwt
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xls")
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet("PrintData")

            # Write headers
            for col_index, header in enumerate(self.headers):
                sheet.write(0, col_index, header)

            # Write data
            for row_index, row in enumerate(self.data, start=1):
                for col_index, cell in enumerate(row):
                    sheet.write(row_index, col_index, cell)

            workbook.save(temp_file.name)
            temp_file.close()

            # Use system print command depending on OS
            if platform.system() == "Windows":
                # Windows print command
                os.startfile(temp_file.name, "print")
            elif platform.system() == "Darwin":
                # macOS print command
                subprocess.run(["lp", temp_file.name])
            else:
                # Linux print command
                subprocess.run(["lp", temp_file.name])

            messagebox.showinfo("Print", "Print job sent to the printer.")
        except Exception as e:
            messagebox.showerror("Print Error", f"Failed to print: {str(e)}")
        finally:
            try:
                os.unlink(temp_file.name)
            except Exception:
                pass
