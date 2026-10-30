# Fix "Research Reports" Text Color on Research Page — Implementation Plan

## Current State Analysis

### Element Location
**File:** `nls_frontend/src/pages/ResearchPage.jsx`, line 52
```jsx
<h1 className="h3 fw-bold">Research Reports</h1>
```

### Current Styling
- Element: `<h1>` with Bootstrap utility classes `h3` (font-size) and `fw-bold` (font-weight)
- Parent: `<div className="text-center mb-4">` — only affects alignment and margin
- No explicit color class or inline style

### Global CSS (from `index.css`)
```css
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading);
  font-weight: 700;
  color: var(--color-text);  /* #F1F5F9 */
}
```
The global `h1` rule should already apply `#F1F5F9` (soft white).

## Potential Issues
1. **CSS specificity conflict** — Another rule may override the global `h1` color
2. **Bootstrap `h3` utility** — Only sets font-size, not color (should not interfere)
3. **Inheritance from parent** — `text-center` has no color property
4. **Missing theme variable** — `var(--color-text)` is defined as `#F1F5F9` in `:root`

## Implementation Plan

### Step 1: Verify Current Rendered Color
- Open `http://localhost:5173/research/` in browser
- Inspect the "Research Reports" `<h1>` element
- Check Computed Styles → `color` value
- Identify any overriding CSS rule

### Step 2: Apply Minimal Fix
**Option A (if global style works):** No change needed — already correct.

**Option B (if overridden):** Add explicit color via one of:
- Inline style: `<h1 className="h3 fw-bold" style={{color: 'var(--color-text)'}}>`
- Utility class: Add `text-white` (if defined) or create `.text-heading { color: var(--color-text) !important; }` in `index.css`
- Recommended: Add `style={{color: 'var(--color-text)'}}` for guaranteed specificity without new CSS

### Step 3: Verify
- Confirm color is `#F1F5F9` in browser
- Check hover/active/focus states (not applicable for static heading)
- Verify no regression on other pages using `h1`

## Files to Modify
| File | Change |
|------|--------|
| `nls_frontend/src/pages/ResearchPage.jsx` | Add inline style or class to `<h1>` (if needed) |

## Validation Checklist
- [ ] "Research Reports" displays in soft white (`#F1F5F9`)
- [ ] No other headings unintentionally affected
- [ ] Page remains responsive
- [ ] `npm run build` passes

## Risk Assessment
- **Low risk** — Single element change, uses existing theme variable
- **No backend changes** — Frontend only
- **No layout changes** — Color only