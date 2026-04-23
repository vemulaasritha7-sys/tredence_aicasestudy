"""
AutoHand — System Tools
========================
Desktop automation utilities: launching apps, typing, key presses,
VS Code integration, and screenshots.
"""

import os
import sys
import time
import subprocess
import pyautogui

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import TYPING_INTERVAL, APP_LAUNCH_WAIT

# Disable pyautogui failsafe (move mouse to corner to abort if needed)
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

# ─── Known app -> executable/command map (Windows) ────────────────────────────
APP_MAP: dict[str, str] = {
    "notepad":    "notepad.exe",
    "excel":      "excel",
    "word":       "winword",
    "paint":      "mspaint.exe",
    "calculator": "calc.exe",
    "cmd":        "cmd.exe",
    "powershell": "powershell.exe",
    "explorer":   "explorer.exe",
    "vscode":     "code",
    "vs code":    "code",
    "chrome":     "chrome",
    "edge":       r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
}


def open_app(app_name: str) -> None:
    """
    Launch a Windows application by name.

    Parameters
    ----------
    app_name : str
        Human-readable app name (e.g., "notepad", "excel").
    """
    key = app_name.lower().strip()
    cmd = APP_MAP.get(key, app_name)    # fall back to raw name

    try:
        subprocess.Popen(cmd, shell=True)
        time.sleep(APP_LAUNCH_WAIT)
    except Exception as e:
        raise RuntimeError(f"Failed to open '{app_name}': {e}")


def type_text(text: str) -> None:
    """
    Type text into the currently focused window.
    Uses typewrite for ASCII-safe characters; falls back to xdotool approach
    for special characters via pyautogui.write with unicode support.

    Parameters
    ----------
    text : str
        Text to type.
    """
    time.sleep(0.3)
    # pyautogui.write handles multi-line strings poorly; use pyperclip paste for safety
    try:
        import pyperclip
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")
    except ImportError:
        # fall back to character-by-character typing
        pyautogui.write(text, interval=TYPING_INTERVAL)


def press_keys(keys: str) -> None:
    """
    Press a keyboard shortcut / hotkey.

    Parameters
    ----------
    keys : str
        Key combo as a plus-separated string, e.g. "ctrl+s", "alt+f4".
    """
    parts = [k.strip() for k in keys.lower().split("+")]
    if len(parts) == 1:
        pyautogui.press(parts[0])
    else:
        pyautogui.hotkey(*parts)
    time.sleep(0.2)


def open_vscode(path: str = "") -> None:
    """
    Open VS Code, optionally at a specific folder/file path.

    Parameters
    ----------
    path : str
        Optional path to open in VS Code (defaults to current dir).
    """
    target = path.strip() or "."
    try:
        subprocess.Popen(f"code {target}", shell=True)
        time.sleep(4)   # VS Code takes a few seconds to start
    except Exception as e:
        raise RuntimeError(f"Failed to open VS Code: {e}")


def write_code(code: str) -> None:
    """
    Type code into the currently focused editor window.
    Adds a small delay before typing so the editor is ready.

    Parameters
    ----------
    code : str
        Source code to type.
    """
    time.sleep(0.5)
    type_text(code)


def take_screenshot(filename: str = "screenshot.png") -> str:
    """
    Capture a screenshot and save it to the Desktop.

    Parameters
    ----------
    filename : str
        Output filename.

    Returns
    -------
    str
        Absolute path to the saved screenshot.
    """
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    os.makedirs(desktop, exist_ok=True)
    path = os.path.join(desktop, filename)
    screenshot = pyautogui.screenshot()
    screenshot.save(path)
    return path


# ─── Quick test ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Opening Notepad...")
    open_app("notepad")
    time.sleep(1)
    type_text("AutoHand system tools test!")
    print("Done.")
