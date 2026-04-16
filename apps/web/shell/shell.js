const composerInput = document.getElementById("composerInput");
const sendButton = document.getElementById("sendButton");
const uploadButton = document.getElementById("uploadButton");
const hiddenUpload = document.getElementById("hiddenUpload");
const surfaceLayer = document.getElementById("surfaceLayer");
const helpDrawer = document.getElementById("helpDrawer");
const contextTitle = document.getElementById("contextTitle");

function makeSurface(title, body) {
  const section = document.createElement("section");
  section.className = "surface card";
  section.innerHTML = `
    <div class="surface-header">
      <h2>${title}</h2>
      <button class="ghost-button" data-action="dismiss-surface">Dismiss</button>
    </div>
    <div class="surface-stack">${body}</div>
  `;
  section
    .querySelector('[data-action="dismiss-surface"]')
    .addEventListener("click", () => section.remove());
  return section;
}

function runObjective(prompt) {
  contextTitle.textContent = prompt || "Nexus Build";
  const body = `
    <div class="mini-surface"><strong>Objective</strong><p>${prompt}</p></div>
    <div class="mini-surface"><strong>Status</strong><p>Reference mode. Runtime wiring intentionally disabled in donor pull.</p></div>
  `;
  surfaceLayer.prepend(makeSurface("Execution Surface", body));
}

function sendPrompt(seed) {
  const prompt = seed || composerInput.value.trim();
  if (!prompt) return;
  composerInput.value = "";
  runObjective(prompt);
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
  runObjective(`Uploaded: ${file.name}`);
});
