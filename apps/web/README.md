# Web App Shell Reference

This directory now contains a controlled donor pull of the Nexus0.5 shell reference.

Scope rules applied:
- Donor source: NEXUS0.5 archive only
- Landing area: apps/web only
- Purpose: UI shell reference only
- Status: adapted for standalone local reference

Implemented reference shell files:
- shell/index.html
- shell/shell.css
- shell/shell.js
- shell/tokens.css
- shell/adaptive/*

These files are intentionally framework-free and not wired to production runtime APIs.

## Run Local Web Shell
```bash
python -m apps.web.app
```

Default bind:
- http://127.0.0.1:8090

Foundation intent:
- sparse workspace-first shell
- premium visual direction with minimal clutter
- control surface centered on composer and summoned surfaces
