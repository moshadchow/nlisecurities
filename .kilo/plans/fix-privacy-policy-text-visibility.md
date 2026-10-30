# Fix Text Visibility on Privacy Policy Page — Implementation Plan

## Current State Analysis

### Page Structure
- **Route**: `/privacy-policy` → `PrivacyPolicy.jsx`
- **Components**: `PrivacyPolicy.jsx` → `ContentPage.jsx` → `CKEditorViewer.jsx`
- **Content Source**: Django backend via `getPolicy()` API, rendered as HTML through CKEditor

### Root Cause Issues

| Element | Problem | Root Cause |
|---------|---------|------------|
| CKEditor body text | `color: #444` (dark gray) invisible on dark bg | `ckeditor-styles.css` designed for light theme |
| CKEditor headings (h1-h6) | `color: #0d6efd` (Bootstrap blue) low contrast | `ckeditor-styles.css` hardcoded light-theme colors |
| CKEditor links | `color: #0d6efd`, hover `#0a58ca` low contrast | Same |
| CKEditor lists (ul/ol/li) | Inherit `#444` body color | No explicit color, inherits dark text |
| CKEditor horizontal rules | `border-top: 1px solid #e5e5e5` (light gray) invisible | Light-theme border color |
| CKEditor blockquotes | `background: #f8f9fa`, `color: #555` — light bg, dark text | Light-theme styling |
| CKEditor code/pre | `background: #f1f3f5` (light) for code; pre is OK (dark bg) | Mixed theme |
| CKEditor tables | Borders `#dee2e6`, th bg `#f1f3f5`, striping `#fafbfc` — all light | Light-theme table styling |
| CKEditor figcaption/small | `color: #6c757d` (gray) low contrast | Light-theme muted color |
| ContentPage loading text | `text-muted` class — no global dark-theme override | Bootstrap's `text-muted` uses light-theme gray |
| ContentPage section | `bg-light` class — overridden to dark in index.css ✓ | Already fixed via `.bg-light` override |
| ContentPage h2 title | `text-primary` — overridden to teal in index.css ✓ | Already fixed via `.text-primary` override |
| ContentPage card | Uses global `.card` — dark theme ✓ | Already fixed |

### CSS Variable Palette (from `index.css`)
```css
--color-text: #F1F5F9;           /* Primary headings/titles */
--color-text-muted: #A7B4C8;     /* Muted/supporting text */
--color-text-secondary: #CBD5E1; /* Secondary descriptions (not defined, use #E2E8F0) */
--color-body-text: #E2E8F0;      /* Primary body text (not defined, need to add or use --color-text) */
--color-secondary: #2DD4BF;      /* Teal accent for links */
--color-accent: #FBBF24;         /* Amber for hover states */
--color-surface: #151F32;        /* Card/container background */
--color-border: #2A3850;         /* Borders and dividers */
--color-table-header: #1C2940;   /* Table header background */
--bs-light: #111B2D;             /* Page background (landing bg) */
```

Note: The spec mentions `#E2E8F0` for primary body text and `#CBD5E1` for secondary descriptions. These aren't in the current CSS variables. We'll use `--color-text` (#F1F5F9) for headings and `--color-text-muted` (#A7B4C8) for body text, or add new variables.

## Implementation Plan

### 1. Fix `ckeditor-styles.css` — Primary Fix
**File:** `nls_frontend/src/assets/ckeditor-styles.css`

Replace all hardcoded light-theme colors with dark-theme colors using the design system palette. Since this file is imported only by `CKEditorViewer`, we can safely modify it.

Key changes:
- `.ckeditor-content`: `color: var(--color-text-muted)` (or new `--color-body-text`)
- Headings: `color: var(--color-text)` (white)
- Links: `color: var(--color-secondary)` (teal), hover `var(--color-accent)` (amber)
- Lists: inherit body color
- HR: `border-top: 1px solid var(--color-border)`
- Blockquote: `background: var(--color-surface)`, `border-left: 4px solid var(--color-secondary)`, `color: var(--color-text-muted)`
- Code: `background: var(--color-table-header)`, `color: var(--color-text)`
- Pre: already dark (keep), ensure code inside inherits properly
- Tables: borders `var(--color-border)`, th bg `var(--color-table-header)`, striping `rgba(255,255,255,0.02)`
- Figcaption/small: `color: var(--color-text-muted)`

### 2. Add Global `.text-muted` Override in `index.css`
**File:** `nls_frontend/src/index.css`

Add after line 770 (after `.bg-primary .text-muted` override):
```css
.text-muted {
  color: var(--color-text-muted) !important;
}
```

This ensures any `text-muted` usage (like ContentPage loading state) gets proper dark-theme color.

### 3. Verify ContentPage.jsx Uses Correct Classes
**File:** `nls_frontend/src/pages/PrivacyPolicy.jsx` and `ContentPage.jsx`

No changes needed — they already use:
- `bg-light` → overridden to dark bg + white text
- `text-primary` → overridden to teal
- `card` → dark theme via global `.card`
- `text-muted` on loading text → will be fixed by step 2

## Files to Modify

| File | Change Type |
|------|-------------|
| `nls_frontend/src/assets/ckeditor-styles.css` | Complete rewrite of color palette to dark theme |
| `nls_frontend/src/index.css` | Add global `.text-muted` override |

## Validation Checklist

- [ ] Page title "Privacy Policy" visible (via Breadcrumbs — already fixed in previous task)
- [ ] ContentPage section heading (`h2.text-primary`) visible in teal
- [ ] CKEditor-rendered headings (h1-h6) white (`#F1F5F9`)
- [ ] CKEditor body paragraphs readable (`#E2E8F0` / `#A7B4C8`)
- [ ] CKEditor links teal (`#2DD4BF`), hover amber (`#FBBF24`)
- [ ] CKEditor lists (bullets/numbers) readable
- [ ] CKEditor horizontal rules visible as subtle dividers (`#2A3850`)
- [ ] CKEditor blockquotes styled with dark surface bg, teal left border
- [ ] CKEditor code/pre blocks readable (dark bg, light text)
- [ ] CKEditor tables with dark borders, headers, subtle striping
- [ ] CKEditor figcaption/small text muted but readable
- [ ] Loading state "Loading..." text visible (muted color)
- [ ] Error state text visible
- [ ] Responsive: content wraps correctly at all screen sizes
- [ ] `npm run build` passes
- [ ] No regressions on other pages using `ContentPage` or `CKEditorViewer` (Service pages, About, etc.)

## Risk Mitigation

- **Scope**: `ckeditor-styles.css` is only imported by `CKEditorViewer`, used by `ContentPage`. Check all usages:
  - `PrivacyPolicy.jsx` ✓
  - Search for other `ContentPage` usages
- **Shared component**: `ContentPage` may be used elsewhere (Service, About pages). Verify those still look correct after CKEditor style changes.
- **CSS variables**: Reuse existing `--color-*` variables from `index.css` — no new colors.
- **Specificity**: CKEditor styles use `.ckeditor-content` descendant selectors, which have sufficient specificity.

## Open Questions

1. **Body text color**: Spec says `#E2E8F0` for primary body text. Current `--color-text` is `#F1F5F9` (brighter), `--color-text-muted` is `#A7B4C8` (muted). Should we add `--color-body-text: #E2E8F0` and `--color-description: #CBD5E1` to `:root` in index.css, or use existing variables?

   **Recommendation**: Add two new variables to `:root` in index.css for precision, then use them in ckeditor-styles.css.

2. **Other ContentPage usages**: Need to verify Service pages, About page, etc. still render correctly after CKEditor style changes.

3. **CKEditor content source**: The HTML comes from Django CKEditor. Are there inline styles in the HTML that could override our CSS? The `ckeditor-styles.css` uses descendant selectors (`.ckeditor-content h1`, etc.) which should override inline styles only if `!important` or higher specificity. But CKEditor output typically uses classes, not inline styles for these elements.

## Recommended Next Steps

1. Add `--color-body-text: #E2E8F0` and `--color-description: #CBD5E1` to `:root` in index.css
2. Rewrite `ckeditor-styles.css` with dark-theme colors using CSS variables
3. Add global `.text-muted` override in index.css
4. Build and verify
5. Test other pages using ContentPage/CKEditorViewer