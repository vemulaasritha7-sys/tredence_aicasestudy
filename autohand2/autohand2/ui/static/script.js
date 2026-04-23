/**
 * AutoHand — script.js
 * Handles chat UI logic: sending queries, rendering responses, animations.
 */

// ─── DOM Refs ─────────────────────────────────────────────────────────────────
const messagesEl      = document.getElementById("messages");
const queryInput      = document.getElementById("queryInput");
const sendBtn         = document.getElementById("sendBtn");
const typingIndicator = document.getElementById("typingIndicator");
const statusDot       = document.getElementById("statusDot");
const statusText      = document.getElementById("statusText");
const btnClear        = document.getElementById("btnClear");
const planSteps       = document.getElementById("planSteps");
const planStepCount   = document.getElementById("planStepCount");
const statTotal       = document.getElementById("statTotal");
const statSuccess     = document.getElementById("statSuccess");
const statError       = document.getElementById("statError");
const statTime        = document.getElementById("statTime");

// ─── Action Icons Map ─────────────────────────────────────────────────────────
const ACTION_ICONS = {
  open_app:          "🚀",
  type_text:         "⌨️",
  press_keys:        "🔑",
  save_file:         "💾",
  create_excel_file: "📊",
  create_text_file:  "📄",
  open_vscode:       "💻",
  write_code:        "🖊️",
  take_screenshot:   "📸",
  wait:              "⏳",
};

function actionIcon(action) {
  return ACTION_ICONS[action] || "⚙️";
}

// ─── Status Helpers ───────────────────────────────────────────────────────────
function setStatus(state, text) {
  statusDot.className = `status-dot ${state}`;
  statusText.textContent = text;
}

// ─── Auto-resize textarea ─────────────────────────────────────────────────────
queryInput.addEventListener("input", () => {
  queryInput.style.height = "auto";
  queryInput.style.height = Math.min(queryInput.scrollHeight, 140) + "px";
});

// ─── Send on Enter (Shift+Enter for newline) ──────────────────────────────────
queryInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    send();
  }
});
sendBtn.addEventListener("click", send);

// ─── Quick task buttons ───────────────────────────────────────────────────────
document.querySelectorAll(".quick-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    queryInput.value = btn.dataset.query;
    queryInput.style.height = "auto";
    queryInput.focus();
    send();
  });
});

// ─── Clear chat ───────────────────────────────────────────────────────────────
btnClear.addEventListener("click", () => {
  // Keep only the welcome message
  const kids = [...messagesEl.children];
  kids.forEach((k) => { if (k.id !== "welcomeMsg") k.remove(); });
  resetSidebar();
});

function resetSidebar() {
  planSteps.innerHTML = '<p class="empty-state">No plan yet. Send a query to get started.</p>';
  planStepCount.textContent = "";
  statTotal.textContent = "—";
  statSuccess.textContent = "—";
  statError.textContent = "—";
  statTime.textContent = "—";
}

// ─── scrollToBottom ───────────────────────────────────────────────────────────
function scrollToBottom() {
  messagesEl.scrollTo({ top: messagesEl.scrollHeight, behavior: "smooth" });
}

// ─── Timestamp helper ─────────────────────────────────────────────────────────
function timeNow() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

// ─── Append user bubble ───────────────────────────────────────────────────────
function appendUserMessage(text) {
  const div = document.createElement("div");
  div.className = "message user-message";
  div.innerHTML = `
    <div class="message-avatar">👤</div>
    <div class="message-body">
      <div class="message-bubble">${escapeHtml(text)}</div>
      <div class="message-meta">You • ${timeNow()}</div>
    </div>`;
  messagesEl.appendChild(div);
  scrollToBottom();
}

// ─── Append agent bubble ──────────────────────────────────────────────────────
function appendAgentMessage(content) {
  const div = document.createElement("div");
  div.className = "message agent-message";
  div.innerHTML = `
    <div class="message-avatar">🤖</div>
    <div class="message-body">
      <div class="message-bubble">${content}</div>
      <div class="message-meta">AutoHand • ${timeNow()}</div>
    </div>`;
  messagesEl.appendChild(div);
  scrollToBottom();
  return div;
}

// ─── Build plan HTML (chat bubble) ───────────────────────────────────────────
function buildPlanHtml(plan) {
  const rows = plan.map((step, i) =>
    `<div class="plan-step-row" id="psr-${i}">
      <div class="step-num">${i + 1}</div>
      <div class="step-content">
        <div class="step-action">${escapeHtml(step.action)}</div>
        <div class="step-value">${escapeHtml(step.value || "—")}</div>
      </div>
      <div class="step-status" id="pss-${i}">⏳</div>
    </div>`
  ).join("");

  return `<div class="plan-bubble">
    <div class="plan-bubble-title">📋 Execution Plan (${plan.length} steps)</div>
    ${rows}
  </div>`;
}

// ─── Build log HTML ───────────────────────────────────────────────────────────
function buildLogHtml(logs) {
  const rows = logs.map((log) => {
    const statusClass = log.status === "success" ? "log-ok" : "log-err";
    const icon = log.status === "success" ? "✅" : "❌";
    return `<div class="log-entry">
      <span class="log-step">[${log.step}]</span>
      <span class="log-action">${escapeHtml(log.action)}</span>
      <span class="log-msg ${statusClass}">${icon} ${escapeHtml(log.message)}</span>
    </div>`;
  }).join("");

  return `<div class="log-bubble">${rows}</div>`;
}

// ─── Update sidebar plan panel ────────────────────────────────────────────────
function renderSidebarPlan(plan) {
  planStepCount.textContent = `${plan.length} steps`;
  planSteps.innerHTML = plan.map((step, i) =>
    `<div class="sidebar-step" id="ss-${i}">
      <span class="ss-num">${i + 1}</span>
      <span class="ss-action">${actionIcon(step.action)} ${step.action}</span>
    </div>`
  ).join("");
}

// ─── Animate execution steps in sidebar ──────────────────────────────────────
async function animateExecution(logs) {
  for (const log of logs) {
    const idx  = log.step - 1;
    const ssEl = document.getElementById(`ss-${idx}`);
    const psrEl = document.getElementById(`psr-${idx}`);
    const pssEl = document.getElementById(`pss-${idx}`);

    if (ssEl)  ssEl.className  = "sidebar-step running";
    if (psrEl) psrEl.className = "plan-step-row running";

    await sleep(120);

    const cls = log.status === "success" ? "success" : "error";
    const icon = log.status === "success" ? "✅" : "❌";

    if (ssEl)  ssEl.className  = `sidebar-step ${cls}`;
    if (psrEl) psrEl.className = `plan-step-row ${cls}`;
    if (pssEl) pssEl.textContent = icon;

    await sleep(80);
  }
}

// ─── Update stats panel ───────────────────────────────────────────────────────
function renderStats(summary, durationMs) {
  statTotal.textContent   = summary.total;
  statSuccess.textContent = summary.success;
  statError.textContent   = summary.error;
  statTime.textContent    = `${(durationMs / 1000).toFixed(1)}s`;
}

function setLoading(isLoading) {
  sendBtn.disabled = isLoading;
  typingIndicator.hidden = !isLoading;
  if (isLoading) {
    setStatus("busy", "Working…");
  } else {
    setStatus("", "Ready");
  }
}

// ─── Main send function ───────────────────────────────────────────────────────
function send() {
  const query = queryInput.value.trim();
  if (!query) return;

  // UI: reset input
  queryInput.value = "";
  queryInput.style.height = "auto";

  appendUserMessage(query);
  scrollToBottom();

  const t0 = Date.now();
  
  setLoading(true); // START LOADING

  fetch("/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  })
  .then(resp => resp.json())
  .then(async data => {
    
    if (data.error) {
      appendAgentMessage(`<p>⚠️ <strong>Error:</strong> ${escapeHtml(data.error)}</p>`);
      setLoading(false);
    } else {
      renderSidebarPlan(data.plan || []);

      const agentMsgEl = appendAgentMessage(
        `<p>✅ Execution initialized!</p>` + buildPlanHtml(data.plan || [])
      );
      
      setLoading(false); // Hide thinking indicator, UI is now animating

      const bubble = agentMsgEl.querySelector(".message-bubble");
      
      if (data.logs && data.logs.length > 0) {
          await animateExecution(data.logs);
          bubble.insertAdjacentHTML("beforeend", buildLogHtml(data.logs));
          
          const strSummaryColor = data.summary.error === 0 ? "var(--success)" : "var(--error)";
          bubble.insertAdjacentHTML(
            "beforeend", `<p style="margin-top:10px; font-weight: bold; color: ${strSummaryColor}">` +
            (data.summary.error === 0 ? "✨ All actions completed successfully!" : `⚠️ Finished with errors.`) +
            `</p>`
          );
          
          renderStats(data.summary, Date.now() - t0);
      }
      
      scrollToBottom();
    }
  })
  .catch(err => {
    appendAgentMessage(`<p>🔴 <strong>Network error:</strong> ${escapeHtml(err.message)}</p>`);
    
    setLoading(false); // END LOADING (ERROR)
  });
}

// ─── Utilities ────────────────────────────────────────────────────────────────
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}
