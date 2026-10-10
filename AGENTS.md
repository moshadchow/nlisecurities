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
npm run build      # Production build -> dist/
npm run lint       # ESLint (react-hooks + react-refresh)
```

### Django Backend (`nls_backend/`)
```bash
cd nls_backend
python manage.py runserver            # Dev server on :8000
python manage.py migrate              # Run migrations
python manage.py collectstatic        # Collect static -> assets/
```
Requires MySQL running locally with `nlsdb` database. MySQL client C libs required (`mysql-devel` on RHEL).

### FastAPI Market Data (`fastapi/`)
```bash
cd fastapi
uvicorn main:app --host 127.0.0.1 --port 8080
```
Requires Chrome + ChromeDriver for Selenium scraping. CSE endpoints need `cse_ca_bundle.pem` in `fastapi/`.

## Architecture Notes

### Routing — the trickiest part

The frontend calls both backends using **relative URLs** (no host/port prefix). Routing is handled by dev proxy or Nginx:

- **Dev**: Vite (`vite.config.js`) proxies individual path prefixes to the correct backend (e.g. `/slider` -> Django :8000, `/ipo_offer` -> FastAPI :8080).
- **Production**: Nginx (`nlisecurities.conf`) does the same. Django paths go direct (e.g. `/slider/` -> Django). FastAPI paths go direct (e.g. `/ipo_offer/` -> FastAPI). The `/api/` prefix only covers `/admin/`, `/ckeditor5/`, `/static/`, `/media/`.

**Critical**: The frontend does NOT prefix API calls with `/api/`. It calls `/slider/`, `/feature/`, `/ipo_offer/`, etc. directly. If you add a new API endpoint, you must add a matching proxy rule in both `vite.config.js` (dev) and `nlisecurities.conf` (production).

### Key architectural facts

- **FastAPI is separate** from Django. It scrapes DSE/CSE stock data every 30s into MySQL and serves it via its own endpoints.
- **Shared MySQL database**: Both Django and FastAPI use `nlsdb`. Django uses `nls_user` user; FastAPI uses `root` — credentials differ between local and production.
- **CKEditor 5** is used for rich text content in Django admin (`django_ckeditor_5`).
- **FastAPI must run with `--workers 1`** in production — the `asyncio.create_task()` periodic scraper is not process-safe.
- **FastAPI auto-creates its own tables** via `create_database_and_table()` on startup. Django migrations handle Django-managed tables only.

## Production Deployment

Server: AlmaLinux at 103.244.247.188:2244 (via jump server).

Key differences from local dev:
- `DEBUG = False`, production `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` in `settings.py`
- Static files served from `/var/www/django_static/` (not Django's dev server)
- Media files at `/var/www/django_media/`
- SSL via Let's Encrypt (certbot)
- SELinux enforcing — may need `setsebool -P httpd_can_network_connect 1` and `chcon` for static/media dirs

Systemd services: `nls-backend` (Django), `fastapi-market` (FastAPI).

Deployment guides for each service: `nls_frontend/nls_frontend_deployment_process.md`, `nls_backend/nls_backend_deployment_process.md`, `fastapi/fastapi_deployment_process.md`.

## Gotchas

- **No TypeScript, no test suite, no CI/CD** — code quality relies on ESLint and manual testing.
- `nli_run_command.txt` and `almalinux-information.txt` contain production credentials — **never commit secrets**. Both are gitignored.
- `.gitignore` excludes `nlsDB/`, `*.pem`, `venv/`, `node_modules/`, `.env` files, Django `assets/` and `media/`.
- Frontend `.env.production` has empty `VITE_API_BASE` and `VITE_FASTAPI_BASE` — production uses same-origin (Nginx proxies everything). The local `.env` has `VITE_API_URL=https://nlisecurities.com/api` (gitignored).
- `STATIC_ROOT` in Django settings points to `BASE_DIR / 'assets'` locally (overridden to `/var/www/django_static/` in production).
- The Nginx config in this repo (`nginx.conf`) is the default template. The real site config is `nlisecurities.conf`.
- Django views use DRF `@api_view` decorators (function-based views). Models use `CKEditor5Field` for rich text.
