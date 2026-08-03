---
name: WorkChord
description: An operational planning workspace that keeps capacity, work, schedules, and handoffs in one visible thread.
colors:
  planning-thread: "rgb(37 99 235)"
  planning-thread-hover: "rgb(29 78 216)"
  planning-thread-soft: "rgb(239 246 255)"
  conductor-navy: "rgb(14 30 64)"
  conductor-panel: "rgb(24 48 91)"
  canvas-mist: "rgb(248 250 252)"
  working-paper: "rgb(255 255 255)"
  primary-ink: "rgb(15 23 42)"
  secondary-ink: "rgb(71 85 105)"
  strong-rule: "rgb(100 116 139)"
  status-planned: "rgb(100 116 139)"
  status-active: "rgb(8 145 178)"
  status-resolved: "rgb(16 185 129)"
  status-closed: "rgb(168 85 247)"
  feedback-warning: "rgb(217 119 6)"
  feedback-danger: "rgb(220 38 38)"
typography:
  display:
    fontFamily: "Inter Variable, Inter, system-ui, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 600
    lineHeight: 1.18
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Inter Variable, Inter, system-ui, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 600
    lineHeight: 1.18
  title:
    fontFamily: "Inter Variable, Inter, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 600
    lineHeight: 1.25
  body:
    fontFamily: "Inter Variable, Inter, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Inter Variable, Inter, system-ui, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 500
    lineHeight: 1.25
rounded:
  compact: "4px"
  control: "6px"
  surface: "8px"
  panel: "10px"
  feature: "14px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  page-gap: "20px"
  lg: "24px"
  page-x: "32px"
  xl: "48px"
components:
  button-primary:
    backgroundColor: "{colors.primary-ink}"
    textColor: "{colors.working-paper}"
    typography: "{typography.body}"
    rounded: "{rounded.control}"
    padding: "0 12px"
    height: "34px"
  button-secondary:
    backgroundColor: "{colors.working-paper}"
    textColor: "{colors.primary-ink}"
    typography: "{typography.body}"
    rounded: "{rounded.control}"
    padding: "0 12px"
    height: "34px"
  input:
    backgroundColor: "{colors.working-paper}"
    textColor: "{colors.primary-ink}"
    typography: "{typography.body}"
    rounded: "{rounded.control}"
    padding: "0 10px"
    height: "34px"
  card:
    backgroundColor: "{colors.working-paper}"
    textColor: "{colors.primary-ink}"
    rounded: "{rounded.surface}"
    padding: "20px"
  workspace-active:
    backgroundColor: "{colors.conductor-panel}"
    textColor: "{colors.working-paper}"
    typography: "{typography.body}"
    rounded: "{rounded.control}"
    padding: "6px 10px"
    height: "36px"
---

# Design System: WorkChord

## Overview

**Creative North Star: "The Planning Thread"**

WorkChord is a restrained operational workspace: dense enough for real planning work, calm enough to scan for hours. A cobalt thread marks hierarchy, selection, and the next meaningful planning step; it is directional infrastructure, not decoration. The deep navy conductor bar owns workspace switching, while contextual navigation and persistent work objects stay on quieter paper-like surfaces.

The interface favors explicit state, compact controls, and visible recovery over KPI volume or ornamental dashboards. Semantic colors describe durable record status and transient feedback consistently across light, dark, blue, and green themes. Motion is brief and explanatory; reduced-motion users retain state feedback without continuous or spatial effects.

**Key Characteristics:**

- A restrained cobalt thread for hierarchy, focus, and planning continuity.
- A 14px operational reading base with compact but distinct hierarchy.
- One persistent work object and one primary action per page.
- Structural borders and low ambient depth instead of decorative elevation.
- Canonical record-status colors that never borrow the action color.
- Contextual side navigation and a labeled workspace drawer at 1180px and below.

## Colors

The palette combines cool paper neutrals with a deliberately scarce cobalt planning thread and a fixed semantic status vocabulary.

### Primary

- **Planning Thread:** Locates the active workspace, current planning step, focus, and directional links. Its soft tint supports selected rows and contextual emphasis.
- **Conductor Navy:** Owns the global workspace layer. It separates workspace switching from page-level actions without turning every page into a dark surface.

### Secondary

- **Active Cyan:** Represents work in progress only.
- **Resolved Emerald:** Represents completed work awaiting final closure.
- **Closed Violet:** Represents durable closure, not generic success.

### Neutral

- **Canvas Mist:** The application ground behind working surfaces.
- **Working Paper:** Cards, fields, menus, and editable work objects.
- **Primary Ink:** Main text and the default primary-action fill.
- **Secondary Ink:** Supporting copy, labels, and inactive controls.
- **Strong Rule:** High-information input borders and structural dividers.
- **Planned Slate:** Neutral record state before work begins.

### Named Rules

**The Planning Thread Rule.** Cobalt communicates hierarchy, focus, or the next planning move; it does not substitute for record status or transient feedback.

**The Canonical Status Rule.** Planned is slate, active is cyan, resolved is emerald, and closed is violet in every theme and component.

**The Exception Rule.** Warning and danger colors appear for actionable exceptions and recovery, not for decoration or KPI variety.

## Typography

**Display Font:** Inter Variable with Inter and system UI fallbacks
**Body Font:** Inter Variable with Inter and system UI fallbacks
**Label/Mono Font:** Platform monospace only for code, identifiers, timelines, and measured data

**Character:** The single-family system is compact, neutral, and highly legible. Weight and spacing—not typeface changes—establish hierarchy.

### Hierarchy

- **Display** (600, page scale, 1.18): Page titles and major KPI values.
- **Headline** (600, step scale, 1.18): Planning-step titles and prominent workspace sections.
- **Title** (600, heading scale, 1.25): Card and section headings.
- **Body** (400, 14px base, 1.5): Operational reading, controls, tables, and task content; prose stays near 65–75 characters per line.
- **Label** (500, 13px, 1.25): Field labels and compact controls. Supporting metadata may step down to 12px; 11px is reserved for axes and counters.

### Named Rules

**The Operational Base Rule.** Interactive and reading text starts at 14px. Smaller sizes support the work; they never carry the primary instruction or action.

**The Quiet Hierarchy Rule.** Use 600 weight and restrained scale changes. Avoid oversized display type inside the application shell.

## Layout

The desktop shell uses a 52px conductor bar, a 220px contextual sidebar, and a fluid main workspace. Standard pages cap at 1240px with 32px horizontal and 24px vertical gutters; data-heavy workbenches can reach 1440px or take the full available height. Repeated page sections use a 20px vertical rhythm, while component internals generally follow 4px, 8px, 12px, 16px, and 20px grouping intervals.

Master-detail workspaces may use a 260px rail, fluid central canvas, and 320px inspector when space permits. At 1180px and below, the persistent sidebar becomes a labeled drawer while the workspace taxonomy remains unchanged. At 520px, page gutters reduce to 16px, multi-column forms and KPI grids become one column, secondary details collapse, and primary actions stretch when that improves reach. Coarse-pointer controls provide at least 44px touch targets, and full-screen layers use dynamic viewport units plus safe-area insets.

**The Persistent Object Rule.** Each page keeps one work object visually dominant; secondary controls belong in Filters, disclosures, or overflow.

## Elevation & Depth

Depth is structural and low-amplitude. Borders and tonal layering establish most hierarchy; shadows are reserved for cards, raised hover state, menus, drawers, and overlays. Dark mode strengthens shadow opacity rather than changing the elevation vocabulary.

### Shadow Vocabulary

- **Resting Surface** (`0 1px 0 rgba(15,18,24,.04), 0 1px 2px rgba(15,18,24,.04)`): Standard cards and contained work objects.
- **Raised Surface** (`0 1px 0 rgba(15,18,24,.04), 0 4px 12px rgba(15,18,24,.06)`): Deliberately raised hover or focused work.
- **Popover** (`0 8px 28px rgba(15,18,24,.10), 0 2px 6px rgba(15,18,24,.06)`): Menus, drawers, and temporary overlays.

### Named Rules

**The Structural-First Rule.** Start with a surface tone or border. Add a shadow only when the element actually changes depth or layer.

## Shapes

WorkChord uses gently compact corners: 4px for tags and tight internal geometry, 6px for controls, 8px for standard cards, 10px for larger panels, and 14px for featured workspace containers. Pills are reserved for small statuses, counts, and filters. Structural containers use 1px semantic borders; colored edge accents are limited to the 1px cobalt hierarchy thread.

## Components

### Buttons

- **Shape:** Compact control corners (6px) and a 34px desktop control height; large actions use 38px and small utilities use 30px.
- **Primary:** Primary ink fill with inverse text. Use once per page or protected decision area.
- **Hover / Focus:** Fast background and border shifts; focus uses the semantic cobalt ring. Disabled and busy actions remain labeled and visibly unavailable.
- **Secondary / Ghost / Danger:** Secondary stays on working paper, ghost removes the border for low-priority commands, and danger uses the semantic danger tint and border.

### Chips

- **Style:** Small bordered pills with tabular numerals when they carry counts. Neutral chips use paper or muted surfaces.
- **State:** Record-state chips use the canonical planned/active/resolved/closed mapping. Feedback chips use success/warning/danger only for current system feedback.

### Cards / Containers

- **Corner Style:** Standard working surfaces use 8px corners.
- **Background:** Working paper over canvas mist or muted sidebar surfaces.
- **Shadow Strategy:** Resting-surface shadow only; nested cards are avoided.
- **Border:** A 1px semantic border carries most separation.
- **Internal Padding:** 16px for compact content, 20px for standard card bodies.

### Inputs / Fields

- **Style:** Working-paper fill, strong semantic border, 6px corners, and 34px control height.
- **Focus:** Cobalt border plus a 3px soft focus ring.
- **Error / Disabled:** Errors use danger border and recovery copy. Disabled fields shift to the muted surface and keep readable text. Required fields include a visible localized indicator.

### Navigation

The conductor bar is a true workspace switcher; its active item uses a soft cobalt surface and a 2px bottom planning thread. The sidebar contains only destinations relevant to the current workspace. At 1180px and below, both workspace switching and contextual destinations move into a labeled, focus-managed drawer.

### Planning Readiness

Readiness is a persistent operational summary, not a KPI cluster. It exposes the next incomplete planning step, uses warnings for actionable exceptions, and provides an explicit retry when aggregate state is unavailable.

## Do's and Don'ts

### Do:

- **Do** keep one primary action and one persistent work object per page.
- **Do** use cobalt to connect workspace, selection, focus, and the next planning move.
- **Do** promote exceptions, missing inputs, and recovery ahead of aggregate KPI volume.
- **Do** put secondary controls into Filters, disclosures, or overflow.
- **Do** preserve visible labels, keyboard focus, 44px coarse-pointer targets, and explicit unavailable-state alternatives.
- **Do** remap semantic roles—not component-specific colors—when adding a theme.

### Don't:

- **Don't** reuse cobalt for task status, success, warning, or danger.
- **Don't** create nested cards or decorate every section with equal elevation.
- **Don't** rely on hover for core information or interaction.
- **Don't** hide required state, loading state, errors, or unavailable behavior behind implicit conventions.
- **Don't** add continuous motion when a static label or state change communicates the same information.
- **Don't** introduce phone-support language or actions; WorkChord has no phone-support contract.
