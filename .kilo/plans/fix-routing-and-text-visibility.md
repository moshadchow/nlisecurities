# Fix Raw JSON Display on Refresh & Text Visibility Across Sub-Pages — Implementation Plan

## Root Cause Analysis

### Issue 1: Raw JSON Display on Browser Refresh
**Root Cause**: Vite dev server proxy uses **prefix matching**. Frontend routes conflict with API proxy rules:

| Frontend Route | Conflicting Proxy Rule | What Happens on Refresh |
|----------------|------------------------|-------------------------|
| `/service_dtl/:id` | `/service` → Django | Proxy intercepts, returns `/service/:id` JSON |
| `/event_dtl/:id` | `/event` → Django | Proxy intercepts, returns `/event/:id` JSON |
| `/event/:id` | `/event` → Django | Proxy intercepts, returns `/event/:id` JSON |
| `/research/:id` | `/research` → Django | Proxy intercepts, returns `/research/:id` JSON |
| `/privacy-policy` | `/privacy-policy` → Django | Proxy intercepts, returns policy JSON |
| `/ipo` | `/ipo` → Django | Proxy intercepts, returns IPO JSON |
| `/branch` | `/branch` → Django | Proxy intercepts, returns branch JSON |

The proxy config in `vite.config.js` lines 12-42 matches ANY request starting with these prefixes.

### Issue 2: Text Visibility on Sub-Pages
**Root Cause**: API returns HTML with inline light-theme styles (white backgrounds, dark text). The `ContentPage` → `CKEditorViewer` pipeline renders this via `dangerouslySetInnerHTML`. The `ckeditor-styles.css` was designed for light theme with hardcoded colors (`#444`, `#0d6efd`, `#e5e5e5`, `#f8f9fa`, etc.).

**Affected pages using `ContentPage`/`CKEditorViewer`:**
- `PrivacyPolicy.jsx` ✅ (partially fixed in previous task)
- `ServiceDetails.jsx` — `/service_dtl/:id`
- `EventDetails.jsx` — `/event_dtl/:id`
- `About.jsx` — `/about`

---

## Implementation Plan

### Phase 1: Fix Routing/Proxy Conflict (Critical)

#### Option A: Add `/api` Prefix to All API Calls (Recommended)
This cleanly separates frontend routes from API routes.

**Files to modify:**
1. **`vite.config.js`** — Replace all proxy rules with single `/api` proxy:
   ```js
   proxy: {
     '/api': { target: DJANGO, changeOrigin: true, rewrite: path => path.replace(/^\/api/, '') },
     '/media': { target: DJANGO, changeOrigin: true },
     '/ipo_offer': { target: FASTAPI, changeOrigin: true },
     '/dse_news': { target: FASTAPI, changeOrigin: true },
     '/cse_news': { target: FASTAPI, changeOrigin: true },
     '/minutes_index_cse': { target: FASTAPI, changeOrigin: true },
   }
   ```

2. **`src/services/getApi.jsx`** — Prepend `/api` to all Django endpoints:
   - `${BASE}/about/` → `${BASE}/api/about/`
   - `${BASE}/service/` → `${BASE}/api/service/`
   - ...all 25+ endpoints

3. **`src/services/chartService.jsx`** — Prepend `/api` to Django endpoints:
   - `${DJANGO_BASE}/minutes_index/${id}` → `${DJANGO_BASE}/api/minutes_index/${id}`
   - ...all Django endpoints

4. **`src/services/postApi.jsx`** — Same change

5. **`src/pages/ResearchPage.jsx`** — Line 17: `http://127.0.0.1:8000/research/${id}` → `http://127.0.0.1:8000/api/research/${id}` (or use relative `/api/research/${id}`)

#### Option B: Use Exact Match Proxy Rules (Alternative)
Use `http-proxy-middleware` path filtering to only proxy exact API paths. More complex, error-prone.

**Decision**: Use Option A (`/api` prefix) — standard practice, robust, future-proof.

---

### Phase 2: Fix Text Visibility — Shared Dark-Theme HTML Renderer

The previous task fixed `ckeditor-styles.css` for dark theme. Need to verify it works for all pages and add any missing styles.

**Files to verify/update:**
1. **`src/assets/ckeditor-styles.css`** — Already updated in previous task. Verify covers all HTML elements from API content.

2. **`src/index.css`** — Ensure global `.text-muted` override exists (added in previous task).

3. **Check all `ContentPage` usages** for additional styling needs:
   - `ServiceDetails.jsx` — Uses `ContentPage` in col-md-9, sidebar has Bootstrap `list-group-item` classes
   - `EventDetails.jsx` — Same structure
   - `About.jsx` — Uses `ContentPage` in col-lg-12
   - `PrivacyPolicy.jsx` — Uses `ContentPage` directly

4. **Add shared dark-theme styles for common components**:
   - `.list-group-item` overrides (sidebar in ServiceDetails/EventDetails)
   - `.card` overrides (ResearchPage cards)
   - Form controls in ResearchPage search input

---

### Phase 3: Verify & Test All Sub-Pages

**Sub-pages to test after fixes:**
| Page | Route | Uses ContentPage | API Endpoint |
|------|-------|------------------|--------------|
| Home | `/` | No | Multiple |
| About | `/about` | Yes | `/api/about/` |
| Service (list) | `/service` | No | `/api/service/` |
| Service Details | `/service_dtl/:id` | Yes | `/api/service/:id` |
| Director | `/director/` | No | `/api/board_member/` |
| Feature | `/feature` | No | `/api/feature/` |
| Contact | `/contact` | No | `/api/contact/` |
| IPO | `/ipo` | No | `/api/ipo/` |
| Market News | `/marketNews` | No | `/api/market_news/` |
| Branch | `/branch` | No | `/api/branch/` |
| Sector | `/sector` | No | N/A |
| Download | `/download` | No | `/api/categories/` |
| Event (list) | `/event/:id` | No | `/api/event/` |
| Event Details | `/event_dtl/:id` | Yes | `/api/event/:id` |
| Privacy Policy | `/privacy-policy` | Yes | `/api/privacy-policy/` |
| Research | `/research/:id` | No | `/api/research/:id` |

---

## Files to Modify

### Routing Fix (Phase 1)
| File | Change |
|------|--------|
| `nls_frontend/vite.config.js` | Replace proxy rules with `/api` prefix |
| `nls_frontend/src/services/getApi.jsx` | Add `/api` prefix to all 25+ Django endpoints |
| `nls_frontend/src/services/chartService.jsx` | Add `/api` prefix to 9 Django endpoints |
| `nls_frontend/src/services/postApi.jsx` | Add `/api` prefix |
| `nls_frontend/src/pages/ResearchPage.jsx` | Change hardcoded URL to use `/api/` |

### Text Visibility Fix (Phase 2)
| File | Change |
|------|--------|
| `nls_frontend/src/index.css` | Add dark-theme overrides for `.list-group-item`, `.form-control`, `.input-group-text`, ResearchPage card styles |
| `nls_frontend/src/assets/ckeditor-styles.css` | Verify completeness (already updated) |

---

## Validation Checklist

### Routing/Refresh Tests
- [ ] Open homepage → renders
- [ ] Navigate to `/service` → renders service list
- [ ] Navigate to `/service_dtl/1` → renders service detail
- [ ] **Refresh `/service_dtl/1`** → renders service detail (NOT JSON)
- [ ] Open `/service_dtl/1` in new tab → renders service detail
- [ ] Refresh `/event_dtl/1` → renders event detail
- [ ] Refresh `/research/some-id` → renders research page
- [ ] Refresh `/privacy-policy` → renders policy page
- [ ] Refresh `/ipo` → renders IPO page
- [ ] Navigate back/forward → works correctly
- [ ] Unknown route `/unknown` → shows 404 (need to add catch-all route)

### Text Visibility Tests
- [ ] Service Details: description text readable, no white backgrounds
- [ ] Event Details: description text readable
- [ ] About page: content readable
- [ ] Privacy Policy: content readable (already fixed)
- [ ] Research Page: cards, search input, text readable
- [ ] All pages: headings `#F1F5F9`, body `#E2E8F0`/`#CBD5E1`, muted `#A7B4C8`, links `#2DD4BF`
- [ ] Tables, lists, blockquotes, code blocks readable
- [ ] Mobile/tablet/desktop: text wraps, no clipping

### API Integration Tests
- [ ] All API calls return expected JSON
- [ ] No console errors on page loads
- [ ] Network tab shows API calls to `/api/...` paths
- [ ] No requests to frontend routes returning JSON

---

## Risk Mitigation

1. **API prefix change affects all frontend API calls** — Test thoroughly, but changes are mechanical (prepend `/api`)
2. **Production Nginx config** — Must also proxy `/api/` to Django. Document this requirement.
3. **ResearchPage uses hardcoded URL** — Only place not using `getApi.jsx`. Fix to use relative `/api/`
4. **FastAPI endpoints** (`/ipo_offer`, `/dse_news`, etc.) — Keep as-is, they don't conflict with frontend routes

---

## Open Questions

1. **Production deployment**: Does the Nginx config need updating to proxy `/api/` to Django? (Yes, but out of scope for dev fix — document it)
2. **Catch-all 404 route**: Should we add `<Route path="*" element={<NotFound/>}>` to App.jsx? (Recommended)
3. **VITE_API_BASE env var**: Currently empty string. After fix, should it be `/api`? Or keep empty and prepend in code? (Prepend in code for clarity)

---

## Implementation Order

1. **Fix routing first** (Phase 1) — unblocks all testing
2. **Verify text visibility** (Phase 2) — apply shared CSS fixes
3. **Full test matrix** (Phase 3) — verify all pages