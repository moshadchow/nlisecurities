# Implementation Plan: Premium Dark Theme for Financial Market Website

## Current State Analysis

**Theme System:** Single `index.css` with `:root` CSS variables (lines 1-70)
- Current palette: Light theme (`--color-bg: #f5f7fa`, `--color-surface: #ffffff`, `--color-text: #1f2937`)
- Bootstrap variables overridden via `--bs-*` CSS variables
- All components use these CSS variables

**Components Requiring Theme Updates:**
1. **Header** (`Header.jsx`, `Ticker.jsx`) - ticker bar, top bar, navbar
2. **Hero Section** (`Home.jsx`, `HeroSlider.jsx`, `MarketBreadth.jsx`, `CSEMarketOverview.jsx`, `IndexTable.jsx`)
3. **Market Dashboard** - `.hero-market-dashboard-row`, `.hero-market-group`, `.market-breadth-cards`, `.stat-card`
4. **Index Tables** - `.hero-index-table-wrap`, `.table` styles
5. **Footer** (`Footer.jsx`) - `.site-footer`
6. **SplashScreen** (`SplashScreen.jsx`, `SplashScreen.css`) - modal dialog
7. **All Pages** (14 pages in `src/pages/`) - use `.container-fluid`, `.card`, buttons, forms
8. **Shared Components** - Breadcrumbs, ContentPage, dropdowns, modals

## Premium Dark Palette Mapping

| Current Variable | Current Value | New Dark Value | Purpose |
|---|---|---|---|
| `--color-primary` | `#003d7a` | `#1E3A5F` | Primary brand (darker navy) |
| `--color-primary-dark` | `#002b56` | `#0F172A` | Darker primary |
| `--color-secondary` | `#0d6efd` | `#2DD4BF` | **Teal accent** (was blue) |
| `--color-accent` | `#ffb400` | `#FBBF24` | Amber accent (kept for warnings) |
| `--color-bg` | `#f5f7fa` | `#0B1120` | **Main page background** (deep midnight navy) |
| `--color-surface` | `#ffffff` | `#151F32` | **Main content surfaces** (slate navy) |
| `--color-text` | `#1f2937` | `#F1F5F9` | **Primary text** (soft white) |
| `--color-text-muted` | `#6b7280` | `#A7B4C8` | **Secondary text** (cool gray) |
| `--color-border` | `#d1d5db` | `#2A3850` | **Borders/dividers** (slate) |
| `--color-success` | `#10b981` | `#34D399` | **Positive movement** (green) |
| `--color-danger` | `#ef4444` | `#FB7185` | **Negative movement** (red) |
| `--color-warning` | `#f59e0b` | `#FBBF24` | Warning/amber |
| `--color-info` | `#3b82f6` | `#60A5FA` | Info (lighter blue) |
| `--color-up` | `#10b981` | `#34D399` | Positive (green) |
| `--color-down` | `#ef4444` | `#FB7185` | Negative (red) |
| `--color-neutral` | `#6b7280` | `#A7B4C8` | Unchanged (gray) |
| `--bs-light` | `#f8f9fa` | `#111B2D` | **Table background** (deep slate) |
| `--bs-dark` | `#002b56` | `#0F172A` | Dark utility |
| `color-scheme` | `light` | `dark` | Browser UI chrome |

**New Variables to Add:**
- `--color-table-header: #1C2940` (muted navy for table headers)
- `--color-card-hover: #1C2940` (hover state for cards)
- `--shadow-sm: 0 1px 2px rgba(0,0,0,0.3)`
- `--shadow-md: 0 4px 6px rgba(0,0,0,0.4)`

## Implementation Steps

### 1. Update CSS Variables in `index.css` (lines 1-70)
Replace all `:root` color variables with premium dark palette. Change `color-scheme: light` to `color-scheme: dark`. Update background/text defaults on `:root`.

### 2. Update Header Styles (lines 192-262)
- `.header-ticker` - keep dark, ensure text contrast
- `.header-top-bar` - dark navy background, white text
- `.header-nav` - dark surface, subtle border, white nav links
- `.navbar .nav-link` - white text, teal hover
- `.navbar .btn-outline` - teal border/text, teal hover fill

### 3. Update Hero Section (lines 302-317, 385-503)
- `.hero-slider-wrap` - ensure images work on dark
- `.hero-market-dashboard-row` - no changes needed (uses variables)
- `.hero-market-group` - dark surface, slate border
- `.hero-market-group-title` - teal color (was primary blue)
- `.market-breadth-cards .stat-card` - dark surface, slate border
- `.stat-card` - dark surface, slate border, white text
- `.stat-card .label` - cool gray
- `.stat-card .value.advance/decline/unchanged` - use new semantic colors

### 4. Update Index Table Styles (lines 385-442)
- `.hero-index-table-wrap` - dark surface, slate border
- `.hero-index-table-title` - teal color
- `.table` - deep slate background (`--bs-light`)
- `.table th` - muted navy header (`--color-table-header`), white text
- `.table td` - white text, slate borders
- `.text-up/.text-down/.text-neutral` - new semantic colors

### 5. Update Footer (lines 264-300)
- `.site-footer` - dark navy background
- Links - cool gray, teal hover
- Social buttons - dark surface, slate border

### 6. Update Ticker (lines 319-340)
- `.ticker-wrap` - dark navy background
- `.ticker-item` - white text

### 7. Update Buttons & Forms (lines 122-140, 543-563)
- `.btn-primary` - teal background, white text
- `.btn-primary:hover` - slightly darker teal
- `.btn-outline` - slate border, white text, teal hover
- `.btn-link` - cool gray, teal hover

### 8. Update Cards & Shared Components (lines 142-148)
- `.card` - dark surface, slate border

### 9. Update Dropdowns & Modals
- Add styles for `.dropdown-menu` - dark surface, slate border
- Update `SplashScreen.css` - dark modal background

### 10. Verify All Pages
Check each page in `src/pages/` for hardcoded light colors or Bootstrap classes that need dark variants.

## Files to Modify

| File | Scope |
|---|---|
| `nls_frontend/src/index.css` | **Primary** - all CSS variables + component styles |
| `nls_frontend/src/components/SplashScreen.css` | Modal dialog dark theme |
| `nls_frontend/src/components/HeroSlider.jsx` | Verify slider works on dark (likely no changes) |

## Validation Checklist

- [ ] `npm run build` passes
- [ ] `npm run lint` passes
- [ ] Header: ticker, top bar, navbar all dark with good contrast
- [ ] Hero: slider visible, market dashboard compact and readable
- [ ] Market breadth: Advance/Decline/Unchanged cards use semantic colors correctly
- [ ] Index tables: DSE (3 indices) and CSE (5 indices) scan easily, headers distinct
- [ ] Positive values: `#34D399` green, Negative: `#FB7185` red, Unchanged: `#A7B4C8` gray
- [ ] Numeric signs (+/-) and % symbols preserved
- [ ] Footer: dark, readable, links work
- [ ] Buttons: primary=teal, outline=teal border, states correct
- [ ] Dropdowns: dark background, readable items
- [ ] SplashScreen: dark modal, readable content
- [ ] All 14 pages: no light-theme remnants, readable text
- [ ] Responsive: mobile/tablet/desktop all usable
- [ ] No backend changes

## Open Questions

1. **Bootstrap `navbar-light` vs `navbar-dark`**: Header uses `navbar-light` class. Should switch to `navbar-dark` for proper Bootstrap dark mode behavior, or rely entirely on CSS variables? Recommendation: Keep `navbar-light` class but override all colors via CSS variables for consistency.

2. **Slick carousel CSS**: Imports `slick-theme.css` which has light theme. May need to override slick dots/arrows colors in index.css.

3. **Font weights**: Current `--font-heading: 'Merriweather', serif` - verify readability on dark. May need to increase weight slightly.

4. **Images in HeroSlider**: Slides use `objectFit: "fill"` - verify they look good on dark background or add overlay.

5. **Form inputs**: Not explicitly styled - need to add dark input styles (background, border, text, placeholder).

6. **Table hover**: Current `.stat-card:hover` uses `--shadow-md`. On dark, subtle border highlight may be better than shadow.