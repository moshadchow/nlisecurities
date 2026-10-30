# Homepage Hero Section Redesign — Implementation Plan

## Current State

**File:** `nls_frontend/src/pages/Home.jsx` (lines 78-95)

The hero section currently contains:
- HeroSlider (full-width carousel)
- A centered text block with:
  - `<h1>` "We Make Your **Invest** Better"
  - `<h5>` "A leading capital market service provider Since 2013"

Below the hero, there's a "MARKET OVERVIEW" section (lines 99-136) that already displays:
- IndexChart / IndexChartCSE (charts)
- DSEIndex / CSEIndex (tables with index name, value, change, percent)
- IssueStatus for DSE and CSE (table with Advance/Decline/Unchanged counts)

## Data Sources (Existing)

| Component | API Endpoint | Key Fields |
|-----------|--------------|------------|
| `IssueStatus` (via `fetchMarketInfo`) | `/market_info/DSE` , `/market_info/CSE` | `advance`, `decline`, `unchange` |
| `DSEIndex` / `CSEIndex` (via `fetchMarketIndex`) | `/market_index/DSE` , `/market_index/CSE` | `index`, `value`, `change`, `percent`, `arrow` |

Both endpoints are already called in `Home.jsx` → `loadMarketIndex()` → `fetchMarketInfo()` which sets `indexData` (DSE) and `indexDataCSE` (CSE).

## Plan

### 1. Create New Compact Widget Components

**File:** `nls_frontend/src/components/MarketWidget.jsx` (new)

Create reusable stat widgets:

```jsx
// MarketStatCard — single metric (Advance/Decline/Unchanged)
const MarketStatCard = ({ label, value, variant }) => {
  // variant: 'advance' (green), 'decline' (red), 'unchanged' (neutral)
}

// IndexStatCard — index value with change
const IndexStatCard = ({ label, indexData, indexKey }) => {
  // finds the relevant index entry (e.g., "DSEX" for DSE, "CSE50" for CSE)
  // displays index name, value, change, percent with color from arrow
}
```

### 2. Modify Home.jsx Hero Section

**File:** `nls_frontend/src/pages/Home.jsx`

Replace lines 82-94 (the `container py-4` with hero text) with:

```jsx
<div className="container py-3">
  <div className="row g-2 g-md-3 market-widget-row">
    {/* 6 Market Breadth Widgets */}
    <MarketStatCard label="DSE Advance" value={indexData?.advance} variant="advance" />
    <MarketStatCard label="DSE Decline" value={indexData?.decline} variant="decline" />
    <MarketStatCard label="DSE Unchanged" value={indexData?.unchange} variant="unchanged" />
    <MarketStatCard label="CSE Advance" value={indexDataCSE?.advance} variant="advance" />
    <MarketStatCard label="CSE Decline" value={indexDataCSE?.decline} variant="decline" />
    <MarketStatCard label="CSE Unchanged" value={indexDataCSE?.unchange} variant="unchanged" />
    {/* 2 Index Widgets */}
    <IndexStatCard label="DSE Index" indexData={indexData} indexKey="DSEX" />
    <IndexStatCard label="CSE Index" indexData={indexDataCSE} indexKey="CSE50" />
  </div>
</div>
```

### 3. Add CSS for Widget Layout

**File:** `nls_frontend/src/index.css`

```css
.market-widget-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  justify-content: center;
}
.market-widget-row > * {
  flex: 1 1 calc(12.5% - var(--space-2)); /* 8 columns desktop */
  min-width: 140px;
}
@media (max-width: 992px) {
  .market-widget-row > * {
    flex: 1 1 calc(25% - var(--space-2)); /* 4 columns tablet */
  }
}
@media (max-width: 576px) {
  .market-widget-row > * {
    flex: 1 1 calc(50% - var(--space-2)); /* 2 columns mobile */
  }
}
.stat-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-3) var(--space-2);
  text-align: center;
}
.stat-card .label { font-size: var(--fs-xs); color: var(--color-text-muted); text-transform: uppercase; }
.stat-card .value { font-size: var(--fs-h3); font-weight: 700; font-family: var(--font-body); }
.stat-card .value.advance { color: var(--color-up); }
.stat-card .value.decline { color: var(--color-down); }
.stat-card .value.unchanged { color: var(--color-neutral); }
```

### 4. Remove Duplicate Market Overview Section (Optional)

The existing "MARKET OVERVIEW" section (lines 99-136) now duplicates the hero widgets. Either:
- **Remove it entirely** (cleanest)
- **Keep it but simplify** (remove IssueStatus since it's now in hero)

Recommendation: Remove lines 99-136 to avoid duplication.

### 5. Responsive Verification

Test at:
- Desktop (≥1200px): 8 widgets in one row
- Tablet (768–992px): 4 per row (2 rows)
- Mobile (<576px): 2 per row (4 rows)

## Files to Modify

| File | Change |
|------|--------|
| `nls_frontend/src/components/MarketWidget.jsx` | New: `MarketStatCard`, `IndexStatCard` |
| `nls_frontend/src/pages/Home.jsx` | Replace hero text with widget row; remove duplicate market overview |
| `nls_frontend/src/index.css` | Add `.market-widget-row`, `.stat-card` styles |

## No Backend Changes

- Reuses existing `indexData` / `indexDataCSE` state
- Reuses existing `fetchMarketInfo` / `fetchMarketIndex` calls
- No new API endpoints, no DB changes

## Validation

1. `npm run build` passes
2. `npm run dev` → verify 8 widgets in hero on desktop
3. Responsive: resize to tablet/mobile breakpoints
4. Data: values match existing IssueStatus / DSEIndex tables
5. Loading/error states preserved
6. 10s auto-refresh still works