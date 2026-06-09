### Django Backend (nls_backend) — AlmaLinux Deployment Guide

 ## Context

 nls_backend is a Django 5.2.7 REST API that serves content (sliders, services, events, market data) for the NLS
 Securities website. It runs via ASGI (uvicorn) at 192.168.101.238:8000, behind Nginx on the AlmaLinux server at
 103.244.247.188:2244 (via jump server 103.244.247.59:8449). The Nginx config (nlisecurities.conf) already has /api/,
 /admin/, /ckeditor5/ proxy blocks pointing to this port. Static files go to /var/www/django_static/ and media to
 /var/www/django_media/.

 Pre-deployment fixes required in settings.py:
 - DEBUG = False
 - Add domain to ALLOWED_HOSTS
 - Generate a new SECRET_KEY
 - Update CORS_ALLOWED_ORIGINS for production

 ---
 ## Step 1 — Connect to the Server

 # Via jump server (ssh -J or PuTTY)
 ssh -J xflmchowdhury@103.244.247.59:8449 root@103.244.247.188 -p 2244
 # PuTTY: Host=103.244.247.188, Port=2244, User=root, Pass=$Password@1$

 ---
 ## Step 2 — Server Prerequisites

 # Update OS
 dnf update -y

 # Python 3, venv, pip
 dnf install python3 python3-venv python3-pip -y

 # MySQL client development libraries (required by mysqlclient pip package)
 dnf install mysql-devel gcc python3-devel -y

 # Nginx (skip if already installed)
 dnf install nginx -y

 # Certbot for SSL (skip if cert already exists for nlisecurities.com)
 dnf install epel-release -y
 dnf install certbot python3-certbot-nginx -y

 # Confirm MySQL is running
 systemctl status mysqld

 ---
 ## Step 3 — Upload Project Files

 Run from your Windows machine (PowerShell). Excludes venv/, assets/, __pycache__/.

 # 1. Create destination on server (run on server first):
 #    mkdir -p /opt/backend

 # 2. Upload project files (excludes venv and collected assets):
 pscp -P 2244 -r E:\xfl-projects\website\nlisecurities\nls_backend\api root@103.244.247.188:/opt/backend/
 pscp -P 2244 -r E:\xfl-projects\website\nlisecurities\nls_backend\nls_backend root@103.244.247.188:/opt/backend/
 pscp -P 2244    E:\xfl-projects\website\nlisecurities\nls_backend\manage.py root@103.244.247.188:/opt/backend/
 pscp -P 2244    E:\xfl-projects\website\nlisecurities\nls_backend\requirements.txt
 root@103.244.247.188:/opt/backend/

 Do NOT upload: venv/, assets/ (re-run collectstatic on server), media/ (upload separately if needed).

 Upload existing media files if any:
 pscp -P 2244 -r E:\xfl-projects\website\nlisecurities\nls_backend\media\*
 root@103.244.247.188:/var/www/django_media/

 ---
 ## Step 4 — Production Settings Changes

 On the server, edit /opt/backend/nls_backend/settings.py:

 vi /opt/backend/nls_backend/settings.py

 Change the following:

 # 1. Disable debug mode
 DEBUG = False

 # 2. Allow the production domain and server IPs
 ALLOWED_HOSTS = ['nlisecurities.com', 'www.nlisecurities.com', '192.168.101.238', '127.0.0.1']

 # 3. Replace the insecure SECRET_KEY with a new one
 # Generate one with: python3 -c "from django.core.management.utils import get_random_secret_key;
 print(get_random_secret_key())"
 SECRET_KEY = 'your-new-secure-secret-key-here'

 # 4. Update CORS origins for production
 CORS_ALLOWED_ORIGINS = [
     "https://nlisecurities.com",
     "https://www.nlisecurities.com",
 ]

 # 5. Update database credentials for production MySQL
 DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'nlsdb',
         'USER': 'nls_user',
         'PASSWORD': 'Nls@123',      # confirm this matches production DB
         'HOST': 'localhost',
         'PORT': '3306',
     }
 }

 # 6. Point static and media to the Nginx-served directories
 STATIC_ROOT = '/var/www/django_static/'
 MEDIA_ROOT  = '/var/www/django_media/'

 ---
 ## Step 5 — Create Virtual Environment & Install Dependencies

 cd /opt/backend

 # Create venv (named v_api to match nli_run_command.txt convention)
 python3 -m venv v_api

 # Activate
 source v_api/bin/activate

 # Upgrade pip
 pip install --upgrade pip

 # Install dependencies (mysqlclient requires mysql-devel from Step 2)
 pip install -r requirements.txt

 # Verify
 python -c "import django, rest_framework, mysqlclient; print('OK')"

 deactivate

 ---
 ## Step 6 — Set Up MySQL Database & User

 mysql -u root -p   # password: $Password@2$

 -- Create database if not exists
 CREATE DATABASE IF NOT EXISTS nlsdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

 -- Create dedicated user (matches settings.py)
 CREATE USER IF NOT EXISTS 'nls_user'@'localhost' IDENTIFIED BY 'Nls@123';
 GRANT ALL PRIVILEGES ON nlsdb.* TO 'nls_user'@'localhost';
 FLUSH PRIVILEGES;
 EXIT;

 ---
 ## Step 7 — Run Django Migrations & Collect Static Files

 cd /opt/backend
 source v_api/bin/activate

 # Run migrations (creates all tables)
 python manage.py migrate

 # Create static files directories
 mkdir -p /var/www/django_static
 mkdir -p /var/www/django_media

 # Collect static files to /var/www/django_static/
 python manage.py collectstatic --noinput

 # Create Django superuser (for /admin/)
 python manage.py createsuperuser

 deactivate

 ---
 ## Step 8 — Test Run (manual, before systemd)

 cd /opt/backend
 source v_api/bin/activate

 uvicorn nls_backend.asgi:application --host 192.168.101.238 --port 8000

 # In another terminal, test:
 curl http://192.168.101.238:8000/admin/     # should return 200 or redirect
 curl http://192.168.101.238:8000/slider/    # should return JSON

 # Ctrl+C to stop
 deactivate

 ---
 ## Step 9 — Create systemd Service

 Create /etc/systemd/system/nls-backend.service:

 vi /etc/systemd/system/nls-backend.service

 [Unit]
 Description=NLS Securities Django Backend
 After=network.target mysqld.service
 Wants=mysqld.service

 [Service]
 Type=simple
 User=root
 WorkingDirectory=/opt/backend
 Environment="PATH=/opt/backend/v_api/bin"
 Environment="DJANGO_SETTINGS_MODULE=nls_backend.settings"
 ExecStart=/opt/backend/v_api/bin/uvicorn nls_backend.asgi:application --host 192.168.101.238 --port 8000 --workers 2
 Restart=always
 RestartSec=5
 StandardOutput=journal
 StandardError=journal
 SyslogIdentifier=nls-backend

 [Install]
 WantedBy=multi-user.target

 # Enable and start
 systemctl daemon-reload
 systemctl enable nls-backend
 systemctl start nls-backend

 # Check status
 systemctl status nls-backend

 # Follow logs
 journalctl -u nls-backend -f

 ---
 ## Step 10 — Verify Nginx Configuration

 The existing /etc/nginx/conf.d/nlisecurities.conf already has the correct proxy blocks for /api/, /admin/,
 /ckeditor5/, /static/, /media/. No changes needed as long as:
 - Django runs on 192.168.101.238:8000 ✓
 - Static files are at /var/www/django_static/ ✓ (Step 7)
 - Media files are at /var/www/django_media/ ✓ (Step 7)

 # Test and reload Nginx
 nginx -t
 systemctl reload nginx

 If the config file is not yet on the server, copy it:
 # Upload from Windows:
 pscp -P 2244 E:\xfl-projects\website\nlisecurities\nlisecurities.conf
 root@103.244.247.188:/etc/nginx/conf.d/nlisecurities.conf

 ---
 ## Step 11 — Firewall Rules

 # HTTP and HTTPS (for Nginx)
 firewall-cmd --permanent --add-service=http
 firewall-cmd --permanent --add-service=https

 # Django port (internal LAN access only — restrict to LAN if possible)
 firewall-cmd --permanent --add-port=8000/tcp

 firewall-cmd --reload

 # Verify
 firewall-cmd --list-all

 ---
 ## Step 12 — SELinux Permissions

 # Check mode
 getenforce   # likely "Enforcing" on AlmaLinux

 # Allow Nginx to proxy to upstream services
 setsebool -P httpd_can_network_connect 1

 # Allow Nginx to read static/media files in /var/www/
 chcon -Rt httpd_sys_content_t /var/www/django_static/
 chcon -Rt httpd_sys_content_t /var/www/django_media/

 # If Django writes to media (uploads), allow write:
 chcon -Rt httpd_sys_rw_content_t /var/www/django_media/

 # If you see AVC denials in audit log:
 ausearch -m avc -ts recent
 ausearch -c 'uvicorn' --raw | audit2allow -M nls-backend-policy
 semodule -i nls-backend-policy.pp

 ---
 ## Step 13 — SSL (Let's Encrypt)

 The SSL cert for nlisecurities.com is likely already in place from the Nginx config
 (/etc/letsencrypt/live/nlisecurities.com/). If not, obtain it:

 # Stop Nginx briefly to allow standalone cert issuance (or use --nginx plugin)
 certbot --nginx -d nlisecurities.com -d www.nlisecurities.com

 # Test renewal
 certbot renew --dry-run

 Auto-renewal is handled by a certbot systemd timer (installed automatically). Verify:
 systemctl status certbot-renew.timer

 ---
 ## Step 14 — Verify Deployment

 # 1. Service running
 systemctl status nls-backend

 # 2. Direct port check
 curl http://192.168.101.238:8000/slider/
 # Expected: [] or JSON array

 # 3. Via Nginx HTTPS
 curl https://nlisecurities.com/api/slider/

 # 4. Admin panel
 # Open browser: https://nlisecurities.com/admin/

 # 5. Static files
 curl -I https://nlisecurities.com/static/admin/css/base.css
 # Expected: HTTP/2 200

 # 6. Media files
 curl -I https://nlisecurities.com/media/xfl.png

 # 7. Live service logs
 journalctl -u nls-backend -f --since "5 min ago"

 ---
 ## Step 15 — Troubleshooting

 ┌───────────────────────┬───────────────────────────────┬───────────────────────────────────────────────────────┐
 │        Problem        │           Diagnosis           │                          Fix                          │
 ├───────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────────┤
 │ DisallowedHost error  │ Domain not in ALLOWED_HOSTS   │ Add nlisecurities.com to ALLOWED_HOSTS in settings.py │
 ├───────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────────┤
 │ 502 Bad Gateway       │ Django not running or wrong   │ curl 192.168.101.238:8000/ directly; check systemctl  │
 │                       │ port                          │ status nls-backend                                    │
 ├───────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────────┤
 │ mysqlclient install   │ Missing C libs                │ dnf install mysql-devel gcc python3-devel -y          │
 │ fails                 │                               │                                                       │
 ├───────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────────┤
 │ Static files 404      │ collectstatic not run or      │ Re-run python manage.py collectstatic; check          │
 │                       │ wrong STATIC_ROOT             │ /var/www/django_static/                               │
 ├───────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────────┤
 │ Media files 404       │ Wrong MEDIA_ROOT or SELinux   │ Check /var/www/django_media/; run chcon command from  │
 │                       │                               │ Step 12                                               │
 ├───────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────────┤
 │ DB connection refused │ Wrong credentials or MySQL    │ Check systemctl status mysqld; verify nls_user        │
 │                       │ down                          │ password                                              │
 ├───────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────────┤
 │ CSRF errors in admin  │ Running behind proxy without  │ Add CSRF_TRUSTED_ORIGINS =                            │
 │                       │ trust                         │ ['https://nlisecurities.com'] to settings.py          │
 ├───────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────────┤
 │ django-insecure       │ DEBUG=True or old SECRET_KEY  │ Set DEBUG=False, generate new SECRET_KEY              │
 │ warnings              │                               │                                                       │
 ├───────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────────┤
 │ CKEditor media not    │ ckeditor static not collected │ Re-run collectstatic; verify /static/ Nginx alias     │
 │ loading               │                               │                                                       │
 └───────────────────────┴───────────────────────────────┴───────────────────────────────────────────────────────┘

 ---
 ## Step 16 — Production Best Practices & Security

 Required settings.py changes (summary)

 DEBUG = False
 SECRET_KEY = '<generated-strong-key>'
 ALLOWED_HOSTS = ['nlisecurities.com', 'www.nlisecurities.com', '192.168.101.238']
 CSRF_TRUSTED_ORIGINS = ['https://nlisecurities.com', 'https://www.nlisecurities.com']
 SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

 Move secrets out of settings.py (recommended)

 # In systemd service file, add environment variables:
 # Environment="DB_PASSWORD=Nls@123"
 # Environment="DJANGO_SECRET_KEY=your-key"

 # In settings.py, read from environment:
 import os
 SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-dev-only')
 DATABASES['default']['PASSWORD'] = os.environ.get('DB_PASSWORD', '')

 Monitoring & auto-restart

 # Check restart count
 systemctl show nls-backend --property=NRestarts

 # Set memory limit in service file
 # MemoryMax=512M

 # Log rotation — journald handles this by default; tune in /etc/systemd/journald.conf
 # SystemMaxUse=500M

 Gunicorn alternative (optional — better for sync-heavy Django)

 pip install gunicorn
 # In systemd ExecStart:
 ExecStart=/opt/backend/v_api/bin/gunicorn nls_backend.wsgi:application \
     --bind 192.168.101.238:8000 \
     --workers 3 \
     --timeout 120 \
     --access-logfile /var/log/gunicorn/nls-access.log \
     --error-logfile /var/log/gunicorn/nls-error.log

 ▎ Use uvicorn (ASGI) if you need async views; gunicorn (WSGI) for standard Django sync views. Current nls_backend 
 ▎ has no async views, so either works.
---                                                                                                           │
# Files to Modify Summary                                                                                       │
     │                                                                                                               │
     │ ┌────────────────────┬─────────────────────────────────────────┬───────────────────────────────────────────── │
     │ ────┐                                                                                                         │
     │ │        File        │                Location                 │                     Change                   │
     │    │                                                                                                          │
     │ ├────────────────────┼─────────────────────────────────────────┼───────────────────────────────────────────── │
     │ ────┤                                                                                                         │
     │ │ settings.py        │ /opt/backend/nls_backend/settings.py    │ DEBUG=False, ALLOWED_HOSTS, SECRET_KEY,      │
     │ CORS,   │                                                                                                     │
     │ │                    │                                         │ STATIC_ROOT, MEDIA_ROOT                      │
     │    │                                                                                                          │
     │ ├────────────────────┼─────────────────────────────────────────┼───────────────────────────────────────────── │
     │ ────┤                                                                                                         │
     │ │ nlisecurities.conf │ /etc/nginx/conf.d/nlisecurities.conf    │ Already correct — no changes needed          │
     │    │                                                                                                          │
     │ ├────────────────────┼─────────────────────────────────────────┼───────────────────────────────────────────── │
     │ ────┤                                                                                                         │
     │ │ New file           │ /etc/systemd/system/nls-backend.service │ Create systemd unit                          │
     │    │                                                                                                          │
     │ └────────────────────┴─────────────────────────────────────────┴───────────────────────────────────────────── │
     │ ────┘                                                                                                         │
     ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯