# Fix Text/Background Styling in "Why Investor Choose Us" Cards

## Problem
The "Professional Expertise" card (and potentially others) displays a white background behind its description text due to inline styles in the CKEditor5 content:
```html
<span style="background-color:rgb(255,255,255);color:rgb(85,85,85);">...</span>
```

This overrides the card's dark theme CSS.

## Root Cause
- `FeatureCard` renders descriptions via `dangerouslySetInnerHTML={{ __html: description }}`
- Descriptions come from Django's `CKEditor5Field` (rich text with inline styles)
- Inline `style` attributes have higher specificity than CSS classes

## Solution
Add CSS rules in `index.css` that force transparent background and correct text color on **all descendants** of `.feature-card-description`, using `!important` to override inline styles.

## Implementation

**File:** `nls_frontend/src/index.css`

Add after existing `.feature-card-description` rules (around line 912):

```css
/* Override inline styles in CKEditor5 content within feature cards */
.feature-card-description * {
  background-color: transparent !important;
  background: transparent !important;
  color: var(--color-text-muted) !important;
}

/* Preserve intentional bold/strong styling */
.feature-card-description strong,
.feature-card-description b {
  color: var(--color-text) !important;
  font-weight: 600 !important;
}

/* Links should remain teal */
.feature-card-description a {
  color: var(--color-secondary) !important;
}
```

## Why This Works
- `*` selector targets all nested elements (span, p, div, etc.)
- `!important` beats inline `style` attributes
- `var(--color-text-muted)` = `#A7B4C8` (close to requested `#CBD5E1`; adjust if needed)
- Preserves semantic bold/links

## Validation Checklist
- [ ] No white background on any card description
- [ ] Text color is light gray (`#CBD5E1` or equivalent) on all cards
- [ ] "Professional Expertise" card renders correctly
- [ ] Bold text (`<strong>`) remains white/bright
- [ ] Links (if any) remain teal
- [ ] All 6 cards consistent
- [ ] `npm run build` passes

## Files Modified
- `nls_frontend/src/index.css` only

## No Backend Changes
- Content remains in database
- API unchanged