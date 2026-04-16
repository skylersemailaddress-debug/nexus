const composerInput = document.getElementById("composerInput");
const sendButton = document.getElementById("sendButton");
const uploadButton = document.getElementById("uploadButton");
const hiddenUpload = document.getElementById("hiddenUpload");
const helpDrawer = document.getElementById("helpDrawer");
const contextTitle = document.getElementById("contextTitle");
const shellModePill = document.getElementById("shellModePill");
const workspaceStateBadge = document.getElementById("workspaceStateBadge");
const systemStateBadge = document.getElementById("systemStateBadge");
const workspaceStatusPanel = document.getElementById("workspaceStatusPanel");
const systemStatusPanel = document.getElementById("systemStatusPanel");
const activityFeed = document.getElementById("activityFeed");
const workspaceRoot = "./";
const apiBaseUrl = "http://127.0.0.1:8085";
const workspaceStatusPath = "/workspace/status";
const sessionStatusPath = "/session/status";
const sessionCommandPath = "/session/command";
const activityLog = [];

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function statusCard(title, value, detail) {
  return `
    <article class="status-card">
      <strong>${escapeHtml(title)}</strong>
      <p>${escapeHtml(value)}</p>
      ${detail ? `<p>${escapeHtml(detail)}</p>` : ""}
    </article>
  `;
}

function renderActivity() {
  activityFeed.innerHTML = activityLog
    .map(
      (entry) => `
        <li class="activity-item">
          <strong>${escapeHtml(entry.title)}</strong>
          <p>${escapeHtml(entry.detail)}</p>
        </li>
      `,
    )
    .join("");
}

function pushActivity(title, detail) {
  activityLog.unshift({ title, detail });
  activityLog.splice(4);
  renderActivity();
}

function renderWorkspaceStatus(payload) {
  const runtime = payload.runtime || {};
  const control = payload.control || {};
  const execution = payload.execution || {};
  const sessionStatus = payload.session_status || {};
  const sessionControl = sessionStatus.control || {};
  const sessionExecution = sessionStatus.execution || {};

  contextTitle.textContent = payload.session?.objective || runtime.objective || "Nexus Build";
  workspaceStateBadge.textContent = runtime.workspace_status || "idle";
  systemStateBadge.textContent = payload.ok ? "ready" : "blocked";
  shellModePill.textContent = payload.ok ? "Linked" : "Offline";

  workspaceStatusPanel.innerHTML = [
    statusCard("Objective", runtime.objective || "Nexus build workspace", runtime.next_action || "Awaiting next action."),
    statusCard("Execution", execution.status || "planned", `${execution.task_count || 0} tasks in run ${execution.run_id || "run-idle"}`),
    statusCard("Control", control.control_status || "stable", `Checkpoint ${control.checkpoint_status || "primed"}`),
    statusCard("Session Phase", sessionExecution.phase || "intake", `Approval ${sessionControl.approval_status || "clear"}`),
  ].join("");

  systemStatusPanel.innerHTML = [
    statusCard("API Version", payload.version || "unknown", payload.service || "nexus-api"),
    statusCard("Readiness", payload.ok ? "ready" : "blocked", `Session ${runtime.session_id || "local-shell"}`),
    statusCard("Workspace Root", workspaceRoot, runtime.updated_at || "pending"),
  ].join("");
}

function renderSessionStatus(payload) {
  const session = payload.session || {};
  contextTitle.textContent = session.objective || contextTitle.textContent || "Nexus Build";
  workspaceStateBadge.textContent = session.workspace_status || "idle";
}

function renderCommandSession(payload) {
  const request = payload.request || {};
  const response = payload.response || {};
  const session = payload.session || {};
  const control = payload.control || {};
  const execution = payload.execution || {};

  contextTitle.textContent = session.objective || "Nexus Build";
  workspaceStateBadge.textContent = session.workspace_status || "active";
  shellModePill.textContent = payload.ok ? "Linked" : "Offline";
  systemStateBadge.textContent = payload.ok ? "ready" : "blocked";

  workspaceStatusPanel.innerHTML = [
    statusCard("Request", request.command || "noop", request.command_id || "cmd-0000"),
    statusCard("Response", response.message || "No response", response.echo || ""),
    statusCard("Session", `Commands ${session.command_count || 0}`, session.next_action || "Awaiting next action."),
    statusCard("Execution", execution.status || "queued", `${execution.run_id || "run-command"} / ${execution.task_id || "task-command"}`),
    statusCard("Control", control.command_status || "accepted", `Review required: ${control.review_required ? "yes" : "no"}`),
  ].join("");
}

function renderSystemFallback(health, readiness, version) {
  shellModePill.textContent = "Linked";
  systemStateBadge.textContent = readiness.status || "ready";
  systemStatusPanel.innerHTML = [
    statusCard("API Health", health.status || "healthy", health.service || "nexus-api"),
    statusCard("Readiness", readiness.status || "ready", readiness.ok ? "Accepting shell requests." : "Not ready."),
    statusCard("Version", version.version || "unknown", "Core surface response."),
  ].join("");
}

function renderOfflineState() {
  shellModePill.textContent = "Offline";
  workspaceStateBadge.textContent = "local";
  systemStateBadge.textContent = "offline";
  workspaceStatusPanel.innerHTML = [
    statusCard("Objective", contextTitle.textContent || "Nexus Build", "API unavailable. Local shell remains interactive."),
    statusCard("Execution", "waiting", "Start the API service to link runtime state."),
    statusCard("Control", "local-only", "No remote status surface detected."),
  ].join("");
  systemStatusPanel.innerHTML = [
    statusCard("API Surface", "offline", "Expected at http://127.0.0.1:8085."),
  ].join("");
}

async function fetchJson(path) {
  const response = await fetch(`${apiBaseUrl}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed for ${path} with ${response.status}`);
  }
  return response.json();
}

async function postJson(path, payload) {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error(`Request failed for ${path} with ${response.status}`);
  }
  return response.json();
}

async function refreshWorkspaceStatus(objective) {
  try {
    const [health, readiness, version, session, workspace] = await Promise.all([
      fetchJson("/health"),
      fetchJson("/readiness"),
      fetchJson("/version"),
      fetchJson(`${sessionStatusPath}${objective ? `?objective=${encodeURIComponent(objective)}` : ""}`),
      fetchJson(`${workspaceStatusPath}${objective ? `?objective=${encodeURIComponent(objective)}` : ""}`),
    ]);
    renderSystemFallback(health, readiness, version);
    renderSessionStatus(session);
    renderWorkspaceStatus(workspace);
    pushActivity("Workspace linked", session.session?.objective || workspace.session?.objective || "Nexus build workspace");
  } catch (_) {
    renderOfflineState();
    pushActivity("Shell running locally", "API status surface not reachable.");
  }
}

async function submitCommand(command) {
  try {
    const [health, readiness, version, commandSession] = await Promise.all([
      fetchJson("/health"),
      fetchJson("/readiness"),
      fetchJson("/version"),
      postJson(sessionCommandPath, { command }),
    ]);
    renderSystemFallback(health, readiness, version);
    renderCommandSession(commandSession);
    pushActivity("Command submitted", `${commandSession.request?.command_id || "cmd"}: ${command}`);
  } catch (_) {
    renderOfflineState();
    pushActivity("Command failed", "API command/session surface not reachable.");
  }
}

function sendPrompt(seed) {
  const prompt = seed || composerInput.value.trim();
  if (!prompt) return;
  composerInput.value = "";
  submitCommand(prompt);
}

sendButton.addEventListener("click", () => sendPrompt());
composerInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    sendPrompt();
  }
});

document.querySelectorAll("[data-seed]").forEach((button) => {
  button.addEventListener("click", () => sendPrompt(button.dataset.seed));
});

document
  .querySelector('[data-action="show-help"]')
  .addEventListener("click", () => helpDrawer.classList.remove("hidden"));
document
  .querySelector('[data-action="close-help"]')
  .addEventListener("click", () => helpDrawer.classList.add("hidden"));

uploadButton.addEventListener("click", () => hiddenUpload.click());
hiddenUpload.addEventListener("change", () => {
  const file = hiddenUpload.files && hiddenUpload.files[0];
  if (!file) return;
  pushActivity("Uploaded asset", file.name);
  refreshWorkspaceStatus(`Review uploaded file ${file.name}`);
});

pushActivity("Shell booted", "Linking system and workspace surfaces.");
refreshWorkspaceStatus();
