# AGENTS.md

## Project Overview

NLS Securities — a financial services website with three services:

| Service | Tech | Dev Port | Production Path |
|---------|------|----------|-----------------|
| Frontend | React 19 + Vite 7 (JSX, no TS) | 5173 | /var/www/reactapp |
| Backend | Django 5.2 + DRF | 8000 | /opt/backend (port 8000) |
| Market Data | FastAPI + Selenium scraper | 8080 | /opt/fastapi (port 8080) |

All behind Nginx reverse proxy on nlisecurities.com.

## Dev Commands

### Frontend (`nls_frontend/`)
```bash
npm run dev        # Vite dev server on :5173
npm run build      # Production build → dist/
npm run lint       # ESLint (react-hooks + react-refresh)
```

### Django Backend (`nls_backend/`)
```bash
cd nls_backend
python manage.py runserver            # Dev server on :8000
python manage.py migrate              # Run migrations
python manage.py collectstatic        # Collect static → assets/
```
Requires MySQL running locally with `nlsdb` database. MySQL client C libs required (`mysql-devel` on RHEL).

### FastAPI Market Data (`fastapi/`)
```bash
cd fastapi
uvicorn main:app --host 127.0.0.1 --port 8080
```
Requires Chrome + ChromeDriver for Selenium scraping. CSE endpoints need `cse_ca_bundle.pem` in `fastapi/`.

## Architecture Notes

- **Django serves API at root (`/`)**, not `/api/`. Nginx adds the `/api/` prefix in production via `proxy_pass`. The Vite dev proxy in `vite.config.js` mirrors this by proxying path-based routes (e.g. `/slider`, `/about`) to Django.
- **FastAPI is separate** from Django. It scrapes DSE/CSE stock data every 30s into MySQL and serves it via its own endpoints. Vite proxies `/ipo_offer`, `/dse_news`, `/cse_news`, `/minutes_index_cse` to FastAPI (port 8080).
- **Shared MySQL database**: Both Django and FastAPI use `nlsdb`. Django uses `nls_user` user; FastAPI uses `root` — credentials differ between local and production.
- **CKEditor 5** is used for rich text content in Django admin (`django_ckeditor_5`).
- **FastAPI must run with `--workers 1`** in production — the `asyncio.create_task()` periodic scraper is not process-safe.

## Production Deployment

Server: AlmaLinux at 103.244.247.188:2244 (via jump server).

Key differences from local dev:
- `DEBUG = False`, production `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` in `settings.py`
- Static files served from `/var/www/django_static/` (not Django's dev server)
- Media files at `/var/www/django_media/`
- SSL via Let's Encrypt (certbot)
- SELinux enforcing — may need `setsebool -P httpd_can_network_connect 1` and `chcon` for static/media dirs

Systemd services: `nls-backend` (Django), `fastapi-market` (FastAPI).

## DB Schema

Tables are auto-created by FastAPI's `create_database_and_table()` on startup. Django migrations handle Django-managed tables. SQL dumps in `nlsDB/` are reference only (gitignored).

## Gotchas

- **No TypeScript, no test suite, no CI/CD** — code quality relies on ESLint and manual testing.
- `nli_run_command.txt` and `almalinux-information.txt` contain production credentials — **never commit secrets**. Both are gitignored.
- `.gitignore` excludes `nlsDB/`, `*.pem`, `venv/`, `node_modules/`, `.env` files, Django `assets/` and `media/`.
- Frontend `.env.production` has empty `VITE_API_BASE` and `VITE_FASTAPI_BASE` — production uses same-origin (Nginx proxies everything).
- `STATIC_ROOT` in Django settings points to `BASE_DIR / 'assets'` locally (overridden to `/var/www/django_static/` in production).
