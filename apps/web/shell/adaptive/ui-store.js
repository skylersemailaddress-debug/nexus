(() => {
  const listeners = new Map();
  const state = {
    runtime: {},
    memory: {},
    continuity: {},
    verification: {},
    signals: [],
    approvals: [],
    panels: {},
    preferences: {
      lockedPanels: {},
      pinnedPanels: {},
      affinity: {},
      attentionZones: {},
    },
    workflow: {
      mode: "monitoring",
      updatedAt: new Date().toISOString(),
    },
  };

  function notify(key) {
    const subs = listeners.get(key) || [];
    for (const fn of subs) fn(get(key));
  }

  function get(key) {
    return state[key];
  }

  function set(key, value) {
    state[key] = value;
    notify(key);
  }

  function merge(key, patch) {
    state[key] = { ...(state[key] || {}), ...(patch || {}) };
    notify(key);
  }

  function subscribe(key, fn) {
    if (!listeners.has(key)) listeners.set(key, []);
    listeners.get(key).push(fn);
    fn(get(key));
    return () => {
      const arr = listeners.get(key) || [];
      listeners.set(
        key,
        arr.filter((x) => x !== fn),
      );
    };
  }

  window.NexusAdaptiveStore = {
    state,
    get,
    set,
    merge,
    subscribe,
  };
})();
