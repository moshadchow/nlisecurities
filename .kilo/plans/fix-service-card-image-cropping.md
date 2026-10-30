# Fix Image Cropping in Service Details Cards — Implementation Plan

## Current State Analysis

### Image Rendering Path
1. **ServiceDetails.jsx** → uses `ContentPage` component
2. **ContentPage.jsx** → uses `CKEditorViewer` component  
3. **CKEditorViewer.jsx** → renders HTML via `dangerouslySetInnerHTML` with class `ckeditor-content`
4. **ckeditor-styles.css** → styles `.ckeditor-content img` (lines 82-88)

### Current Image Styles (ckeditor-styles.css:82-88)
```css
.ckeditor-content img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1rem auto;
  border-radius: 6px;
}
```

**Missing:** `object-fit` and `object-position` properties — defaults to `object-fit: fill` which stretches/crops images.

### Root Cause
Images from the API (service descriptions) contain embedded text/graphics. Without `object-fit: contain`, the browser stretches images to fill the container width, cropping content that doesn't match the container's aspect ratio.

## Implementation Plan

### 1. Fix Image Styles in `ckeditor-styles.css`
**File:** `nls_frontend/src/assets/ckeditor-styles.css`

Add `object-fit: contain` and `object-position: center` to `.ckeditor-content img`:
```css
.ckeditor-content img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1rem auto;
  border-radius: 6px;
  object-fit: contain;
  object-position: center;
}
```

Also apply to CKEditor figure images (lines 96-99):
```css
.ckeditor-content figure.image,
.ckeditor-content figure.image img {
  max-width: 100%;
  object-fit: contain;
  object-position: center;
}
```

### 2. Ensure Proper Container Background
When `object-fit: contain` leaves empty space (letterboxing), add a dark background to the image wrapper so empty areas blend with the dark theme:
```css
.ckeditor-content figure.image {
  background: var(--color-surface);
  border-radius: 6px;
  padding: 0.5rem;
}
```

### 3. Verify Responsive Behavior
Test at all breakpoints:
- Desktop (≥1200px)
- Laptop (992-1199px)
- Tablet (768-991px)
- Mobile (<768px)

## Files to Modify
| File | Change |
|------|--------|
| `nls_frontend/src/assets/ckeditor-styles.css` | Add `object-fit: contain`, `object-position: center` to `.ckeditor-content img` and `.ckeditor-content figure.image img`; add background to `.ckeditor-content figure.image` |

## Validation Checklist
- [ ] All 4 service cards show complete images (Depository, Margin, Brokerage, Advisory)
- [ ] Embedded text in images is fully readable
- [ ] No image stretching or distortion
- [ ] Aspect ratios preserved
- [ ] No horizontal overflow on any screen size
- [ ] Dark theme background fills letterboxed areas
- [ ] `npm run build` passes
- [ ] No regression on other pages using `ContentPage`/`CKEditorViewer` (PrivacyPolicy, About, EventDetails)

## Risk Assessment
- **Low risk** — Single CSS file change, uses existing theme variables
- **Scope limited** — Only affects `.ckeditor-content` rendered images
- **No layout changes** — Container dimensions unchanged
- **No backend changes** — Frontend only