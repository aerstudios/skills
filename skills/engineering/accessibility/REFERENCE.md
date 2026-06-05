# Accessibility Reference

Comprehensive accessibility guidance for web application development. Use this file as a review and remediation reference. Treat legal notes as orientation only and verify current jurisdiction-specific obligations before citing them as compliance advice.

## Severity Levels

- `CRITICAL`: users cannot access content at all; fix before merge
- `IMPORTANT`: significant barrier for assistive technology or keyboard users; fix in the same sprint
- `SUGGESTION`: useful improvement; schedule deliberately

## Durable Legal Posture

- Target WCAG 2.2 AA by default unless the user explicitly asks for a different conformance target.
- WCAG 2.2 AA is a practical superset for current common regulatory baselines.
- Legal dates, fines, and enforcement thresholds change. Verify them against current primary sources before relying on them.

## WCAG 2.2 AA Quick Reference

### Perceivable

| Criterion | Level | Summary |
|-----------|-------|---------|
| 1.1.1 Non-text Content | A | All non-text content has a text alternative. Decorative images use `alt=""`. |
| 1.2.1 Audio/Video-only | A | Provide transcript for audio or text alternative for video. |
| 1.2.2 Captions (Prerecorded) | A | All prerecorded video has synchronized captions. |
| 1.3.1 Info and Relationships | A | Structure such as headings, lists, tables, labels, and landmarks is programmatically conveyed. |
| 1.3.2 Meaningful Sequence | A | Visual and programmatic ordering align when sequence matters. |
| 1.3.3 Sensory Characteristics | A | Instructions do not rely only on shape, size, position, or sound. |
| 1.3.4 Orientation | AA | Content is not restricted to a single orientation unless essential. |
| 1.3.5 Identify Input Purpose | AA | User-information inputs use appropriate `autocomplete` attributes. |
| 1.4.1 Use of Color | A | Color is not the only means of conveying information. |
| 1.4.3 Contrast (Minimum) | AA | Text contrast is at least 4.5:1 for normal text and 3:1 for large text. |
| 1.4.4 Resize Text | AA | Text resizes to 200% without loss of content or function. |
| 1.4.10 Reflow | AA | Content reflows within a 320px CSS viewport without two-dimensional scrolling for reading. |
| 1.4.11 Non-text Contrast | AA | UI components and graphics have 3:1 contrast against adjacent colors. |
| 1.4.12 Text Spacing | AA | User-overridden text spacing does not break content or behaviour. |
| 1.4.13 Content on Hover/Focus | AA | Hover or focus content is dismissible, hoverable, and persistent. |

### Operable

| Criterion | Level | Summary |
|-----------|-------|---------|
| 2.1.1 Keyboard | A | All functionality works by keyboard. |
| 2.1.2 No Keyboard Trap | A | Users can leave any component with a keyboard. |
| 2.2.1 Timing Adjustable | A | Time limits can be extended or disabled. |
| 2.2.2 Pause, Stop, Hide | A | Auto-updating content can be paused. |
| 2.3.1 Three Flashes | A | No content flashes more than 3 times per second. |
| 2.4.1 Bypass Blocks | A | Provide a skip link or equivalent mechanism. |
| 2.4.2 Page Titled | A | Pages have descriptive titles. |
| 2.4.3 Focus Order | A | Focus order preserves meaning and operability. |
| 2.4.4 Link Purpose | A | Link purpose is clear from text or context. |
| 2.4.6 Headings and Labels | AA | Headings and labels describe topic or purpose. |
| 2.4.7 Focus Visible | AA | Keyboard focus indicator is visible. |
| 2.4.11 Focus Not Obscured | AA | Focus is not completely hidden by overlays or sticky UI. |
| 2.5.1 Pointer Gestures | A | Multi-point gestures have a single-pointer alternative. |
| 2.5.2 Pointer Cancellation | A | Activation occurs on up-event or can be aborted, reversed, or is essential. |
| 2.5.3 Label in Name | A | Accessible name contains the visible label text. |
| 2.5.4 Motion Actuation | A | Motion-triggered actions have UI alternatives and can be disabled. |
| 2.5.7 Dragging Movements | AA | Drag-and-drop has a click or tap alternative. |
| 2.5.8 Target Size (Minimum) | AA | Targets or their spacing are at least 24 by 24 CSS px. |

### Understandable

| Criterion | Level | Summary |
|-----------|-------|---------|
| 3.1.1 Language of Page | A | The root document language is set correctly. |
| 3.1.2 Language of Parts | AA | Language changes inside content are marked. |
| 3.2.1 On Focus | A | Focus does not trigger unexpected context changes. |
| 3.2.2 On Input | A | Input changes do not unexpectedly change context. |
| 3.2.6 Consistent Help | A | Help mechanisms remain in the same relative order. |
| 3.3.1 Error Identification | A | Errors are described in text. |
| 3.3.2 Labels or Instructions | A | Inputs have labels or instructions. |
| 3.3.3 Error Suggestion | AA | Suggested corrections are provided when errors are detected. |
| 3.3.4 Error Prevention | AA | Important submissions are reversible, checked, or confirmed. |
| 3.3.7 Redundant Entry | A | Users are not forced to re-enter information in the same process. |
| 3.3.8 Accessible Authentication (Minimum) | AA | Authentication avoids cognitive tests and allows paste and autofill. |

### Robust

| Criterion | Level | Summary |
|-----------|-------|---------|
| 4.1.2 Name, Role, Value | A | UI components expose accessible name, role, and state. |
| 4.1.3 Status Messages | AA | Status messages are announced without moving focus. |

Notes:

- WCAG `4.1.1 Parsing` is obsolete in WCAG 2.2.
- WCAG 3.0 remains a draft; keep targeting WCAG 2.2 AA for implementation work.

## Five Rules of ARIA

1. Prefer native HTML over custom roles.
2. Do not override native semantics where prohibited.
3. All ARIA controls must be keyboard operable.
4. Do not use `aria-hidden="true"` on focusable elements.
5. All interactive elements need an accessible name.

## Anti-Pattern Catalog

### Semantic HTML

- `S1 Missing html lang`.
  Severity: `CRITICAL`.
  Detection: root HTML element lacks `lang`.
  WCAG: `3.1.1`.
  Fix: set the document language, for example `<html lang="en">`.
- `S2 Multiple h1 elements with unclear structure`.
  Severity: `SUGGESTION`.
  Detection: multiple top-level headings blur the page outline.
  WCAG: supports `1.3.1`.
  Fix: prefer one main page heading and use nested headings for sections.
- `S3 Heading level gaps`.
  Severity: `IMPORTANT`.
  Detection: heading sequence skips levels such as `h1` to `h3`.
  WCAG: `1.3.1`.
  Fix: keep heading levels logically nested and style with CSS instead of misusing semantics.
- `S4 Landmark-free div soup`.
  Severity: `IMPORTANT`.
  Detection: page structure built entirely from generic containers.
  WCAG: supports `1.3.1` and `2.4.1`.
  Fix: use `header`, `nav`, `main`, and `footer` where appropriate.
- `S5 Layout tables without presentation semantics`.
  Severity: `IMPORTANT`.
  Detection: table used for layout without headers or `role="presentation"`.
  WCAG: `1.3.1`.
  Fix: use CSS layout, or explicitly mark purely presentational tables.
- `S6 Data tables without headers`.
  Severity: `CRITICAL`.
  Detection: data table with no `th` cells or caption.
  WCAG: `1.3.1`.
  Fix: add a caption and scoped header cells.
- `S7 Non-descriptive link text`.
  Severity: `IMPORTANT`.
  Detection: vague text such as "click here", "read more", or "more".
  WCAG: `2.4.4`.
  Fix: make link text describe the destination or action.
- `S8 Non-semantic click targets`.
  Severity: `CRITICAL`.
  Detection: generic elements handling clicks as controls.
  WCAG: `4.1.2`.
  Fix: replace them with native controls such as `button`.

### ARIA Misuse

- `A1 Redundant ARIA on native elements`.
  Severity: `SUGGESTION`.
  Detection: native elements restating their implicit roles.
  Fix: remove redundant ARIA.
- `A2 aria-hidden on focusable content`.
  Severity: `CRITICAL`.
  Detection: focusable elements hidden from assistive technology.
  Fix: remove focusability or use `disabled`, `hidden`, `inert`, or DOM removal as appropriate.
- `A3 Missing required ARIA properties`.
  Severity: `CRITICAL`.
  Detection: ARIA roles without their required states or properties.
  WCAG: `4.1.2`.
  Fix: add the required role-specific properties such as `aria-selected`, `aria-expanded`, or `aria-checked`.
- `A4 Invalid ARIA roles`.
  Severity: `CRITICAL`.
  Detection: non-existent or misspelled role values.
  WCAG: `4.1.2`.
  Fix: use valid ARIA roles only.
- `A5 ARIA where native HTML works`.
  Severity: `IMPORTANT`.
  Detection: role-based recreation of controls that HTML already provides.
  Fix: replace with the correct native element.
- `A6 Missing accessible name on icon-only buttons`.
  Severity: `CRITICAL`.
  Detection: icon-only controls with no text, `aria-label`, or `aria-labelledby`.
  WCAG: `4.1.2`.
  Fix: supply an explicit accessible name and hide decorative SVG content from assistive technology.
- `A7 role=presentation on focusable elements`.
  Severity: `IMPORTANT`.
  Detection: presentational role applied to interactive elements.
  Fix: use correct semantics; browsers ignore presentation on focusable controls.
- `A8 Missing live regions for dynamic content`.
  Severity: `IMPORTANT`.
  Detection: toasts, alerts, or async status messages with no live region semantics.
  WCAG: `4.1.3`.
  Fix: use `role="status"`, `role="alert"`, or `aria-live` on a pre-existing container.

### Keyboard and Focus

- `K1 Click handlers on non-native elements without keyboard support`.
  Severity: `CRITICAL`.
  Detection: click-only generic elements.
  WCAG: `2.1.1`.
  Fix: use a native element. If unavoidable, add role, tab stop, and Enter plus Space handling.
- `K2 Positive tabindex`.
  Severity: `CRITICAL`.
  Detection: `tabindex` greater than zero.
  WCAG: `2.4.3`.
  Fix: use only `0` and `-1`.
- `K3 Trapped focus or no escape path in custom modal UI`.
  Severity: `CRITICAL`.
  Detection: modal or overlay without correct dismissal and focus handling.
  WCAG: `2.1.2`.
  Fix: prefer native `dialog` where it fits. Otherwise trap focus appropriately, dismiss on Escape unless the action must be confirmed, and restore focus on close.
- `K4 Missing skip link`.
  Severity: `IMPORTANT`.
  Detection: no primary bypass mechanism near the start of the page.
  WCAG: `2.4.1`.
  Fix: provide a visible-on-focus skip link to main content.
- `K5 outline none without a real replacement`.
  Severity: `CRITICAL`.
  Detection: focus outline removed without equivalent visible focus styling.
  WCAG: `2.4.7`.
  Fix: use a visible `:focus-visible` treatment.
- `K6 Mouse-only behaviour`.
  Severity: `IMPORTANT`.
  Detection: hover-only interactions without keyboard equivalents.
  WCAG: `2.1.1`.
  Fix: pair hover behaviour with focus behaviour.
- `K7 Focus not restored after modal close`.
  Severity: `IMPORTANT`.
  Detection: close flow leaves focus lost or behind the user.
  WCAG: `2.4.3`.
  Fix: restore focus to the invoking element or best logical follow-up target.

### Forms and Validation

- `F1 Inputs without labels`.
  Severity: `CRITICAL`.
  Detection: `input`, `select`, or `textarea` with no associated label or accessible name.
  WCAG: `1.3.1`, `3.3.2`.
  Fix: associate a `label`, `aria-label`, or `aria-labelledby`.
- `F2 Errors not linked to inputs`.
  Severity: `CRITICAL`.
  Detection: error text exists but is not referenced from the control.
  WCAG: `3.3.1`.
  Fix: link the message with `aria-describedby` and expose invalid state.
- `F3 Required state indicated only by color or symbol`.
  Severity: `IMPORTANT`.
  Detection: required state shown only visually.
  WCAG: `3.3.2`, `1.4.1`.
  Fix: use `required` or `aria-required` and explain notation in text.
- `F4 No error summary or first-error focus strategy`.
  Severity: `IMPORTANT`.
  Detection: submit failure leaves the user guessing where to recover.
  WCAG: `3.3.1`.
  Fix: focus the first invalid field or an error summary.
- `F5 Inaccessible CAPTCHA or authentication friction`.
  Severity: `IMPORTANT`.
  Detection: puzzle CAPTCHA without fallback, blocked paste, or disabled autofill.
  WCAG: `3.3.8`.
  Fix: offer accessible alternatives and allow paste and autofill.
- `F6 Placeholder used as the label`.
  Severity: `IMPORTANT`.
  Detection: placeholder present with no real label.
  WCAG: `3.3.2`.
  Fix: keep a visible label and use placeholder only as a hint.

### Visual, Motion, and Layout

- `V1 Insufficient text contrast`.
  Severity: `CRITICAL`.
  Detection: text contrast below 4.5:1 for normal text or 3:1 for large text.
  WCAG: `1.4.3`.
  Fix: increase foreground or background contrast.
- `V2 Information conveyed by color alone`.
  Severity: `CRITICAL`.
  Detection: state expressed only by color.
  WCAG: `1.4.1`.
  Fix: add text, icons, patterns, or another non-color cue.
- `V3 Fixed content font sizes blocking resize`.
  Severity: `IMPORTANT`.
  Detection: rigid pixel-based content typography.
  WCAG: `1.4.4`.
  Fix: use `rem` or `em` for scalable text.
- `V4 No reflow at 320px`.
  Severity: `IMPORTANT`.
  Detection: horizontal scrolling for normal reading tasks.
  WCAG: `1.4.10`.
  Fix: use responsive layout and test at 320 CSS px.
- `V5 Motion without reduced-motion handling`.
  Severity: `SUGGESTION`.
  Detection: non-essential animation or transition without a reduced-motion path.
  Fix: gate non-essential motion behind `prefers-reduced-motion`.

### Media and Non-Text Content

- `D1 Informational images without alt text`.
  Severity: `CRITICAL`.
  Detection: image elements with no `alt`.
  WCAG: `1.1.1`.
  Fix: provide descriptive alt text or an empty alt for decorative images.
- `D2 Decorative images with meaningful alt text`.
  Severity: `SUGGESTION`.
  Detection: decorative media announced unnecessarily.
  WCAG: `1.1.1`.
  Fix: use `alt=""` and optionally `aria-hidden="true"` for decorative SVGs.
- `D3 Video without captions`.
  Severity: `CRITICAL`.
  Detection: prerecorded video lacks caption tracks.
  WCAG: `1.2.2`.
  Fix: provide synchronized captions.
- `D4 Autoplaying audio or video`.
  Severity: `IMPORTANT`.
  Detection: autoplaying media, especially with sound.
  WCAG: `1.4.2`.
  Fix: avoid autoplay audio and keep autoplaying video muted with controls.

## Framework-Specific Notes

### React and Next.js

- Use `htmlFor` on JSX labels.
- For SPA route changes, ensure the destination has a unique page title and meaningful heading; announce or focus the new context when needed.
- Preserve focus across re-renders when conditional trees replace focused nodes.
- Validate injected HTML for structure and semantics.

### Angular

- Avoid `(click)` on generic elements unless full keyboard and role support is present.
- Prefer Angular CDK dialog and focus-management utilities for overlays.
- Announce route changes when router transitions do not already expose the new context clearly.
- Bind invalid and described-by states from form control state.

### Vue

- Avoid `@click` on generic elements unless role and keyboard support are complete.
- Manage focus after `v-if` toggles when content appears or disappears.
- Validate `v-html` content for headings, labels, alt text, and ARIA structure.

## Keyboard Reference

- `Tab`: move to the next focusable element in DOM order.
- `Shift+Tab`: move to the previous focusable element.
- `Enter`: activate buttons and links.
- `Space`: activate buttons and toggle checkboxes.
- `Escape`: close dialogs, popovers, dropdowns, and menus when appropriate.
- `Arrow` keys: navigate within composite widgets such as menus, tabs, listboxes, trees, and radios.
- `Home`: move to the first item in a managed collection.
- `End`: move to the last item in a managed collection.

## Contrast Thresholds

- Normal text: `4.5:1`
- Large text: `3:1`
- UI component boundaries and icons: `3:1`
- Graphical objects: `3:1`
- Focus indicators: `3:1`

## Review Checklist

### Perceivable Review

- [ ] Images have appropriate alt text.
- [ ] Video has captions where required.
- [ ] Landmarks and headings expose the page structure.
- [ ] Contrast meets minimum thresholds.
- [ ] Content reflows at narrow widths.
- [ ] Language is declared correctly.

### Operable Review

- [ ] All functionality works with a keyboard.
- [ ] No keyboard trap exists.
- [ ] A bypass mechanism exists for repeated navigation.
- [ ] Focus remains visible and not obscured.
- [ ] Focus returns logically after overlays close.
- [ ] Motion and pointer interactions have accessible alternatives.

### Understandable Review

- [ ] Inputs have labels or instructions.
- [ ] Errors are linked and recoverable.
- [ ] Required state is communicated beyond color.
- [ ] No unexpected context changes happen on focus or input.

### Robust Review

- [ ] Interactive elements expose correct names, roles, and states.
- [ ] ARIA roles include required properties.
- [ ] No focusable content is hidden from assistive technology.
- [ ] Dynamic updates are announced appropriately.
