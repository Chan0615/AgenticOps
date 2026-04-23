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

## Incremental Migration Scripts
- `python backend/add_dataquery_menu.py` — adds 智能问数 module: creates 3 new tables (`dq_datasource`, `dq_table_metadata`, `dq_query_history`), inserts 6 menu records, assigns to admin role. Safe to run on existing DB; skips already-existing records.
- `python backend/add_server_menu.py` — migrates legacy `/server/*` menu records to `/ops/*`.
- These scripts are idempotent; running them multiple times is safe.

## Runtime Topology
- FastAPI serves REST on `http://localhost:8000`; docs at `/docs`.
- Celery worker (`celery -A celery_app worker --loglevel=info -Q salt,scheduler`) executes Salt tasks.
- Celery beat (`celery -A celery_app beat --loglevel=info`) scans enabled cron tasks every minute.
- Paramiko direct SSH is removed from Ops flows; `/api/ops/servers/test-connection` now validates through JumpServer REST API.
- Legacy local WebSocket SSH handler remains only as a deprecation stub and returns an error message.
- PostgreSQL + pgvector runs on `10.225.138.183:5432` (Docker container `pgvector`), used by RAG knowledge base module for vector storage.

## Database Architecture
- **Primary DB (MySQL)**: `kefu_ai` on `10.225.138.121:3306` via `aiomysql`. Stores all system tables (`sys_*`), ops tables (`ops_*`), agent tables (`agent_*`), dataquery tables (`dq_*`), and operation logs.
- **Vector DB (PostgreSQL + pgvector)**: `agenticops_vector` on `10.225.138.183:5432` via `asyncpg`. Stores document embeddings and vector indices for RAG knowledge base semantic search.
- pgvector connection is configured under `pgvector` key in `backend/config.yaml`. See `PGVECTOR_INSTALL.md` for deployment instructions.

## Frontend/Backend Contract
- Frontend API client (`frontend/src/api/index.ts`) uses `baseURL: '/api'`.
- Vite proxy (`frontend/vite.config.ts`) forwards `/api` to `http://localhost:8000`; backend should stay on port 8000 in local dev unless proxy is updated.
- Ops APIs are under `/api/ops/*` (`servers`, `scripts`, `tasks`, `logs`). Legacy `/api/logs` route returns a migration message.
- Dataquery APIs are under `/api/dataquery/*` (`datasources`, `chat`). The dataquery router is registered in `main.py` without `/api` prefix (sub-routers carry full prefixes).
- Legacy frontend `/server/*` pages and `/api/server/*` client are removed; `/server/*` routes now redirect to `/ops/servers`.

## Frontend Component Convention
- Ant Design Vue is **NOT** globally registered. All components must be imported per-file:
  ```typescript
  import { Button, Card, Table, Tag, message } from 'ant-design-vue'
  const FormItem = Form.Item
  const SelectOption = Select.Option
  ```
- Use `<Card>`, `<Table>`, `<Button>` (PascalCase) in templates, **NOT** `<a-card>`, `<a-table>` (kebab-case).
- Sub-components are destructured from parent: `Form.Item`, `Select.Option`, `Input.Password`, `Input.TextArea`, `Collapse.Panel`.

## Module Overview

### 智能问数 (Dataquery) — `/dataquery/*`
- **数据源管理** (`/dataquery/datasources`): CRUD for external database connections (MySQL/PostgreSQL), metadata sync, table structure browsing.
- **智能问数** (`/dataquery/chat`): NL2SQL — user asks questions in natural language, AI generates SQL, executes against selected datasource, returns results with table/chart/summary.
- Backend services: `db_connector.py` (multi-datasource connection pool), `dataquery_service.py` (NL2SQL core with SQL safety validation, chart recommendation, Excel export).
- SSE streaming protocol: `[SQL]` → `[EXECUTING]` → `[RESULT]` → summary chunks → `[DONE]`.
- SQL safety: only `SELECT`/`WITH`/`SHOW`/`DESCRIBE` allowed; `LIMIT` auto-appended for `SELECT`/`WITH` only.
- Datasource passwords stored with Base64 encoding (`db_connector.encrypt_password`).

### RAG 知识库 — `/rag/*`
- Current state: two disconnected implementations exist (API-driven SQL LIKE search vs standalone FAISS in `agents.py`).
- Frontend KnowledgeBase.vue calls non-existent `/v1/common/knowledge/*` endpoints — page is non-functional.
- Frontend Chat.vue works for basic Q&A but does not pass `kb_id`, so retrieval is never triggered.
- Planned upgrade: migrate to pgvector, add LangChain Vector Store, hybrid retrieval (vector + BM25), LLM semantic chunking, conversation memory, PDF/Word/Markdown/TXT file upload.

## Verification Reality
- No backend test suite or CI workflow is present in repo.
- Frontend `npm run build` runs `vite build` and is the reliable packaging check.
- Frontend type check is separate: `npm run typecheck` (`vue-tsc --noEmit`) and currently reports many existing type issues.
- `npm run lint` exists, but no ESLint config file is committed; expect to add/configure ESLint before relying on lint output.
