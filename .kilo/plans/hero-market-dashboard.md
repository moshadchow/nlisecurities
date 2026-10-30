# Implementation Plan: Combined Exchange-Wise Market Breadth & Index Tables in Hero

## Current State Analysis

**Hero Section:** `nls_frontend/src/pages/Home.jsx` lines 74-98
- Currently shows two `IndexTable` components side by side (DSE and CSE)
- Fetches only `fetchMarketIndex` for both exchanges (index data)
- **Missing:** `fetchMarketInfo` calls for market breadth (advance/decline/unchanged)

**Available Data Sources:**
| API | Endpoint | Returns | Currently Used |
|-----|----------|---------|----------------|
| `fetchMarketInfo("DSE")` | `/market_info/DSE` | `{ advance, decline, unchange }` | ❌ No |
| `fetchMarketInfo("CSE")` | `/market_info/CSE` | `{ advance, decline, unchange }` | ❌ No |
| `fetchMarketIndex("DSE")` | `/market_index/DSE` | `[{ index, value, change, percent, arrow }, ...]` | ✅ Yes |
| `fetchMarketIndex("CSE")` | `/market_index/CSE` | `[{ index, value, change, percent, arrow }, ...]` | ✅ Yes |

**Required Indices — All Available:**
| Exchange | Market Breadth | Index Table |
|----------|----------------|-------------|
| DSE | Advance, Decline, Unchanged | DSEX, DS30, DSES |
| CSE | Advance, Decline, Unchanged | CSCX, CSE50, CSE30, CASPI, CSI |

**Existing Components:**
- `MarketStatCard` — compact card for single metric (label + value with variant color)
- `IndexTable` — full table with 4 columns (Index, Value, Change, Change %)
- CSS: `.stat-card` variants (advance/decline/unchanged), `.hero-index-table-wrap`

## Plan

### 1. Update Home.jsx — Add Market Breadth Fetching
**File:** `nls_frontend/src/pages/Home.jsx`

- Add `fetchMarketInfo` to imports
- Add state for market breadth: `marketBreadthDSE`, `marketBreadthCSE`
- In `loadMarketIndex`, also call `fetchMarketInfo("DSE")` and `fetchMarketInfo("CSE")`
- Set breadth state alongside index state

### 2. Create `MarketBreadth` Component
**File:** `nls_frontend/src/components/MarketBreadth.jsx` (new)

```jsx
const MarketBreadth = ({ title, data }) => {
  // data: { advance, decline, unchange }
  // Renders 3 MarketStatCards horizontally: Advance | Decline | Unchanged
  // With exchange title above
}
```

Props:
- `title` — "Dhaka Stock Exchange (DSE)" or "Chittagong Stock Exchange (CSE)"
- `data` — object with advance, decline, unchange

### 3. Create `CSEMarketOverview` Component
**File:** `nls_frontend/src/components/CSEMarketOverview.jsx` (new)

Combines CSE market breadth + CSE index table in a single vertical stack for Group 3.

```jsx
const CSEMarketOverview = ({ breadthData, indexData }) => {
  // Renders MarketBreadth (CSE) on top, IndexTable (CSE) below
  // Single component for Group 3
}
```

### 4. Update Home.jsx Hero Layout
**File:** `nls_frontend/src/pages/Home.jsx`

Replace current two-column layout with three-group horizontal row:

```jsx
<div className="row g-3 hero-market-dashboard-row align-items-start">
  {/* Group 1: DSE Market Breadth */}
  <div className="col-12 col-lg-3 col-xl-2">
    <MarketBreadth 
      title="Dhaka Stock Exchange (DSE)" 
      data={marketBreadthDSE} 
    />
  </div>
  
  {/* Group 2: DSE Index Table */}
  <div className="col-12 col-lg-4 col-xl-5">
    <IndexTable
      title="DSE Indices"
      indices={["DSEX", "DS30", "DSES"]}
      indexData={indexValues}
    />
  </div>
  
  {/* Group 3: CSE Market Breadth + Index Table */}
  <div className="col-12 col-lg-5 col-xl-5">
    <CSEMarketOverview
      breadthData={marketBreadthCSE}
      indexData={indexValuesCSE}
    />
  </div>
</div>
```

**Column width rationale:**
- Group 1 (DSE Breadth): ~2-3 columns (3 compact cards)
- Group 2 (DSE Index): ~4-5 columns (3-row table)
- Group 3 (CSE Breadth + Table): ~5 columns (3 cards + 5-row table)

### 5. Add CSS for New Layout
**File:** `nls_frontend/src/index.css`

Add after `.hero-index-table-wrap` styles:

```css
/* ===== Hero Market Dashboard ===== */
.hero-market-dashboard-row {
  margin-top: var(--space-3);
}
.hero-market-group {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-3);
  height: 100%;
}
.hero-market-group-title {
  font-size: var(--fs-sm);
  font-weight: 600;
  color: var(--color-primary);
  margin-bottom: var(--space-3);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.market-breadth-cards {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
  justify-content: center;
}
.market-breadth-cards .stat-card {
  flex: 1;
  min-width: 100px;
  padding: var(--space-2);
  min-height: auto;
}
.market-breadth-cards .stat-card .label {
  font-size: 0.65rem;
  margin-bottom: var(--space-1);
}
.market-breadth-cards .stat-card .value {
  font-size: var(--fs-h3);
}

@media (max-width: 991px) {
  .hero-market-dashboard-row > div {
    margin-bottom: var(--space-3);
  }
  .market-breadth-cards {
    justify-content: space-between;
  }
  .market-breadth-cards .stat-card {
    flex: 1 1 30%;
  }
}
@media (max-width: 576px) {
  .hero-market-dashboard-row {
    flex-direction: column;
  }
  .hero-market-dashboard-row > div {
    width: 100%;
  }
  .market-breadth-cards .stat-card {
    flex: 1 1 45%;
  }
}
```

### 6. Responsive Behavior
| Breakpoint | Layout |
|------------|--------|
| Desktop (≥1200px) | 3 groups horizontal: 2/5/5 columns |
| Laptop (992–1199px) | 3 groups horizontal: 3/4/5 columns |
| Tablet (768–991px) | 3 groups horizontal but narrower, or stack Group 1 |
| Mobile (<768px) | All groups stacked vertically |

### 7. Files to Modify

| File | Change |
|------|--------|
| `nls_frontend/src/components/MarketBreadth.jsx` | New: 3-card market breadth display |
| `nls_frontend/src/components/CSEMarketOverview.jsx` | New: combines CSE breadth + index table |
| `nls_frontend/src/pages/Home.jsx` | Add fetchMarketInfo, new state, new hero layout |
| `nls_frontend/src/index.css` | Add `.hero-market-dashboard-row`, `.hero-market-group`, responsive styles |

### 8. Validation Checklist
- [ ] `npm run build` passes
- [ ] `npm run lint` — no new errors
- [ ] Desktop: all 3 groups in one horizontal row, no clipping
- [ ] DSE Breadth: Advance/Decline/Unchanged values display correctly
- [ ] DSE Index Table: DSEX, DS30, DSES with correct data
- [ ] CSE Breadth: Advance/Decline/Unchanged values display correctly
- [ ] CSE Index Table: CSCX, CSE50, CSE30, CASPI, CSI with correct data
- [ ] Green for positive, red for negative, neutral for unchanged
- [ ] Mobile: vertical stacking, no horizontal overflow
- [ ] 10s auto-refresh works for both data sources
- [ ] Loading/error states preserved

## Open Questions

1. **Column widths:** The exact `col-lg-*` values may need tuning. Start with `col-lg-3` / `col-lg-4` / `col-lg-5` and adjust based on visual verification.

2. **CSE group structure:** Should CSE breadth cards be above the table (vertical stack) or side-by-side? Spec says "together within remaining horizontal space" — vertical stack within Group 3 seems most compact.

3. **Loading states:** When breadth loads but index doesn't (or vice versa), show spinner in each group independently.