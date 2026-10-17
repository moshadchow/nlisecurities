# Spec: Landing Page Splash Image

## Overview

Implement a Django-admin-managed promotional splash image on the NLS Securities landing page (`/`), displayed once per browser tab session on the first eligible visit, with a dismiss control and an optional click-through link.

The splash must follow the visual layout of the attached EBL Securities screenshot:

- Display the promotional image inside a compact, white modal centered horizontally and vertically in the viewport.
- Cover the viewport with a semi-transparent dark backdrop so the existing landing page remains visible but dimmed.
- Place a close (`×`) button near the upper-right corner of the modal.
- Preserve the image's original aspect ratio and scale it down proportionally when necessary.
- Keep the image contained within the modal; it must never occupy the entire viewport.
- Keep the existing landing page, navigation, hero slider, market ticker, and other components intact behind the overlay.

**Important:** Only the backdrop covers the viewport. The promotional image must not become a full-screen image, a standalone loading page, or a replacement for the landing page.

Administrators should be able to manage the promotional image through Django admin without requiring a code deployment.

## Depends on

*No previous steps/specs required.* `specs/` is currently empty; this is step `01` and is self-contained.

Reuse existing patterns from `Sliders`, `GET /slider/`, and `HeroSlider.jsx` where appropriate, but do not modify the existing slider functionality.

Use the attached EBL Securities screenshot as the visual reference for the modal position, image presentation, backdrop, and close control.

## Service ownership

- **Django backend** (`nls_backend/`, port `8000`): new `SplashImage` content model, serializer, Django admin registration, and read-only endpoint.
- **Frontend** (`nls_frontend/`): new splash modal component, API service method, responsive styling, session-based display control, and landing page integration.
- **Market Data** (`fastapi/`, port `8080`): no changes.

## Routes

- `GET /splash/` — returns the active splash image entry containing `title`, `image`, `link_url`, and `is_active`. Owner: Django on port `8000`.
- The endpoint must follow the existing public content API response conventions. Return the active entry or the established empty response when no active entry exists. Never return inactive entries.
- `nls_frontend/vite.config.js`: add a `/splash` proxy entry targeting the Django backend, following the existing `/slider`, `/service`, and `/media` proxy patterns.
- Frontend API calls must use relative URLs, such as `${BASE}/splash/`, without hardcoded hostnames or ports.
- Production Nginx (`nlisecurities.conf`, potentially gitignored and available only on the production server): configure `/splash/` to proxy to Django on `127.0.0.1:8000`, following the existing content endpoint configuration.
- Verify that `/media/` is correctly routed so the uploaded splash image is accessible in production.
- Content endpoints must follow the existing root-level routing convention; do not introduce an `/api/` prefix unless the existing routing architecture requires it.
- FastAPI routes: none.

## Database changes

- Add a new Django-managed `SplashImage` model after verifying that an equivalent model does not already exist in `nls_backend/api/models.py`.
- Suggested fields:
  - `title = CharField(max_length=100)`
  - `image = ImageField(upload_to='splash/')`
  - `link_url = URLField(blank=True)`
  - `is_active = BooleanField(default=True)`
  - `created_at = DateTimeField(auto_now_add=True)`
- Set model ordering to `['-created_at']`.
- Ensure only one splash image can be active at a time through appropriate application-level validation or database constraints compatible with the existing database and Django version.
- Register the model in Django admin so authorized administrators can upload images, configure an optional destination URL, and activate or deactivate the splash.
- Generate and apply the Django migration:

  ```bash
  python manage.py makemigrations api
  python manage.py migrate
  ```

- Uploaded images must be stored under the configured Django `MEDIA_ROOT`: locally in the existing media directory and in production at `/var/www/django_media/`, if that matches the actual deployment configuration.
- FastAPI-managed tables, including `api_share_prices`, `api_market_info`, `api_minute_data`, `api_market_index`, `api_ticker_price`, and `api_sector_inst`, must remain unchanged. The shared `nlsdb` MySQL database used by FastAPI must not be modified by this feature.

## Frontend changes

React 19 + Vite 7, JSX only; no TypeScript.

- Add `src/components/SplashScreen.jsx`.
  - Fetch the active splash entry from Django.
  - Render a fixed-position, semi-transparent backdrop covering the viewport.
  - Center a compact white modal within the viewport.
  - Display the promotional image inside the modal with appropriate padding.
  - Position a close (`×`) button near the modal's upper-right corner.
  - Preserve the image's aspect ratio and prevent it from stretching or cropping.
  - Constrain the modal to the available viewport dimensions, including on mobile.
  - Support dismissal through the close button, `Escape`, and clicks outside the modal.
  - Prevent clicks inside the modal or on its image/link from triggering outside-click dismissal.
  - Follow accessible dialog practices, including an accessible close-button label and appropriate focus handling.
  - Display the splash only on the landing page (`/`).
  - Render nothing if the API returns no active entry, the request fails, or the image cannot be loaded.
  - Clean up event listeners when the component unmounts.
  - Use two-space indentation.

- **Display once per browser session:**
  - Use `sessionStorage` with a stable key such as `nls_splash_seen`.
  - Show the splash only on the first eligible visit within the current browser tab session.
  - Record the session flag when the splash is actually displayed.
  - After dismissal, do not display it again during that session, including after refreshing the landing page or navigating away and returning to `/`.
  - Allow it to display again in a new browser session.
  - Do not use `localStorage`, persistent cookies, or arbitrary timer-based dismissal.
  - If the API fails or no valid image is available, do not mark the session as seen.

- **Modal styling:**
  - Use a viewport-fixed backdrop with a sufficiently high `z-index`.
  - Apply a dark translucent background, similar to the attached screenshot.
  - Center the modal horizontally and vertically.
  - Use a white modal container with modest padding.
  - Keep the close control visible and accessible without covering important image content.
  - Ensure the image is scaled proportionally and the modal does not overflow the viewport.

  Example starting CSS:

  ```css
  .splash-backdrop {
    position: fixed;
    inset: 0;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px 16px;
    background: rgba(0, 0, 0, 0.5);
    box-sizing: border-box;
  }

  .splash-modal {
    position: relative;
    width: fit-content;
    max-width: calc(100vw - 32px);
    max-height: calc(100vh - 48px);
    padding: 16px;
    background: #fff;
    box-sizing: border-box;
  }

  .splash-modal__image {
    display: block;
    width: auto;
    height: auto;
    max-width: 100%;
    max-height: calc(100vh - 80px);
    object-fit: contain;
  }
  ```

  Adapt the CSS to the actual image dimensions and existing styling conventions. The image should use its natural dimensions when it fits, otherwise scale down proportionally.

- **Optional click-through link:**
  - If `link_url` is configured, allow the promotional image to link to that destination.
  - If no link is configured, display the image without a link.
  - Ensure clicking the image does not trigger outside-click dismissal.
  - Use appropriate security attributes if opening external links in a new tab.
  - Keep the close button independently clickable.

- Modify `src/services/getApi.jsx`:
  - Add `getSplash()` following the existing `getCarousal()` pattern.
  - Fetch `${BASE}/splash/` using GET.
  - Follow existing JSON parsing and error-handling conventions.
  - Do not hardcode `http://127.0.0.1:8000`.
  - Do not modify unrelated API methods.

- Modify `src/pages/Home.jsx`:
  - Mount `<SplashScreen />` at the top of the landing page tree, above the hero-slider block in render order.
  - Ensure the component is only active on `/`, not globally across all routes.
  - Do not otherwise modify the hero slider, navigation, market ticker, or unrelated landing page sections.

- Do not use Jinja2 templates.
- Do not modify `chartService.jsx` or unrelated market-data functionality.

## Files to change

Every file expected to be modified:

- `nls_backend/api/models.py` — add the `SplashImage` model.
- `nls_backend/api/serializers.py` — add `SplashImageSerializer`.
- `nls_backend/api/views.py` — add the read-only `Splash_view` function using `@api_view(['GET'])`.
- `nls_backend/api/urls.py` — register the root-level `splash/` route.
- `nls_backend/api/admin.py` — register `SplashImage` with appropriate list display and administration options.
- `nls_frontend/vite.config.js` — add the `/splash` development proxy entry targeting Django on port `8000`.
- `nls_frontend/src/services/getApi.jsx` — add `getSplash()`.
- `nls_frontend/src/pages/Home.jsx` — integrate `SplashScreen` on the landing page.
- `nlisecurities.conf` — configure production `/splash/` and verify `/media/` routing, if the live configuration is accessible and can be changed appropriately.

Do not modify unrelated files.

## Files to create

Every new file expected to be created:

- `specs/01-landing-page-splash-image.md` — this specification.
- `nls_frontend/src/components/SplashScreen.jsx` — the splash modal component.
- `nls_backend/api/migrations/00XX_splashimage.py` — generated by Django, with the actual filename determined by `makemigrations`.

Create any additional CSS file only if required by the existing frontend architecture; otherwise, follow the project's existing styling conventions.

## New dependencies

No new dependencies.

Do not add npm packages or Python packages for this feature. Use the existing React, Django, Django REST Framework, and frontend styling capabilities.

## Rules for implementation

- **Visual behavior:** the backdrop covers the viewport, but the image remains inside a compact, centered modal. Never implement a full-screen image overlay.
- **Session behavior:** show the splash once per browser tab session on the first eligible visit. Use `sessionStorage`, not `localStorage`.
- **Dismissal:** support the close button, `Escape`, and outside clicks. Prevent clicks within the modal from dismissing it.
- **Routing:** display the splash only on `/`. Do not mount it globally across all routes.
- **Failure handling:** missing configuration, API errors, invalid image URLs, or image-loading failures must not block or break the landing page.
- **Backend:** use Django REST Framework function-based views in `nls_backend/api/views.py`, serializers in `serializers.py`, models in `models.py`, routes in `urls.py`, and admin registration in `admin.py`.
- **Rich text:** use `CKEditor5Field` only if a rich-text field is genuinely required. It is not required for the image-only model.
- **Migrations:** generate and apply Django migrations after model changes. Run `python manage.py check` and `python manage.py collectstatic` where appropriate for the deployment workflow.
- **Frontend:** JSX only, two-space indentation, components in `src/components/`, pages in `src/pages/`, and API calls in `src/services/`.
- **API URLs:** use relative URLs and the existing `BASE` convention. Do not hardcode hostnames or ports.
- **Proxy configuration:** add the development proxy in `vite.config.js`. Verify production Nginx routing before deployment.
- **FastAPI:** no changes to `fastapi/main.py`, `fastapi/services/`, `fastapi/models/db.py`, or `fastapi/models/repository.py`.
- **Production:** preserve `DEBUG = False`, existing secret configuration, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and current deployment conventions.
- **Repository hygiene:** never commit secrets, `.env` files, `*.pem`, `venv/`, `node_modules/`, uploaded media, generated deployment assets, or other ignored operational files.
- **Testing:** do not claim tests passed unless they were actually executed.

## Definition of done

- [ ] `SplashImage` is available in Django admin, and authorized administrators can upload an image, configure an optional link, and activate or deactivate the splash.
- [ ] The Django migration applies cleanly.
- [ ] `python manage.py check` passes.
- [ ] `GET /splash/` returns the active entry in the expected response format, or the established empty response when no active entry exists.
- [ ] Inactive entries are excluded, and multiple active entries cannot cause ambiguous selection.
- [ ] The endpoint works directly against Django on port `8000` and through the Vite proxy on port `5173`.
- [ ] Uploaded images resolve correctly through the configured `/media/` URL.
- [ ] `npm run lint` passes if the script is defined in the project, and the production frontend build succeeds.
- [ ] The splash appears only on the landing page (`/`).
- [ ] The image is centered inside a compact white modal, with a dark translucent backdrop and a visible close button, matching the attached screenshot.
- [ ] The image preserves its aspect ratio and never fills the viewport.
- [ ] The landing page remains visible behind the backdrop, and existing functionality remains intact.
- [ ] The close button, `Escape`, and outside click dismiss the modal correctly.
- [ ] The splash appears at most once per browser tab session and does not reappear after dismissal during the same session.
- [ ] A new browser session can display the splash again.
- [ ] The optional click-through link works when configured.
- [ ] API failures, absent active entries, and broken images do not block the landing page.
- [ ] Desktop, tablet, and mobile layouts work without overflow.
- [ ] Production Nginx changes are verified or clearly documented if the live configuration is unavailable.
- [ ] No unrelated FastAPI, market-data, slider, or landing page functionality is changed.

---