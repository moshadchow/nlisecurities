---
description: Create a spec file and feature branch for the next NLS Securities step
argument-hint: "Step number and feature name e.g. 02 Market News Alerts"
allowed-tools: Read, Write, Glob, Edit, Bash(git:*)
---

You are a senior developer spinning up a new feature for the NLS Securities
financial services site. Always follow the rules in AGENTS.md.

User input: $ARGUMENTS

## Step 1 — Parse the arguments

From $ARGUMENTS extract:

1. `step_number` — zero-padded to 2 digits: 2 → 02, 11 → 11

2. `feature_title` — human readable title in Title Case
   - Example: "Market News Alerts" or "Login and Logout"

3. `feature_slug` — git and file safe slug
   - Lowercase, kebab-case
   - Only a-z, 0-9 and -
   - Maximum 40 characters
   - Example: market-news-alerts, login-logout

If you cannot infer these from $ARGUMENTS, ask the user
to clarify before proceeding.


## Step 2 — Research the codebase

Read these files before writing the spec:

- `AGENTS.md` — roadmap, conventions, schema, routing, services, ports
- `nls_backend/nls_backend/settings.py` — Django settings, DATABASES (`nlsdb`), MEDIA/STATIC roots
- `nls_backend/nls_backend/urls.py` — root URLCONF mounts `api.urls` at root (`''`)
- `nls_backend/api/urls.py` — root-level content routes (no `/api/` prefix)
- `nls_backend/api/views.py` — existing `@api_view(['GET'])` patterns
- `nls_backend/api/models.py` — Django models and `Meta.ordering`
- `nls_backend/api/serializers.py` — DRF `ModelSerializer` patterns
- `nls_backend/api/admin.py` — `admin.site.register` / `@admin.register` patterns
- `nls_frontend/vite.config.js` — dev proxy rules (Django :8000 vs FastAPI :8080)
- `nls_frontend/src/services/getApi.jsx` — `BASE = import.meta.env.VITE_API_BASE ?? ''` pattern
- `nls_frontend/src/pages/Home.jsx` — page component conventions
- `fastapi/main.py` — scrape-trigger endpoints and lifespan `periodic_runner()`
- All files in `specs/` — avoid duplicating existing plans/specs

Check `AGENTS.md` to confirm the requested step is not already
marked complete. If it is, warn the user and stop.

Routing reminder (from AGENTS.md):
- Content paths (`/slider`, `/service`, `/market_info`, `/ticker_price`, …) → Django :8000
- Live-scrape trigger paths (`/ipo_offer`, `/dse_news`, `/cse_news`, `/minutes_index_cse`) → FastAPI :8080
- Django reads FastAPI-scraped tables via raw SQL (`connections['default']`), e.g. `Top_share_price_by`, `market_info`, `minutes_index`
- New endpoint → add a proxy rule in `vite.config.js` **and** a matching Nginx rule on the server, or it 404s in one environment


## Step 3 — Write the spec

Generate a spec document with this exact structure:

---
# Spec: <feature_title>

## Overview
One paragraph describing what this feature does and why
it exists at this stage of the NLS Securities roadmap.

## Depends on
Which previous steps this feature requires to be complete.
If this is step `01` and `specs/` is empty, state that explicitly.

## Service ownership
- **Django backend** (`nls_backend/`, port `8000`): models, serializers, views, urls, admin, migrations.
- **Frontend** (`nls_frontend/`, port `5173`): components, pages, services, vite proxy.
- **Market Data** (`fastapi/`, port `8080`): only if new scrape triggers are needed; otherwise state "no changes".

## Routes
Every new route needed:
- `METHOD /path` — description — access level (public/authenticated/staff) — owner (Django or FastAPI)

If no new routes: state "No new routes".

Routing rules:
- Django content endpoints live at root level in `nls_backend/api/urls.py` (no `/api/` prefix).
- Function-based `@api_view` views in `nls_backend/api/views.py`.
- FastAPI live-scrape triggers in `fastapi/main.py` (`--workers 1` only).
- Development proxy entries in `nls_frontend/vite.config.js` targeting Django `http://127.0.0.1:8000` or FastAPI `http://127.0.0.1:8080`.
- Frontend API calls use relative URLs via `BASE = import.meta.env.VITE_API_BASE ?? ''`.
- Production Nginx (`nlisecurities.conf`, gitignored/local-only): matching proxy rule required or the endpoint 404s in production.

## Database changes
Any new tables, columns, or constraints needed.
- Verify against `nls_backend/api/models.py` before writing.
- The shared MySQL database `nlsdb` is also used by FastAPI for `api_share_prices`, `api_market_info`, `api_minute_data`, `api_market_index`, `api_ticker_price`, `api_sector_inst` — do not modify FastAPI-managed tables.
- Django migrations: `python manage.py makemigrations api` and `python manage.py migrate`.
- If none: state "No database changes".

## Frontend changes
React 19 + Vite 7, JSX only; no TypeScript.

- Component placement: `src/components/` for presentational UI, `src/pages/` for route pages.
- API calls in `src/services/getApi.jsx` (Django content) or `src/services/chartService.jsx` (market data), using `${BASE}/...` relative URLs.
- Two-space indentation.
- Do not hardcode `http://127.0.0.1:8000` or `http://127.0.0.1:8080`.
- Do not use Jinja2 templates.

## Files to change
Every file that will be modified.

## Files to create
Every new file that will be created.

## New dependencies
Any new pip packages or npm packages. If none: state "No new dependencies".
Do not add packages unless explicitly approved.

## Rules for implementation
Specific constraints. Always include:

- Use Django REST Framework function-based `@api_view` views in `nls_backend/api/views.py`.
- Register routes at root level in `nls_backend/api/urls.py` (no `/api/` prefix unless the existing architecture requires it).
- Models in `nls_backend/api/models.py`, serializers in `nls_backend/api/serializers.py`, admin registration in `nls_backend/api/admin.py`.
- Rich-text model fields use `CKEditor5Field` (see `ckeditorconfig.py`).
- Generate and apply Django migrations after model changes; run `python manage.py check`.
- Frontend: JSX only, two-space indent, `PascalCase` components, `camelCase` hooks/stores.
- API URLs: relative URLs via `BASE` convention (`import.meta.env.VITE_API_BASE ?? ''`); never hardcode hostnames or ports.
- Proxy configuration: add the dev proxy in `vite.config.js`; verify production Nginx routing before deployment.
- FastAPI: run with `--workers 1` or scrapes duplicate; tables auto-created by `create_database_and_table()` on startup.
- Never expose secrets or sensitive data in logs; never commit `.env`, `*.pem`, `venv/`, `node_modules/`, or media.
- Preserve `DEBUG = False`, `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` in production.
- Add/update tests for every implemented feature (FastAPI: `pytest tests/`; Django: no existing test suite).
- Do not modify unrelated slider, hero, market-ticker, or chart functionality.
- Fix the known `chartService.jsx` double-quote interpolation bug (`"${FASTAPI_BASE}/..."`) only when touching that file.

## Definition of done
A specific testable checklist. Each item must be
something that can be verified by running the app.
---

## Step 4 — Save the spec

Save to: `specs/<step_number>-<feature_slug>.md`

Create a feature branch: `feature/<step_number>-<feature_slug>`

## Step 5 — Report to the user

Print a short summary in this exact format:

```
Branch:    feature/<step_number>-<feature_slug>
Spec file: specs/<step_number>-<feature_slug>.md
Title:     <feature_title>
```

Then tell the user:
"Review the spec at `specs/<step_number>-<feature_slug>.md`
then enter Plan Mode with Shift+Tab twice to begin implementation."

Do not print the full spec in chat unless explicitly asked.
