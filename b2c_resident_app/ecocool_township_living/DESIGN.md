---
name: EcoCool Township Living
colors:
  surface: '#f7f9fb'
  surface-dim: '#d8dadc'
  surface-bright: '#f7f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#eceef0'
  surface-container-high: '#e6e8ea'
  surface-container-highest: '#e0e3e5'
  on-surface: '#191c1e'
  on-surface-variant: '#5a413a'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f3'
  outline: '#8e7068'
  outline-variant: '#e2bfb5'
  surface-tint: '#af3100'
  primary: '#aa2f00'
  on-primary: '#ffffff'
  primary-container: '#d14311'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb59f'
  secondary: '#5c5f62'
  on-secondary: '#ffffff'
  secondary-container: '#dee0e3'
  on-secondary-container: '#606366'
  tertiary: '#006947'
  on-tertiary: '#ffffff'
  tertiary-container: '#00855b'
  on-tertiary-container: '#f5fff6'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdbd1'
  primary-fixed-dim: '#ffb59f'
  on-primary-fixed: '#3a0a00'
  on-primary-fixed-variant: '#852300'
  secondary-fixed: '#e1e2e6'
  secondary-fixed-dim: '#c5c6ca'
  on-secondary-fixed: '#191c1f'
  on-secondary-fixed-variant: '#44474a'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#f7f9fb'
  on-background: '#191c1e'
  surface-variant: '#e0e3e5'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '800'
    lineHeight: 40px
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 20px
    fontWeight: '700'
    lineHeight: 28px
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 13px
    fontWeight: '700'
    lineHeight: 18px
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 16px
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 10px
    fontWeight: '600'
    lineHeight: 14px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 0.75rem
  margin: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.25rem
  space-xl: 1.75rem
---

## Brand & Style

This design system establishes a high-tier Malaysian township lifestyle and climate-resilience mobile experience. Designed for contemporary township residents and property owners, the interface balances warm hospitality with proactive, sustainable microclimate intelligence.

The visual style merges modern tropical minimalism with responsive environmental telemetry:
- **Atmospheric Warmth:** Drawing inspiration from rich Malaysian sunsets and brand heritage, large-format fluid gradients (#E04E1D transitioning to #C43516) frame key marketing states, onboarding flows, and township headers.
- **Pristine Utility Surfaces:** Content resides primarily on pure white and ivory-tinted card decks layered above ambient backgrounds, providing immediate clarity, reading comfort, and high scannability in harsh tropical sunlight.
- **Eco-Resilience HUD:** Functional environmental telemetry elements (such as shaded corridor pathfinders, tree canopy indexes, and ambient heat warnings) introduce balanced emerald greens and diagnostic alerts without breaking the clean hospitality feel.
- **Confidence & Precision:** Visual cues convey reliability, safety, and effortless access to residential services, community access passkeys, facilities booking, and climate-safe outdoor activities.

## Colors

The palette balances energetic brand warmth, structural charcoal discipline, and ecological intelligence tokens.

### Core Roles
- **Primary Tone (`#E04E1D` / `#EB5A28` / `#C43516`):** The signature warm sunset spectrum. Used for primary CTAs, active segmented tabs, highlight badges, and vibrant backdrop mesh gradients.
- **Secondary Tone (`#1E2124`):** Deep charcoal used for top navigation bars, structural headers, high-emphasis text, and dark utility states. It grounds the warm vibrancy with executive solidity.
- **Tertiary Environmental Tone (`#10B981` / `#059669`):** EcoCool signals designating optimal comfort conditions, lush canopy trails, EV charging status, and sustainable community milestones.
- **Neutral Foundation (`#FFFFFF` to `#F8FAFC`):** Clinical white container cards and subtle off-white backgrounds ensuring high contrast in direct sunlight.

### Climate & Telemetry Accents
- **Heat Alert Amber (`#F59E0B`):** Warns of rising UV index and afternoon peak thermal zones.
- **Extreme Thermal Red (`#EF4444`):** Highlights unsafe outdoor microclimates, high thermal index hours, and critical maintenance alerts.
- **Shaded Canopy Emerald (`#10B981`):** Indicates low-temperature jogging loops, shaded walkability corridors, and green communal spaces.

## Typography

The typography system relies exclusively on **Plus Jakarta Sans** to establish a contemporary, highly legible, and approachable brand personality.

- **Display & Headlines:** Set in bold and extrabold weights. Used for welcoming splash messages, dynamic weather readings, property titles, and section dividers.
- **Body:** Engineered for concise residential logs, billing information, and community announcements. Keep weights regular (400) with generous line heights to preserve clarity on mobile viewports under variable lighting.
- **Labels & Microcopy:** Used for circular quick-access links, EcoCool metrics (e.g., "31°C Feels like 28°C"), and status tags. Heavy use of uppercase or semi-bold weights for rapid scanning.

## Layout & Spacing

The layout is built for native mobile ergonomics with strict one-handed interaction zones:
- **Canvas Margins:** Fixed at 16px (`1rem`) on standard mobile devices, expanding to 24px (`1.5rem`) on larger foldable screens and tablets.
- **Column Structure:** A 4-column fluid mobile grid accommodating horizontal card carousels (e.g., property project cards, community alerts) with 12px (`0.75rem`) inner gutters.
- **Vertical Hierarchy:** Sections use `space-xl` (28px) separations to delineate between high-priority township telemetry, property quick-action menus, and community feeds.
- **Adaptive Floating Surfaces:** Main content panels slide up over the ambient gradient backdrop, leaving 56px–80px of exposed gradient area at the screen crown for time, location, and weather summaries.

## Elevation & Depth

Visual depth is achieved through clean, white structural cards elevated above dynamic warm background canvases:

- **Base Ambient Canvas:** Full-bleed warm diagonal linear gradients (`linear-gradient(145deg, #EB5A28 0%, #C43516 100%)`) forming the foundation of top navigation headers and marketing splash surfaces.
- **Card Surface Level 1 (Default Cards):** Pure `#FFFFFF` fill with an ultra-soft ambient shadow: `box-shadow: 0 4px 16px -2px rgba(30, 33, 36, 0.06), 0 2px 6px -1px rgba(30, 33, 36, 0.04)`.
- **Card Surface Level 2 (Floating Popovers & Climate HUD):** `#FFFFFF` fill with a subtle warm-tinted shadow: `box-shadow: 0 10px 25px -4px rgba(224, 78, 29, 0.12), 0 4px 10px -2px rgba(30, 33, 36, 0.05)`.
- **Divider Outlines:** 1px hairline borders using `#F1F5F9` to subtly define data tables and filter lists without adding heavy visual friction.

## Shapes

The design adopts a refined, friendly geometry balanced by roundedness scale `2`:
- **Card Surfaces & Modals:** Standardized with `16px` (`rounded-lg`) to `24px` (`rounded-xl`) corner radiuses, softening the physical envelope and matching modern flagship mobile hardware edges.
- **Quick Action Icon Pods:** Outer bounding surfaces use soft circles or rounded squircles (12px radius) to frame red-tinted micro-illustrations.
- **Interactive Buttons & Badges:** Primary interactive buttons employ `12px` roundedness or full capsule pill shapes (`9999px`) for contextual metric tags, notification counts, and pagination indicators.

## Components

### Buttons & Call-to-Actions
- **Primary Button:** High-visibility `#E04E1D` background with crisp `#FFFFFF` typography, 48px height for touch compliance, bold weight, and a subtle active compression animation.
- **Secondary / Ghost Button:** Transparent background with a 1.5px `#E04E1D` border and matching text color, or soft tinted `#FFF3ED` fills for non-intrusive in-card actions.
- **Pagination Buttons:** Minimal numeric blocks with the active item highlighted in solid `#C43516` and white text, flanked by subtle text arrows.

### Quick Access Grid Pods
- Circular or squircle `#FFF3ED` container tiles holding mono-weight red/orange property icons (My Property, News, Events, EcoCool Tracker).
- Paired with strict 11px semi-bold centered labels underneath.

### EcoCool Climate HUD & Badges
- **Comfort Meter:** Pill badge displaying ambient heat levels and shaded route recommendations. 
  - *Cool / Shaded:* Emerald fill `#ECFDF5`, text `#059669`.
  - *Cautionary:* Warm amber fill `#FEF3C7`, text `#D97706`.
  - *Extreme Alert:* Crimson red fill `#FEF2F2`, text `#DC2626`.
- Integrated micro-icons indicate real-time tree canopy coverage and solar UV indices.

### Navigation Headers
- Deep charcoal `#1E2124` top bars with white typography, back chevrons, and rounded notification counters (pill shaped with deep orange/red accents).

### Property Showcase Cards
- Rounded white cards housing 16:10 ratio architectural photography, featuring subtle tag pills for tenure ("Freehold", "New Launch") and bedroom/bathroom metric summaries paired with clean gray iconography.