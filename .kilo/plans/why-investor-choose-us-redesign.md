# "Why Investor Choose Us" Section Redesign — Implementation Plan

## Current State

**File:** `nls_frontend/src/pages/Home.jsx` (lines 214-252)

- Section wrapper: `<div className="container-fluid py-5 bg-dark">`
- Heading: `<h1 className="mb-5 text-primary bg-light">` with "Why Investor Choose Us"
- Grid: `<div className="row g-5 align-items-center text-center">`
- Items: 6 features from API (`/feature/`), mapped with hardcoded icons array
- Render: icon (`fa-4x text-primary`), `<h4>`, `<p className="mb-0 text-light">{getPlainText(item.description)}</p>`
- Responsive: `col-md-6 col-lg-4` (2-col tablet, 3-col desktop)
- Uses `getPlainText()` to strip HTML from CKEditor5 descriptions

**Data Source:** `getFeatures(null)` → `/feature/` → `Features` model (title, description)

## Issues to Address

1. **HTML escaping bug**: "Professional Expertise" description contains literal HTML tags (`<p>`, `<strong>`) that render as text instead of being parsed
2. **Not card-based**: Current layout is bare icons + text, no card containers
3. **Heading style**: `bg-light` on heading conflicts with dark theme
3. **No hover/interaction**: Static presentation

## Plan

### 1. Create Feature Card Component

**File:** `nls_frontend/src/components/FeatureCard.jsx` (new)

```jsx
const FeatureCard = ({ title, description, iconClass, index }) => {
  return (
    <div className="feature-card">
      <div className="feature-card-icon">
        <i className={`fa ${iconClass} fa-2x`} aria-hidden="true" />
      </div>
      <h3 className="feature-card-title">{title}</h3>
      <div className="feature-card-description" dangerouslySetInnerHTML={{ __html: description }} />
    </div>
  );
};
```

**Key decisions:**
- Use `dangerouslySetInnerHTML` to render rich text from CKEditor5 (fixes HTML escaping bug)
- Icons passed as prop (not hardcoded in component)
- Icon size: `fa-2x` (smaller than current `fa-4x` for card proportion)

### 2. Update Home.jsx

**File:** `nls_frontend/src/pages/Home.jsx`

- Import `FeatureCard` from `../components/FeatureCard`
- Replace lines 214-252 with new section structure
- Keep `features` state and `getFeatures` call unchanged
- Define icon mapping as constant array (matching current order)

```jsx
const FEATURE_ICONS = [
  'fa-calendar-alt',        // 25+ Years Experience
  'fa-tasks',               // Regulatory Compliance
  'fa-pencil-ruler',        // Secure Transaction Handling
  'fa-user',                // Professional Expertise
  'fa-hand-holding-usd',    // Transparent Communication
  'fa-check',               // Efficient Customer Support
];

// In JSX:
<div className="container-fluid py-5 feature-section">
  <div className="container py-5">
    <div className="text-center mb-5">
      <h2 className="feature-section-title">
        Why Investor <span className="text-teal">Choose Us</span>
      </h2>
    </div>
    <div className="row g-4 feature-card-grid">
      {features?.map((item, index) => (
        <div key={item.id ?? index} className="col-12 col-md-6 col-lg-4">
          <FeatureCard
            title={item.title}
            description={item.description}
            iconClass={FEATURE_ICONS[index]}
            index={index}
          />
        </div>
      ))}
    </div>
  </div>
</div>
```

### 3. Add CSS Styles

**File:** `nls_frontend/src/index.css` (append to end)

```css
/* ===== Feature Section ===== */
.feature-section {
  background: var(--color-landing-bg);
}
.feature-section-title {
  font-family: var(--font-heading);
  font-size: var(--fs-h2);
  font-weight: 700;
  color: var(--color-text);
}
.feature-section-title .text-teal {
  color: var(--color-secondary) !important;
}
.feature-card-grid {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  justify-content: center;
}
.feature-card-grid > .col-12 {
  flex: 0 0 auto;
}
.feature-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-5) var(--space-4);
  text-align: center;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  transition: box-shadow var(--transition), border-color var(--transition), transform var(--transition);
}
.feature-card:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--color-secondary);
  transform: translateY(-2px);
}
.feature-card-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(45, 212, 191, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto var(--space-3);
  color: var(--color-secondary);
  font-size: 1.5rem;
  transition: background var(--transition), color var(--transition);
}
.feature-card:hover .feature-card-icon {
  background: var(--color-secondary);
  color: var(--color-primary-dark);
}
.feature-card-title {
  font-family: var(--font-body);
  font-size: var(--fs-h3);
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 var(--space-2);
  line-height: 1.3;
}
.feature-card-description {
  font-size: var(--fs-sm);
  color: var(--color-text-muted);
  line-height: 1.6;
  margin: 0;
  flex: 1;
}
.feature-card-description p {
  margin: 0 0 var(--space-2);
}
.feature-card-description p:last-child {
  margin-bottom: 0;
}
.feature-card-description strong {
  color: var(--color-text);
  font-weight: 600;
}

/* Responsive grid handled by Bootstrap col-12 col-md-6 col-lg-4 */
/* Equal height cards via flexbox on parent row (align-items: stretch default) */

@media (max-width: 991px) {
  .feature-section-title { font-size: var(--fs-h3); }
}
```

### 4. Fix HTML Escaping Bug

The `getPlainText()` call is removed; `FeatureCard` uses `dangerouslySetInnerHTML` to render the CKEditor5 HTML directly. This correctly renders the "Professional Expertise" description with its `<p>` and `<strong>` tags.

**Note:** Since the API returns sanitized CKEditor5 content, XSS risk is minimal. If extra caution needed, a lightweight sanitizer (DOMPurify, already in deps) could be added, but the current CMS-controlled content is trusted.

## Files to Modify

| File | Change |
|------|--------|
| `nls_frontend/src/components/FeatureCard.jsx` | New component |
| `nls_frontend/src/pages/Home.jsx` | Replace section, import FeatureCard |
| `nls_frontend/src/index.css` | Add `.feature-section`, `.feature-card`, etc. styles |

## No Backend Changes

- Reuses existing `/feature/` endpoint
- Reuses existing `getFeatures` service
- Features model/serializer unchanged

## Validation

1. `npm run build` passes
2. `npm run dev` → verify:
   - 6 cards render in 3-col (desktop), 2-col (tablet), 1-col (mobile)
   - Icons match spec (calendar, tasks, pencil-ruler, user, hand-holding-usd, check)
   - "Professional Expertise" renders bold text correctly (no escaped HTML)
   - Hover: subtle lift, border teal, icon background fills teal
   - Section heading: "Why Investor Choose Us" with teal "Choose Us"
   - Cards equal height, consistent spacing
3. Responsive test: resize viewport to tablet/mobile breakpoints