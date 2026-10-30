# Implementation Plan: Add Exchange-Wise Market Performance Tables

## Current State Analysis

**Market (At a Glance) Section Location:** `nls_frontend/src/pages/Home.jsx` lines 120-148

**Current Structure:**
```jsx
<div className="container-fluid py-5 bg-dark">  // "Chart Start" section
  <div className="container">
    <h1>Market (At a Glance)</h1>
    <div className="market-pair-row">
      <div className="col-lg-6">
        <FetchTopShareBy />  // DSE tabbed: Gainer/Loser/Value/Volume
      </div>
      <div className="col-lg-6">
        <FetchTopShareCSEBy />  // CSE tabbed: Gainer/Loser/Value/Volume
      </div>
    </div>
  </div>
</div>
```

**Existing Data Source:**
- API: `/top_share_price_by/DSE` and `/top_share_price_by/CSE` (via `fetchTopSharePrice`)
- Returns array with: `symbol`, `ltp`, `ycp`, `change_val`, `change_per`, `value_mn`, `volume`
- Already sorted/filtered in `FetchTopShareBy`/`FetchTopShareCSEBy` components
- Top 10 items displayed via `RenderTable`

**Required Tables (8 total):**
| Exchange | Tables | Required Columns |
|----------|--------|------------------|
| DSE | Gainers, Losers, Highest Value, Highest Volume | Instrument, LTP, YCP, Change, Change(%) |
| CSE | Gainers, Losers, Highest Value, Highest Volume | Instrument, LTP, YCP, Change, Change(%) |

---

## Plan

### 1. Create Reusable `MarketPerformanceTable` Component
**File:** `nls_frontend/src/components/MarketPerformanceTable.jsx` (new)

```jsx
const MarketPerformanceTable = ({ title, data, category }) => {
  // category: 'gainer' | 'loser' | 'value' | 'volume'
  // Sort data based on category
  // Render table with columns: Instrument | LTP | YCP | Change | Change(%) [or Value/Volume]
  // Use existing dark theme styles from index.css
  // Show top 10 items
  // Handle loading/error/empty states
}
```

**Props:**
- `title` — e.g., "DSE Gainers"
- `data` — array of stock objects from API
- `category` — determines sorting and which extra column to show

**Sorting Logic (reuse from existing components):**
- `gainer`: sort by `change_per` descending
- `loser`: sort by `change_per` ascending
- `value`: sort by `value_mn` descending
- `volume`: sort by `volume` descending

**Columns:**
- Always: Instrument, LTP, YCP
- For Gainer/Loser: Change, Change(%)
- For Value: Value(mn)
- For Volume: Volume

### 2. Update Home.jsx — Add Market Performance Tables
**File:** `nls_frontend/src/pages/Home.jsx`

**Changes:**
- Import `MarketPerformanceTable`
- In the "Chart Start" section (lines 121-148), replace the tabbed view with 8 static tables:

```jsx
<div className="container-fluid py-5 bg-dark">
  <div className="container">
    <div className="text-center wow fadeIn" data-wow-delay="0.1s">
      <h1 className="mb-4 text-primary bg-light">
        Market{" "}
        <span className="text-uppercase px-2">(At a Glance)</span>
      </h1>
    </div>

    {/* DSE Market Performance */}
    <div className="mb-5">
      <h3 className="text-primary mb-3">Dhaka Stock Exchange (DSE)</h3>
      <div className="row g-4">
        <div className="col-12 col-lg-6">
          <MarketPerformanceTable title="DSE Gainers" data={dseData} category="gainer" />
        </div>
        <div className="col-12 col-lg-6">
          <MarketPerformanceTable title="DSE Losers" data={dseData} category="loser" />
        </div>
        <div className="col-12 col-lg-6">
          <MarketPerformanceTable title="DSE Highest Value" data={dseData} category="value" />
        </div>
        <div className="col-12 col-lg-6">
          <MarketPerformanceTable title="DSE Highest Volume" data={dseData} category="volume" />
        </div>
      </div>
    </div>

    {/* CSE Market Performance */}
    <div className="mb-5">
      <h3 className="text-primary mb-3">Chittagong Stock Exchange (CSE)</h3>
      <div className="row g-4">
        <div className="col-12 col-lg-6">
          <MarketPerformanceTable title="CSE Gainers" data={cseData} category="gainer" />
        </div>
        <div className="col-12 col-lg-6">
          <MarketPerformanceTable title="CSE Losers" data={cseData} category="loser" />
        </div>
        <div className="col-12 col-lg-6">
          <MarketPerformanceTable title="CSE Highest Value" data={cseData} category="value" />
        </div>
        <div className="col-12 col-lg-6">
          <MarketPerformanceTable title="CSE Highest Volume" data={cseData} category="volume" />
        </div>
      </div>
    </div>
  </div>
</div>
```

**State Management:**
- Add `dseData` and `cseData` state to Home.jsx (or reuse existing fetch logic)
- Fetch data in `useEffect` with 10s refresh (reuse existing pattern)
- Share data between the 4 tables per exchange (single fetch per exchange)

### 3. Add CSS for Market Performance Tables
**File:** `nls_frontend/src/index.css`

Add styles consistent with existing dark theme:
```css
/* ===== Market Performance Tables ===== */
.market-performance-section {
  margin-top: var(--space-6);
}
.market-performance-title {
  color: var(--color-secondary);
  font-size: var(--fs-h3);
  margin-bottom: var(--space-4);
}
.market-performance-table-wrap {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-3);
}
.market-performance-table-wrap .table {
  margin-bottom: 0;
  font-size: var(--fs-sm);
  background: var(--bs-light);
}
.market-performance-table-wrap .table th {
  background: var(--color-table-header);
  font-weight: 600;
  font-size: var(--fs-xs);
  text-transform: uppercase;
  letter-spacing: 0.03em;
  padding: var(--space-2);
  color: var(--color-text);
}
.market-performance-table-wrap .table td {
  padding: var(--space-2);
  vertical-align: middle;
  color: var(--color-text);
}
.market-performance-table-wrap .table td:first-child {
  font-weight: 600;
  font-family: var(--font-body);
}
.market-performance-table-wrap .table .text-up { color: var(--color-up); }
.market-performance-table-wrap .table .text-down { color: var(--color-down); }
.market-performance-table-wrap .table .text-neutral { color: var(--color-neutral); }
.market-performance-table-wrap .table .value-col,
.market-performance-table-wrap .table .volume-col {
  font-variant-numeric: tabular-nums;
  font-family: var(--font-body);
}

@media (max-width: 768px) {
  .market-performance-table-wrap {
    padding: var(--space-2);
  }
  .market-performance-table-wrap .table th,
  .market-performance-table-wrap .table td {
    padding: var(--space-1) var(--space-2);
    font-size: var(--fs-xs);
  }
}
```

### 4. Responsive Behavior
- **Desktop (≥992px):** 2 tables per row (col-lg-6)
- **Tablet (768-991px):** 2 tables per row
- **Mobile (<768px):** 1 table per row (col-12), horizontal scroll within tables

### 5. Files to Modify

| File | Change |
|------|--------|
| `nls_frontend/src/components/MarketPerformanceTable.jsx` | New reusable table component |
| `nls_frontend/src/pages/Home.jsx` | Add state, fetch logic, render 8 tables in Chart section |
| `nls_frontend/src/index.css` | Add `.market-performance-table-wrap` styles |

### 6. Data Fetching Strategy
- Reuse existing `fetchTopSharePrice("DSE")` and `fetchTopSharePrice("CSE")`
- Single fetch per exchange, shared across 4 tables
- Maintain 10s refresh interval
- Handle loading/error states per exchange

### 7. Validation Checklist
- [ ] `npm run build` passes
- [ ] 8 tables render correctly (4 DSE + 4 CSE)
- [ ] Tables appear below market index overview (in Chart section)
- [ ] Gainers sorted by change_per desc
- [ ] Losers sorted by change_per asc
- [ ] Highest Value sorted by value_mn desc
- [ ] Highest Volume sorted by volume desc
- [ ] Columns: Instrument, LTP, YCP, Change, Change(%) / Value / Volume
- [ ] DSE/CSE data separated correctly
- [ ] Dark theme preserved (bg: #111B2D, surface: #151F32, text: #F1F5F9)
- [ ] Green/red/neutral for changes
- [ ] Responsive: desktop 2-col, mobile stacked with horizontal scroll
- [ ] Loading/error/empty states work
- [ ] 10s auto-refresh works
- [ ] No backend changes

## Open Questions

1. **Tabbed view:** Keep the existing `FetchTopShareBy`/`FetchTopShareCSEBy` tabbed view, or replace entirely? The spec says "adding" tables below the index overview, which suggests keeping the current section but the new tables would be redundant. Recommendation: Replace the tabbed view with the 8 static tables since they show all categories simultaneously.

2. **Top 10 limit:** Current `RenderTable` shows `slice(0, 10)`. Keep this limit for all 8 tables?

3. **Table headers for Value/Volume:** Should "Change" and "Change(%)" columns be hidden for Value/Volume tables (as current RenderTable does), or show them anyway? Spec says every table must have 5 columns: Instrument, LTP, YCP, Change, Change(%). But for Value/Volume, Change/Change(%) may not be meaningful. Recommendation: Follow spec - show all 5 columns, with Change/Change(%) calculated from ltp/ycp.

4. **Existing `market-pair-row` CSS:** Currently used for the tabbed view spacing. May need adjustment for new table grid layout.