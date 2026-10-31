# Implementation Plan: Fix Gainers and Losers Filtering in Market Performance Table

## Root Cause Analysis

### 1. API Endpoint Misuse
- **Frontend** calls `fetchTopSharePrice("DSE")` → `/api/top_share_price_by/DSE`
- **Backend** `Top_share_price_by` expects `pk` = "Gainer"|"Loser"|"Value"|"Volume" for category-specific sorting
- **Reality**: Backend receives "DSE"/"CSE" as `pk`, which matches NONE of the sorting conditions
- **Result**: Returns ALL records for that market without category sorting

### 2. Frontend Filtering Missing
- `getSortedTop10()` sorts by `_changePer` but doesn't filter:
  - **Gainers**: Should only show `change_per > 0`
  - **Losers**: Should only show `change_per < 0`
- Currently shows all 10 records regardless of positive/negative/zero change

### 3. Missing `change_per` Field
- API returns: `change_val`, `ycp`, `ltp`, `value_mn`, `volume`, `symbol`
- API does NOT return: `change_per` (percentage change)
- Frontend uses `item.change_per` → undefined → displays "-"
- Need to calculate: `(change_val / ycp) * 100`

### 4. Tab Click Handling Works
- `onCategoryChange` correctly updates state in Home.jsx
- Category state flows to MarketMovers via props
- Active tab styling works correctly

## Files to Modify

### 1. `nls_frontend/src/components/MarketMovers.jsx`
**Primary fix location** - Update `getSortedTop10` function:
- Calculate `_changePer` from `change_val / ycp * 100` (not from `change_per`)
- Add filtering for Gainers (`_changePer > 0`) and Losers (`_changePer < 0`)
- Apply filter BEFORE sorting and top-10 limit
- Handle null/zero ycp to avoid division by zero
- Update `formatPercent` to use calculated `_changePer`

### 2. `nls_frontend/src/pages/Home.jsx` (Optional optimization)
- Could fetch category-specific data from backend by calling `/api/top_share_price_by/Gainer`, `/api/top_share_price_by/Loser`, etc.
- But spec says: "Do not introduce unnecessary duplicate API requests when switching tabs"
- Current approach (fetch all, filter client-side) is acceptable

## Implementation Details

### MarketMovers.jsx - getSortedTop10 Function Changes

```javascript
const getSortedTop10 = (data, cat) => {
  if (!data || !Array.isArray(data) || data.length === 0) return [];

  const numeric = data
    .map((item) => {
      const changeVal = parseFloat(item.change_val) || 0;
      const ycp = parseFloat(item.ycp) || 0;
      // Calculate percentage change: (change_val / ycp) * 100
      const changePer = (ycp !== 0) ? (changeVal / ycp) * 100 : 0;
      
      return {
        ...item,
        _changePer: changePer,
        _changeVal: changeVal,
        _valueMn: parseFloat(item.value_mn) || 0,
        _volume: parseFloat(item.volume) || 0,
      };
    })
    .filter((item) => {
      // Exclude records with all zero/invalid values
      return !(item._changePer === 0 && item._changeVal === 0 && 
               item._valueMn === 0 && item._volume === 0);
    });

  let filtered = [...numeric];

  // Apply category-specific filtering
  switch (cat) {
    case "gainer":
      filtered = filtered.filter(item => item._changePer > 0);
      break;
    case "loser":
      filtered = filtered.filter(item => item._changePer < 0);
      break;
    case "value":
    case "volume":
      // No filtering, just sorting
      break;
  }

  const sorted = filtered.sort((a, b) => {
    let cmp = 0;
    switch (cat) {
      case "gainer":
        cmp = b._changePer - a._changePer;
        break;
      case "loser":
        cmp = a._changePer - b._changePer;
        break;
      case "value":
        cmp = b._valueMn - a._valueMn;
        break;
      case "volume":
        cmp = b._volume - a._volume;
        break;
    }
    if (cmp === 0) {
      const sa = (a.symbol || "").toString().toLowerCase();
      const sb = (b.symbol || "").toString().toLowerCase();
      return sa < sb ? -1 : sa > sb ? 1 : 0;
    }
    return cmp;
  });

  return sorted.slice(0, 10);
};
```

### formatPercent Function Update
```javascript
const formatPercent = (item) => {
  const val = item._changePer ?? parseFloat(item.change_per);
  if (isNaN(val)) return "-";
  const sign = val > 0 ? "+" : val < 0 ? "" : "";
  return `${sign}${val.toFixed(2)}%`; // 2 decimal places
};
```

### getChangeClass Function Update
```javascript
const getChangeClass = (item) => {
  const val = item._changePer ?? parseFloat(item.change_per) || 0;
  if (val > 0) return "text-up";
  if (val < 0) return "text-down";
  return "text-neutral";
};
```
Update usage in JSX to pass `item` instead of `item.change_per`.

## Testing Checklist

### DSE Testing
- [ ] Gainers tab: Only positive % change, sorted desc, max 10
- [ ] Losers tab: Only negative % change, sorted asc, max 10
- [ ] Highest Value: Sorted by value_mn desc, max 10
- [ ] Highest Volume: Sorted by volume desc, max 10
- [ ] Change(%) column shows calculated percentages (e.g., "+8.01%")

### CSE Testing
- [ ] Same as DSE but with CSE data
- [ ] Switching between DSE/CSE doesn't leak data
- [ ] Switching tabs doesn't reset exchange selection

### Edge Cases
- [ ] No gainers: Shows "No data available for the selected category"
- [ ] No losers: Shows "No data available for the selected category"
- [ ] Invalid/zero YCP: Excluded from Gainers/Losers, not treated as zero
- [ ] Missing change_val: Treated as 0, excluded from Gainers/Losers

## Acceptance Criteria Mapping

| Spec Requirement | Implementation |
|-----------------|----------------|
| Gainers: positive % only, sorted desc | Filter `_changePer > 0`, sort desc |
| Losers: negative % only, sorted asc | Filter `_changePer < 0`, sort asc |
| Max 10 records each | `.slice(0, 10)` after filter+sort |
| Change(%) displays actual % | Calculate from `change_val/ycp*100`, 2 decimals |
| Independent per exchange | Filter applied on exchange-specific data |
| No extra API calls | Single fetch per exchange, client-side filter |
| Empty states handled | Check `items.length === 0` |
| Dark theme preserved | No CSS changes needed |