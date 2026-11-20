---
name: CekBuah
description: A market-inspired fruit photo inspection interface.
colors:
  forest-dark: "#10392f"
  forest: "#194d3f"
  citrus: "#f2c84b"
  ink: "#173b31"
  ink-soft: "#465c52"
  ground: "#f3f6ef"
  paper: "#ffffff"
  line: "#d4dfd4"
  tomato-pale: "#fff0ec"
  success-pale: "#e7f5e9"
typography:
  display:
    fontFamily: "Manrope Variable, Segoe UI, sans-serif"
    fontSize: "clamp(3.1rem, 5.6vw, 4.65rem)"
    fontWeight: 740
    lineHeight: 0.99
    letterSpacing: "-0.035em"
  body:
    fontFamily: "Manrope Variable, Segoe UI, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Manrope Variable, Segoe UI, sans-serif"
    fontSize: "0.9rem"
    fontWeight: 700
    letterSpacing: "0.01em"
rounded:
  small: "8px"
  button: "9px"
  medium: "12px"
  panel: "16px"
  pill: "999px"
spacing:
  small: "8px"
  medium: "16px"
  large: "24px"
  panel: "32px"
components:
  button-primary:
    backgroundColor: "{colors.forest-dark}"
    textColor: "{colors.paper}"
    rounded: "{rounded.button}"
    padding: "13px 18px"
    height: "52px"
  fruit-chip:
    backgroundColor: "#f9fbf7"
    textColor: "{colors.forest-dark}"
    rounded: "{rounded.pill}"
    padding: "8px 14px"
  inspection-panel:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "clamp(22px, 3vw, 32px)"
  file-dropzone:
    backgroundColor: "#f8faf6"
    textColor: "{colors.ink}"
    rounded: "{rounded.medium}"
    padding: "24px 18px"
  navigation-links:
    textColor: "{colors.ink-soft}"
    typography: "{typography.label}"
    padding: "4px"
  result-fresh:
    backgroundColor: "{colors.success-pale}"
    textColor: "#164a35"
    rounded: "{rounded.medium}"
    padding: "17px"
---

# Design System: CekBuah

## Overview

**Creative North Star: “The Market Inspection Ticket”**

CekBuah treats a fruit photo like a single item brought to a contemporary market stall for inspection. Its interface uses the familiar structure of a produce ticket: a bold identification, a clear upload area, and one plain-language result. The visual character is practical and bright, with crate greens, citrus accents, and paper-like surfaces.

The interface keeps the task ahead of decoration. One supported fruit photo moves through preview and an explicit check; the resulting “Segar” or “Busuk” state stays readable through both words and color.

**Key Characteristics:**
- Market greens and citrus yellow frame a clean, paper-white inspection surface.
- Manrope carries the hierarchy from large, direct headings to compact ticket labels.
- Result states use quiet tinted panels and always pair color with a written status.

## Colors

The palette balances leafy greens with warm produce accents against a soft off-white page and clean white working surface.

### Primary
- **Crate Green** (`{colors.forest-dark}`): Main action button, strong navigation text, and the darkest readable interface emphasis.
- **Market Leaf** (`{colors.forest}`): Secondary emphasis for icons, links, and focus-adjacent accents.

### Secondary
- **Citrus Tag** (`{colors.citrus}`): Small brand mark and fruit-market signal; keep it as an accent rather than a large text background.

### Tertiary
- **Soft Tomato Paper** (`{colors.tomato-pale}`): Busuk and upload-error surfaces. Pair it with the written state and dark red-brown text.
- **Fresh Produce Paper** (`#e7f5e9`): Segar result surface with dark green text.

### Neutral
- **Produce Ink** (`{colors.ink}`): Headlines and high-priority copy.
- **Soft Leaf Ink** (`{colors.ink-soft}`): Supporting text and instructions.
- **Stall Ground** (`{colors.ground}`): Main page background.
- **Ticket White** (`{colors.paper}`): Upload and result working surfaces.
- **Pale Crate Line** (`{colors.line}`): Quiet boundaries between regions and controls.

**The Result Mark Rule.** Use amber for uncertain results and the tomato tint for Busuk or errors; color always appears alongside a plain text label.

## Typography

**Display Font:** Manrope Variable (with Segoe UI, sans-serif fallbacks)

**Body Font:** Manrope Variable (with Segoe UI, sans-serif fallbacks)

**Label/Mono Font:** Manrope Variable; no separate monospace face is used.

**Character:** Manrope gives the interface sturdy market-ticket lettering without sacrificing small-screen clarity. The same family keeps upload instructions, model stamps, and results visually related.

### Hierarchy
- **Display** (weight 740, responsive 3.1–4.65rem, line-height 0.99): Main task heading.
- **Headline** (weight 740, responsive 1.9–2.5rem, line-height 1.1): Section headings.
- **Title** (weight 740, 1.19–1.28rem): Inspection panel and result headings.
- **Body** (weight 400, 0.9–1.08rem, line-height about 1.5–1.72): Instructions and explanatory copy, kept to readable line lengths.
- **Label** (weight 650–750, 0.78–0.94rem): Fruit chips, model stamp, action labels, and result metadata.

## Layout

The desktop shell uses a centered content width capped at 1160px, with a two-column hero: explanation and supported fruit on the left, the inspection ticket on the right. At 900px the hero becomes one column; at 620px the page tightens its side margins and stacks the navigation, upload surface, and information sections for a narrow screen. The upload ticket stays the strongest working surface, with generous padding and a clear primary action below the image chooser.

## Elevation & Depth

Depth is mostly tonal: the ground recedes behind white panels, and pale borders separate neighboring regions. A soft ambient shadow lifts the main inspection panel; smaller shadows only lift the floating image-removal control. Keep the rest of the page calm and flat.

### Shadow Vocabulary
- **Inspection lift** (`0 16px 36px rgb(23 59 49 / 8%)`): Separates the primary upload ticket from the page ground.
- **Floating control** (`0 3px 12px rgb(16 57 47 / 13%)`): Keeps the image-removal control legible over a photo preview.

## Shapes

The interface uses softly rounded rectangles for working surfaces, buttons, and result blocks. Fruit labels use a full pill silhouette; the image preview clips to the same rounded edge as its frame. Thin, pale borders do most of the structural work.

## Components

### Buttons
- **Shape:** Gently rounded corners (9px).
- **Primary:** Full-width forest action with white text, a 52px minimum height, and 13px 18px padding.
- **Hover / Focus:** Hover darkens toward a brighter forest and rises by 1px. Keyboard focus uses a high-contrast amber outline with a 3px stroke and 3px offset.
- **Disabled:** The submit button remains visible, with a progress cursor and reduced opacity while inference is running.

### Chips
- **Style:** Fruit names use small, pale surfaces with a thin green-gray border and pill corners.
- **State:** These labels indicate supported fruit types; they do not behave as filters or selectable controls.

### Cards / Containers
- **Corner Style:** The inspection panel uses 16px corners; the preview and result panels use 12px.
- **Background:** White inspection ticket on the soft page ground.
- **Shadow Strategy:** The main panel receives a soft ambient shadow; result blocks use border and tint instead.
- **Border:** A quiet green-gray line frames the panel and preview.
- **Internal Padding:** Responsive 22–32px inside the ticket; result blocks use compact 17px padding.

### Inputs / Fields
- **Style:** The file input is visually hidden inside a large, dashed upload target with a pale surface and 12px corners.
- **Focus:** The target shows the shared visible keyboard outline when focused.
- **Error / Disabled:** Upload errors use a pale tomato panel with explicit text; file replacement is disabled during inference.

### Navigation
- **Style:** A restrained top bar places the wordmark left and two in-page links right. Links use supporting ink, then shift to forest on hover. On narrow screens the gaps and type size tighten while preserving both links.

### Inspection Result
- **Style:** A single result block pairs an icon, a plain-language status, and a concise explanation.
- **States:** Segar uses pale green and Busuk uses pale tomato. The component remains text-first so color is never the only indicator.

**The One-Photo Rule.** Keep the upload target and explicit action on one ticket. Show one result for one submitted image.

## Do's and Don'ts

### Do:
- **Do** keep the supported fruit labels near the upload task.
- **Do** pair every result tint with a written status and its short explanation.
- **Do** preserve the clear two-column desktop layout and the single-column mobile flow.
- **Do** keep keyboard focus visible with the existing amber outline treatment.

### Don't:
- **Don't** make status depend on color alone.
- **Don't** let decorative market motifs compete with the photo preview or upload action.
