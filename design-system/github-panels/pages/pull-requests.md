# Pull Requests Page Overrides

> **PROJECT:** GitHub Panels
> **Generated:** 2026-10-30 23:14:08
> **Page Type:** Code Review & Merge Operations

> ⚠️ **IMPORTANT:** Rules in this file **override** the Master file (`design-system/MASTER.md`).
> Only deviations from the Master are documented here. For all other rules, refer to the Master.

---

## Layout Overrides

- **Max Width:** 1200px (full-width table at ≥768px)
- **Layout:** Sticky filter bar → PR list → merge options modal (on select)
- **Grid:** Single-column list <768px; full-width table ≥768px
- **Sticky Elements:** Filter/sort bar sticks to top; merge action bar appears when items selected

---

## Color Overrides

| Role | Hex | Usage |
|------|-----|-------|
| Open PR badge bg | `#0D419D` (blue-900) | Open status |
| Open PR badge text | `#6CB4EE` (blue-400) | Open status text |
| Merged PR badge bg | `#5B21B6` (purple-900) | Merged status |
| Merged PR badge text | `#A78BFA` (purple-400) | Merged status text |
| Closed PR (unmerged) badge bg | `#374151` (gray-700) | Closed status |
| Closed PR badge text | `#9CA3AF` (gray-400) | Closed status text |
| CI passing | `#22C55E` (green-500) | All checks pass |
| CI failing | `#EF4444` (red-500) | Check failed |
| CI pending | `#F59E0B` (amber-500) | Checks running |
| Conflicted bg | `#7C2D12` (orange-900) | Merge conflict |
| Conflicted text | `#FDBA74` (orange-300) | Conflict label |
| Selected row bg | `rgba(167,139,250,0.08)` | Multi-select highlight |

---

## Component Specs

### 1. PR Card / Table Row

**Structure:**
```
[Checkbox] [Status Badge] [CI Status Icon] [Branch: title] [Base branch] [Diff stats] [Review status] [Assignee avatars] [Meta]
```

**Specs:**
- **Height:** 64px per row (compact), 80px+ with diff preview expanded
- **Title column:** Branch name in JetBrains Mono (`feature/auth-flow`), PR title below in IBM Plex Sans body weight 400
- **Status badge:** Pill shape, color-coded by state (open/merged/closed)
- **CI status icon:** Right-aligned before meta — ● green (passing), ● red (failing), ● amber (pending), ○ gray (not run)
- **Diff stats:** `+142 -23` in monospace, green for additions, red for deletions
- **Review status:** "✓ Approved", "⏳ Changes requested", "💬 Commented" — shown as small badge next to CI icon
- **Base branch:** Shown in muted text (`main ← feature/auth-flow`)
- **Assignee avatars:** Circle, 24px, max 3 inline + "+N"
- **Meta column (right-aligned):** Time since last activity, comment count

**Accessibility:**
- Each row focusable with `tabindex="0"`
- CI status announced: "All checks passing" or "2 of 5 checks failed"
- Review status announced contextually: "Approved by alice, changes requested by bob"

### 2. Diff Preview (Expandable)

**Triggers on row click or expand button.**

**Structure:**
```
[File path] [± stats] [3-line diff snippet]
[File path] [± stats] [3-line diff snippet]
...
```

**Specs:**
- **Background:** `--color-muted` (`#272F42`) for the preview panel
- **File paths:** JetBrains Mono, 12px, `--color-muted-foreground`
- **Line numbers:** Right-aligned, muted, monospace
- **Additions:** Green text (`#22C55E`), subtle green background on line (`rgba(34,197,94,0.06)`)
- **Deletions:** Red text (`#EF4444`), subtle red background (`rgba(239,68,68,0.06)`)
- **Context lines:** `--color-muted-foreground`, no background
- **Max 5 files shown** in compact preview; "View all N changes" link below

**Rules:**
- Diff preview collapses to file list on <768px
- Line wrapping enabled for narrow viewports
- Syntax highlighting applied where possible (at minimum: strings, keywords, comments distinguished)

### 3. Review Status Badge

```css
.review-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 500;
}

.review-approved {
  background: rgba(34,197,94,0.15);
  color: #4ADE80;
}

.review-changes {
  background: rgba(245,158,11,0.15);
  color: #FBBF24;
}

.review-commented {
  background: rgba(96,165,250,0.15);
  color: #93C5FD;
}
```

### 4. CI Status Indicator

```css
.ci-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
}

.ci-passing { color: #22C55E; }
.ci-failing { color: #EF4444; }
.ci-pending { color: #F59E0B; }
```

**Rules:**
- Pending CI shows animated pulse (subtle, respects `prefers-reduced-motion`)
- Failing CI is clickable → opens check details panel
- Passing CI does not animate — static dot only

### 5. Merge Options Modal / Inline Bar

**Triggers when PR is mergeable and user has permissions.**

**Structure:**
```
[Merge pull request] ▼ (dropdown arrow)
├─ Merge commit
├─ Squash and merge
└─ Rebase and merge
[Delete branch] [Close PR]
```

**Specs:**
- **Primary button:** `--color-accent` (`#A16207`) background, white text
- **Dropdown:** Shows merge strategy options with descriptions
- **Secondary actions:** Outlined buttons in muted colors
- **Delete branch:** Destructive style (red outline)

**Accessibility:**
- Merge button has `aria-label="Merge pull request #1234: title"`
- Dropdown options have descriptive labels
- Keyboard: Enter to merge, Escape to close dropdown

---

## Page-Specific UX Guidelines

| Guideline | Do | Don't |
|-----------|----|-------|
| **CI Feedback** | Show loading → success/error state after merge action click | Button click with no response |
| **Contextual Badges** | `<span role="status" aria-atomic="true">2 of 5 checks failed</span>` | Bare numbers without context |
| **Diff Readability** | Color additions green, deletions red; line numbers right-aligned | Monochrome diffs without clear add/remove distinction |
| **Review State** | Show reviewer names + status inline | Hide review state until clicked |
| **Merge Strategy** | Present all 3 strategies with brief explanation | Default to merge commit without showing options |

---

## GSAP Motion (Standard)

```js
// PR list stagger animation
gsap.from('.pr-row', {
  opacity: 0,
  y: 12,
  duration: 0.35,
  stagger: { each: 0.04, from: 'start' },
  ease: 'power2.out'
});

// CI pending pulse (subtle)
gsap.to('.ci-pending', {
  opacity: 0.4,
  duration: 0.8,
  repeat: -1,
  yoyo: true,
  ease: 'sine.inOut',
  paused: true // only when checks are running
});
```

---

## Anti-Patterns to Avoid

- Pull-to-refresh enabled where not needed (disable on desktop table view)
- CI status shown without clickable detail for failures
- Diff preview that doesn't wrap on mobile — causes horizontal scroll
- Merge button that changes state silently after click
- Review badges that use color alone (always include icon + text)
