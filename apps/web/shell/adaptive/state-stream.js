(() => {
  function injectDemoState() {
    window.NexusAdaptiveStore.merge("runtime", {
      ok: true,
      mode: "reference",
      next_action: "wire runtime API later",
    });
    window.NexusAdaptiveStore.merge("memory", {
      ok: true,
      memory_store_valid: true,
      warnings: [],
    });
    window.NexusAdaptiveStore.merge("continuity", {
      ok: true,
      warnings: ["checkpoint logic scaffold only"],
    });
    window.NexusAdaptiveStore.merge("verification", {
      ok: false,
      mode: "placeholder",
      missing: ["live backend integration"],
    });
  }

  window.NexusAdaptiveStream = {
    start() {
      injectDemoState();
      setInterval(injectDemoState, 15000);
    },
  };
})();
