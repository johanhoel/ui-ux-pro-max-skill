# UI/UX Pro Max v2.0

Complete design system generator with BM25 search, WCAG validation, visual mockups, and cross-domain intelligence.

## What's New in v2.0

### 🎯 Phase 1: Data Foundation (Completed)

| Improvement | Details |
|-------------|---------|
| **Status Column** | All 88 styles now have Status (50 active, 9 deprecated, 29 supplemental) |
| **Stack Coverage** | Added SvelteKit, SolidJS, Qwik stacks (+3 new frameworks) |
| **Synonym Expansion** | 42 synonym groups for fuzzy query matching |
| **WCAG Contrast** | All 192 palettes validated for light/dark mode (≥4.5:1 ratio) |
| **Component Database** | 54 UI components with Do/Don't, code examples, WCAG refs |

### 🚀 Phase 2: Intelligence Layer (Completed)

| Improvement | Details |
|-------------|---------|
| **Product Types** | Expanded from 192 to 212 (+20 emerging domains: AI Agents, Spatial Computing, AR Shopping, Voice UI, Digital Health, Creator Economy, Autonomous Systems, Sustainable Energy, Web3/DeFi, AI Fitness, Smart City, AI Music, Gesture Control, AI Design Tools, Real-Time Collaboration, Legal Tech, Immersive Learning) |
| **Cross-Domain Search** | Auto-detects relevant domains from query keywords across 10 domains |
| **Query Expansion** | Synonym-based expansion improves recall without precision loss |

### 🎨 Phase 3: Visual Output (Completed)

| Improvement | Details |
|-------------|---------|
| **Color Swatches** | ASCII color palette display in MASTER.md output |
| **Page Wireframes** | Context-aware ASCII wireframes based on page pattern type |
| **Component Placement** | Layout guides showing where components go |
| **Page Override Mockups** | Dashboard, Pricing, Login, Checkout, Settings wireframes |

### 📦 Phase 4: Packaging (Completed)

| Improvement | Details |
|-------------|---------|
| **npm Package** | `@ui-ux-pro-max/design-system` with CLI wrapper |
| **CLI Tool** | `ui-ux-pro-max search`, `design-system`, `validate` commands |
| **Cross-Domain Flag** | `--cross-domain` searches all relevant domains simultaneously |

## Data Inventory

```
styles.csv          88 design styles (50 active, 9 deprecated, 29 supplemental)
colors.csv         192 color palettes (WCAG AA validated for light & dark mode)
products.csv       212 product types (+20 emerging domains added in v2.0)
components.csv      54 UI components with accessibility guidance
synonyms.csv        42 synonym groups for query expansion
charts.csv          25 chart type recommendations
ux-guidelines.csv  119 UX guidelines across all platforms
motion.csv          17 GSAP motion presets
icons.csv           105 curated icons + 1,512 upstream Phosphor icons
google-fonts.csv  1,934 Google Font pairings (74 curated)

stacks/             25 framework stacks with current version tracking
```

## Quick Start

### Search the Knowledge Base

```bash
# Basic search
python scripts/search.py "dark mode dashboard"

# With stack-specific guidelines
python scripts/search.py "dark mode dashboard" --stack react -n 5

# Cross-domain search (auto-detects relevant domains)
python scripts/search.py "modern saas landing page typography" --cross-domain

# JSON output for programmatic use
python scripts/search.py "e-commerce luxury" --json
```

### Generate a Design System

```bash
# Basic generation
python scripts/search.py "SaaS analytics platform" --design-system -p "MyApp"

# With persistence (saves to design-system/<project>/)
python scripts/search.py "SaaS analytics platform" --design-system -p "MyApp" --persist

# With page override
python scripts/search.py "e-commerce luxury" --design-system -p "Shop" --page checkout --persist

# With design dials (1-10 sliders)
python scripts/search.py "modern dashboard" --design-system \
  -p "Dashboard" \
  --variance 7 \
  --motion 5 \
  --density 6 \
  --persist
```

### Validate Data Files

```bash
python scripts/validate_data.py
```

## Design System Output Structure

When using `--persist`, the output follows a Master + Overrides pattern:

```
design-system/<project-slug>/
├── MASTER.md              # Global design rules (color palette, typography, spacing)
│                          # Includes visual mockups: color swatches, wireframes
└── pages/
    ├── dashboard.md       # Dashboard-specific overrides with layout wireframe
    ├── checkout.md        # Checkout page overrides
    └── settings.md        # Settings page overrides
```

### MASTER.md Contents

1. **Logic Header** - Override instructions
2. **Color Palette** - Semantic color tokens + CSS variables + ASCII swatches
3. **Typography** - Font pairings with Google Fonts URLs and CSS imports
4. **Spacing Variables** - Tokenized spacing scale (xs through 3xl)
5. **Shadow Depths** - Elevation system
6. **Component Specs** - Buttons, cards, inputs, modals with CSS
7. **Style Guidelines** - Style recommendations + ASCII wireframes
8. **Page Pattern** - Layout pattern with component placement guide
9. **Motion** (optional) - GSAP snippets when --motion dial is set
10. **Anti-Patterns** - What to avoid
11. **Pre-Delivery Checklist** - Accessibility and quality gates

## Cross-Domain Search

The `--cross-domain` flag searches across multiple domains simultaneously:

```bash
python scripts/search.py "modern saas landing page typography" --cross-domain
```

This auto-detects relevant domains from query keywords and returns aggregated results from:
- **style** - Design styles and aesthetics
- **color** - Color palettes and contrast ratios
- **product** - Product type recommendations
- **ux** - UX guidelines for accessibility and interaction
- **typography** - Font pairings and text styling
- **icons** - Icon recommendations
- **chart** - Data visualization guidance
- **landing** - Landing page patterns

## Stack Support (25 frameworks)

| Category | Stacks |
|----------|--------|
| **Web Frontend** | React, Next.js, Vue, Svelte, Astro, Angular, Nuxt.js, Nuxt UI, Qwik, SolidJS, SvelteKit |
| **CSS/UI Libraries** | HTML+Tailwind, shadcn/ui, UnoCSS |
| **Mobile** | React Native, Flutter, SwiftUI, Jetpack Compose |
| **Desktop** | WPF, WinUI, Avalonia, JavaFX, UWP |
| **3D/WebGL** | Three.js |

## WCAG Validation

All color palettes are validated against WCAG 2.0 AA requirements:
- **Light mode**: ≥4.5:1 contrast ratio for normal text
- **Dark mode**: ≥4.5:1 contrast ratio for normal text
- Palettes that fail either mode are flagged with `contrast_status`

## Product Type Coverage (212 types)

### Core Categories (existing 192)
SaaS, E-commerce, Dashboard, Portfolio, Blog, CMS, CRM, ERP, LMS, HRIS, Analytics, etc.

### New in v2.0 (+20 emerging domains)
| # | Product Type | Domain |
|---|-------------|--------|
| 193 | AI Agent Platform | AI/ML |
| 194 | AI Image Generator | AI/ML |
| 195 | AI Code Assistant | Developer Tools |
| 196 | Spatial Computing App | XR/MR |
| 197 | AR Shopping Experience | Commerce |
| 198 | Voice-First Interface | Voice UI |
| 199 | Multimodal AI Assistant | AI/ML |
| 200 | Digital Health Platform | Healthcare |
| 201 | Creator Economy Tool | Social/Monetization |
| 202 | Autonomous Systems Dashboard | IoT/Fleet |
| 203 | Sustainable Energy Platform | Green Tech |
| 204 | Web3 Wallet & DeFi Hub | Blockchain |
| 205 | AI-Powered Fitness App | Health/Wellness |
| 206 | Smart City Dashboard | Urban Tech |
| 207 | AI Music Platform | Creative Tools |
| 208 | Gesture-Controlled Interface | Interaction |
| 209 | AI-Powered Design Tool | Creative Tools |
| 210 | Real-Time Collaboration Platform | Productivity |
| 211 | AI-Powered Legal Tech Platform | Legal Tech |
| 212 | Immersive Learning Platform | EdTech |

## npm Package

```bash
npm install @ui-ux-pro-max/design-system
```

Or use directly:

```bash
npx @ui-ux-pro-max/design-system search "dark mode dashboard" --stack react -n 5
npx @ui-ux-pro-max/design-system design-system "SaaS platform" -p "MyApp" --persist
```

## References

- [pro-rules.md](references/pro-rules.md) - Native/mobile app UI rules
- [quick-reference.md](references/quick-reference.md) - Full rule set index (all 10 categories)
- [SKILL.md](SKILL.md) - Main skill definition file

## Version History

### v2.0 (2026-10-31)
- ✅ Added 20 new product types (AI Agents, Spatial Computing, Voice UI, etc.)
- ✅ Visual mockups: color swatches, ASCII wireframes, component placement guides
- ✅ Cross-domain search via `--cross-domain` CLI flag
- ✅ npm package with CLI wrapper (`ui-ux-pro-max`)
- ✅ Updated catalog-summary.json counts

### v1.2 (Previous)
- ✅ Fixed Status column in styles.csv
- ✅ Added SvelteKit, SolidJS, Qwik stack coverage
- ✅ Synonym expansion for fuzzy matching
- ✅ WCAG contrast validation for all palettes
- ✅ Component database with 54 UI components

---

Built with BM25 search, WCAG 2.0 AA compliance, and design system best practices.
