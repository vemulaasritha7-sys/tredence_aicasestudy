import re

def analyze_intent(user_input):
    """
    Analyzes raw string to explicitly map deterministic paths matching strict semantic routing overrides.
    Returns -> {"action": str, "target_file": str, "metadata": dict}
    """
    user = str(user_input).lower()

    if "patient" in user or ("open" in user and "excel" in user and "record" in user) or "hospital" in user:
        return {
            "action": "open_excel_file",
            "target_file": "patient_data.xlsx",
            "metadata": {}
        }

    if "excel" in user:
        return {
            "action": "create_excel_file",
            "target_file": "autohand_employee_table.xlsx",
            "metadata": {}
        }
        
    if "email" in user or "mail" in user:
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', user_input)
        target = email_match.group(0) if email_match else "unknown@target.com"
        return {
            "action": "send_email",
            "target_file": "",
            "metadata": {"recipient": target}
        }
        
    if "code" in user or "python" in user or "program" in user:
        return {
            "action": "write_code",
            "target_file": "main.py",
            "metadata": {}
        }
        
    if "file" in user or "text" in user or "notes" in user or "summary" in user:
        return {
            "action": "write_file",
            "target_file": "auto_generated_notes.txt",
            "metadata": {}
        }
        
    # Default to raw payload response rendered directly onto the UI bounds.
    return {
        "action": "generate_ai_response",
        "target_file": "",
        "metadata": {}
    }
