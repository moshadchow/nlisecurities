# Implementation Plan: Fix Text Visibility in Navbar and Our Recent Events Section

## Current State Analysis

**Navbar (Header.jsx):**
- Uses `navbar-light` class on `<nav>` element
- Nav links use `nav-link site-nav-link` classes
- Dropdown items use `dropdown-item` class
- "Investor Portal" button uses `btn btn-outline btn-sm`
- Current CSS: `.navbar .nav-link` has `color: var(--color-text)` (#F1F5F9), hover/active uses teal
- Problem: Bootstrap's `navbar-light` has `background-color: #fff` and text color overrides; `site-nav-link` has no explicit styles

**Our Recent Events Section (Home.jsx lines 191-228):**
- Section wrapper: `<div className="container-fluid bg-primary newsletter p-0">`
- Cards: `<div className="card h-100 shadow-sm border-0">`
- Card images: `card-img-top`
- Card body: `card-body`
- Event titles: `card-title fw-semibold` (no explicit color)
- Descriptions: `card-text text-muted small`
- Card footer: `<div className="card-footer bg-white border-0 text-end">` - **bg-white is the problem**
- "Read More" button: `btn btn-outline-primary btn-sm` - uses Bootstrap's primary blue

**Current CSS Gaps:**
- No override for `.bg-primary` (Bootstrap's blue)
- No explicit styles for `.card-title`, `.card-text`, `.card-footer`
- No override for `.bg-white` in card footer
- No styles for `.btn-outline-primary` in dark theme
- No override for `.newsletter` class

## Plan

### 1. Fix Navbar Text Visibility

**File:** `nls_frontend/src/index.css` (in Header section around line 332-350)

**Changes:**
- Increase specificity for nav links to override Bootstrap
- Ensure `site-nav-link` class has explicit styles
- Add focus/active states for accessibility
- Verify dropdown items work correctly

```css
/* Navbar - higher specificity to override Bootstrap navbar-light */
.header-nav .navbar-nav .nav-link,
.header-nav .navbar-nav .site-nav-link {
  color: var(--color-text) !important;  /* #F1F5F9 */
}
.header-nav .navbar-nav .nav-link:hover,
.header-nav .navbar-nav .nav-link:focus,
.header-nav .navbar-nav .site-nav-link:hover,
.header-nav .navbar-nav .site-nav-link:focus {
  color: var(--color-secondary) !important;  /* teal */
}
.header-nav .navbar-nav .nav-link.active,
.header-nav .navbar-nav .site-nav-link.active {
  color: var(--color-secondary) !important;  /* teal */
}
/* Dropdown toggle */
.header-nav .navbar-nav .dropdown-toggle::after {
  border-top-color: var(--color-text) !important;
}
```

### 2. Fix Our Recent Events Section

**File:** `nls_frontend/src/index.css` (add new section after Footer or in a new Events section)

**Changes:**
- Override `.bg-primary` / `.newsletter` to use dark navy
- Fix card backgrounds to use dark surface
- Fix card footer to remove white background
- Style event titles, descriptions, dates
- Fix "Read More" button to use teal outline

```css
/* ===== Our Recent Events Section ===== */
.newsletter,
.bg-primary {
  background: var(--color-primary-dark) !important;  /* #0F172A */
  color: var(--color-text) !important;
}

/* Event cards */
.newsletter .card,
.bg-primary .card {
  background: var(--color-surface) !important;  /* #151F32 */
  border: 1px solid var(--color-border) !important;
  box-shadow: var(--shadow-sm) !important;
}

.newsletter .card-img-top,
.bg-primary .card-img-top {
  border-bottom: 1px solid var(--color-border);
}

.newsletter .card-body,
.bg-primary .card-body {
  background: transparent !important;
  color: var(--color-text) !important;
}

.newsletter .card-title,
.bg-primary .card-title {
  color: var(--color-text) !important;  /* #F1F5F9 */
  font-weight: 600 !important;
}

.newsletter .card-text,
.bg-primary .card-text {
  color: var(--color-text-muted) !important;  /* #A7B4C8 */
}

.newsletter .card-text small,
.bg-primary .card-text small {
  color: var(--color-text-muted) !important;
}

/* Card footer - remove white background */
.newsletter .card-footer,
.bg-primary .card-footer {
  background: transparent !important;
  border-top: 1px solid var(--color-border) !important;
  color: var(--color-text-muted) !important;
}

/* Read More button - teal outline */
.newsletter .btn-outline-primary,
.bg-primary .btn-outline-primary {
  background: transparent !important;
  border-color: var(--color-secondary) !important;  /* teal */
  color: var(--color-secondary) !important;
}
.newsletter .btn-outline-primary:hover,
.bg-primary .btn-outline-primary:hover {
  background: var(--color-secondary) !important;
  color: var(--color-bg) !important;  /* dark navy text on teal */
  border-color: var(--color-secondary) !important;
}

/* Section heading */
.newsletter h1,
.bg-primary h1 {
  color: var(--color-text) !important;  /* #F1F5F9 */
}

/* Event meta info (dates, etc.) */
.newsletter .text-muted,
.bg-primary .text-muted {
  color: var(--color-text-muted) !important;  /* #A7B4C8 */
}
```

### 3. Verify and Test

**Verification Steps:**
1. Run `npm run build` - ensure no errors
2. Start dev server and inspect:
   - Navbar: all menu items readable (#F1F5F9), active/hover teal (#2DD4BF), dropdowns readable
   - Events section: heading white, titles white, descriptions cool gray, dates cool gray, links teal
   - Card footers: no white background, border separator visible
   - Buttons: teal outline, teal fill on hover
3. Test responsive: mobile navbar toggle, dropdowns on mobile
4. Check keyboard navigation: focus states visible
5. Ensure no regression in other sections

## Files to Modify

| File | Changes |
|------|---------|
| `nls_frontend/src/index.css` | Add navbar specificity fixes, add Events section styles |

## No Backend Changes

All changes are CSS-only. No JSX modifications needed.

## Validation Checklist

- [ ] Navbar menu items: normal `#F1F5F9`, hover/active `#2DD4BF`, focus visible
- [ ] Dropdown menus: readable on dark surface
- [ ] Mobile navbar: toggle works, items readable
- [ ] Events section background: dark navy `#0F172A`
- [ ] Events heading: `#F1F5F9`
- [ ] Event titles: `#F1F5F9`
- [ ] Event descriptions: `#CBD5E1` (or `#A7B4C8` via text-muted)
- [ ] Event dates/meta: `#A7B4C8`
- [ ] Card footer: no white bg, subtle border separator
- [ ] Read More button: teal outline, teal fill on hover
- [ ] No regression in market dashboard, index tables, footer
- [ ] `npm run build` passes