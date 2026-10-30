# Fix Text Visibility on Forthcoming IPO Page — Implementation Plan

## Current State Analysis

### IPO Page (`src/pages/Ipo.jsx`)
- Uses `table table-success table-striped` (Bootstrap classes)
- Table has columns: Sl#, Company, Details (link to DSE)
- Loading state: `text-muted` spinner + text
- No page heading in the component (Breadcrumbs provides it)

### Breadcrumbs Component (`src/components/Breadcrumbs.jsx`)
- Wrapper: `container-fluid bg-primary hero-header` with inline `paddingTop: 120px, paddingBottom: 40px`
- Page heading: `h1.display-2.fw-bold.text-blue`
- Breadcrumb: `ol.breadcrumb.mb-0.bg-transparent`
- Links: `text-blue text-decoration-none`
- Active: `text-blue-50`

### Root Cause Issues

| Element | Problem | Root Cause |
|---------|---------|------------|
| IPO Table | `table-success` applies green bg with dark text | Bootstrap's `table-success` designed for light theme |
| IPO Table | `table-striped` uses light striping | Bootstrap defaults |
| IPO Table Cells | Text may be dark on dark bg | Bootstrap defaults |
| Breadcrumbs Heading | `text-blue` may not contrast | Bootstrap's blue on dark bg |
| Breadcrumb Links | `text-blue` low contrast | Bootstrap's blue on dark bg |
| Breadcrumb Active | `text-blue-50` may be too light | Bootstrap utility |
| Loading Text | `text-muted` may be too dark | Bootstrap's muted on dark bg |
| Table Link | Default link color | May not contrast |

### CSS Variable Palette (from `index.css`)
```css
--color-text: #F1F5F9;           /* Primary text */
--color-text-muted: #A7B4C8;     /* Muted text */
--color-secondary: #2DD4BF;      /* Teal accent */
--color-landing-bg: #111B2D;     /* Page bg */
--color-surface: #151F32;        /* Card bg */
--color-border: #2A3850;         /* Borders */
--color-table-header: #1C2940;   /* Table header bg */
```

## Implementation Plan

### 1. Fix IPO Page Table Styles
**File:** `src/index.css` — Add new `.ipo-table-wrap` styles

```css
/* ===== IPO Page Table ===== */
.ipo-table-wrap {
  background: var(--color-landing-bg);
}
.ipo-table-wrap .table {
  background: var(--color-surface);
  border-color: var(--color-border);
}
.ipo-table-wrap .table th,
.ipo-table-wrap .table td {
  border-color: var(--color-border);
  color: var(--color-text);
  background: transparent;
}
.ipo-table-wrap .table thead th {
  background: var(--color-table-header);
  color: var(--color-text);
  font-weight: 600;
  text-transform: uppercase;
  font-size: var(--fs-xs);
  letter-spacing: 0.05em;
}
.ipo-table-wrap .table tbody tr {
  transition: background var(--transition);
}
.ipo-table-wrap .table tbody tr:nth-child(odd) {
  background: rgba(255,255,255,0.02);
}
.ipo-table-wrap .table tbody tr:hover {
  background: rgba(45, 212, 191, 0.08);
}
.ipo-table-wrap .table td:first-child {
  font-weight: 600;
  color: var(--color-text-muted);
}
.ipo-table-wrap .table a {
  color: var(--color-secondary);
  text-decoration: none;
}
.ipo-table-wrap .table a:hover {
  color: var(--color-accent);
  text-decoration: underline;
}
```

### 2. Fix Breadcrumbs Component
**File:** `src/components/Breadcrumbs.jsx` — Replace Bootstrap text utilities with custom classes

Changes:
- Remove `text-blue`, `text-blue-50` classes
- Add custom breadcrumb link styles
- Ensure heading uses theme colors

**File:** `src/index.css` — Add breadcrumb styles

```css
/* ===== Breadcrumbs ===== */
.breadcrumb {
  background: transparent !important;
  padding: 0;
  margin: 0;
}
.breadcrumb-item + .breadcrumb-item::before {
  color: var(--color-text-muted);
  content: "/";
}
.breadcrumb-item a {
  color: var(--color-text-muted) !important;
  text-decoration: none;
}
.breadcrumb-item a:hover {
  color: var(--color-secondary) !important;
}
.breadcrumb-item.active {
  color: var(--color-text) !important;
}
.hero-header {
  background: var(--color-landing-bg) !important;
  color: var(--color-text) !important;
}
.hero-header h1 {
  color: var(--color-text) !important;
}
```

### 3. Fix IPO Page Component
**File:** `src/pages/Ipo.jsx`

Changes:
- Wrap table in `<div className="ipo-table-wrap">`
- Add page heading inside container (optional, Breadcrumbs already provides)
- Ensure loading text uses theme colors

### 3. Fix Loading State
**File:** `src/index.css` — Ensure loading text is visible

```css
.ipo-table-wrap .text-muted,
.ipo-table-wrap p {
  color: var(--color-text-muted) !important;
}
.ipo-table-wrap .spinner-border {
  border-color: var(--color-secondary) transparent var(--color-secondary) transparent !important;
}
```

## Files to Modify

| File | Change Type |
|------|-------------|
| `src/index.css` | Add `.ipo-table-wrap`, breadcrumb, hero-header styles |
| `src/components/Breadcrumbs.jsx` | Remove Bootstrap text-blue classes |
| `src/pages/Ipo.jsx` | Wrap table in `ipo-table-wrap` |

## Validation Checklist

- [ ] IPO page heading visible (via Breadcrumbs)
- [ ] Breadcrumb links readable (muted → teal on hover)
- [ ] Breadcrumb active page visible
- [ ] IPO table headers readable (white on dark header)
- [ ] IPO company names readable (white)
- [ ] IPO "Details" links teal, hover → amber
- [ ] Table rows have subtle striping (not white)
- [ ] Hover row highlight (teal tint)
- [ ] Loading spinner teal, text muted readable
- [ ] Responsive: table scrolls horizontally on mobile
- [ ] No white backgrounds behind text
- [ ] `npm run build` passes
- [ ] No regressions on other pages using tables/breadcrumbs

## Risk Mitigation

- Use specific wrapper classes (`.ipo-table-wrap`, `.hero-header`) to avoid global side effects
- Reuse existing CSS variables — no new colors
- Test Home page tables (MarketBreadth, IndexTable, MarketPerformanceTable) still work
- Test other pages using Breadcrumbs (About, Service, etc.)

## Open Questions

1. Should the IPO page have its own section heading inside the container (in addition to Breadcrumbs)?
2. Are there other pages using `table-success` or `table-striped` that need similar fixes?
3. Should the `text-blue` class be defined globally or removed entirely?

**Recommendation:** Remove `text-blue` usage entirely, replace with theme-aware classes. Define it as an alias for teal if needed elsewhere.