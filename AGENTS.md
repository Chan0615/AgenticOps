# AgenticOps Agent Notes

## Verified Entrypoints
- Backend app entrypoint is `backend/app/main.py`; run `uvicorn app.main:app --reload --port 8000` from `backend/`.
- Avoid `python backend/main.py` for new work; it uses different imports than `backend/app/main.py` and can drift.
- Frontend entrypoint is `frontend/src/main.ts`; dev server is Vite on `5173`.

## Required Local Setup
- `backend/app/core/config.py` loads `backend/config.yaml` at import time and raises `FileNotFoundError` if missing.
- First-time setup order: copy `backend/config.yaml.example` -> create/edit `backend/config.yaml` -> install deps -> start services.
- `backend/config.yaml` is gitignored; do not commit env-specific credentials.
- Ops server connectivity now depends on JumpServer API config (`jumpserver.base_url`, auth fields, `org_id`) in `backend/config.yaml`.
- For existing DBs upgraded from legacy UI, run `python backend/add_server_menu.py` once to migrate `/server/*` menu records to `/ops/*`.

## High-Risk Commands
- `python backend/init_db.py` is destructive by default (`force_reset=True`): drops all tables, recreates schema, reseeds data.
- Seeded admin credentials after reset are `admin / admin123`.

## Runtime Topology
- FastAPI serves REST on `http://localhost:8000`; docs at `/docs`.
- Celery worker (`celery -A celery_app worker --loglevel=info -Q salt,scheduler`) executes Salt tasks.
- Celery beat (`celery -A celery_app beat --loglevel=info`) scans enabled cron tasks every minute.
- Paramiko direct SSH is removed from Ops flows; `/api/ops/servers/test-connection` now validates through JumpServer REST API.
- Legacy local WebSocket SSH handler remains only as a deprecation stub and returns an error message.

## Frontend/Backend Contract
- Frontend API client (`frontend/src/api/index.ts`) uses `baseURL: '/api'`.
- Vite proxy (`frontend/vite.config.ts`) forwards `/api` to `http://localhost:8000`; backend should stay on port 8000 in local dev unless proxy is updated.
- Ops APIs are under `/api/ops/*` (`servers`, `scripts`, `tasks`, `logs`). Legacy `/api/logs` route returns a migration message.
- Legacy frontend `/server/*` pages and `/api/server/*` client are removed; `/server/*` routes now redirect to `/ops/servers`.

## Verification Reality
- No backend test suite or CI workflow is present in repo.
- Frontend `npm run build` runs `vite build` and is the reliable packaging check.
- Frontend type check is separate: `npm run typecheck` (`vue-tsc --noEmit`) and currently reports many existing type issues.
- `npm run lint` exists, but no ESLint config file is committed; expect to add/configure ESLint before relying on lint output.
