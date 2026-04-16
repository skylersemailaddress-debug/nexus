(() => {
  const ZONES = {
    top: { x: 0.5, y: 0.1 },
    left: { x: 0.18, y: 0.5 },
    center: { x: 0.5, y: 0.5 },
    right: { x: 0.82, y: 0.5 },
    bottom: { x: 0.5, y: 0.88 },
  };

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function scorePanel(panel) {
    return (
      (panel.importance || 0) * 0.4 +
      (panel.urgency || 0) * 0.3 +
      (panel.user_affinity || 0) * 0.2 +
      (panel.recency || 0) * 0.1
    );
  }

  function inferZone(panel) {
    const workflow = panel.workflow || "monitoring";
    if (panel.urgency >= 0.75) return "center";
    if (panel.kind === "runtime" || panel.kind === "verification") return "top";
    if (panel.kind === "signals" || workflow === "investigating") return "left";
    if (panel.kind === "actions" || panel.kind === "approvals") return "right";
    if (panel.kind === "memory" || panel.kind === "history") return "bottom";
    return "center";
  }

  function computeSize(score) {
    const w = clamp(260 + score * 420, 260, 640);
    const h = clamp(180 + score * 280, 180, 460);
    return { w: Math.round(w), h: Math.round(h) };
  }

  function computeLayout(panels, viewport = { width: window.innerWidth, height: window.innerHeight }) {
    const sorted = [...panels].sort((a, b) => scorePanel(b) - scorePanel(a));
    const buckets = { top: [], left: [], center: [], right: [], bottom: [] };
    for (const p of sorted) buckets[inferZone(p)].push(p);

    const placed = {};
    for (const [zone, items] of Object.entries(buckets)) {
      items.forEach((panel, idx) => {
        const zoneAnchor = ZONES[zone];
        const score = scorePanel(panel);
        const size = computeSize(score);
        const spread = 140;
        let x = zoneAnchor.x * viewport.width - size.w / 2;
        let y = zoneAnchor.y * viewport.height - size.h / 2;

        if (zone === "left" || zone === "right") {
          y += (idx - (items.length - 1) / 2) * spread;
        } else {
          x += (idx - (items.length - 1) / 2) * spread;
        }

        placed[panel.id] = {
          ...panel,
          score,
          zone,
          size,
          x: Math.round(clamp(x, 16, viewport.width - size.w - 16)),
          y: Math.round(clamp(y, 16, viewport.height - size.h - 16)),
        };
      });
    }
    return placed;
  }

  window.NexusAdaptiveLayout = {
    computeLayout,
    scorePanel,
    inferZone,
  };
})();
