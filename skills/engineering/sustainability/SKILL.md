---
name: sustainability
description: "Audit and improve web sustainability by minimizing bytes shipped, preferring native platform features over JavaScript, and reducing page weight, requests, and estimated carbon impact. Use when reviewing or optimizing page weight, bundle size, images, fonts, third-party scripts, render-blocking resources, hosting, or when the user mentions sustainability, carbon footprint, CO2, green web, page weight, or performance budgets."
argument-hint: "Describe the surface/pages to audit, and whether you want an audit, implementation guidance, or to run the local CO2/Lighthouse report"
---

# Sustainability

Use this skill to audit, design, and remediate for digital sustainability: less code and fewer bytes, delivered efficiently, without regressing functionality or accessibility.

## Core Principles

Every recommendation should trace back to one of these:

1. **Performance is sustainability.** The lowest-carbon byte is the one never sent. Prefer building less for the same or better outcome over optimizing something that shouldn't exist.
2. **Use the platform first.** Reach for native HTML and CSS before JavaScript, and before a library. `<details>` beats an accordion library; CSS `:has()` beats a JS class toggler; native `<img loading="lazy">` beats an intersection-observer package.
3. **Every byte has a cost.** JS, images, fonts, and third-party tags all cost transfer, parse/compile time, and energy. Justify every KB, not just the big ones.

## Outcome

Produce changes/recommendations that:

- reduce total transferred bytes and request count without breaking functionality
- replace JavaScript-dependent UI with native HTML/CSS where the interaction allows it
- cut unnecessary or oversized images, fonts, and third-party scripts
- are ranked by estimated impact (bytes/requests saved) vs. effort

## Workflow

1. Classify the task.
   - Audit: measure/estimate current weight, find the heaviest offenders, rank by impact.
   - Implementation: design the lightest solution that meets the requirement, native-first.
   - Review: check a PR/diff for weight regressions before merge.
2. Establish a baseline.
   - Look at build output size, network panel/HAR, or an existing Lighthouse/CO2 report if present.
   - In this repository, offer to run the local CO2 + Lighthouse report (see below) — treat it as optional and skip it outright in any repo that doesn't have an equivalent tool.
3. Find the heaviest levers first.
   - JS bundles and third-party scripts usually dominate weight and CPU cost — check these before micro-optimizing markup.
   - Then images/video, then fonts, then CSS.
4. Apply "use the platform first" to each finding.
   - Before adding or keeping a JS dependency, check for a native HTML/CSS/browser API equivalent.
   - Prefer removing a script over lazy-loading it over deferring it, in that order.
5. Quantify and rank.
   - Estimate bytes/requests saved per fix where possible, not just "this is bad."
   - Rank by impact-to-effort, and call out anything that would trade away accessibility or correctness for weight.
6. Report the result.
   - Classify issues as `CRITICAL` (materially bloats every page load), `IMPORTANT` (meaningful, fixable waste), or `SUGGESTION` (marginal/nice-to-have).
   - Tie each recommendation to one of the three core principles.

## Running the local CO2/Lighthouse report (this repo only)

This repository ships `tools/co2-report`, the same tool `.github/workflows/co2-report.yml` runs on every PR. Running it locally is **optional** — offer it, don't run it unprompted, and skip this whole section entirely in any other codebase that has no equivalent tool.

```bash
yarn workspace @aer-studios-web/website-ui run build:static
yarn workspace @aerstudios/co2-report run report
```

The report is written to `tools/co2-report/co2-report.md` (a CO2 grade per page plus a Lighthouse SEO/performance pass). Use it to ground an audit in real numbers instead of estimates.

## Decision Points

- A JS library/component could be replaced by native HTML/CSS:
  replace it, unless the native option demonstrably fails a real requirement (browser support target, complex interaction).
- A third-party script is requested:
  question whether it's needed at all first; if it is, self-host or lazy-load it off the critical path.
- An image/video is large:
  fix format, dimensions, and compression before reaching for lazy-loading as the whole fix.
- A fix would reduce weight but harm accessibility or correctness:
  do not make that trade — flag the conflict instead of silently picking one.
- A local measurement tool exists in this repo:
  offer to run it before finalizing an audit; if unavailable (different repo), rely on build output size and manual review instead.

## Completion Checklist

- [ ] Findings are tied to one of the three core principles.
- [ ] JS bundles and third-party scripts were checked before micro-optimizations.
- [ ] Native HTML/CSS alternatives were considered before any JS-based fix.
- [ ] Each recommendation has an estimated impact (bytes/requests) where feasible.
- [ ] No fix trades away accessibility or correctness for weight without flagging it.
- [ ] The local CO2/Lighthouse report was offered (this repo) or explicitly skipped (other repos).

See [REFERENCE.md](./REFERENCE.md) for the anti-pattern catalog, byte-budget guidance, and platform-first replacement table.
