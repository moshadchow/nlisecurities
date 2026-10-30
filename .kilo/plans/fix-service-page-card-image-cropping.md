# Fix Service Card Image Cropping on /service Page — Implementation Plan

## Current State Analysis

### Component
**File:** `nls_frontend/src/pages/Service.jsx` (lines 84-128)

### Problem Code (lines 95-108)
```jsx
<Link to={`/service_dtl/${item.id}`} className="service-img position-relative mb-3">
  <img
    className="img-fluid w-100"
    src={item.image ? "http://127.0.0.1:8000" + item.image : "/placeholder-service.jpg"}
    alt={item.title || "Service image"}
    style={{
      height: "250px",
      objectFit: "cover",        // ← ROOT CAUSE: crops left/right edges
      borderRadius: "8px",
    }}
  />
  <h3 className="mt-2 mb-0 text-white">{item.title}</h3>
</Link>
```

### Root Cause
- **Fixed height:** `height: "250px"` forces a specific container height
- **`objectFit: "cover"`** stretches image to fill container while maintaining aspect ratio — crops left/right edges to avoid empty space
- The source images contain embedded text on the **left side** (e.g., "DEPOSITORY PARTICIPANT (DP) SERVICE") which gets cut off

### Why `cover` Crops Left Side
`object-fit: cover` centers the image by default (`object-position: 50% 50%`). When the container aspect ratio differs from the image aspect ratio, it crops **equally from both sides**. The visual evidence shows only the left text is cut off, suggesting the images may have more content on the left, or the container is wider than the image's natural aspect ratio would suggest.

## Implementation Plan

### 1. Change `object-fit` to `contain`
**File:** `nls_frontend/src/pages/Service.jsx` (line 105)

```jsx
// Before
objectFit: "cover"

// After  
objectFit: "contain"
```

This displays the **entire** image proportionally within the 250px height container.

### 2. Add `object-position: center` (explicit)
```jsx
objectFit: "contain",
objectPosition: "center center"
```

### 3. Handle Letterboxing (empty space from `contain`)
When `contain` leaves empty space (letterboxing/pillarboxing), the dark theme background will show. This is acceptable per the spec. Optionally add a background to the image wrapper:

```jsx
<div className="service-img position-relative mb-3" style={{ background: 'var(--color-surface)', borderRadius: '8px' }}>
```

### 4. Preserve Card Consistency
- Keep `height: "250px"` for consistent card alignment
- Keep `borderRadius: "8px"` on the image (or move to wrapper)
- Keep existing layout: 2-column grid, titles, descriptions

## Files to Modify
| File | Change |
|------|--------|
| `nls_frontend/src/pages/Service.jsx` | Lines 104-107: Change `objectFit: "cover"` to `objectFit: "contain"`, add `objectPosition: "center center"`; optionally add background to wrapper |

## Validation Checklist
- [ ] All 4 service cards show complete embedded text:
  - Depository: "DEPOSITORY PARTICIPANT (DP) SERVICE" fully visible
  - Margin: "MARGIN SERVICE" fully visible  
  - Brokerage: "BROKERAGE SERVICE" fully visible
  - Advisory: "ADVISORY SERVICE" fully visible
- [ ] NLI Securities branding visible
- [ ] Right-side financial illustrations visible
- [ ] No image stretching/distortion
- [ ] Cards remain aligned in 2-column grid
- [ ] Responsive: works on desktop, tablet, mobile
- [ ] `npm run build` passes

## Risk Assessment
- **Low risk** — Single inline style change
- **Scope limited** — Only affects Service page card images
- **No layout restructuring** — Container dimensions unchanged
- **No backend changes**