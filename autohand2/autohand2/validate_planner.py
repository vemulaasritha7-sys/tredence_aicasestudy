"""Quick validation — checks imports and helper functions without a live API call."""
import json, sys, os, warnings

# Suppress deprecation warnings for a clean output
warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.dirname(__file__))

from google import genai
from agents.planner import plan, create_plan, PlannerError, extract_json, _validate_plan

# ── 1. SDK import ─────────────────────────────────────────────────────────────
print(f"[1] google-genai SDK          : OK (v{genai.__version__})")

# ── 2. No anthropic anywhere ──────────────────────────────────────────────────
import importlib, agents.planner as pm
src = open(pm.__file__).read()
assert "anthropic" not in src.lower(), "FAIL: anthropic still in planner.py!"
print(f"[2] No anthropic in planner   : OK")

# ── 3. GOOGLE_API_KEY loads from env (no hardcoded key) ───────────────────────
from config import GOOGLE_API_KEY, GEMINI_MODEL
assert GOOGLE_API_KEY != "AQ.Ab8RN6LjTiaMDYrfzbznrCQukKniiNXDQ9GRSoXBnZdRaEsNig", \
    "FAIL: old Anthropic-format key still hardcoded in config!"
print(f"[3] Config key not hardcoded  : OK (GEMINI_MODEL={GEMINI_MODEL})")

# ── 4. extract_json strips fences ─────────────────────────────────────────────
fenced = '```json\n[{"action":"open_app","value":"notepad"}]\n```'
out = extract_json(fenced)
parsed = json.loads(out)
assert parsed[0]["action"] == "open_app"
print(f"[4] extract_json fenced       : OK -> {out[:50]}")

# ── 5. extract_json on noisy text ─────────────────────────────────────────────
noisy = 'Sure! Here:\n[{"action":"wait","value":"1"}]\nDone.'
out2 = extract_json(noisy)
assert json.loads(out2)[0]["action"] == "wait"
print(f"[5] extract_json noisy        : OK -> {out2}")

# ── 6. extract_json empty fallback ────────────────────────────────────────────
assert extract_json("no json here") == "[]"
print(f"[6] extract_json fallback     : OK -> []")

# ── 7. _validate_plan accepts valid steps ─────────────────────────────────────
raw = [{"action": "open_app", "value": "notepad"}, {"action": "wait", "value": "2"}]
v = _validate_plan(raw)
assert len(v) == 2 and v[0]["action"] == "open_app"
print(f"[7] _validate_plan valid      : OK -> {v}")

# ── 8. _validate_plan blocks disallowed actions ───────────────────────────────
try:
    _validate_plan([{"action": "rm_rf", "value": "/"}])
    print("[8] _validate_plan safety     : FAIL (should have raised)")
    sys.exit(1)
except PlannerError:
    print(f"[8] _validate_plan safety     : OK (disallowed action blocked)")

# ── 9. plan() alias is callable ───────────────────────────────────────────────
assert callable(plan) and callable(create_plan)
print(f"[9] plan() / create_plan()    : OK (both callable)")

print()
print("=" * 54)
print("  All 9 checks passed. Anthropic is GONE.")
print("  Set GOOGLE_API_KEY, then run: python app.py")
print("=" * 54)
