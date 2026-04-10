# AgenticOps Agent Notes

## Verified Entrypoints
- Backend app entrypoint is `backend/app/main.py`; run `uvicorn app.main:app --reload --port 8000` from `backend/`.
- Avoid `python backend/main.py` for new work; it uses different imports than `backend/app/main.py` and can drift.
- Frontend entrypoint is `frontend/src/main.ts`; dev server is Vite on `5173`.

## Required Local Setup
- `backend/app/core/config.py` loads `backend/config.yaml` at import time and raises `FileNotFoundError` if missing.
- First-time setup order: copy `backend/config.yaml.example` -> create/edit `backend/config.yaml` -> install deps -> start services.
- `backend/config.yaml` is gitignored; do not commit env-specific credentials.

## High-Risk Commands
- `python backend/init_db.py` is destructive by default (`force_reset=True`): drops all tables, recreates schema, reseeds data.
- Seeded admin credentials after reset are `admin / admin123`.

## Runtime Topology
- FastAPI serves REST on `http://localhost:8000`; docs at `/docs`.
- Web SSH is a separate websocket process on `ws://localhost:8765` (not mounted in FastAPI).
- `python -m app.api.server.websocket_handler` does not start the websocket server by itself (module has no `__main__` runner).
- Use: `python -c "from app.api.server.websocket_handler import start_websocket_server; start_websocket_server()"`.

## Frontend/Backend Contract
- Frontend API client (`frontend/src/api/index.ts`) uses `baseURL: '/api'`.
- Vite proxy (`frontend/vite.config.ts`) forwards `/api` to `http://localhost:8000`; backend should stay on port 8000 in local dev unless proxy is updated.
- Ops APIs are under `/api/ops/*` (`servers`, `scripts`, `tasks`, `logs`). Legacy `/api/logs` route returns a migration message.

## Verification Reality
- No backend test suite or CI workflow is present in repo.
- Frontend `npm run build` (`vue-tsc -b && vite build`) is the most reliable full check.
- `npm run lint` exists, but no ESLint config file is committed; expect to add/configure ESLint before relying on lint output.
