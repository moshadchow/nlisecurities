# Implementation Plan: Standardize Landing Page Background Color

## Current State Analysis

**Hero Section Background:**
- File: `nls_frontend/src/pages/Home.jsx` line 87
- Class: `bg-light` on `<div className="container-fluid hero-header bg-light">`
- CSS: `.bg-light` overridden at `index.css` line 357-359:
  ```css
  .bg-light {
    background: var(--bs-light) !important;
    color: var(--color-text) !important;
  }
  ```
- Variable: `--bs-light: #111B2D` (defined at `index.css` line 28)

**Hero Background Color: `#111B2D` (from `--bs-light`)**

---

## Sections Requiring Background Updates

| Section | File | Current Class | Current Background | Target |
|---------|------|---------------|-------------------|--------|
| Hero | Home.jsx:87 | `bg-light` | `--bs-light: #111B2D` | ✓ Already correct |
| Chart / Market Index | Home.jsx:121 | `bg-dark` | Bootstrap default (dark) | → `--bs-light` |
| Feature / Why Investor | Home.jsx:150 | `bg-dark` | Bootstrap default (dark) | → `--bs-light` |
| Our Recent Events | Home.jsx:191 | `bg-primary newsletter` | Overridden to `--color-primary-dark` (#0F172A) | → `--bs-light` |
| FAQ | FaqSection.jsx:25,40 | `bg-dark` | Bootstrap default (dark) | → `--bs-light` |
| Footer | Footer.jsx:6 / index.css:387 | Inline `.site-footer` | `--color-primary-dark` (#0F172A) | → `--bs-light` |

---

## Plan

### 1. Define Shared Landing Page Background Variable
**File:** `nls_frontend/src/index.css` (in `:root` block)

Add explicit variable for landing page background (reuses hero color):
```css
--color-landing-bg: #111B2D;  /* Same as --bs-light */
```

### 2. Override Bootstrap Background Classes
**File:** `nls_frontend/src/index.css` (after `.bg-light` override, around line 360)

Add overrides for `.bg-dark`, `.bg-primary`, and `.newsletter`:
```css
.bg-dark {
  background: var(--color-landing-bg) !important;
  color: var(--color-text) !important;
}
.bg-primary {
  background: var(--color-landing-bg) !important;
  color: var(--color-text) !important;
}
.newsletter {
  background: var(--color-landing-bg) !important;
  color: var(--color-text) !important;
}
```

### 3. Remove Conflicting Events Section Override
**File:** `nls_frontend/src/index.css` (lines 690-692)

Remove the existing `.newsletter, .bg-primary` override that sets background to `--color-primary-dark`:
```css
/* REMOVE THIS BLOCK:
.newsletter,
.bg-primary {
  background: var(--color-primary-dark) !important;
  color: var(--color-text) !important;
}
*/
```

The new overrides from Step 2 will handle these classes.

### 4. Update Footer Background
**File:** `nls_frontend/src/index.css` (line 387)

Change footer background from `--color-primary-dark` to `--color-landing-bg`:
```css
.site-footer {
  background: var(--color-landing-bg);
  color: var(--color-text-muted);
  border-top: 1px solid var(--color-border);
}
```

Also update the footer text color to ensure readability on the new background:
- `.site-footer a` → keep `var(--color-text-muted)` 
- `.site-footer h5` → keep `var(--color-text)`
- `.site-footer .btn-link` → keep `var(--color-text-muted)`

### 5. Update FAQ Section Error State
**File:** `nls_frontend/src/components/FaqSection.jsx` (line 25)

Change error state background from `bg-dark` to `bg-light`:
```jsx
<div className="container-fluid py-5 bg-light">
```
(Uses the now-standardized `bg-light` class)

---

## Readability Preservation

With unified background, ensure component separation via:
- **Cards/Tables**: Keep `var(--color-surface)` (#151F32) background on `.card`, `.hero-market-group`, `.hero-index-table-wrap`
- **Borders**: Keep `var(--color-border)` (#2A3850) on cards, tables, dividers
- **Shadows**: Keep `var(--shadow-sm)` for depth
- **Text**: Keep existing light text colors (`--color-text`, `--color-text-muted`)

No changes needed to card/table styles — they already use surface color distinct from page background.

---

## Files to Modify

| File | Changes |
|------|---------|
| `nls_frontend/src/index.css` | Add `--color-landing-bg`, override `.bg-dark`, `.bg-primary`, `.newsletter`, remove old `.newsletter/.bg-primary` override, update `.site-footer` |
| `nls_frontend/src/components/FaqSection.jsx` | Change error state `bg-dark` → `bg-light` |

---

## Validation Checklist

- [ ] `npm run build` passes
- [ ] Hero section background: `#111B2D`
- [ ] Chart section background: `#111B2D`
- [ ] Feature section background: `#111B2D`
- [ ] Events section background: `#111B2D` (not `#0F172A`)
- [ ] FAQ section background: `#111B2D`
- [ ] Footer background: `#111B2D` (not `#0F172A`)
- [ ] No alternating background bands visible
- [ ] Text readable on all sections
- [ ] Cards/tables still visually distinct (surface color, borders, shadows)
- [ ] Events section: heading, titles, descriptions, buttons readable
- [ ] Footer: links, headings readable
- [ ] Responsive layouts correct
- [ ] Other pages unaffected (only landing page sections use these classes in context)

---

## Open Questions

1. **Footer readability**: The footer currently uses a slightly darker navy (`#0F172A`) which provides subtle separation. Changing to `#111B2D` may reduce visual hierarchy. If footer text becomes harder to read, we may need to adjust footer text colors or keep footer distinct. The task says "including Footer" so we'll apply the change and verify.

2. **Other pages**: These class overrides are global. Other pages using `bg-dark`/`bg-primary` will also get the landing page background. This is likely acceptable since the design system is dark-theme unified.

3. **Bootstrap `bg-dark` on other pages**: If other pages rely on `bg-dark` being darker for contrast, they'll be affected. We can scope overrides to landing page if needed, but global is simpler and consistent with "premium dark theme".