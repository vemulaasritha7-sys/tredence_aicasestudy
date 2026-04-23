import os
import openpyxl

def generate_and_open_excel(target_filename="autohand_employee_table.xlsx"):
    """
    Constructs accurate programmatic schema bypassing generic fallback dictionaries explicitly.
    Ensures .startfile() handles dynamic focus perfectly cleanly immediately hitting native OS interfaces natively.
    """
    wb = openpyxl.Workbook()
    ws = wb.active

    # Insert structured dataset
    ws.append(["ID", "Name", "Department", "Role", "Salary"])
    ws.append([101, "AutoHand System", "Orchestration", "Chief AI Operator", 950000])
    ws.append([102, "John Doe", "Engineering", "Developer", 120000])
    ws.append([103, "Jane Smith", "Design", "Product Architect", 145000])
    ws.append([104, "Alan Turing", "Research", "Scientist", 300000])

    path = os.path.join(os.path.expanduser("~"), "Desktop", target_filename)
    wb.save(path)
    
    os.startfile(path)
    return f"Structured Employee dataset matrix generated and launched utilizing openpyxl: {path}"

def open_existing_excel(filepath):
    """
    Opens an existing Excel file directly using OS file launch.
    """
    if not os.path.exists(filepath):
        return f"Error: Excel file not found at {filepath}"
    try:
        os.startfile(filepath)
        return f"Successfully opened the requested Excel file: {filepath}"
    except Exception as e:
        return f"Failed to open the Excel file. Error: {e}"

