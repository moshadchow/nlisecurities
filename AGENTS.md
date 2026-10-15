# AGENTS.md

## Project Overview

NLS Securities — financial services site, three services:

| Service | Tech | Dev Port | Entry |
|---------|------|----------|-------|
| Frontend | React 19 + Vite 7 (JSX, no TS) | 5173 | `nls_frontend/` (`npm run dev`) |
| Backend | Django 5.2 + DRF | 8000 | `nls_backend/` (`python manage.py runserver`) |
| Market Data | FastAPI + Selenium scraper | 8080 | `fastapi/main.py` (`uvicorn main:app --host 127.0.0.1 --port 8080`) |

Shared MySQL database `nlsdb` (Django connects as `nls_user`, FastAPI as `root` — see `nls_backend/nls_backend/settings.py` vs `fastapi/models/db.py`). Requires MySQL running locally.

## Dev Commands

Frontend (`nls_frontend/`): `npm run dev` | `npm run build` (→ `dist/`) | `npm run lint` (ESLint react-hooks + react-refresh).
Django (`nls_backend/`): `python manage.py runserver` | `migrate` | `collectstatic` (→ `assets/`).
FastAPI tests (`fastapi/`): `pytest tests/` — parser/repository/failure tests with fixtures, no DB or browser needed. No Django or JS tests, no CI.

## Routing — the trickiest part

Frontend uses **relative URLs** (`VITE_API_BASE` / `VITE_FASTAPI_BASE`, both default `''`). Path→backend mapping lives in `nls_frontend/vite.config.js` (dev proxy): content paths (`/slider`, `/service`, `/market_info`, `/ticker_price`, …) → Django :8000; live-scrape paths (`/ipo_offer`, `/dse_news`, `/cse_news`, `/minutes_index_cse`) → FastAPI :8080.

- New endpoint → add a proxy rule in `vite.config.js` **and** a matching Nginx rule on the server, or it 404s in one environment.
- `nls_backend/api/urls.py` mounts at root (`''`, no `/api/` prefix). `nlisecurities.conf` in this checkout is gitignored/local-only and currently only proxies `/api/`, `/admin/`, `/ckeditor5/`, `/static/`, `/media/` — it does **not** cover the content endpoints, so verify the live server config before trusting it.
- Read path for market data is Django (`market_info/`, `minutes_index/`, `market_index/`, `ticker_price/`, `sector_wise_inst/` read the tables FastAPI scrapes into). FastAPI's same-named live endpoints are scrape triggers, not what the frontend reads.

## Conventions

- New Django endpoint: function-based `@api_view` in `nls_backend/api/views.py` + route in `api/urls.py` (root-level path). Rich-text model fields use `CKEditor5Field`.
- FastAPI `lifespan` starts `periodic_runner()` via `asyncio.create_task()` on a 30s loop — **run with `--workers 1`** or scrapes duplicate. Tables are auto-created by `create_database_and_table()` on startup; Django migrations only cover Django-managed tables.
- Known bug: `nls_frontend/src/services/chartService.jsx` `fetchIPO`/`fetchDSENews`/`fetchCSENews`/`fetchSectorWiseSymbol` use double-quoted `"${FASTAPI_BASE}/..."` (never interpolates) — fix to backticks when touching that file.

## Production

AlmaLinux + Nginx + systemd (`nls-backend`, `fastapi-market`). Per-service deploy docs: `nls_frontend/nls_frontend_deployment_process.md`, `nls_backend/nls_backend_deployment_process.md`, `fastapi/fastapi_deployment_process.md`. Prod differs: `DEBUG=False`, prod secrets/hosts, static → `/var/www/django_static/`, media → `/var/www/django_media/`, SELinux `httpd_can_network_connect`.

## Gotchas

- `nli_run_command.txt`, `almalinux-information.txt`, `nlisecurities.conf`, `.env*`, `*.pem`, `venv/`, `nlsDB/` are gitignored local-only — **never commit**; dev passwords in tracked `settings.py` are local-only.
- `nginx.conf` is the stock template, not the site config. No TypeScript, no CI.
