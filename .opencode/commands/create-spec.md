---
description: Create a spec file and feature branch for the next NLS Securities feature
argument-hint: "Step number and feature name e.g. 06 Branch Locator"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git:*)
---

You are a senior developer spinning up a new feature for
NLS Securities (React 19 + Vite 7 JSX frontend, Django 5.2 + DRF backend,
FastAPI + Selenium market-data service).
Always follow the rules in AGENTS.md.

User input: $ARGUMENTS

## Step 1 — Parse the arguments
From $ARGUMENTS extract:

1. `step_number` — zero-padded to 2 digits: 2 → 02, 11 → 11

2. `feature_title` — human readable title in Title Case
   - Example: "Branch Locator" or "Research Download"

3. `feature_slug` — git and file safe slug
   - Lowercase, kebab-case
   - Only a-z, 0-9 and -
   - Maximum 40 characters
   - Example: branch-locator, research-download


If you cannot infer these from $ARGUMENTS, ask the user
to clarify before proceeding.

Define `branch_name` as: `feature/<step_number>-<feature_slug>`
Example: `feature/06-branch-locator`

## Step 2 — Research the codebase
Read these files before writing the spec:
- `AGENTS.md` — services, ports, routing rules, gotchas
- `nls_backend/api/models.py` — existing Django models (CKEditor5Field for rich text)
- `nls_backend/api/serializers.py` — existing DRF serializers
- `nls_backend/api/views.py` — existing DRF `@api_view` function-based views
- `nls_backend/api/urls.py` — existing Django routes
- `nls_backend/api/admin.py` — existing admin registrations
- `nls_frontend/vite.config.js` — dev proxy rules (DJANGO :8000 vs FASTAPI :8080)
- `nls_frontend/src/services/getApi.jsx`, `postApi.jsx`, `chartService.jsx` — frontend API call patterns (relative URLs, no host prefix)
- `nls_frontend/src/pages/`, `nls_frontend/src/components/` — existing pages/components
- `fastapi/main.py` — existing FastAPI endpoints and `periodic_runner()` (30s scraper)
- `fastapi/services/dse_service.py` — Selenium scraping logic
- `fastapi/models/db.py`, `fastapi/models/repository.py` — FastAPI tables (`create_database_and_table()` auto-creates, no migrations)
- `nlisecurities.conf` — production Nginx routing (must mirror `vite.config.js`)
- All files in `specs/` — avoid duplicating existing specs

There is no `core/`, `middleware/`, `seed.py`, or `plans/` in this project.
Do not reference DMS, SQLModel, JWT auth, RBAC, audit middleware, Azure AD,
bcrypt, or TypeScript — none of these apply to NLS Securities.

## Step 3 — Write the spec
Generate a spec document with this exact structure:

---
# Spec: <feature_title>

## Overview
One paragraph describing what this feature does and why
it exists for NLS Securities (financial services website).

## Depends on
Which previous steps/specs this feature requires to be complete.

## Service ownership
Which service(s) change: Frontend (`nls_frontend/`) and/or
Django backend (`nls_backend/`, port 8000) and/or
Market Data (`fastapi/`, port 8080).

## Routes
Every new/changed endpoint, with its owning backend:
- `METHOD /path/` — description — owner (Django :8000 / FastAPI :8080)

State which Vite proxy rule (`nls_frontend/vite.config.js`) and which
Nginx rule (`nlisecurities.conf`) each route needs. Frontend calls
backends via relative URLs only — a new endpoint MUST add a matching
proxy rule in both files.

If no new routes: state "No new routes".

## Database changes
Any new tables, columns, or constraints needed.
- Django-managed tables: needs a migration (`python manage.py migrate`).
  Always verify against `nls_backend/api/models.py` first.
- FastAPI-managed tables (`api_share_prices`, `api_market_info`,
  `api_minute_data`, `api_market_index`, `api_ticker_price`,
  `api_sector_inst`, etc.): auto-created via `create_database_and_table()`
  on startup — no migrations. Verify against `fastapi/models/db.py` and
  `fastapi/models/repository.py` first. Both backends share the `nlsdb`
  MySQL database.
If none: state "No database changes".

## Frontend changes
React 19 + Vite 7, JSX only (no TypeScript). List pages/components/services
to add or modify (e.g. `src/pages/`, `src/components/`,
`src/services/getApi.jsx`). No Jinja2 templates.

## Files to change
Every file that will be modified.

## Files to create
Every new file that will be created.

## New dependencies
Any new pip packages (`nls_backend/requirements.txt`,
`fastapi/requirements.txt`) or npm packages (`nls_frontend/package.json`).
If none: state "No new dependencies".

## Rules for implementation
Specific constraints the implementer must follow. Always include:
- Django: DRF `@api_view` function-based views in `nls_backend/api/views.py`;
  serializers in `serializers.py`; models in `models.py`; routes in `urls.py`;
  register content models in `admin.py`
- Django: use `CKEditor5Field` (config `extends`) for rich-text content fields
- Django: run `python manage.py migrate` after model changes; collect static
  via `python manage.py collectstatic` (outputs to `assets/` locally,
  `/var/www/django_static/` in production)
- FastAPI: plain FastAPI route functions in `fastapi/main.py` + scraping logic
  in `fastapi/services/`; DB access via `fastapi/models/repository.py`
- FastAPI: never add a second worker in production (`--workers 1` only —
  `asyncio.create_task(periodic_runner())` is not process-safe); scraper
  interval is 30s; tables auto-create via `create_database_and_table()`
- Frontend: JSX only, no TypeScript; 2-space indent; pages in `src/pages/`,
  shared UI in `src/components/`, API calls in `src/services/` using
  relative URLs (no host/port prefix)
- Routing: every new API path needs a proxy entry in BOTH
  `nls_frontend/vite.config.js` (dev) and `nlisecurities.conf` (production
  Nginx); `/api/` prefix only covers `/admin/`, `/ckeditor5/`, `/static/`,
  `/media/` — content/market endpoints go direct (e.g. `/slider/`, `/ipo_offer/`)
- Python: 4-space indent, `snake_case`
- No test suite / no CI in this repo — verify with `npm run lint`,
  `python manage.py check`, and manual browser test on :5173 with Django
  (:8000) and FastAPI (:8080) both running
- No new dependencies unless explicitly approved
- Never commit secrets: `.env` files, `*.pem`, `venv/`, `node_modules/`,
  Django `assets/`/`media/`, `nli_run_command.txt`,
  `almalinux-information.txt` (all gitignored)
- `DEBUG = False`, production `SECRET_KEY`/`ALLOWED_HOSTS`/
  `CSRF_TRUSTED_ORIGINS` in production; media at `/var/www/django_media/`

## Definition of done
A specific testable checklist. Each item must be
something verifiable by running the app (e.g. "GET /slider/ returns 200
via Vite proxy", "page renders on :5173 with both backends running",
"`npm run lint` passes", "`python manage.py check` passes").
---

## Step 4 — Create the branch and save the spec
1. Create the feature branch: `git checkout -b <branch_name>`
   (if it already exists, check it out instead — never commit or push
   unless explicitly asked).
2. Save to: `specs/<step_number>-<feature_slug>.md`

## Step 5 — Report to the user
Print a short summary in this exact format:
```
Branch:    <branch_name>
Spec file: specs/<step_number>-<feature_slug>.md
Title:     <feature_title>
```

Then tell the user:
"Review the spec at `specs/<step_number>-<feature_slug>.md`
then enter Plan Mode with Shift+Tab twice to begin implementation."

Do not print the full spec in chat unless explicitly asked.
