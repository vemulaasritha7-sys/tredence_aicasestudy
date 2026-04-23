"""
AutoHand — Flask Web Portal
============================
Serves the chat UI and provides a /run endpoint that returns the
full plan + execution log as JSON.
"""

import sys
import os
import json
import threading

from flask import Flask, request, jsonify, render_template, Response

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(__file__))

from config import FLASK_PORT, FLASK_DEBUG
from core.planner import plan, PlannerError
from agents.executor import execute

# Templates & static files live under ui/
app = Flask(
    __name__,
    template_folder=os.path.join("ui", "templates"),
    static_folder=os.path.join("ui", "static"),
)

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/run", methods=["POST"])
def run():
    """
    POST body: {"query": "Open notepad and type hello"}

    Response JSON:
    {
        "query":  str,
        "plan":   [{"action": str, "value": str}],
        "logs":   [{"step": int, "action": str, "value": str,
                    "status": str, "message": str, "elapsed_ms": int}],
        "summary": {"total": int, "success": int, "error": int}
    }
    """
    data = request.get_json(silent=True) or {}
    query = (data.get("query") or "").strip()

    if not query:
        return jsonify({"error": "No query provided"}), 400

    # ── Plan ──────────────────────────────────────────────────────────────────
    try:
        action_plan = plan(query)
    except PlannerError as e:
        return jsonify({"error": f"Planner failed: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected planner error: {e}"}), 500

    # ── Execute ───────────────────────────────────────────────────────────────
    try:
        logs = execute(action_plan)
    except Exception as e:
        return jsonify({"error": f"Executor crashed: {e}"}), 500

    logs_dicts = [l.to_dict() for l in logs]
    successes  = sum(1 for l in logs if l.status == "success")
    errors      = sum(1 for l in logs if l.status == "error")

    return jsonify({
        "query":   query,
        "plan":    action_plan,
        "logs":    logs_dicts,
        "summary": {
            "total":   len(logs),
            "success": successes,
            "error":   errors,
        },
    })


@app.route("/ping")
def ping():
    return jsonify({"status": "ok", "agent": "AutoHand"})


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"\n[AutoHand] Web Portal starting on http://localhost:{FLASK_PORT}\n")
    app.run(
        host="0.0.0.0",
        port=FLASK_PORT,
        debug=FLASK_DEBUG,
        threaded=True,
    )
