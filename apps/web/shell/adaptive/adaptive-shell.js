(() => {
  function buildPanels(runtime, memory, continuity, verification) {
    return [
      {
        id: "runtime",
        title: "Runtime Authority",
        kind: "runtime",
        importance: runtime.ok ? 0.72 : 0.92,
        urgency: runtime.ok ? 0.28 : 0.88,
        user_affinity: 0.74,
        recency: 0.8,
        body: `<div>Mode: ${runtime.mode || "unknown"}</div><div>Next: ${runtime.next_action || "n/a"}</div>`,
      },
      {
        id: "memory",
        title: "Memory Governance",
        kind: "memory",
        importance: 0.64,
        urgency: memory.ok ? 0.24 : 0.72,
        user_affinity: 0.68,
        recency: 0.72,
        body: `<div>Store valid: ${String(memory.memory_store_valid ?? "unknown")}</div><div>Warnings: ${(memory.warnings || []).join(", ") || "none"}</div>`,
      },
      {
        id: "continuity",
        title: "Continuity",
        kind: "history",
        importance: 0.66,
        urgency: continuity.ok ? 0.2 : 0.7,
        user_affinity: 0.61,
        recency: 0.69,
        body: `<div>Warnings: ${(continuity.warnings || []).join(", ") || "none"}</div>`,
      },
      {
        id: "verification",
        title: "Verification",
        kind: "verification",
        importance: verification.ok ? 0.7 : 0.9,
        urgency: verification.ok ? 0.22 : 0.76,
        user_affinity: 0.77,
        recency: 0.76,
        body: `<div>Mode: ${verification.mode || "baseline"}</div><div>Missing: ${(verification.missing || []).join(", ") || "none"}</div>`,
      },
    ];
  }

  function renderFromStore() {
    const runtime = window.NexusAdaptiveStore.get("runtime") || {};
    const memory = window.NexusAdaptiveStore.get("memory") || {};
    const continuity = window.NexusAdaptiveStore.get("continuity") || {};
    const verification = window.NexusAdaptiveStore.get("verification") || {};
    const panels = buildPanels(runtime, memory, continuity, verification);
    const placed = window.NexusAdaptiveLayout.computeLayout(panels);
    window.NexusAdaptivePanels.render(placed);
  }

  function boot() {
    ["runtime", "memory", "continuity", "verification"].forEach((key) => {
      window.NexusAdaptiveStore.subscribe(key, renderFromStore);
    });
    window.NexusAdaptiveStream.start();
    renderFromStore();
    window.addEventListener("resize", renderFromStore);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
