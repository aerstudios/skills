---
name: architect-css
description: "Design and review component styles using CSS Modules, design tokens, and CSS custom properties. Use when creating/refactoring component styles, defining theme variables, reviewing CSS architecture, applying modern CSS (logical properties, container queries), or ensuring CSS accessibility. Triggers on: margin-inline, @container, gap, flex, grid, theme, token, accessibility, prefers-reduced-motion, focus-visible."
argument-hint: "Describe the component and whether this is a new style system, a refactor, or a review"
---

# Architect CSS

## Quick Start

```css
/* Good: Local tokens, logical properties, parent layout, strict accessibility */
.container {
  /* Local component tokens mapped from global theme */
  --c-cmp-card-bg: var(--theme-surface);
  --c-cmp-card-padding: var(--spacing-4);

  background-color: var(--c-cmp-card-bg);
  padding-block: var(--c-cmp-card-padding);

  /* Layout handled strictly by parent */
  display: flex;
  gap: var(--spacing-2);
}

.button {
  /* Accessibility: explicit focus states and motion preferences */
  &:focus-visible {
    outline: 2px solid var(--theme-focus-ring);
    outline-offset: 2px;
  }

  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }
}
```

## Outcome

Produce maintainable, token-driven styles that:

- preserve global theming through root-level tokens
- enable local component theming via scoped custom properties
- enforce strict accessibility standards for interactive elements and motion
- strictly use CSS-native layout, state, and responsiveness over JavaScript

## When to Use

- building or refactoring component styles in `*.module.css`
- defining global theme tokens or component-level local theme variables
- reviewing CSS for architectural consistency, modern CSS usage, and accessibility
- evaluating or fixing layout (`gap`, `grid`), responsiveness (`@container`), or logical properties

## Workflow

1. Classify the styling decision.
   - Global concern: define or update token variables in theme scope.
   - Component concern: define local component variables and consume them in CSS Modules.
2. Model tokens before declarations.
   - Replace raw values with semantic tokens.
   - Must use existing token categories and naming patterns from the reference.
3. Author module styles with composable classes.
   - Use class selectors, not element selectors.
   - Keep class names short, contextual, and camelCase.
   - Minimize nesting and compose atomic styles where useful.
4. Enforce modern CSS primitives.
   - Must use logical properties (`margin-inline`, `padding-block`, etc.).
   - Must use parent elements for layout (e.g. using `display: flex` or `display: grid` with `gap`). Do not apply margin to elements that affect layout outside their boundary.
   - Use container queries for component-level responsiveness.
   - Use cascade layers where layering concerns exist.
5. Keep behaviour in CSS when CSS is the right tool.
   - Use pseudo-classes, media queries, container queries, custom properties, transitions, and keyframes for visual behaviour.
   - Do not move styling logic to JavaScript unless CSS cannot express the requirement.
6. Strictly enforce accessibility best practices.
   - Must use `:focus-visible` for keyboard navigation states; never use `outline: none` without providing a highly visible alternative.
   - Must respect `@media (prefers-reduced-motion: reduce)` for animations and transitions.
   - Must use high-contrast theme tokens for text and interactive elements.
   - Preserve semantic markup and accessible state styling (e.g., `aria-expanded`, `aria-hidden`).

## Decision Points

- Need cross-product consistency or brand semantics:
  define/update global token(s).
- Need one component variant or local adaptation:
  add local component token(s) (for example `--c-cmp-*`, `--s-cmp-*`).
- Need responsive behaviour inside reusable components:
  use container queries instead of viewport media queries.
- Requirement is purely visual/stateful:
  keep in CSS; do not use JS state toggles unless required for interaction semantics.

## Completion Checklist

- [ ] No hard-coded design values when token equivalents exist.
- [ ] Tokens follow established naming patterns and categories.
- [ ] Layout is strictly managed by parent elements (flexbox/grid with gap); no element-level outside margins.
- [ ] Styles live in CSS Modules with class-based selectors.
- [ ] Logical properties are used for all directional spacing/sizing.
- [ ] Responsiveness uses container queries where component-scoped.
- [ ] Interactive elements have distinct `:focus-visible` states and respect `prefers-reduced-motion`.
- [ ] Local theme overrides are implemented through custom properties.
- [ ] No unnecessary JavaScript styling logic introduced.

See [Repository CSS Architecture Reference](./reference/reference.md).
