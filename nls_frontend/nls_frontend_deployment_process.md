###  React Frontend (nls_frontend) — AlmaLinux Deployment Guide

## Context

 nls_frontend is a React 19 + Vite 7 SPA for NLI Securities. The built dist/ folder is served as static files from
 /var/www/reactapp/ by Nginx (already configured in nlisecurities.conf). No Node.js process runs in production —
 Nginx serves the static bundle directly.

 Critical issue to fix before building: All API service files have hardcoded http://127.0.0.1:8000 and
 http://127.0.0.1:8080 URLs. In production these will fail because the browser is on a remote machine. The fix is to
 use relative URLs so Nginx proxies them — the existing nlisecurities.conf already has /api/ and other proxy blocks
 for this.

 ---
 ## Step 1 — Fix API URLs in the Frontend (BEFORE Building)

 This must be done on your Windows dev machine before uploading.

 Option A — Environment Variable (Recommended)

 Create nls_frontend/.env.production:

 VITE_API_BASE=
 VITE_FASTAPI_BASE=

 Empty values mean relative URLs (same domain), which Nginx will proxy correctly.

 Then update each service file to use the env var.

 src/services/getApi.jsx and src/services/postApi.jsx — replace http://127.0.0.1:8000 with:
 const BASE = import.meta.env.VITE_API_BASE ?? '';

 src/services/chartService.jsx — replace:
 - http://127.0.0.1:8000 with import.meta.env.VITE_API_BASE ?? ''
 - http://127.0.0.1:8080 with import.meta.env.VITE_FASTAPI_BASE ?? ''

 Option B — Quick Find & Replace (Simpler)

 In each service file, replace:
 - http://127.0.0.1:8000 → `` (empty string — relative URL)
 - http://127.0.0.1:8080 → `` (empty string)

 This works because Nginx serves everything from the same domain and proxies /api/, /slider/, etc. to the Django
 backend.

 ▎ Note: The existing Nginx config proxies /api/, /admin/, /ckeditor5/, /static/, /media/ to Django. But the frontend
 ▎ calls endpoints like /slider/, /feature/, /event/ directly — these are NOT proxied in the current
 ▎ nlisecurities.conf. You must add proxy blocks for all raw Django API paths (see ## Step 7).

 ---
 ## Step 2 — Build the Production Bundle (on Windows)

 cd E:\xfl-projects\website\nlisecurities\nls_frontend

 # Install dependencies if needed
 npm install

 # Production build
 npm run build
 # Output: nls_frontend/dist/

 Verify dist/index.html exists and dist/assets/ contains JS/CSS bundles.

 ---
 ## Step 3 — Connect to the Server

 # Via jump server
 ssh -J xflmchowdhury@103.244.247.59:8449 root@103.244.247.188 -p 2244
 # PuTTY: Host=103.244.247.188, Port=2244, User=root, Pass=$Password@1$

 ---
 ## Step 4 — Server Prerequisites

 # Nginx (likely already installed — skip if present)
 dnf install nginx -y
 systemctl enable nginx
 systemctl start nginx

 # Certbot (skip if SSL cert already exists)
 dnf install epel-release -y
 dnf install certbot python3-certbot-nginx -y

 No Node.js needed on the server — the build runs locally and you upload the dist/ folder.

 ---
 ## Step 5 — Create Web Directory & Upload Build

 # On server: create target directory
 mkdir -p /var/www/reactapp

 From your Windows machine (PowerShell):

 # Upload the entire dist/ folder contents to /var/www/reactapp/
 pscp -P 2244 -r E:\xfl-projects\website\nlisecurities\nls_frontend\dist\* root@103.244.247.188:/var/www/reactapp/

 Verify on the server:
 ls /var/www/reactapp/
 # Should show: index.html  assets/  vite.svg

 ---
 ## Step 6 — Set File Permissions

 # Nginx runs as nginx user — give it read access
 chown -R nginx:nginx /var/www/reactapp/
 chmod -R 755 /var/www/reactapp/

 ---
 ## Step 7 — Update Nginx Configuration

 The existing /etc/nginx/conf.d/nlisecurities.conf serves the React SPA but is missing proxy blocks for the raw
 Django API endpoints the frontend calls (/slider/, /feature/, /event/, etc.). Add them.

 Upload the updated config from Windows:
 pscp -P 2244 E:\xfl-projects\website\nlisecurities\nlisecurities.conf
 root@103.244.247.188:/etc/nginx/conf.d/nlisecurities.conf

 Or edit directly on the server. The full updated config should be:

 server {
     listen 80;
     server_name nlisecurities.com www.nlisecurities.com;
     return 301 https://$host$request_uri;
 }

 server {
     listen 443 ssl http2;
     server_name nlisecurities.com www.nlisecurities.com;

     ssl_certificate     /etc/letsencrypt/live/nlisecurities.com/fullchain.pem;
     ssl_certificate_key /etc/letsencrypt/live/nlisecurities.com/privkey.pem;

     # React SPA
     root /var/www/reactapp;
     index index.html;

     location / {
         try_files $uri /index.html;
     }

     # ── Django CMS / admin endpoints ──────────────────────────────
     location /admin/ {
         proxy_pass http://192.168.101.238:8000/admin/;
         proxy_set_header Host $host;
         proxy_set_header X-Real-IP $remote_addr;
         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
         proxy_set_header X-Forwarded-Proto $scheme;
     }
     location /ckeditor5/ {
         proxy_pass http://192.168.101.238:8000/ckeditor5/;
         proxy_set_header Host $host;
         proxy_set_header X-Real-IP $remote_addr;
         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
         proxy_set_header X-Forwarded-Proto $scheme;
     }

     # ── Django REST API endpoints (all raw paths) ─────────────────
     location ~ ^/(about|about_image|slider|service|product|feature|offer|board_member|mancom|tech|event|market_news|
 client|faq|privacy-policy|ipo|branch|top_share_price_by|categories|contact|minutes_index|market_info|market_index|ti
 cker_price|sector_wise_inst|event_dtl|service_dtl|research)/ {
         proxy_pass http://192.168.101.238:8000;
         proxy_set_header Host $host;
         proxy_set_header X-Real-IP $remote_addr;
         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
         proxy_set_header X-Forwarded-Proto $scheme;
     }

     # ── FastAPI market data endpoints ─────────────────────────────
     location ~
 ^/(minutes_index_cse|market_info|market_index|ticker_price|top_share_price_by|ipo_offer|dse_news|cse_news)/ {
         proxy_pass http://192.168.101.238:8080;
         proxy_set_header Host $host;
         proxy_set_header X-Real-IP $remote_addr;
         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
         proxy_set_header X-Forwarded-Proto $scheme;
         proxy_read_timeout 120s;
     }

     # ── Static & media ─────────────────────────────────────────────
     location /static/ {
         alias /var/www/django_static/;
     }
     location /media/ {
         alias /var/www/django_media/;
     }
 }

 # Test config then reload
 nginx -t
 systemctl reload nginx

 ---
 ## Step 8 — SELinux Permissions

 # Check mode
 getenforce   # likely "Enforcing"

 # Allow Nginx to serve files from /var/www/reactapp/
 chcon -Rt httpd_sys_content_t /var/www/reactapp/

 # Allow Nginx to make network connections (for proxy_pass)
 setsebool -P httpd_can_network_connect 1

 # If you see AVC denials:
 ausearch -m avc -ts recent

 ---
 ## Step 9 — Firewall Rules

 # HTTP and HTTPS must be open for Nginx
 firewall-cmd --permanent --add-service=http
 firewall-cmd --permanent --add-service=https
 firewall-cmd --reload

 # Verify
 firewall-cmd --list-all

 No extra ports needed — the React app is served by Nginx on 443/80. The backend ports (8000, 8080) are internal LAN
 only.

 ---
 ## Step 10 — SSL (Let's Encrypt)

 If the cert for nlisecurities.com already exists (likely from Django deployment):
 # Just verify it's active
 certbot certificates
 # Check expiry date shown

 If not yet obtained:
 certbot --nginx -d nlisecurities.com -d www.nlisecurities.com

 Verify auto-renewal:
 certbot renew --dry-run
 systemctl status certbot-renew.timer

 ---
 ## Step 11 — Verify Deployment

 # 1. Nginx serving the SPA
 curl -I https://nlisecurities.com/
 # Expected: HTTP/2 200, Content-Type: text/html

 # 2. React router fallback works (deep link)
 curl -I https://nlisecurities.com/about
 # Expected: HTTP/2 200 (returns index.html, not 404)

 # 3. API proxy working
 curl https://nlisecurities.com/slider/
 # Expected: JSON array (not HTML error page)

 curl https://nlisecurities.com/feature/
 curl https://nlisecurities.com/event/

 # 4. Market data (FastAPI)
 curl https://nlisecurities.com/market_info/DSE
 # Expected: JSON with trade/volume/value fields

 # 5. Static assets loading
 curl -I https://nlisecurities.com/assets/   # Vite JS bundle

 Open browser at https://nlisecurities.com and check the browser console for any remaining CORS or 404 errors.

 ---
 ## Step 12 — Troubleshooting

 ┌─────────────────────┬──────────────────────────────────┬──────────────────────────────────────────────────────┐
 │       Problem       │            Diagnosis             │                         Fix                          │
 ├─────────────────────┼──────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ Blank page / white  │ index.html not at                │ ls /var/www/reactapp/ — re-upload if missing         │
 │ screen              │ /var/www/reactapp/               │                                                      │
 ├─────────────────────┼──────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ React routes return │ try_files $uri /index.html       │ Verify location / block in Nginx config              │
 │  404                │ missing                          │                                                      │
 ├─────────────────────┼──────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ API calls fail      │ Frontend still using hardcoded   │ Re-do ## Step 1, rebuild, re-upload dist/               │
 │ (CORS/404)          │ 127.0.0.1                        │                                                      │
 ├─────────────────────┼──────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ 502 Bad Gateway on  │ Django/FastAPI not running       │ systemctl status nls-backend fastapi-market          │
 │ API                 │                                  │                                                      │
 ├─────────────────────┼──────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ CSS/JS assets 404   │ Vite base path mismatch          │ Add base: '/' to vite.config.js, rebuild             │
 ├─────────────────────┼──────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ SELinux denies      │ AVC in audit log                 │ chcon -Rt httpd_sys_content_t /var/www/reactapp/     │
 │ Nginx               │                                  │                                                      │
 ├─────────────────────┼──────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ SSL cert missing    │ certbot not run                  │ certbot --nginx -d nlisecurities.com                 │
 ├─────────────────────┼──────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ Media images broken │ /media/ not served               │ Verify /var/www/django_media/ exists and is          │
 │                     │                                  │ populated                                            │
 ├─────────────────────┼──────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ Old build cached    │ Browser cache                    │ Hard refresh (Ctrl+Shift+R); Vite adds content       │
 │                     │                                  │ hashes so this is rare                               │
 └─────────────────────┴──────────────────────────────────┴──────────────────────────────────────────────────────┘

 ---
 ## Step 13 — Production Best Practices

 Rebuild & Redeploy Workflow

 Every time frontend code changes:

 # On Windows dev machine:
 cd E:\xfl-projects\website\nlisecurities\nls_frontend
 npm run build

 # Upload new dist/ to server:
 pscp -P 2244 -r dist\* root@103.244.247.188:/var/www/reactapp/

 No server restart needed — Nginx serves static files directly.

 Automate deploy with a script (optional)

 Save as deploy-frontend.ps1 on Windows:
 cd E:\xfl-projects\website\nlisecurities\nls_frontend
 npm run build
 pscp -P 2244 -r dist\* root@103.244.247.188:/var/www/reactapp/
 Write-Host "Deploy complete"

 Security

 - Never commit .env.production with real secrets to git
 - Nginx already handles HTTPS termination — no further SSL config needed in React
 - Set Cache-Control headers for static assets in Nginx for performance:
 location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2)$ {
     expires 1y;
     add_header Cache-Control "public, immutable";
 }

 No systemd service needed

 React in production is pure static files — Nginx serves them directly. There is no Node.js process to manage or keep
 alive. The Nginx service itself is the only thing that needs to be running (systemctl enable nginx).

 ---
 Files to Modify Summary

 ┌────────────────────┬────────────────────────────────────────────┬──────────────────────────────────────────────┐
 │        File        │                  Location                  │                    Change                    │
 ├────────────────────┼────────────────────────────────────────────┼──────────────────────────────────────────────┤
 │ getApi.jsx         │ nls_frontend/src/services/getApi.jsx       │ Replace http://127.0.0.1:8000 with ''        │
 │                    │                                            │ (relative)                                   │
 ├────────────────────┼────────────────────────────────────────────┼──────────────────────────────────────────────┤
 │ postApi.jsx        │ nls_frontend/src/services/postApi.jsx      │ Replace http://127.0.0.1:8000 with ''        │
 │                    │                                            │ (relative)                                   │
 ├────────────────────┼────────────────────────────────────────────┼──────────────────────────────────────────────┤
 │ chartService.jsx   │ nls_frontend/src/services/chartService.jsx │ Replace both hardcoded URLs with ''          │
 │                    │                                            │ (relative)                                   │
 ├────────────────────┼────────────────────────────────────────────┼──────────────────────────────────────────────┤
 │ nlisecurities.conf │ /etc/nginx/conf.d/nlisecurities.conf       │ Add regex proxy blocks for all raw Django +  │
 │                    │                                            │ FastAPI endpoints                            │
 ├────────────────────┼────────────────────────────────────────────┼──────────────────────────────────────────────┤
 │ Upload dist/       │ /var/www/reactapp/                         │ Upload after running npm run build           │
 └────────────────────┴────────────────────────────────────────────┴──────────────────────────────────────────────┘
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌