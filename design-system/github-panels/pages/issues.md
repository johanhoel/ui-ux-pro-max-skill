# Issues Page Overrides

> **PROJECT:** GitHub Panels
> **Generated:** 2026-10-30 23:14:02
> **Page Type:** Real-Time Operations Landing (Issues List)

> ⚠️ **IMPORTANT:** Rules in this file **override** the Master file (`design-system/MASTER.md`).
> Only deviations from the Master are documented here. For all other rules, refer to the Master.

---

## Layout Overrides

- **Max Width:** 1200px (full-width table mode at ≥1024px)
- **Layout:** Sticky filter bar → sortable issue list → bulk action toolbar (appears on selection)
- **Grid:** Single-column list at <768px; full-width table at ≥768px
- **Sticky Elements:** Filter/sort bar sticks to top on scroll; bulk action bar slides up from bottom when items selected

---

## Color Overrides

| Role | Hex | Usage |
|------|-----|-------|
| Open issue badge bg | `#0D419D` (blue-900) | Open status |
| Open issue badge text | `#6CB4EE` (blue-400) | Open status text |
| Closed issue badge bg | `#1A3A2D` (green-950) | Closed status |
| Closed issue badge text | `#4ADE80` (green-400) | Closed status text |
| Priority high | `#DC2626` (red-500) | Critical/high priority |
| Priority medium | `#F59E0B` (amber-500) | Medium priority |
| Priority low | `#6B7280` (gray-500) | Low priority |
| Selected row bg | `rgba(34,197,94,0.08)` | Multi-select highlight |

---

## Component Specs

### 1. Issue Card / Table Row

**Structure:**
```
[Checkbox] [Status Badge] [Priority Icon] [Title/Description] [Labels] [Assignee Avatars] [Meta: time, comments]
```

**Specs:**
- **Height:** 56px per row (compact), 72px (expanded detail)
- **Min-width for title column:** 300px on desktop, full-width on mobile
- **Status badge:** Pill shape, `border-radius: 9999px`, padding `4px 10px`, font-size `12px`, font-weight `600`
- **Priority indicator:** Left-aligned icon (▲ high, ◆ medium, ● low) — color-coded as above
- **Labels:** Max 3 visible per row; overflow shows "+N" chip operable to expand
- **Assignee avatars:** Circle, 24px diameter, max 3 shown inline; overflow shows "+N"
- **Meta column (right-aligned):** Relative time (`2h ago`), comment count icon + number

**Accessibility:**
- Each row is focusable with `tabindex="0"`
- Status badges use `<span role="status">` with contextual text: "Open, 3 items"
- Checkbox has explicit aria-label: "Select issue #1234: title"

### 2. Filter / Sort Bar (Sticky)

**Structure:**
```
[Search input] [Filter dropdowns: Status, Assignee, Label, Priority] [Sort dropdown] [Clear all]
```

**Specs:**
- **Height:** 48px compact, expands to 96px with filter panels open
- **Background:** `--color-card` (`#0E1223`) with bottom border `1px solid --color-border`
- **Search input:** Full-width on mobile; constrained to 40% width on desktop (rest for filters)
- **Filter pills:** Show active filters as removable chips below the bar
- **Sort dropdown:** Options — Last updated, Created, Comments, Priority (custom)

**Accessibility:**
- Search has `aria-label="Search issues"`
- Each filter group has a visible label
- Active filter count announced: "3 filters active"

### 3. Bulk Action Toolbar (Slide-up)

**Triggers when ≥1 issue selected.**

**Structure:**
```
[X items selected] [Change status ▼] [Assign to... ▼] [Label ▼] [Delete] [Cancel]
```

**Specs:**
- **Position:** Fixed bottom-center, slides up with `transform: translateY(100%) → translateY(0)` transition (200ms ease)
- **Background:** `--color-primary` (`#0F172A`) with top border `1px solid --color-border`
- **Padding:** `12px 24px`
- **Shadow:** `--shadow-lg` for elevation
- **Items selected count:** Bold, white text on left
- **Actions:** Secondary buttons (outlined) except Delete (destructive, red)

**Accessibility:**
- Announced via `aria-live="polite"`: "3 issues selected. Bulk actions available."
- Focus moves to toolbar when it appears; Escape dismisses selection

### 4. Status Badge Component

```css
.badge-status {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 600;
  line-height: 1;
}

.badge-open {
  background: #0D419D;
  color: #6CB4EE;
}

.badge-closed {
  background: #1A3A2D;
  color: #4ADE80;
}
```

### 5. Label Chip Component

```css
.label-chip {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 500;
  line-height: 1.4;
  white-space: nowrap;
  min-width: 0; /* allows shrink */
}
```

**Rules:**
- Labels are bounded by unpredictable values (the color); the text label uses `nowrap` with overflow disclosure
- Full label text exposed via operable disclosure (click to expand), not hover-only tooltip
- Minimum contrast: 4.5:1 between label text and label background

---

## Page-Specific UX Guidelines

| Guideline | Do | Don't |
|-----------|----|-------|
| **Bulk Actions** | Checkbox column + slide-up action bar | Repeated actions per row |
| **Badge Updates** | `<span role="status" aria-atomic="true">3 items in cart</span>` | Bare number announcements |
| **Label Overflow** | Flexible label with `min-width: 0` + operable disclosure | Fixed-width badge wraps or clips with title-only tooltip |
| **Empty State** | Illustration + "No issues match your filters" + Clear filters button | Blank white space |
| **Loading** | Skeleton rows matching card structure | Spinner in corner while content shifts |

---

## GSAP Motion (Standard)

```js
// Filter bar slide-in on page load
gsap.from('.filter-bar', {
  y: -20,
  opacity: 0,
  duration: 0.3,
  ease: 'power2.out'
});

// Bulk toolbar slide-up
gsap.to('.bulk-toolbar', {
  y: 0,
  duration: 0.2,
  ease: 'power2.out',
  paused: true // controlled by selection state
});
```

---

## Anti-Patterns to Avoid

- Single row actions only (use bulk toolbar)
- Force all chips into one clipped row without overflow disclosure
- Silent success — always show brief confirmation toast after bulk action
- Status badges that change color without announcing the change to screen readers
- Filter bar that collapses on mobile without a "Show filters" toggle
