 # FastAPI Deployment Guide — AlmaLinux Server

 # Context

 The fastapi/ project is a DSE/CSE Market Data API that scrapes real-time stock market data every 30 seconds and
 serves it via REST endpoints. It needs to be deployed on the AlmaLinux server at 103.244.247.188:2244 (via jump
 server 103.244.247.59:8449), running at 192.168.101.238:8080, alongside the existing Django backend (port 8000) and
 React frontend. The existing nlisecurities.conf Nginx config needs a new location block added for the FastAPI
 service. The app uses Selenium (requires ChromeDriver), pymysql (MySQL at localhost), and a CSE-specific SSL cert
 bundle.

 ---
 ## Step 1 — Connect to the Server

 # From your machine via jump server (PuTTY or ssh -J)
 ssh -J xflmchowdhury@103.244.247.59:8449 root@103.244.247.188 -p 2244
 # Or open PuTTY: Host=103.244.247.188, Port=2244, User=root, Pass=$Password@1$

 ---
 ## Step 2 — Server Prerequisites

 # Update OS
 dnf update -y

 # Python 3 + venv
 dnf install python3 python3-venv python3-pip -y

 # Nginx (likely already installed — skip if present)
 dnf install nginx -y

 # Google Chrome + ChromeDriver for Selenium
 dnf install -y wget
 wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
 dnf install -y ./google-chrome-stable_current_x86_64.rpm

 # ChromeDriver — match version to installed Chrome
 google-chrome --version          # note version, e.g. 136.x.x
 # Download matching chromedriver from https://chromedriver.chromium.org/downloads
 # OR use the automatic method:
 pip3 install webdriver-manager   # add to requirements.txt too if not present

 # MySQL client libs (pymysql is pure Python — no C libs needed)
 # Confirm MySQL is running
 systemctl status mysqld

 ---
 ## Step 3 — Upload Project Files

 From your Windows machine (PowerShell), using pscp (PuTTY's scp):

 # Create destination directory on server first (run on server):
 # mkdir -p /opt/fastapi

 # Upload from local Windows machine:
 pscp -P 2244 -r E:\xfl-projects\website\nlisecurities\fastapi\* root@103.244.247.188:/opt/fastapi/

 Important files to upload (exclude venv/, __pycache__/):
 - main.py
 - requirements.txt
 - models/db.py, models/repository.py
 - services/dse_service.py, services/dse_service_async.py
 - utils/parser.py
 - cse_ca_bundle.pem (critical — CSE SSL fix)
 - cse_intermediate_ca.pem, leaf.pem

 ---
 ## Step 4 — Update Database Credentials for Production

 Edit /opt/fastapi/models/db.py on the server — change credentials to match the production MySQL:

 conn_params = {
     "host": "127.0.0.1",
     "user": "root",
     "password": "$Password@2$",   # production DB password
     "database": "nlsdb",
     "port": 3306,
     "cursorclass": pymysql.cursors.DictCursor
 }

 Also update CORS origins in main.py if not already done (already includes https://nlisecurities.com).

 ---
 ## Step 5 — Create Virtual Environment & Install Dependencies

 cd /opt/fastapi

 # Create venv (named myenv to match existing convention from almalinux-information.txt)
 python3 -m venv myenv

 # Activate
 source myenv/bin/activate

 # Install dependencies
 pip install --upgrade pip
 pip install -r requirements.txt

 # Verify key packages
 python -c "import fastapi, uvicorn, pymysql, selenium; print('OK')"

 # Deactivate when done
 deactivate

 ---
 ## Step 6 — Create MySQL Database & User (if not exists)

 mysql -u root -p   # password: $Password@2$

 CREATE DATABASE IF NOT EXISTS nlsdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
 -- Tables are auto-created by create_database_and_table() on FastAPI startup
 EXIT;

 ---
 ## Step 7 — Test Run (manual, before systemd)

 cd /opt/fastapi
 source myenv/bin/activate
 uvicorn main:app --host 192.168.101.238 --port 8080
 # Verify: curl http://192.168.101.238:8080/health  → {"status":"OK"}
 # Check logs for periodic_runner startup and first data fetch
 # Ctrl+C to stop
 deactivate

 ---
 ## Step 8 — Create systemd Service

 Create /etc/systemd/system/fastapi-market.service:

 [Unit]
 Description=NLI Securities FastAPI Market Data Service
 After=network.target mysqld.service
 Wants=mysqld.service

 [Service]
 Type=simple
 User=root
 WorkingDirectory=/opt/fastapi
 Environment="PATH=/opt/fastapi/myenv/bin"
 ExecStart=/opt/fastapi/myenv/bin/uvicorn main:app --host 192.168.101.238 --port 8080 --workers 1
 Restart=always
 RestartSec=5
 StandardOutput=journal
 StandardError=journal
 SyslogIdentifier=fastapi-market

 [Install]
 WantedBy=multi-user.target

 ▎ Note: Use --workers 1 only. The app uses asyncio.create_task() inside the lifespan for the periodic scraper —
 ▎ multiple workers would each spawn their own scraper, causing duplicate DB writes and rate-limit issues on DSE/CSE
 ▎ websites.

 # Enable and start
 systemctl daemon-reload
 systemctl enable fastapi-market
 systemctl start fastapi-market

 # Check status
 systemctl status fastapi-market

 # Follow logs
 journalctl -u fastapi-market -f

 ---
 ## Step 9 — Configure Nginx Reverse Proxy

 The existing config is at /etc/nginx/conf.d/nlisecurities.conf. Add a new location block inside the existing server
 { listen 443 ... } block:

 # FastAPI Market Data API
 location /mktapi/ {
     proxy_pass http://192.168.101.238:8080/;
     proxy_http_version 1.1;
     proxy_set_header Upgrade $http_upgrade;
     proxy_set_header Connection "upgrade";
     proxy_set_header Host $host;
     proxy_set_header X-Real-IP $remote_addr;
     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     proxy_set_header X-Forwarded-Proto $scheme;
     proxy_read_timeout 120s;
 }

 ▎ Note: The React frontend currently calls http://127.0.0.1:8000/... directly (Django). The FastAPI is on port 8080.
 ▎ If the frontend needs to call FastAPI through Nginx, update CORS and proxy path accordingly. For now the FastAPI
 ▎ is accessible directly on the LAN at 192.168.101.238:8080 — same pattern as Django.

 # Test and reload Nginx
 nginx -t
 systemctl reload nginx

 ---
 ## Step 10 — Firewall Rules

 # Open FastAPI port (internal LAN only if behind load balancer; open 8080)
 firewall-cmd --permanent --add-port=8080/tcp
 firewall-cmd --reload

 # Verify
 firewall-cmd --list-ports

 ---
 ## Step 11 — SELinux (AlmaLinux default: enforcing)

 # Check current mode
 getenforce   # likely "Enforcing"

 # Allow Nginx to connect to upstream (proxy_pass)
 setsebool -P httpd_can_network_connect 1

 # Allow the FastAPI process (runs as root — usually no additional policy needed)
 # If you see AVC denials:
 ausearch -c 'uvicorn' --raw | audit2allow -M fastapi-policy
 semodule -i fastapi-policy.pp

 ---
 ## Step 12 — SSL (Let's Encrypt)

 SSL is already configured for nlisecurities.com in the existing Nginx config
 (/etc/letsencrypt/live/nlisecurities.com/fullchain.pem). No new certificate is needed — the FastAPI service sits
 behind the existing SSL-terminated Nginx.

 To renew when needed:
 certbot renew --dry-run   # test renewal
 certbot renew             # actual renewal

 ---
 ## Step 13 — Verify Deployment

 # 1. Service health
 systemctl status fastapi-market

 # 2. API health check
 curl http://192.168.101.238:8080/health
 # Expected: {"status":"OK"}

 # 3. Market info endpoint (after ~30s for first scrape cycle)
 curl http://192.168.101.238:8080/market_info/DSE
 curl http://192.168.101.238:8080/market_info/CSE

 # 4. Via Nginx (HTTPS)
 curl https://nlisecurities.com/mktapi/health

 # 5. Live logs (watch periodic_runner output)
 journalctl -u fastapi-market -f --since "5 min ago"

 ---
 ## Step 14 — Troubleshooting

 ┌────────────────────────┬─────────────────────────┬────────────────────────────────────────────────────────────┐
 │        Problem         │        Diagnosis        │                            Fix                             │
 ├────────────────────────┼─────────────────────────┼────────────────────────────────────────────────────────────┤
 │ Connection refused on  │ Service not running     │ systemctl restart fastapi-market                           │
 │ 8080                   │                         │                                                            │
 ├────────────────────────┼─────────────────────────┼────────────────────────────────────────────────────────────┤
 │ Table doesn't exist    │ DB not initialized      │ Check create_database_and_table() ran on startup in logs   │
 ├────────────────────────┼─────────────────────────┼────────────────────────────────────────────────────────────┤
 │ Out of range value     │ Column too narrow       │ Already fixed in db.py — ensure updated file was uploaded  │
 ├────────────────────────┼─────────────────────────┼────────────────────────────────────────────────────────────┤
 │ Selenium ChromeDriver  │ Chrome/driver version   │ google-chrome --version, download matching chromedriver    │
 │ error                  │ mismatch                │                                                            │
 ├────────────────────────┼─────────────────────────┼────────────────────────────────────────────────────────────┤
 │ Permission denied on   │ cert bundle path wrong  │ Check CSE_CA_BUNDLE path in dse_service.py resolves to     │
 │ CSE SSL                │                         │ /opt/fastapi/cse_ca_bundle.pem                             │
 ├────────────────────────┼─────────────────────────┼────────────────────────────────────────────────────────────┤
 │ SELinux blocking       │ AVC denial in audit log │ ausearch -m avc -ts recent then apply policy               │
 ├────────────────────────┼─────────────────────────┼────────────────────────────────────────────────────────────┤
 │ Nginx 502 Bad Gateway  │ FastAPI not running or  │ curl 192.168.101.238:8080/health directly                  │
 │                        │ wrong port              │                                                            │
 ├────────────────────────┼─────────────────────────┼────────────────────────────────────────────────────────────┤
 │ Duplicate DB writes    │ Multiple workers        │ Confirm --workers 1 in systemd ExecStart                   │
 │ after restart          │                         │                                                            │
 └────────────────────────┴─────────────────────────┴────────────────────────────────────────────────────────────┘

 ---
 ## Step 15 — Production Best Practices

 # Log rotation (add to /etc/logrotate.d/fastapi-market)
 /var/log/fastapi-market/*.log {
     daily
     rotate 14
     compress
     missingok
     notifempty
 }

 # Monitor service restart count
 systemctl show fastapi-market --property=NRestarts

 # Set resource limits in systemd service (optional)
 [Service]
 MemoryMax=512M
 CPUQuota=50%

 # Keep Chrome/ChromeDriver updated (Selenium dep)
 # Add to a weekly cron:
 dnf update -y google-chrome-stable

##  Security notes:
 - Move DB credentials out of db.py into environment variables in the systemd unit:
 [Service]
 Environment="DB_PASSWORD=$Password@2$"
 - Then read with os.environ.get("DB_PASSWORD") in db.py
 - Remove --reload flag from uvicorn in production (already absent in the systemd unit above)
 - The --workers 1 constraint is architectural — the periodic scraper uses asyncio tasks, not process-safe shared
 state

 ---
 Files to Modify Summary

 ┌────────────────────┬────────────────────────────────────────────┬────────────────────────────────────┐
 │        File        │                  Location                  │               Change               │
 ├────────────────────┼────────────────────────────────────────────┼────────────────────────────────────┤
 │ models/db.py       │ /opt/fastapi/models/db.py                  │ Update DB password to $Password@2$ │
 ├────────────────────┼────────────────────────────────────────────┼────────────────────────────────────┤
 │ nlisecurities.conf │ /etc/nginx/conf.d/nlisecurities.conf       │ Add /mktapi/ location block        │
 ├────────────────────┼────────────────────────────────────────────┼────────────────────────────────────┤
     │                                                                                                               │
     │ Security notes:                                                                                               │
     │ - Move DB credentials out of db.py into environment variables in the systemd unit:                            │
     │ [Service]                                                                                                     │
     │ Environment="DB_PASSWORD=$Password@2$"                                                                        │
     │ - Then read with os.environ.get("DB_PASSWORD") in db.py                                                       │
     │ - Remove --reload flag from uvicorn in production (already absent in the systemd unit above)                  │
     │ - The --workers 1 constraint is architectural — the periodic scraper uses asyncio tasks, not process-safe     │
     │ shared state                                                                                                  │
     │                                                                                                               │
     │ ---                                                                                                           │
     │ Files to Modify Summary                                                                                       │
     │                                                                                                               │
     │ ┌────────────────────┬────────────────────────────────────────────┬────────────────────────────────────┐      │
     │ │        File        │                  Location                  │               Change               │      │
     │ ├────────────────────┼────────────────────────────────────────────┼────────────────────────────────────┤      │
     │ │ models/db.py       │ /opt/fastapi/models/db.py                  │ Update DB password to $Password@2$ │      │
     │ ├────────────────────┼────────────────────────────────────────────┼────────────────────────────────────┤      │
     │ │ nlisecurities.conf │ /etc/nginx/conf.d/nlisecurities.conf       │ Add /mktapi/ location block        │      │
     │ ├────────────────────┼────────────────────────────────────────────┼────────────────────────────────────┤      │
     │ │ New file           │ /etc/systemd/system/fastapi-market.service │ Create systemd unit                │      │
     │ └────────────────────┴────────────────────────────────────────────┴────────────────────────────────────┘     