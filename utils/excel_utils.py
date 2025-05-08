import xlrd
import xlwt
from tkinter import filedialog, messagebox
import os

def import_xls_file():
    """Open a file dialog to select an .xls file and return the workbook object."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xls")],
        title="Select Excel file to import"
    )
    if not file_path:
        return None, "No file selected"
    if not file_path.lower().endswith('.xls'):
        return None, "Selected file is not an .xls file"
    try:
        workbook = xlrd.open_workbook(file_path)
        return workbook, None
    except Exception as e:
        return None, f"Failed to open Excel file: {str(e)}"

def export_xls_file(data, headers, title="Exported Data"):
    """
    Export data to an .xls file.
    data: list of tuples or lists representing rows
    headers: list of column headers
    """
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xls",
        filetypes=[("Excel files", "*.xls")],
        title="Save Excel file"
    )
    if not file_path:
        return "No file selected"
    if not file_path.lower().endswith('.xls'):
        file_path += '.xls'
    try:
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(title)

        # Write headers
        for col_index, header in enumerate(headers):
            sheet.write(0, col_index, header)

        # Write data rows
        for row_index, row in enumerate(data, start=1):
            for col_index, cell_value in enumerate(row):
                sheet.write(row_index, col_index, cell_value)

        workbook.save(file_path)
        return None
    except Exception as e:
        return f"Failed to save Excel file: {str(e)}"
