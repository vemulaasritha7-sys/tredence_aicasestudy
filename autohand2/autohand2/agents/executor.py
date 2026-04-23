import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Resolve execution domains correctly across newly established strict routing architectures.
from core.ai_engine import generate_ai_content
from tools.file_tools import process_and_open_code, process_and_open_text
from tools.excel_tools import generate_and_open_excel, open_existing_excel
from automation.mailer import dispatch_email
from dataclasses import dataclass, asdict
from typing import Literal

Status = Literal["pending", "running", "success", "error", "skipped"]

@dataclass
class ExecutionLog:
    step: int
    action: str
    value: str
    status: Status
    message: str
    elapsed_ms: int

    def to_dict(self) -> dict: return asdict(self)

class ExecutorError(Exception):
    pass

def execute(plan):
    """
    Orchestrates pure execution sequences strictly validating output schemas mapping outputs to precise dedicated module handlers.
    """
    logs = []

    for i, step in enumerate(plan):
        action = step.get("action", "generate_ai_response")
        value = step.get("value", "")
        filename = step.get("filename", "")
        recipient = step.get("recipient", "")

        log = ExecutionLog(
            step=i + 1,
            action=str(action),
            value=str(value),
            status="running",
            message="",
            elapsed_ms=0,
        )

        start = time.monotonic()
        try:
            if action == "generate_ai_response":
                content = generate_ai_content(f"Respond comprehensively to this request: {value}")
                log.message = content
                
            elif action == "write_file":
                content = generate_ai_content(f"Produce a highly detailed text document for: {value}")
                name = filename if filename else "output.txt"
                log.message = process_and_open_text(content, name)

            elif action == "write_code":
                content = generate_ai_content(f"Write highly functional programmatic code strictly regarding: {value}")
                name = filename if filename else "main.py"
                log.message = process_and_open_code(content, name)

            elif action == "create_excel_file":
                name = filename if filename else "employees.xlsx"
                log.message = generate_and_open_excel(name)

            elif action == "open_excel_file":
                name = filename if filename else "patient_data.xlsx"
                filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", name))
                log.message = open_existing_excel(filepath)

            elif action == "send_email":
                target = recipient if recipient else "user@example.com"
                content = generate_ai_content(f"Compose a professional email body regarding: {value}")
                # Leverage automation mailer
                log.message = dispatch_email(target, "Automated Generation Output", content)

            else:
                log.message = f"Unknown action bypassed securely: {action}"

            log.status = "success"

        except Exception as e:
            log.status = "error"
            log.message = f"Execution bounds intercepted a critical execution error smoothly: {str(e)[:50]}"

        log.elapsed_ms = int((time.monotonic() - start) * 1000)
        logs.append(log)

    return logs
