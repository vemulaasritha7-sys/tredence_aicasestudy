# AutoHand 🤖 — AI Desktop Operator

**AutoHand** is a production-style AI agent system that understands natural language instructions, plans them using Claude, and executes them on your Windows desktop — opening apps, typing text, creating files, and more.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 AI Planner | Gemini converts natural language → structured JSON plan |
| ⚙️ Executor | Runs each step sequentially with retry logic |
| 🖥️ Desktop Automation | Opens apps, types text, saves files via pyautogui |
| 📊 Excel Creation | Generates styled `.xlsx` files via openpyxl |
| 💻 VS Code Integration | Opens VS Code and writes code |
| 🌐 Web Portal | Beautiful dark chat UI on `localhost:5000` |
| 🖤 CLI Mode | Rich terminal UI with live step logs |

---

## 📂 Project Structure

```
autohand2/
│
├── main.py              ← CLI interface
├── app.py               ← Flask web portal (port 5000)
├── config.py            ← API keys, model settings, action schema
│
├── agents/
│   ├── __init__.py
│   ├── planner.py       ← Claude-powered task planner
│   └── executor.py      ← Step runner with retry logic
│
├── tools/
│   ├── __init__.py
│   ├── system_tools.py  ← open_app, type_text, press_keys, vscode
│   └── file_tools.py    ← save_file, create_excel_file, create_text_file
│
├── ui/
│   ├── templates/
│   │   └── index.html   ← Chat interface template
│   └── static/
│       ├── style.css    ← Dark neon glassmorphism UI
│       └── script.js    ← Vanilla JS chat logic
│
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Set Up Python Environment

```powershell
cd autohand2
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Set Your API Key

Open `config.py` and replace the placeholder with your actual Gemini API key:

```python
GOOGLE_API_KEY = "PASTE_YOUR_REAL_GEMINI_API_KEY_HERE"
```

### 3. Run the Web Portal

```powershell
python app.py
```

Open your browser at **http://localhost:5000**

### 4. Run the CLI

```powershell
python main.py
```

---

## 🧪 Demo Tasks

Paste these into the Web Portal or CLI:

```
Open Notepad and write a project summary about AutoHand
```

```
Create an Excel file with sample employee data including Name, Department, and Salary
```

```
Open VS Code and write a Python hello world program
```

```
Create a text file named project_notes.txt with notes about the AutoHand project
```

---

## 🎬 Execution Flow

```
User Input
   │
   ▼
Planner (Gemini)
   │  Outputs: JSON action plan
   ▼
Executor
   │  Dispatches each step to tools layer
   ▼
Tools  ──►  system_tools / file_tools
   │
   ▼
Desktop Actions  ──►  Logs  ──►  Web UI / CLI
```

---

## ⚙️ Supported Actions

| Action | What it Does |
|---|---|
| `open_app` | Launches a Windows application |
| `type_text` | Types text into the focused window |
| `press_keys` | Presses a key combo (e.g., `ctrl+s`) |
| `save_file` | Triggers Ctrl+S and names the file |
| `create_excel_file` | Creates a styled `.xlsx` file on Desktop |
| `create_text_file` | Writes a `.txt` file directly to Desktop |
| `open_vscode` | Opens VS Code |
| `write_code` | Types code into the focused editor |
| `take_screenshot` | Captures a screenshot to Desktop |
| `wait` | Pauses execution (seconds) |

---

## 🔒 Safety

- All actions run through a **whitelist** in `config.py`
- No system-level destructive operations
- `SAFE_MODE = True` blocks any unlisted actions

---

## 🛠 Configuration

Edit `config.py` to customize:

```python
GEMINI_MODEL      = "gemini-1.5-flash"    # Model to use
MAX_TOKENS        = 2048                   # Max response length
TYPING_INTERVAL   = 0.04                  # Keyboard speed (seconds/char)
APP_LAUNCH_WAIT   = 2                     # Seconds to wait after opening app
FLASK_PORT        = 5000                  # Web portal port
SAFE_MODE         = True                  # Whitelist-only actions
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `google-generativeai` | Gemini API |
| `flask` | Web portal |
| `pyautogui` | Desktop automation |
| `pyperclip` | Fast clipboard paste |
| `openpyxl` | Excel file creation |
| `rich` | Beautiful CLI output |
| `pillow` | Screenshot support |

---

## ⚠️ Notes

- **pyautogui failsafe**: Move the mouse to the top-left corner to abort any running automation.
- **Clipboard paste**: Requires clipboard access (enabled by default on Windows).
- **VS Code**: Must be installed and the `code` command must be in your PATH.
- **Excel**: Files are saved to your Desktop as `autohand_data.xlsx`.

---

*Built with ❤️ using Gemini + Flask + pyautogui*
