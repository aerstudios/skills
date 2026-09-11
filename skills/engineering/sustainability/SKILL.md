---
name: sustainability
description: "Audit and improve web sustainability by minimizing bytes shipped, preferring native platform features over JavaScript, and reducing measured page weight, requests, and CO2 impact. Use when reviewing or optimizing page weight, bundle size, images, fonts, third-party scripts, render-blocking resources, hosting, or when the user mentions sustainability, carbon footprint, CO2, green web, page weight, or performance budgets."
argument-hint: "Describe the surface/pages to audit, and whether you want an audit, implementation guidance, or a measurement run"
---

# Sustainability

Use this skill to audit, design, and remediate for digital sustainability: less code and fewer bytes, delivered efficiently, backed by real measurements rather than guesses.

This skill is project-agnostic. Nothing here should assume a specific repo, build tool, or CI setup — where an example refers to one, treat it as illustrative, not a requirement.

## Core Principles

Every recommendation should trace back to one of these:

1. **Performance is sustainability.** The lowest-carbon byte is the one never sent, and the cheapest CPU cycle is the one never spent. Inefficient code doesn't just feel slow — it burns real energy on every device that runs it and every server that serves it. Prefer building less for the same or better outcome over optimizing something that shouldn't exist.
2. **Use the platform first.** Reach for native HTML and CSS before JavaScript, and before a library. Browser capability and best practice move fast — don't rely on a static list of replacements. Where a maintained platform-guidance resource is available (for example, Google Chrome's Modern Web Guidance: https://github.com/GoogleChrome/modern-web-guidance), load it with the explicit intent of preferring platform-native elements over bespoke builds, rather than pattern-matching against a fixed table.
3. **Every byte has a cost.** JS, images, fonts, and third-party tags all cost transfer, parse/compile time, and energy. Justify every KB, not just the big ones.

## What Overrides This

- Accessibility and security always win. Never strip semantics, labels, keyboard support, or a security control to save bytes — if the two conflict, keep the accessible/secure implementation and flag the tradeoff instead of silently optimizing it away.
- Correctness wins. A smaller, broken implementation is not an improvement.
- If the project has its own accessibility, security, or performance-budget process, defer to it when it disagrees with anything here.

## Outcome

Produce changes/recommendations that:

- reduce total transferred bytes and request count without breaking functionality
- replace JavaScript-dependent UI with native HTML/CSS where the interaction allows it
- cut unnecessary or oversized images, fonts, and third-party scripts
- are backed by a real measurement, and ranked by estimated impact (bytes/requests saved) vs. effort

## Workflow

1. Classify the task.
   - Audit: measure current weight, find the heaviest offenders, rank by impact.
   - Implementation: design the lightest solution that meets the requirement, native-first.
   - Review: check a PR/diff for weight regressions before merge.
2. Measure — don't estimate.
   - Never invent a byte count, request count, or CO2 figure. If you can't measure something, say so explicitly rather than guessing a plausible-sounding number.
   - Check for a measurement tool the project already has (a Lighthouse/CO2 script, a bundle analyzer config, a CI job) and use that first.
   - Otherwise, measure directly:
     - **Bundle/build size**: build output stats, or a bundle analyzer for the project's bundler (e.g. `source-map-explorer`, `rollup-plugin-visualizer`, `webpack-bundle-analyzer`).
     - **Page weight & performance**: Lighthouse against a locally served build (`npx lighthouse <url> --output=json`), or WebPageTest.
     - **CO2 estimate**: feed the total transferred bytes (from the Lighthouse report or a HAR) through CO2.js (`@tgwf/co2`'s `perVisit(bytes, isGreenHosted)`), and check hosting greenness via the Green Web Foundation's green-hosting check before assuming non-green.
   - If no tooling exists yet, run [scripts/measure.sh](./scripts/measure.sh) (bundled with this skill) against a locally served build — it installs `lighthouse` and `@tgwf/co2` on demand via `npx` and prints transferred bytes plus a CO2 estimate. See [REFERENCE.md](./REFERENCE.md) for what drives the number.
3. Find the heaviest levers first.
   - JS bundles and third-party scripts usually dominate weight and CPU cost — check these before micro-optimizing markup.
   - Then images/video, then fonts, then CSS.
4. Apply "use the platform first" to each finding.
   - Before adding or keeping a JS dependency, check for a native HTML/CSS/browser API equivalent.
   - Prefer removing a script over lazy-loading it over deferring it, in that order.
5. Quantify and rank.
   - State the measured bytes/requests saved per fix, not just "this is bad."
   - Rank by impact-to-effort, and call out anything that would trade away accessibility, security, or correctness for weight (see "What Overrides This").
6. Re-check after every change.
   - Run the project's linter, type-check, and test suite.
   - Re-run the measurement from step 2 and compare against the baseline — a fix isn't verified until the number actually moved.
   - If a needed tool is missing, install it (see step 2) rather than skipping the check.
7. Report the result.
   - Classify each finding on the team's Boulder → Sand review scale (`BOULDER`, `ROCK`, `STONE`, `PEBBLE`, `SAND`), and use `Q` instead of a severity when you need the author's input rather than asserting a defect. See [REFERENCE.md](./REFERENCE.md) for the full scale.
   - Tie each recommendation to one of the three core principles and its measured impact.

## Decision Points

- A JS library/component could be replaced by native HTML/CSS:
  replace it, unless the native option demonstrably fails a real requirement (browser support target, complex interaction). Consult platform guidance (see Core Principle 2) rather than relying on memory.
- A third-party script is requested:
  question whether it's needed at all first; if it is, self-host or lazy-load it off the critical path — ideally proxied through a web worker (e.g. Partytown) rather than run on the main thread.
- An image/video is large:
  fix format, dimensions, and compression before reaching for lazy-loading as the whole fix.
- A fix would reduce weight but harm accessibility, security, or correctness:
  do not make that trade — see "What Overrides This."
- No measurement tool exists in this project:
  install one (see Workflow step 2) rather than estimating or skipping measurement.

## Completion Checklist

- [ ] Findings are backed by a real measurement, not an estimate.
- [ ] Findings are tied to one of the three core principles.
- [ ] JS bundles and third-party scripts were checked before micro-optimizations.
- [ ] Native HTML/CSS alternatives were considered before any JS-based fix.
- [ ] Each recommendation states its measured impact (bytes/requests).
- [ ] Nothing traded away accessibility, security, or correctness for weight without flagging it.
- [ ] The project's linter, type-check, tests, and CO2/perf measurement were re-run after the change.

See [REFERENCE.md](./REFERENCE.md) for the severity scale, byte-budget guidance, and example anti-patterns.
