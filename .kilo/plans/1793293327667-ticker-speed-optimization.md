# Market Ticker Speed Fix — Implementation Plan

## Root Cause Analysis

**Why the previous CSS change had no visible effect:**

1. **Content not duplicated** — `Ticker.jsx` renders `mergedData` once inside `.ticker-track`
2. **Keyframe logic requires duplication** — `translateX(0) → translateX(-50%)` moves exactly half the track width. With single content, this moves half the items then **jumps back to start** (visible reset)
3. **Effective speed ≠ animation duration** — The jump makes it feel faster; the 40s duration moves only half the content
4. **No width constraint** — `.ticker-wrap` has `overflow: hidden` but no fixed width; `.ticker-track` expands to fit all items

**Current behavior (broken):**
```
[Item1 Item2 Item3 Item4] → animate -50% → [Item3 Item4 Item1 Item2] → JUMP to start
```
Animation: 40s for half the content, then hard reset.

**Required behavior (seamless):**
```
[Item1 Item2 Item3 Item4][Item1 Item2 Item3 Item4] → animate -50% → seamless loop
```
Animation: 40s for ONE full content pass, continuous.

## Implementation Plan

### Phase 1: Duplicate Content in JSX (Critical)
**File:** `nls_frontend/src/components/Ticker.jsx`

Render `mergedData` **twice** in the track:
```jsx
<div className="ticker-track">
  {/* First copy */}
  {mergedData.map((item, i) => <TickerItem key={i} item={item} />)}
  {/* Second copy — key offset to avoid collisions */}
  {mergedData.map((item, i) => <TickerItem key={i + 1000} item={item} />)}
</div>
```
Extract `<TickerItem />` sub-component to avoid duplication.

### Phase 2: Set Correct Animation Duration
**File:** `nls_frontend/src/index.css`

Target: **75% slower than current perceived speed**

- Current (broken): half-content in 40s → perceived ~80s for full pass with jump
- Target: 4× slower = **~320s for full pass** (or 160s if measuring differently)
- **Start with 160s** for duplicated content (one full pass = 160s), verify in browser, adjust to 200s–320s as needed

```css
.ticker-track {
  animation: ticker-scroll 160s linear infinite; /* was 40s */
}
```

### Phase 3: Ensure Layout Stability
- Verify `.ticker-wrap` constrains width (add `width: 100%` if needed)
- Confirm `.ticker-track` has no conflicting inline styles
- Test with varying data lengths (few items vs many items)

### Phase 4: Verify & Fine-Tune
1. `npm run dev` → observe in browser
2. Confirm: smooth, no jumps, readable (~3–5 seconds per item)
3. Adjust duration up/down if needed
4. Test on mobile (viewport width affects perceived speed)
4. `npm run build` passes

## Files to Modify

| File | Change |
|------|--------|
| `nls_frontend/src/components/Ticker.jsx` | Duplicate content, extract `TickerItem` |
| `nls_frontend/src/index.css` | Increase `animation` duration to `160s` |

## What NOT to Change
- Backend/API (`chartService.jsx`, `getApi.jsx`, Django/FastAPI)
- Data fetching interval (10s refresh is separate from scroll speed)
- Ticker visual design, colors, direction
- Other components

## Validation Checklist
- [ ] Ticker scrolls continuously without visible jumps/resets
- [ ] Speed is ~75% slower than before (items readable for 3–5s each)
- [ ] Smooth linear motion, no jitter
- [ ] Works on desktop, tablet, mobile
- [ ] Data refresh (10s) still updates content without breaking animation
- [ ] `npm run build` passes

## Risk Mitigation
- If duplicated content causes layout issues (too wide): ensure `.ticker-wrap` has `width: 100%; overflow: hidden;`
- If animation still doesn't run: check CSS specificity, ensure no `!important` overrides
- If too slow/fast: adjust duration in 20s increments