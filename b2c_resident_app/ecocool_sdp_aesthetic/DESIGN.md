---
name: EcoCool SDP Aesthetic
colors:
  surface: '#f4fbf3'
  surface-dim: '#d5dcd4'
  surface-bright: '#f4fbf3'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eef6ee'
  surface-container: '#e9f0e8'
  surface-container-high: '#e3eae2'
  surface-container-highest: '#dde4dd'
  on-surface: '#161d19'
  on-surface-variant: '#434842'
  inverse-surface: '#2b322d'
  inverse-on-surface: '#ebf3eb'
  outline: '#737872'
  outline-variant: '#c3c8c0'
  surface-tint: '#4e6451'
  primary: '#4e6350'
  on-primary: '#ffffff'
  primary-container: '#667c68'
  on-primary-container: '#ffffff'
  inverse-primary: '#b5cdb6'
  secondary: '#54634d'
  on-secondary: '#ffffff'
  secondary-container: '#d7e8cd'
  on-secondary-container: '#5a6953'
  tertiary: '#436800'
  on-tertiary: '#ffffff'
  tertiary-container: '#558300'
  on-tertiary-container: '#ffffff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d1e9d1'
  primary-fixed-dim: '#b5cdb6'
  on-primary-fixed: '#0c2011'
  on-primary-fixed-variant: '#374c3a'
  secondary-fixed: '#d7e8cd'
  secondary-fixed-dim: '#bbcbb2'
  on-secondary-fixed: '#121f0e'
  on-secondary-fixed-variant: '#3d4b37'
  tertiary-fixed: '#aff743'
  tertiary-fixed-dim: '#94da23'
  on-tertiary-fixed: '#111f00'
  on-tertiary-fixed-variant: '#314f00'
  background: '#f4fbf3'
  on-background: '#161d19'
  surface-variant: '#dde4dd'
typography:
  display-hero:
    fontFamily: Plus Jakarta Sans
    fontSize: 56px
    fontWeight: '800'
    lineHeight: 64px
    letterSpacing: -0.03em
  display-hero-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 40px
    fontWeight: '800'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-metric:
    fontFamily: Space Grotesk
    fontSize: 44px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.04em
  headline-metric-mobile:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.03em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: 0em
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: 0em
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-data:
    fontFamily: Space Grotesk
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.08em
  label-ui:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.25rem
  margin: 1.5rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.25rem
---

## Brand & Style

This design system blends the calming, restorative aura of high-end wellness interfaces with the crisp precision of sports telemetry platforms. Rooted in nature-inspired minimalism, it balances grounded organic tones with luminous, high-energy accents to make sustainable cooling, environmental telemetry, and personal wellness feel aspirational, effortless, and technologically advanced.

The visual tone is tranquil yet precise, human yet engineered. It strips away technical clutter in favor of spacious, airy layouts, rhythmic data presentation, and rich tactile cards. The interface avoids cold industrial tropes, instead welcoming users into an atmosphere of fresh air, mindful efficiency, and high-performance lifestyle monitoring.

## Colors

The palette establishes an organic sanctuary contrasted against precise, high-visibility telemetry cues.

- **Primary (`#667C68` - Sage Green):** The anchor of the brand. Represents natural equilibrium, restorative shade, and mindful cooling. Used for primary controls, structural branding, selected states, and core metric highlights.
- **Secondary (`#A9B9A0` - Muted Green):** Soft ambient tint used for supportive chips, muted charts, progress track backgrounds, and gentle dividing accents.
- **Tertiary / Accent (`#B6FF4A` - Electric Lime):** High-velocity telemetry beacon inspired by performance tracking. Used sparingly for active status indicators, peak eco-efficiency readouts, live sensor beacons, and high-impact calls to action.
- **Neutral / Text (`#252C27` - Deep Charcoal):** Grounded, low-glare organic black for sharp typography, deep-contrast readouts, and high-legibility interface controls.
- **Surface Foundations:**
  - Base canvas: `#F7F5EF` (Warm Ivory) providing a soft, paper-like warmth that prevents screen fatigue.
  - Secondary surface / Container: `#E7D9C9` (Soft Nude) delivering subtle structural warmth for nested cards, controls, and segregated telemetry bays.
- **State Signals:**
  - Warning: `#EAB308` (Amber) for thermal thresholds and filter maintenance reminders.
  - Hazard: `#EF4444` (Coral Red) for critical flow, heat hazard, or system disconnect.

## Typography

The type system blends friendly, human-centric geometry with the technical discipline of real-time diagnostics.

- **Primary & Interface (Plus Jakarta Sans):** Delivers clean curves, open counters, and high approachability. Used across titles, running narrative copy, buttons, and user interaction cues.
- **Telemetry & Metrics (Space Grotesk):** Deployed for prominent numerical statistics, telemetry gauges, time stamps, and data labels. Its structured, monospaced-leaning architecture gives sensors and temperatures a crisp, analytical character.
- **Metric Formatting:** Telemetry metrics always render numbers in heavy weights (`700` or `800`) paired with secondary unit indicators (e.g., `°C`, `RPM`, `kW/h`) styled down at `0.5x` font size and set to label weight to maintain clear optical hierarchy.

## Layout & Spacing

The layout language uses a responsive fluid grid structure driven by generous negative space to evoke breathability and clean airflow.

- **Mobile (< 768px):** 4-column layout with `1rem` outer canvas padding and `0.75rem` gutters. Metric modules stack into vertical cards or twin-column modular tiles.
- **Tablet (768px – 1024px):** 8-column system with `1.5rem` margins and `1rem` gutters. Telemetry shifts into side-by-side comparative widgets.
- **Desktop (> 1024px):** 12-column layout capped at a maximum width of `1320px`, with `2rem` margins and `1.25rem` gutters. Ample room is dedicated to circular dials, multi-stream trend graphs, and control decks.
- **Rhythm & Whitespace:** Elements prioritize vertical breathing room. Related inputs and small telemetry pairings use `space-sm` (`8px`) or `space-md` (`16px`), while major card interiors and container groupings consistently enforce `space-lg` (`24px`) to `space-xl` (`36px`) separation.

## Elevation & Depth

Depth is established through soft tonal tiers and luminous physical presence rather than harsh drop shadows.

- **Tonal Layering:** The primary mechanism for elevation. The base application sits on Warm Ivory (`#F7F5EF`). Elevated surfaces layer Soft Nude (`#E7D9C9`) or pristine white cards with subtle opacity (`rgba(255, 255, 255, 0.7)`).
- **Subtle Organic Borders:** Low-contrast outlines using Sage or Muted Green at 10–18% opacity (`rgba(102, 124, 104, 0.12)`) frame every elevated card, preventing visual bleed while avoiding stiff container boxes.
- **Ambient Shadow System:** When cards or floating action bars require true elevation, they cast a broad, highly diffused, tinted ambient shadow: `0px 12px 32px -4px rgba(37, 44, 39, 0.05)`.
- **Active Telemetry Glow:** Active states or pulse beacons leverage an Electric Lime glow (`0 0 20px rgba(182, 255, 74, 0.45)`) to convey live activity, energy generation, and operational health.

## Shapes

The shape system emphasizes ergonomic softness, drawing inspiration from smooth river stones and tactile consumer electronics.

- **Standard Cards & Modals:** Built with `rounded-2xl` (`1rem` to `1.5rem`), lending structural warmth to data modules and telemetry panels.
- **Interactive Controls & Buttons:** Use full pill shapes (`rounded-full`) for high-touch triggers, quick filters, and status tags to enhance tap-target comfort.
- **Inner Containers & Secondary Wells:** Internal modules (such as sub-stat panels within larger cards) use `rounded-xl` (`0.75rem`) to ensure concentric corner curves that harmonize with parent frames.

## Components

### Buttons
- **Primary:** Pill-shaped, Deep Charcoal (`#252C27`) background with Warm Ivory (`#F7F5EF`) text. On hover, smooth transition to Sage Green (`#667C68`).
- **Telemetry Action (Hero):** Electric Lime (`#B6FF4A`) with Deep Charcoal typography; applied to high-priority actions like "Activate Eco Mode" or "Sync Device."
- **Secondary / Ghost:** Transparent surface enclosed by a `1.5px` border in `#667C68` at 25% opacity; Deep Charcoal text; fills with Soft Nude (`#E7D9C9`) on hover.

### Telemetry Cards & Metric Panels
- Base card surface: Pure white with 85% opacity or Soft Nude (`#E7D9C9`), bordered by `1px` solid `rgba(102, 124, 104, 0.14)`.
- Large metric figures rendered in Space Grotesk Bold, anchored by micro uppercase metadata labels at the top-left and real-time status pills at the top-right.

### Status Chips & Badges
- Pill-shaped (`rounded-full`), padded with `0.25rem` vertical and `0.75rem` horizontal spacing.
- Styled with subtle tint backgrounds (`rgba(102, 124, 104, 0.12)`) and Sage Green text. Live modes include an inset `6px` pulsing Electric Lime beacon dot.

### Form Inputs & Sliders
- **Text Inputs:** Soft Nude background (`#E7D9C9`), rounded-xl corners, recessed borders that focus-shift to Sage Green with a soft `2px` focus ring.
- **Sensory Sliders / Airflow Dials:** Thick pill tracks with Muted Green bases and deep Sage handles, providing tactile feedback points and continuous numeric readout badges overhead.

### Selection Controls (Checkboxes & Radios)
- Rounded-md for checkboxes; circular for radios. Unchecked states carry a gentle `1.5px` Sage outline; checked states fill with Sage Green and display a crisp Ivory check or inner dot.

### Specialized Lifestyle Telemetry Widgets
- **Ring Gauges (Apple Fitness / Strava Style):** Concentric circular progress tracks with rounded stroke ends; background tracks rendered in `#E7D9C9`, primary progress in `#667C68`, and peak efficiency arcs in vivid `#B6FF4A`.
- **Sparklines & Area Streams:** Gradient-filled area charts fading from Electric Lime/Sage into transparent Ivory bases, showcasing thermal history and fan energy conservation over time.