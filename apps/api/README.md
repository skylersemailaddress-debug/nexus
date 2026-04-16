# API App

Minimal deterministic local API foundation for Nexus.

## Endpoints
- GET /health
- GET /readiness
- GET /version

## Run Local API
```bash
python -m apps.api.app
```

Default bind:
- http://127.0.0.1:8085

Behavior notes:
- endpoint payloads are deterministic JSON
- readiness is a strict boolean state
