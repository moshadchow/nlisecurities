# Fix: DSE/CSE Index Widgets Show No Data in Hero Section

## Root Cause

**Data source mismatch**: 

| API Call | Endpoint | Returns | Used By |
|----------|----------|---------|---------|
| `fetchMarketInfo("DSE")` | `/market_info/DSE` | `{ advance, decline, unchange }` (object) | `MarketStatCard` ✓ |
| `fetchMarketIndex("DSE")` | `/market_index/DSE` | `[{ index: "DSEX", value, change, percent, arrow }, ...]` (array) | `IndexStatCard` ✗ |

**Current bug**: `Home.jsx` calls only `fetchMarketInfo` and stores results in `indexData`/`indexDataCSE`. The `MarketStatCard` widgets work (they read `advance/decline/unchange`), but `IndexStatCard` expects an **array** to find `indexKey` ("DSEX"/"CSE50"). Since it receives an object, `Array.isArray(indexData)` is false → shows "-".

## Fix Plan

### 1. Update `Home.jsx` — Add index value state & fetch

**File**: `nls_frontend/src/pages/Home.jsx`

- Add two new state variables:
  ```jsx
  const [indexValues, setIndexValues] = useState(null);
  const [indexValuesCSE, setIndexValuesCSE] = useState(null);
  ```

- In `loadMarketIndex`, also call `fetchMarketIndex` for DSE and CSE:
  ```jsx
  const loadMarketIndex = async () => {
    try {
      const response = await fetchMarketInfo("DSE");
      const res_cse = await fetchMarketInfo("CSE");
      const idxResponse = await fetchMarketIndex("DSE");
      const idxResponseCSE = await fetchMarketIndex("CSE");
      
      if (response.error) throw new Error(response.error);
      if (res_cse.error) throw new Error(res_cse.error);
      if (idxResponse.error) throw new Error(idxResponse.error);
      if (idxResponseCSE.error) throw new Error(idxResponseCSE.error);
      
      setIndexData(response);        // market breadth for MarketStatCard
      setIndexDataCSE(res_cse);      // market breadth for MarketStatCard
      setIndexValues(idxResponse);   // index array for IndexStatCard
      setIndexValuesCSE(idxResponseCSE);
    } catch (err) { ... }
  };
  ```

- Pass correct data to `IndexStatCard`:
  ```jsx
  <IndexStatCard label="DSE Index" indexData={indexValues} indexKey="DSEX" />
  <IndexStatCard label="CSE Index" indexData={indexValuesCSE} indexKey="CSE50" />
  ```

- Add import for `fetchMarketIndex`:
  ```jsx
  import { fetchMarketInfo, fetchMarketIndex } from "../services/chartService";
  ```

### 2. Validation

1. `npm run build` passes
2. `npm run dev` → verify DSE Index and CSE Index widgets show values (not "-")
3. Values match the `DSEIndex`/`CSEIndex` tables on the page (which use same endpoint)
4. 10s auto-refresh still works for both data sets

## Files to Modify

| File | Change |
|------|--------|
| `nls_frontend/src/pages/Home.jsx` | Add indexValues state, fetchMarketIndex calls, pass correct props |

No CSS or component changes needed.