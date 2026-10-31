# Implementation Plan: Fix Market At a Glance Dashboard Layout

## Issues Analysis

### Current Problems
1. **Duplicate heading** - "Market At A Glance" appears in both Home.jsx (line 97) and MarketMovers.jsx (line 130)
2. **Fixed heights** - `.hero-market-group` and `.hero-index-table-wrap` have `height: 100%`, causing excessive empty space when combined with `align-items-stretch`
3. **Nested containers** - `container-fluid` → `container` → `container py-3` creates unnecessary nesting
4. **Insufficient section spacing** - `market-performance-section` only has `margin-top: 24px`
5. **MarketMovers internal state** - Exchange selector and category tabs are inside MarketMovers, preventing clean separation

## Files to Modify

### 1. nls_frontend/src/index.css
**Add new layout classes:**
```css
/* Market At a Glance - new layout */
.market-at-glance {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.market-at-glance-title {
  text-align: center;
  margin-bottom: var(--space-2);
  color: var(--color-text);
}

.exchange-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-4);
  align-items: start;
}

.exchange-column {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.market-breadth-panel,
.market-index-panel {
  width: 100%;
  height: auto;
  min-height: 0;
}

.market-breadth-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-2);
}

.market-performance-section {
  width: 100%;
  margin-top: var(--space-4);
}

/* Remove height: 100% from existing panels */
.hero-market-group,
.hero-index-table-wrap {
  height: auto;
  min-height: 0;
}

/* Responsive */
@media (max-width: 991px) {
  .exchange-grid {
    grid-template-columns: 1fr;
  }
}
```

**Remove/modify:**
- Remove `height: 100%` from `.hero-market-group` (line 589) and `.hero-index-table-wrap` (line 528)
- Keep existing responsive styles for `.market-breadth-cards`

### 2. nls_frontend/src/components/MarketMovers.jsx
**Convert to controlled component:**
- Remove internal state: `exchange`, `category`, `dseData`, `cseData`, `loading`, `error`
- Accept props: `exchange`, `category`, `onExchangeChange`, `onCategoryChange`, `dseData`, `cseData`, `loading`, `error`
- Remove duplicate "Market At A Glance" heading (line 130)
- Render only: exchange selector buttons, category tabs, and table
- Keep all sorting/formatting logic

### 3. nls_frontend/src/pages/Home.jsx
**Restructure layout:**
- Fetch both DSE and CSE share data in `loadMarketIndex` (already done)
- Pass data to MarketMovers as props
- New structure:
```jsx
<div className="market-at-glance">
  <h1 className="market-at-glance-title">Market (At a Glance)</h1>
  
  <div className="exchange-grid">
    <div className="exchange-column">
      <DSEMarketOverview breadthData={marketBreadthDSE} indexData={indexValues} />
    </div>
    <div className="exchange-column">
      <CSEMarketOverview breadthData={marketBreadthCSE} indexData={indexValuesCSE} />
    </div>
  </div>

  <MarketMovers
    exchange={exchange}
    category={category}
    onExchangeChange={setExchange}
    onCategoryChange={setCategory}
    dseData={dseShareData}
    cseData={cseShareData}
    loading={loading}
    error={error}
  />
</div>
```
- Add local state for `exchange`, `category`, `dseShareData`, `cseShareData`, `loading`, `error`
- Fetch share data in `loadMarketIndex` (parallel with other calls)
- Remove nested containers (`container-fluid` → `container` → `container py-3`)

### 4. DSEMarketOverview.jsx & CSEMarketOverview.jsx
**Minor updates:**
- Change wrapper class from `hero-market-group` to `market-breadth-panel` / `market-index-panel` or keep existing but ensure no `height: 100%`
- The existing `mt-3` between breadth and index table is fine

## Validation Checklist
- [ ] No duplicate "Market At A Glance" heading
- [ ] DSE/CSE breadth panels side by side on desktop, stacked on mobile
- [ ] Breadth metrics (Advance/Decline/Unchanged) horizontal in each panel
- [ ] Index tables directly below their respective breadth panels
- [ ] CSE index table grows naturally (5 rows) without forcing DSE to match height
- [ ] Market Performance section below both index tables with proper spacing
- [ ] Exchange selector and category tabs work correctly
- [ ] Table switches data when exchange/category changes
- [ ] No overlapping elements at any viewport
- [ ] Dark theme colors preserved
- [ ] Lint passes with no new errors