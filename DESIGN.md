---
name: CekBuah
description: A focused fruit-photo inspection experience in a luminous dark interface.
colors:
  ground: "#091326"
  frame-teal: "#086c87"
  frame-blue: "#121b45"
  frame-violet: "#24208d"
  surface: "#08090f"
  surface-raised: "#10111a"
  surface-quiet: "#0d0e15"
  ink: "#f6f4ff"
  ink-soft: "#cbc8da"
  muted: "#9693a8"
  primary: "#5754ee"
  primary-bright: "#7774ff"
  accent-soft: "#bebaff"
  line: "rgb(220 216 255 / 14%)"
  fresh-state: "#e2f8e8"
  rotten-state: "#ffe2dc"
typography:
  display:
    fontFamily: "DM Serif Display, Georgia, serif"
    fontSize: "clamp(3.3rem, 6.4vw, 5.45rem)"
    fontWeight: 400
    lineHeight: 0.98
    letterSpacing: "-0.022em"
  title:
    fontFamily: "DM Serif Display, Georgia, serif"
    fontSize: "clamp(2.3rem, 4vw, 3.55rem)"
    fontWeight: 400
    lineHeight: 1
    letterSpacing: "-0.02em"
  body:
    fontFamily: "Manrope Variable, Segoe UI, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Manrope Variable, Segoe UI, sans-serif"
    fontSize: "0.78rem"
    fontWeight: 700
    lineHeight: 1.4
rounded:
  control: "10px"
  content: "13px"
  card: "18px"
  panel: "22px"
  shell: "32px"
  pill: "999px"
spacing:
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  section: "32px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "12px 19px"
    height: "48px"
  button-secondary:
    backgroundColor: "rgb(11 11 16 / 38%)"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "11px 19px"
    height: "48px"
  navigation-pill:
    backgroundColor: "rgb(255 255 255 / 5%)"
    textColor: "{colors.ink-soft}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "5px"
  inspection-panel:
    backgroundColor: "linear-gradient(145deg, rgb(20 21 30 / 98%), rgb(12 13 19 / 98%))"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "clamp(19px, 2.6vw, 28px)"
  upload-target:
    backgroundColor: "#0c0d14"
    textColor: "{colors.ink}"
    rounded: "15px"
    padding: "24px 18px"
  processing-history:
    backgroundColor: "#0b0c13"
    textColor: "{colors.ink-soft}"
    rounded: "13px"
    padding: "14px 15px 8px"
  result-fresh:
    backgroundColor: "linear-gradient(130deg, rgb(30 77 58 / 38%), rgb(18 42 35 / 72%))"
    textColor: "{colors.fresh-state}"
    rounded: "{rounded.content}"
    padding: "16px"
  result-rotten:
    backgroundColor: "linear-gradient(130deg, rgb(102 39 40 / 34%), rgb(48 23 30 / 67%))"
    textColor: "{colors.rotten-state}"
    rounded: "{rounded.content}"
    padding: "16px"
---

# Design System: CekBuah

## Overview

**Creative North Star: “The Luminous Inspection Window”**

CekBuah places one clear fruit-inspection task inside a near-black, softly framed surface. A blue, teal, and violet field surrounds the application; a single CSS-drawn orbit gives the headline its luminous focus. The interface follows the user's supplied Clarid reference while replacing its finance claims with CekBuah's actual supported fruits and model details.

DM Serif Display gives the page a calm editorial voice. Manrope keeps the working copy, controls, upload guidance, processing history, and result states compact and readable. The page moves from introduction to upload, five actual backend/model steps, then the ResNet50 label. Segar and Busuk stay explicit in text and use distinct colors. The model result remains a visual estimate.

**Key Characteristics:**
- A near-black inset surface inside a teal-to-blue-to-violet outer field.
- One editorial headline and one geometric orbit lead into a practical upload flow.
- The proof strip uses only three supported fruits and real ResNet50 specifications.
- Result colors always accompany the words Segar or Busuk.

## Colors

The palette uses an almost-black working surface, a saturated violet action color, and a luminous outer frame that stays behind the application content.

### Primary
- **Signal Violet** (`{colors.primary}`): Main actions and the strongest interactive emphasis.
- **Bright Violet** (`{colors.primary-bright}`): Hover state for violet actions.
- **Soft Violet** (`{colors.accent-soft}`): Secondary emphasis, model stamps, and interface icons.

### Secondary
- **Market Teal** (`{colors.frame-teal}`): The left side of the ambient page frame.
- **Night Blue** (`{colors.frame-blue}`): The middle ground of the outer frame.
- **Orbit Violet** (`{colors.frame-violet}`): The right and lower edge of the outer frame.

### Tertiary
- **Fresh Result Ink** (`{colors.fresh-state}`): Text in the Segar result state.
- **Rotten Result Ink** (`{colors.rotten-state}`): Text in the Busuk result state.

### Neutral
- **Night Ground** (`{colors.ground}`): Base page color visible behind the gradient frame.
- **Black Glass** (`{colors.surface}`): Main inset application surface.
- **Raised Charcoal** (`{colors.surface-raised}`): Inspection panel and elevated working surfaces.
- **Quiet Charcoal** (`{colors.surface-quiet}`): Drop target and secondary working surface.
- **Ivory Ink** (`{colors.ink}`): Main text on dark surfaces.
- **Lavender Copy** (`{colors.ink-soft}`): Supporting text and descriptions.
- **Muted Lavender** (`{colors.muted}`): Lowest-priority helper text.
- **Moonlit Line** (`{colors.line}`): Quiet borders and dividers.

**The Truth-Only Proof Rule.** Use the supported fruit names and actual model specifications as proof. Do not add audience counts, partner claims, reliability claims, or an accuracy percentage to the interface.

**The Written Result Rule.** Segar and Busuk must remain visible words; color may reinforce a result but never replace its label.

## Typography

**Display Font:** DM Serif Display (with Georgia, serif fallbacks)
**Body Font:** Manrope Variable (with Segoe UI, sans-serif fallbacks)
**Label/Mono Font:** Manrope Variable; no separate monospace face is used.

**Character:** DM Serif Display supplies the high-contrast editorial headline from the reference. Manrope supports the compact Indonesian interface copy and keeps upload, status, and timing details easy to scan.

### Hierarchy
- **Display** (weight 400, responsive 3.3–5.45rem on desktop, line-height 0.98): Centered hero headline; it scales down separately on phones.
- **Title** (weight 400, responsive 2.3–3.55rem, line-height 1): Section headings.
- **Component title** (weight 700–780, about 0.86–1.19rem): Inspection, history, and result headings.
- **Body** (weight 400, 0.86–1.08rem, line-height 1.5–1.68): Supporting copy and explanations, kept to readable measures.
- **Label** (weight 600–750, about 0.68–0.94rem): Navigation, model stamp, result metadata, and processing status.

**The Two-Voice Rule.** Reserve the serif face for display and section titles. Keep controls, long copy, and status details in Manrope.

## Layout

The page uses a centered inset shell capped at 1320px, with a content column capped at 1100px. The top bar places the wordmark, a centered pill navigation, and a violet action on one row. The hero is centered over the orbit; supported fruits follow as a short proof strip, and the real specifications sit in a three-part capsule.

The inspection section uses two columns above 900px: product guidance on the left and the upload panel on the right. At 900px and below, those areas stack. At 620px and below, the navigation moves below the wordmark and action, the hero and specification capsule tighten, and the process rows stack vertically. The layout was inspected at 320px, 390px, 620px, 768px, 900px, 1024px, and 1440px without horizontal overflow.

## Elevation & Depth

Depth comes from nested charcoal surfaces, fine lavender-tinted borders, and a few soft shadows. The outer shell lifts from the ambient background; the upload panel sits above the main application surface; smaller shadows appear on the primary actions. The orbit's glow is part of the hero lighting, not a layer behind controls.

### Shadow Vocabulary
- **Outer frame** (`0 34px 100px rgb(0 0 0 / 34%)`): Separates the large inset page from the colored outer field.
- **Inspection panel** (`0 22px 60px rgb(0 0 0 / 29%)`): Lifts the upload task within the page.
- **Primary action** (`0 8px 22px rgb(75 69 224 / 20%)`): Adds restrained violet depth to the main action.

**The Border-and-Tone Rule.** Use a quiet border or a shadow to separate a surface. Do not stack both as competing elevation cues.

## Shapes

The app shell has generous rounded corners (32px on desktop, 23px on mobile). Working panels use medium corners (17–22px); controls use compact corners (9–11px); navigation and the specification capsule use pill shapes. The orbit is a large, abstract geometric ellipse. It stays behind the headline and does not imitate a fruit photograph.

## Components

### Buttons
- **Shape:** Compact rounded controls (10–11px radius).
- **Primary:** Signal Violet fill, ivory label, and a soft violet shadow; primary links and the submit action share this treatment.
- **Hover / Focus:** Hover lifts the control by one pixel and brightens it. Focus uses a clear lavender outline with a four-pixel offset.
- **Secondary:** Transparent dark fill with a restrained lavender-gray border.
- **Disabled / Loading:** Keep the primary action visible; reduce opacity while loading and show the spinner with “Sedang memeriksa”.

### Cards / Containers
- **Corner Style:** The application shell uses the largest radius; the inspection panel is smaller; nested result and history regions are compact.
- **Background:** Charcoal surfaces distinguish work areas from the near-black inset.
- **Shadow Strategy:** Use the inspection-panel shadow once; results and history rely mainly on tone and borders.
- **Border:** Thin lavender-gray lines define panel edges and quiet dividers.
- **Internal Padding:** 19–28px for the inspection panel, tightening at mobile widths.

### Inputs / Fields
- **Style:** A dark, dashed upload target with a centered image icon and plain format/size guidance.
- **Focus:** The upload target receives the shared visible focus outline.
- **Hover / Drag / Error:** Hover and drag highlight the dashed edge in violet. Errors use a dark red surface with a written recovery message.
- **Selected Photo:** Show a contained preview, file name, size, remove control, and replace action.

### Navigation
- **Style:** A centered translucent pill with compact Manrope links, between the wordmark and violet action.
- **Hover / Focus:** Links gain a brighter pill surface and visible keyboard outline.
- **Mobile:** The navigation moves to a centered row below the wordmark and primary action.

### Processing History
The panel lists the five backend events in their actual order: validation, preprocessing, model setup, inference, and label mapping. Each row pairs a step name with its live state and backend duration when available. The history is local to the current check and is not saved as an account history.

### Inspection Result
Segar and Busuk use distinct dark-tinted result surfaces. Each result includes a state icon, written label, recognized fruit when available, the backend reason, model version, and a control to try another photo.

## Do's and Don'ts

### Do:
- **Do** keep the first actions, supported fruit types, and ResNet50 purpose clear at a glance.
- **Do** use the orb as restrained geometric lighting behind the hero text.
- **Do** pair Segar and Busuk with their written labels and distinct state colors.
- **Do** preserve all five live processing steps and their backend timings.
- **Do** keep the outer teal-blue-violet field outside the near-black application surface.

### Don't:
- **Don't** add invented partner names, audience counts, uptime claims, or an accuracy percentage.
- **Don't** present a model result as a guarantee about the fruit's interior.
- **Don't** let decorative lighting reduce the contrast of the headline or upload controls.
- **Don't** hide an interactive state behind color alone.
