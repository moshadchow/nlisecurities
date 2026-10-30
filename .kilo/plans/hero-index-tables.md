# Implementation Plan: Hero Section - Exchange-Wise Market Index Tables

## Current State Analysis

**Hero Section Location:** `nls_frontend/src/pages/Home.jsx` lines 84-114
- HeroSlider at top
- Below slider: `hero-market-row` with two `col-lg-6` columns:
  - **Left (order-1 order-lg-2):** Title "We Make Your Invest Better" + subtitle
  - **Right (order-lg-1):** `market-widget-row` with 8 cards (6 MarketStatCard + 2 IndexStatCard)

**Data Sources (Already Fetched in Home.jsx):**
- `indexValues` — DSE indices array from `fetchMarketIndex("DSE")` → `[{ index: "DSEX|DSES|DS30|CDSET", value, change, percent, arrow }, ...]`
- `indexValuesCSE` — CSE indices array from `fetchMarketIndex("CSE")` → `[{ index: "CSE50|CSE30|CSCX|CASPI|CSI", value, change, percent, arrow }, ...]`

**Required Indices — All Available:**
| Exchange | Required | Available in API |
|----------|----------|------------------|
| DSE | DSEX, DS30, DSES | ✓ DSEX, DSES, DS30, CDSET |
| CSE | CSCX, CSE50, CSE30, CASPI, CSI | ✓ CSCX, CSE50, CSE30, CASPI, CSI |

**Existing Table Components (Reference):**
- `DSEIndex` in `ChartContainer.jsx` — renders full index table with color-coded rows
- `CSEIndex` in `ChartContainerCSE.jsx` — similar but hardcoded yellow rows (bug)
- Both use `fetchMarketIndex` independently with own 10s interval

**Design Tokens Available (index.css):**
- Colors: `--color-up` (green), `--color-down` (red), `--color-neutral` (gray)
- Table styles: `.table`, `.table-responsive`, `.text-up`, `.text-down`, `.text-neutral`
- Spacing/typography: `--space-*`, `--fs-*`, `--radius-*`

## Plan

### 1. Create Reusable `IndexTable` Component
**File:** `nls_frontend/src/components/IndexTable.jsx` (new)

```jsx
const IndexTable = ({ title, indices, indexData }) => {
  // indices: array of index keys to display in order, e.g., ["DSEX", "DS30", "DSES"]
  // indexData: full array from fetchMarketIndex
  
  // Filter and sort indexData to match required indices order
  // Render table with columns: Index | Index Value | Index Change | Change (%)
  // Color-code change/percent: green (upArrow), red (downArrow), neutral (else)
  // Handle loading (null) and missing indices gracefully
}
```

**Props:**
- `title` — exchange label (e.g., "Dhaka Stock Exchange (DSE)")
- `indices` — ordered array of index keys to display
- `indexData` — full array from API (already fetched in Home.jsx)

### 2. Update Home.jsx Hero Section
**File:** `nls_frontend/src/pages/Home.jsx`

**Changes:**
- Import `IndexTable` from `../components/IndexTable`
- Remove title/subtitle block (lines 91-98)
- Remove `market-widget-row` and its 8 cards (lines 100-110)
- Remove unused imports: `MarketStatCard`, `IndexStatCard`
- Replace entire `hero-market-row` with new layout:

```jsx
<div className="row g-3 hero-index-tables-row">
  <div className="col-12 col-lg-6">
    <IndexTable
      title="Dhaka Stock Exchange (DSE)"
      indices={["DSEX", "DS30", "DSES"]}
      indexData={indexValues}
    />
  </div>
  <div className="col-12 col-lg-6">
    <IndexTable
      title="Chittagong Stock Exchange (CSE)"
      indices={["CSCX", "CSE50", "CSE30", "CASPI", "CSI"]}
      indexData={indexValuesCSE}
    />
  </div>
</div>
```

### 3. Add CSS for Hero Index Tables
**File:** `nls_frontend/src/index.css`

Add after `.market-widget-row` styles (around line 108):

```css
/* ===== Hero Index Tables ===== */
.hero-index-tables-row {
  margin-top: var(--space-3);
}
.hero-index-table-wrap {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-3);
  height: 100%;
}
.hero-index-table-title {
  font-size: var(--fs-sm);
  font-weight: 600;
  color: var(--color-primary);
  margin-bottom: var(--space-3);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.hero-index-table-wrap .table {
  margin-bottom: 0;
  font-size: var(--fs-sm);
}
.hero-index-table-wrap .table th {
  background: var(--color-bg);
  font-weight: 600;
  font-size: var(--fs-xs);
  text-transform: uppercase;
  letter-spacing: 0.03em;
  padding: var(--space-2);
}
.hero-index-table-wrap .table td {
  padding: var(--space-2);
  vertical-align: middle;
}
.hero-index-table-wrap .table td:first-child {
  font-weight: 600;
  font-family: var(--font-body);
}
.hero-index-table-wrap .table .change-cell,
.hero-index-table-wrap .table .pct-cell {
  font-variant-numeric: tabular-nums;
  font-family: var(--font-body);
}
.hero-index-table-wrap .table .text-up { color: var(--color-up); }
.hero-index-table-wrap .table .text-down { color: var(--color-down); }
.hero-index-table-wrap .table .text-neutral { color: var(--color-neutral); }

@media (max-width: 768px) {
  .hero-index-table-wrap {
    padding: var(--space-2);
  }
  .hero-index-table-wrap .table th,
  .hero-index-table-wrap .table td {
    padding: var(--space-1) var(--space-2);
    font-size: var(--fs-xs);
  }
}
```

### 4. Responsive Behavior
- **Desktop (≥992px):** Two tables side by side (`col-lg-6` each)
- **Tablet (768–991px):** Two columns if readable, else stack — Bootstrap `col-12 col-lg-6` handles this
- **Mobile (<768px):** Stack vertically (`col-12`)

### 5. Data Flow (No Backend Changes)
- Home.jsx already fetches `indexValues` (DSE) and `indexValuesCSE` (CSE) every 10s
- `IndexTable` receives filtered data via props — no new API calls
- Loading state: when `indexData` is null, show spinner row (reuse existing pattern from DSEIndex)
- Missing index: show "—" in value/change/percent cells

### 6. Files to Modify

| File | Change |
|------|--------|
| `nls_frontend/src/components/IndexTable.jsx` | New reusable table component |
| `nls_frontend/src/pages/Home.jsx` | Replace hero content, import IndexTable, remove widgets |
| `nls_frontend/src/index.css` | Add `.hero-index-table-wrap` and responsive styles |

### 7. Validation Checklist
- [ ] `npm run build` passes
- [ ] `npm run lint` — no new errors in modified files
- [ ] Dev server: hero shows two tables side by side on desktop
- [ ] Tables display correct indices in specified order
- [ ] Values match existing `DSEIndex`/`CSEIndex` tables on page
- [ ] Green for positive, red for negative, neutral for unchanged
- [ ] Percentage changes show % symbol and sign
- [ ] Mobile: tables stack vertically, no horizontal overflow
- [ ] 10s auto-refresh still works
- [ ] Loading/error states preserved

## Open Questions (None — All Resolved)

All required indices confirmed available in existing API response. No backend changes needed. Existing design tokens and table styles sufficient.