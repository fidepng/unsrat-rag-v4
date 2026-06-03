---
name: Asisten Informasi Akademik UNSRAT
description: Sistem RAG Informasi Regulasi Akademik Universitas Sam Ratulangi
colors:
  primary: "#7B2D2D"
  primary-hover: "#963E3E"
  primary-active: "#5C1F1F"
  sidebar-start: "#5B1A1A"
  neutral-bg: "#FAF9F6"
  neutral-surface: "#FFFFFF"
  neutral-light: "#EBE7E1"
  border-color: "#E4DFD9"
  scrollbar-thumb: "#D1C9BE"
  scrollbar-hover: "#A82040"
  text-primary: "#2D1A1A"
typography:
  display:
    fontFamily: "Crimson Pro, serif"
    fontSize: "1.25rem"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "tight"
  headline:
    fontFamily: "Inter, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "tight"
  title:
    fontFamily: "Inter, sans-serif"
    fontSize: "1.000rem"
    fontWeight: 600
    lineHeight: 1.500
  body:
    fontFamily: "Inter, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.625
  label:
    fontFamily: "Inter, sans-serif"
    fontSize: "0.750rem"
    fontWeight: 500
    lineHeight: 1.000
rounded:
  sm: "4px"
  md: "8px"
  xl: "12px"
  full: "9999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
components:
  sidebar-tab-active:
    backgroundColor: "rgba(255, 255, 255, 0.15)"
    textColor: "#FFFFFF"
    rounded: "{rounded.xl}"
    padding: "14px 16px"
  sidebar-tab-inactive:
    backgroundColor: "transparent"
    textColor: "rgba(255, 255, 255, 0.70)"
    rounded: "{rounded.xl}"
    padding: "14px 16px"
  chat-bubble-bot:
    backgroundColor: "{colors.neutral-surface}"
    textColor: "#1F2937"
    rounded: "16px 16px 16px 0px"
    padding: "16px"
  chat-bubble-user:
    backgroundColor: "{colors.primary}"
    textColor: "#FFFFFF"
    rounded: "16px 16px 0px 16px"
    padding: "16px"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.full}"
    padding: "8px"
---

# Design System: Asisten Informasi Akademik UNSRAT

## 1. Overview: The Dignified Academy

**Creative North Star: "Dignified Academy" (Akademi Bermartabat)**

The visual system is designed to convey institutional trust, academic authority, and precise guidance. This is achieved by combining the traditional and academic UNSRAT Maroon identity color with a clean, light off-white layout. Visual complexity is minimized to keep the academic references and RAG-evaluation metrics readable and easily digestible. 

This system rejects the flashing blue/cyan borders, glowing text, and generic "AI sci-fi" aesthetics commonly found in modern chatbots. Spacing is comfortable, visual hierarchy is sharp, and interactive elements respond immediately with subtle, tactile feedback.

**Key Characteristics:**
* **Dignified Color Scheme**: Maroon-driven visual anchors paired with warm white surfaces.
* **Typographic Contrast**: Generous font-weight scale using the Inter font family.
* **Rounded and Tactile Details**: 12px rounded corners (rounded-xl) for interfaces and containers, giving a modern look that frames text blocks nicely.
* **Structural Precision**: Explicit separations between conversational areas and evaluation panels.

## 2. Colors: The Maroon Klasik Palette

The color strategy focuses on the official UNSRAT maroon branding, applied selectively to actions, highlights, and sidebar states to project authority and precision.

### Primary
* **Maroon Klasik** (`#7B2D2D`): The main brand identity color. Used for the chatbot's icon, primary buttons, headers, links, and user chat bubbles.
* **Deep Maroon Accent** (`#5B1A1A`): Used at the start of the sidebar gradient, establishing a deep contrast anchor.
* **Maroon Hover** (`#963E3E`): Hover state background for maroon buttons and action elements.
* **Maroon Active** (`#5C1F1F`): Active/click state background for primary actions.

### Neutral
* **Warm Neutral BG** (`#FAF9F6`): Canvas background color for the main chat and evaluation areas. Reduces eye strain compared to pure white.
* **Canvas White** (`#FFFFFF`): Applied to cards, bot chat bubbles, and panel content blocks to create layers of information.
* **Muted Neutral Light** (`#EBE7E1`): Soft background color for inputs, non-active states, and general panel backgrounds.
* **Border Color** (`#E4DFD9`): Universal thin border color for cards, accordions, and separators.

### Named Rules
**The 10% Maroon Rule.** The primary Maroon Klasik accent is used on ≤10% of any given screen (excluding user message bubbles). Its sparseness is what creates visual focus and authority.

**The Scroll Contrast Rule.** Scroll elements must use `#D1C9BE` for the scroll-thumb and transition to `#A82040` on hover, ensuring high visibility without cluttering the screen.

## 3. Typography

**Display Font:** Inter (fallback: `sans-serif`)
**Body Font:** Inter (fallback: `sans-serif`)
**Label/Mono Font:** Space Mono, Courier New (fallback: `monospace` — for source codes and dataset IDs)

The typography is structured for readability. It pairs bold, tightly tracked headings with tall, readable body line heights.

### Hierarchy
* **Display** (Bold (700), `1.25rem` (~20px), Line height 1.25): System name and main interface headers.
* **Headline** (Bold (700), `1.125rem` (~18px), Line height 1.25): Section names and title indicators on the evaluation panels.
* **Title** (Semi-bold (600), `1.000rem` (~16px), Line height 1.5): Chat text headers, document reference subtitles, and modal headers.
* **Body** (Regular (400), `0.875rem` (~14px), Line height 1.625): Primary chat bubbles, markdown parsed answers, and evaluation details. Cap line lengths to 75ch.
* **Label** (Medium (500), `0.750rem` (~12px), Line height 1): Eyebrows, parameters, model identifiers, and timestamp indicators.

### Named Rules
**The Balanced Headline Rule.** All headings from h1 to h3 must use `text-wrap: balance` to prevent awkward word orphans. Long text paragraphs in chat bubbles must use `text-wrap: pretty`.

## 4. Elevation: The Flat & Layered Hybrid

Depth is created primarily using borders (`#E4DFD9`) and background contrasts (`#FAF9F6` vs `#FFFFFF`). Shadows are reserved solely for interactive hover states and overlay dialog elements.

### Shadow Vocabulary
* **Rest State (Flat)**: Elements are flat against the background using thin 1px `#E4DFD9` borders.
* **Active/Hover Shadow** (`box-shadow: 0 1px 3px rgba(0,0,0,0.06)`): Used on cards and message bubbles to provide a subtle lift from the background canvas.
* **Dialog/Overlay Shadow** (`box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05)`): Reserved for dropdown menus and absolute modals.

### Named Rules
**The Flat-By-Default Rule.** Containers and buttons are flat at rest. Subtle shadows appear only as a response to state (e.g. chat bubbles or button hover actions).

## 5. Components

Components utilize rounded-xl (12px) shapes and clean, border-delimited layouts.

### Buttons
* **Shape**: Rounded corners (12px / `rounded-xl`). Send button uses a full circle (`rounded-full`).
* **Primary (Send Button)**: `#7B2D2D` background, white icon. Hover is `#963E3E`, active is `#5C1F1F`. Size is 40px x 40px (`w-10 h-10`).
* **Reset Button**: White outline, background `rgba(255,255,255,0.1)`, hover `bg-white/20`, active `bg-white/30`.

### Navigation Tabs
* **Active Tab**: Background `rgba(255,255,255,0.15)`, white text, left border `border-l-4 border-white`.
* **Inactive Tab**: Transparent background, text `text-white/70`, left border `border-l-4 border-transparent`. Hover transitions to `bg-white/5` and text white.

### Chat Bubbles
* **Bot Bubble**: Background `white`, border `1px solid #EBE7E1`, text color `text-gray-800`. Shape uses `rounded-2xl rounded-tl-none` (16px).
* **User Bubble**: Background `#7B2D2D`, text color `white`. Shape uses `rounded-2xl rounded-tr-none` (16px).

### Inputs
* **User Input Area**: Main container uses `rounded-full` (24px) or `rounded-2xl` (16px), background `#F5F3F1`, border `1px solid #E0DCD8`.

### Accordion Citations (Rujukan)
* **Header Button**: Background `#FAF9F6`, border-bottom `1px solid #E4DFD9`. Active state highlights the Lucide book-open icon in `#7B2D2D`.
* **Content Box**: Background `#FFFFFF`, internal elements divided by `divide-y divide-gray-100`. Snippets use a light gray `#F9FAFB` box with a 1px border.

## 6. Do's and Don'ts

Concrete design rules to prevent visual deterioration and maintain codebase integrity:

### Do:
* **Do** enforce color contrast. Ensure all text on `#FAF9F6` has a contrast ratio of at least 4.5:1.
* **Do** use `text-wrap: balance` on headers and `text-wrap: pretty` on chat bubble paragraphs.
* **Do** style the citations accordion dynamically, using Lucide icons (`book-open`, `chevron-down`).
* **Do** align data chart labels properly and make sure the Y-axis starts at zero.

### Don't:
* **Don't** use neon-cyan or blue borders. Maintain the Maroon Klasik brand language.
* **Don't** use side-stripe borders (border-left or border-right > 1px) on cards or content blocks.
* **Don't** use gradient text under any circumstances; rely on bold weighting and font size.
* **Don't** animate image tags on hover. Any card scaling animations must target the container wrapper.
* **Don't** use tiny tracked uppercase eyebrows (`text-[10px] tracking-widest`) on every section. Reserve uppercase only for short, functional identifiers.
* **Don't** let text overflow its containers. Keep headlines clamped on smaller viewports.
