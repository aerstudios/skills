# CSS Architecture Reference

This document supplements the `architect-css` skill by defining the strict naming conventions and technical boundaries. Do not deviate from these patterns.

## Token Naming Conventions

Global design tokens must use the following semantic prefixes assigned at `:root`:

- `--c-*` : Color (e.g., `--c-background`, `--c-primary-text`)
- `--s-*` : Spacing and layout sizing (e.g., `--s-4`, `--s-container-width`)
- `--sh-*`: Shadows and elevation (e.g., `--sh-dropdown`)
- `--fw-*`: Font weight (e.g., `--fw-bold`)
- `--t-*` / `--lh-*`: Typography and line-height (e.g., `--t-body`, `--lh-relaxed`)

### Component-Scoped Tokens

Local component variables must map from global tokens and include the `-cmp-` identifier to denote component scope:

- `--c-cmp-button-bg: var(--c-primary);`
- `--s-cmp-card-padding: var(--s-4);`

## File Conventions

- **Module Naming:** Must strictly use `ComponentName.module.css` or `ComponentName.module.css`.
- **Encapsulation:** All component styles must be fully encapsulated within their module structure without leaking to or relying on global element selectors.

## Strict CSS vs JavaScript Boundaries

**Must be handled entirely in CSS:**

- Visual state changes (`:hover`, `:focus-visible`, `:disabled`, `:active`)
- Responsive breakpoints (Container Queries, Media Queries)
- Theme overrides (exclusively through custom property redeclaration)
- Motion and animation (Transitions, Keyframes)

**Permitted in JavaScript:**

- State modelling for interaction semantics (e.g., toggling `aria-expanded="true"`, which CSS then targets for styling).
- Measuring layout data that is impossible to calculate or represent in CSS (e.g., dynamic `getBoundingClientRect` for popover positioning, though CSS `anchor()` should be preferred where supported).
