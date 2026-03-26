# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Math PISA Bot — a Telegram Mini App for school-level math learning based on the PISA assessment model.

- User-facing language: **Kazakh**. Engineering language: English.
- Formula format: LaTeX (`$...$` inline, `$$...$$` block), rendered with KaTeX.
- Core stack: React 18 + Vite 5 + TailwindCSS 3, FastAPI + SQLAlchemy 2 + Pydantic 2, aiogram 3, Groq (llama-3.3-70b via OpenAI SDK), SQLite.
- No test suite exists. No linting/formatting configs.

## Local Development Commands

```bash
# Backend (API docs at localhost:8000/docs) — must run from backend/
cd backend && source .venv/bin/activate && pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend — Vite dev server on :3000, proxies /api → localhost:8000
cd frontend && npm install && npm run dev

# Bot
cd bot && pip install -r requirements.txt && python main.py

# Admin panel — Vite dev server on :5174
cd admin && npm install && npm run dev

# Docker (all services: frontend :3000, backend :8000, admin :5174)
docker-compose up --build
```

### Deployment

```bash
# Frontend — Cloudflare Pages
cd frontend && npm run build && npm run pages:deploy
```

## Architecture

### Four services

- **frontend/** — Telegram Mini App. React + Zustand + axios. Sends `X-Telegram-Init-Data` header on every API request (interceptor in `src/api/client.js`). Deployed via Cloudflare Pages.
- **backend/** — FastAPI REST API. All routes under `/api/`. Thin routers → `app/services/` for business logic. SQLite DB auto-creates, migrates columns, and seeds data on startup (`create_tables()` in lifespan).
- **bot/** — aiogram 3 long-polling bot. Communicates with backend via httpx. Runs hourly `notification_loop` background task for engagement reminders.
- **admin/** — Separate React app (React 18 + Vite + Tailwind + Recharts + react-hook-form/zod). JWT auth against `/api/admin/login`. Manages theory content, problems, tests, users, broadcasts.

### Backend internals

- **AI service** (`app/services/gemini_service.py`): Filename is misleading — actually uses **Groq API** via `AsyncOpenAI(base_url="https://api.groq.com/openai/v1")`. Model: `llama-3.3-70b-versatile`, temp 0.3, max 1000 tokens. System prompt enforces Kazakh-only math responses with jailbreak detection.
- **Database** (`app/database/database.py`): `create_tables()` on startup: create all tables → `_migrate_sqlite()` (ALTER TABLE for missing columns) → seed admin user from env → seed test bank → seed 4 PISA theory topics. All idempotent.
- **Auth** (`app/utils/auth.py`): Admin JWT (HS256, 12h expiry). Password hashing: SHA256 with JWT_SECRET_KEY as pepper. No Telegram initData validation on backend — trusts frontend header.
- **Progress** (`app/services/progress_service.py`): `get_or_create_user()`, `update_streak()` (increment if active yesterday, reset if >1 day gap), `calculate_user_score()` (sum of test percentages).
- **Models**: User, Problem, AdminTestQuestion, TheoryContent (JSON blocks), TestResult, Progress, ChatHistory, BroadcastLog, AdminUser. User → TestResult/Progress have cascade delete. ChatHistory has no FK.

### Backend API routes (`/api/`)

| Group | Key endpoints |
|-------|--------------|
| `/users` | `POST /register`, `GET /{id}/avatar` (proxies Telegram API), `POST /level`, `GET /inactive` |
| `/theory` | `GET /topics` (4 PISA domains), `GET /topics/{id}` (hardcoded subtopics + formulas) |
| `/problems` | `GET /` (filter by difficulty/topic), `POST /{id}/check` (normalizes comma→period, case-insensitive) |
| `/tests` | `GET /daily` (date-seeded deterministic set), `GET /random`, `POST /submit` (calculates XP + streak + daily bonus 50xp) |
| `/progress` | `GET /{telegram_id}`, `POST /update` |
| `/rating` | `GET /leaderboard?period=week\|month` (aggregates test percentages), `GET /rank/{id}` |
| `/ai` | `POST /ask` (with jailbreak check), `GET /history/{id}`, `DELETE /history/{id}`, `POST /hint` |
| `/admin` | JWT-protected. Full CRUD for problems/tests/theory/users. `POST /broadcast`, `GET /stats`, `POST /problems/bulk` (CSV import). |

### Frontend internals

- **State**: `store/userStore.js` (user + isAuthenticated), `store/progressStore.js` (topics cache, score, streak). Zustand, no persist middleware.
- **API layer**: `src/api/client.js` (axios, baseURL from `VITE_API_URL` or `/api`, 15s timeout, auto-attaches Telegram initData). Individual API modules in `src/api/` for each domain.
- **FormulaRenderer** (`src/components/FormulaRenderer.jsx`): Core component used across 5+ pages. Regex-parses mixed text+LaTeX (`$$...$$`, `$...$`, `\[...\]`, `\(...\)`). Has `glow` prop for styled display.
- **Telegram SDK**: `WebApp.ready()` + `expand()` + `setHeaderColor('#0F0F1A')` in App.jsx. Onboarding gate via `localStorage.onboarding_completed`.
- **Vite config**: `envDir: '../'` (reads .env from project root), dev proxy `/api` → `localhost:8000`.
- **Tailwind theme**: Dark mode only. Custom colors (bg: #0F0F1A, surface: #1A1A2E, primary: #6C63FF). Font: Inter.

### Bot internals

- **Handlers**: start (register + stats display), profile, rating (top-10), streak (visual bar), help (static), menu (text button routing), notifications (hourly loop + disable callback).
- **Communication**: All backend calls via `httpx.AsyncClient` with 5-10s timeout. Silent failure pattern (try/except pass).

### Admin internals

- **Auth**: JWT stored in localStorage (`admin_jwt_token`). 401 response → auto-logout + redirect to /login.
- **Theory editor**: Drag-and-drop block editor (hello-pangea/dnd). Block types: text, formula, example, image, divider. Live KaTeX preview.
- **Bulk operations**: CSV import for problems, CSV export for users.

## PISA Math Model

Four content domains with `topic_id` keys: `quantity`, `change_and_relationships`, `space_and_shape`, `uncertainty_and_data`.

Six competency levels (1=basic → 6=advanced reasoning). User default level: 3. Problems and user levels both use this 1-6 scale.

## Engineering Conventions

- User-facing content in Kazakh; code/docs in English.
- Frontend: 100% Tailwind utilities (no .module.css). Mobile-first, Telegram WebView compatible. Haptic feedback on interactions.
- Backend: Thin routers → services. Pydantic schemas for all request/response. LaTeX validation checks brace/$ balance in admin schemas.
- `.env` sits at project root (this directory), loaded by backend and bot via python-dotenv, by frontend via Vite `envDir: '../'`. Admin panel does **not** set `envDir` — it defaults `VITE_API_URL` to `http://localhost:8000` in code.

## Environment Variables

Required in `.env`:
```
BOT_TOKEN, TELEGRAM_BOT_TOKEN, MINI_APP_URL, GROQ_API_KEY,
BACKEND_URL (default http://localhost:8000), DATABASE_URL (default sqlite:///./math_pisa_bot.db),
ADMIN_USERNAME, ADMIN_PASSWORD, JWT_SECRET_KEY
```
Frontend/Admin: `VITE_API_URL` (frontend defaults to `/api` via proxy; admin defaults to `http://localhost:8000`).
