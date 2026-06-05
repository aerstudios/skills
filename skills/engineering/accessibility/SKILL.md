---
name: accessibility
description: "Audit and improve web accessibility using WCAG 2.2 AA, restrained ARIA usage, keyboard and focus checks, and accessible testing patterns. Use when reviewing or fixing forms, dialogs, menus, navigation, tables, media, or SPA flows, or when the user mentions accessibility, a11y, WCAG, ARIA, keyboard access, screen readers, contrast, reduced motion, or focus management."
argument-hint: "Describe the surface, framework, and whether you need an audit, bug fix, or standards review"
---

# Accessibility

Use this skill to review, design, and remediate accessible web UI while keeping fixes grounded in native semantics and WCAG 2.2 AA.

## Outcome

Produce changes that:

- prefer semantic HTML and use ARIA only when native semantics are insufficient
- preserve keyboard access, visible focus, and correct focus movement
- expose accessible names, roles, states, errors, and status updates correctly
- reflect accessibility expectations in tests and review output

## Workflow

1. Classify the task.
   - Audit: find barriers, rank them by severity, and propose the smallest durable fixes.
   - Implementation: design from native semantics and expected interaction patterns first.
   - Regression: reproduce the broken keyboard, focus, naming, or announcement behaviour before editing.
2. Start with semantic structure.
   - Prefer native elements over custom roles.
   - Check landmarks, headings, labels, tables, and media alternatives.
   - Add ARIA only when native semantics cannot express the interaction.
3. Verify operability.
   - Ensure full keyboard access.
   - Check visible focus, focus order, focus containment where needed, and focus restoration.
   - For layered UI, confirm dismissal and escape paths.
4. Verify robust behaviour.
   - Check names, roles, values, required states, error linkage, and live announcements.
   - Confirm color is not the only signal and motion respects user preferences.
5. Lock the fix with tests.
   - Prefer accessible queries such as `getByRole` and `getByLabelText`.
   - Add automated accessibility assertions when feasible.
6. Report the result.
   - Classify issues as critical, important, or suggestion.
   - Tie recommendations back to specific WCAG criteria when useful.

## Decision Points

- Native element fits the interaction:
  use it instead of recreating it with ARIA.
- Composite widget is required:
  implement the full keyboard and state model, not just the visuals.
- Layered surface opens:
  decide whether native `dialog` is sufficient before building a custom modal.
- Dynamic updates occur:
  decide whether focus should move or whether a live region should announce the change.
- Compliance or legal guidance is requested:
  use the reference as implementation guidance, but tell the user to verify current jurisdiction-specific requirements before treating it as legal advice.

## Completion Checklist

- [ ] Native semantics were preferred over custom roles.
- [ ] Interactive elements have correct names, roles, and states.
- [ ] Keyboard operation works end to end, with visible focus preserved.
- [ ] Focus management is correct for overlays and route changes.
- [ ] Errors and status updates are programmatically exposed.
- [ ] Tests use accessible queries rather than implementation details.
- [ ] Severity and WCAG impact are clear in the final review.

See [REFERENCE.md](./REFERENCE.md) for the WCAG quick reference, anti-pattern catalog, legal context notes, framework-specific fixes, and review checklist.
