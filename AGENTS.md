# AgenticOps Repository Guidelines

## Project Overview
Full-stack platform: FastAPI + Vue3 + MySQL + Redis with RAG knowledge base and server management features.

## Directory Structure
- `backend/` - FastAPI backend services
- `frontend/` - Vue 3 frontend application

## Development Commands

### Backend (Python)
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Initialize database
python init_db.py

# Start FastAPI server
python main.py
# OR
uvicorn app.main:app --reload --port 8000

# Start WebSocket SSH server (separate terminal)
python -m app.api.server.websocket_handler
```

### Frontend (Node.js/Vue)
```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm run dev
```

### Testing & Quality
- Lint frontend: `npm run lint` (in frontend directory)
- Build frontend: `npm run build` (in frontend directory)

## Environment Setup
1. Copy `backend/config.yaml.example` to `backend/config.yaml`
2. Edit config.yaml with database, Redis, and AI service credentials
3. Ensure MySQL 8.0+ and Redis 6.0+ are running

## Important Notes
- WebSocket SSH server runs on port 8765 (separate from main API on 8000)
- Frontend dev server runs on port 5173
- API documentation available at http://localhost:8000/docs after backend starts
- For production builds: npm run build in frontend, then deploy dist/ folder

## Frontend-Specific Notes
- Server list table (`frontend/src/views/ops/ServerList.vue`): ID column removed, description column width constrained with ellipsis/tooltip for hover details, action column fixed to right with sufficient width and tag-based actions (blue for test, default for edit, red for delete)
- Main layout (`frontend/src/layouts/MainLayout.vue`): Removed "智能知识库平台" subtitle from header