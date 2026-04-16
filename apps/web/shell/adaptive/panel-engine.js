(() => {
  const rootId = "nexus-adaptive-root";

  function semanticClass(panel) {
    if ((panel.urgency || 0) >= 0.8) return "urgent";
    if ((panel.importance || 0) >= 0.75) return "important";
    if ((panel.kind || "") === "verification") return "verification";
    if ((panel.kind || "") === "memory") return "memory";
    return "normal";
  }

  function ensureRoot() {
    let root = document.getElementById(rootId);
    if (!root) {
      root = document.createElement("div");
      root.id = rootId;
      document.body.appendChild(root);
    }
    return root;
  }

  function renderPanel(panel) {
    const div = document.createElement("section");
    div.className = `nexus-panel ${semanticClass(panel)}`;
    div.dataset.panelId = panel.id;
    div.style.left = `${panel.x}px`;
    div.style.top = `${panel.y}px`;
    div.style.width = `${panel.size.w}px`;
    div.style.height = `${panel.size.h}px`;
    div.style.zIndex = String(100 + Math.round(panel.score * 100));

    div.innerHTML = `
      <header class="nexus-panel-header">
        <div>
          <div class="nexus-panel-title">${panel.title}</div>
          <div class="nexus-panel-subtitle">${panel.zone} | score ${panel.score.toFixed(2)}</div>
        </div>
        <div class="nexus-panel-badges">
          <span>${Math.round((panel.importance || 0) * 100)}I</span>
          <span>${Math.round((panel.urgency || 0) * 100)}U</span>
        </div>
      </header>
      <div class="nexus-panel-body">${panel.body || ""}</div>
    `;
    return div;
  }

  function render(panelsById) {
    const root = ensureRoot();
    root.innerHTML = "";
    Object.values(panelsById).forEach((panel) => root.appendChild(renderPanel(panel)));
  }

  window.NexusAdaptivePanels = { render };
})();
