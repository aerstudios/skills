# Sustainability Reference

Guidance for auditing and reducing the environmental and performance footprint of web pages. Use this file as a review and remediation reference alongside [SKILL.md](./SKILL.md).

## Severity Levels

This skill's own Boulder → Sand scale, used to classify sustainability findings consistently. `Q` is not a severity — use it when you need the author's input before a verdict can be given, rather than asserting a defect.

- `BOULDER`: blocks the page from rendering/loading correctly, or is a foundational, site-wide defect (e.g. a script blocking the critical path, no compression on text assets). Must fix before merge.
- `ROCK`: a serious, high-impact defect that isn't outright blocking but meaningfully hurts every affected page. Fix before merge where practical.
- `STONE`: a real, fixable waste. Fix in the same sprint.
- `PEBBLE`: a modest improvement — worth doing, schedule deliberately.
- `SAND`: a trivial/cosmetic nit. Negligible on its own; mention it, don't block on it.
- `Q`: not a defect — flag something that needs the author's input (e.g. "is this third-party script actually required?") before assigning a severity.

## What Drives a CO2 Estimate

A page's estimated CO2 per view (as computed by tools like CO2.js) comes down to two inputs, in order of how much they matter:

1. **Total bytes transferred.** By far the dominant factor — halving transferred weight roughly halves the estimate. This is why "every byte has a cost" is the most actionable lever.
2. **Whether hosting is green.** A green-hosted site (renewable-powered, verifiable via the Green Web Foundation's green-hosting check) scores meaningfully better than the same bytes served from non-green hosting. Don't assume green hosting without checking — tools default to assuming non-green, which is the conservative choice.

Request count and render-blocking behaviour don't feed the CO2 number directly, but they drive real-world performance (and therefore CPU/battery energy), so treat them as part of the same problem. See [scripts/measure.sh](./scripts/measure.sh) for a portable way to get a real number instead of estimating.

## Byte-Budget Guidance

Directional targets — ground specific numbers in a measured baseline (see above) rather than asserting them from memory.

- Total transferred weight per page: investigate anything well over ~500KB–1MB; the right number depends on the page's purpose.
- JS shipped to the client: prefer under ~150KB compressed for a typical content page; more requires justification.
- Largest Contentful Paint image: compressed, correctly sized, modern format (AVIF/WebP with a fallback).
- Web fonts: 1–2 families, subset to used characters/scripts, `font-display: swap` or `optional`.
- Third-party scripts: each one costs a request and main-thread parse/execution time, not just bytes — justify every one, load it `defer`/`async` off the critical path, and where the vendor supports it (e.g. via [Partytown](https://partytown.builder.io/)), run it in a web worker instead of on the main thread.

## Platform-First Guidance

Prefer a maintained, continuously-updated platform-guidance resource over a fixed lookup table — browsers and best practice change faster than any static list can track. Where one is available, load it with the explicit intent: *prefer platform-native elements over bespoke builds.* Google Chrome's Modern Web Guidance (https://github.com/GoogleChrome/modern-web-guidance) is one such resource.

A handful of illustrative examples, not an exhaustive list:

- `<details>` / `<summary>` instead of an accordion library.
- CSS `:has()`, `:is()`, `:focus-within` instead of a JS class toggler for state-driven styling.
- Native `loading="lazy"` instead of a scroll-listener/intersection-observer package.
- `<dialog>` instead of a modal library.
- CSS `scroll-snap` instead of a carousel library for simple cases.

Only reach past the platform when it genuinely can't meet a real requirement — not for a marginal visual preference.

## Example Anti-Patterns

Illustrative, not exhaustive — models keep getting better at spotting these on their own. Use these as a calibration for the *kind* of problem to flag and how severe it typically is, and apply the core principles above to anything not listed here.

### Platform Use

- `P1 JS reimplements a native element or behaviour`.
  Severity: `ROCK`.
  Detection: a custom component duplicates `<details>`, `<dialog>`, native form validation, or native lazy-loading.
  Fix: replace with the native element/attribute.
- `P2 Client-side rendering for static/build-time content`.
  Severity: `ROCK`.
  Detection: content that doesn't depend on runtime user state is rendered client-side instead of at build time.
  Fix: render at build time and hydrate only the interactive parts.

### JavaScript & Bundles

- `J1 Render-blocking synchronous scripts in the document head`.
  Severity: `BOULDER`.
  Detection: a `<script>` without `defer`, `async`, or `type="module"` blocking parse.
  Fix: defer or move non-critical scripts; keep only what first paint actually needs blocking.
- `J2 Unused or duplicate dependencies shipped to the client`.
  Severity: `STONE`.
  Detection: bundle analysis shows dead code, duplicate versions of a library, or a large library used for one small utility.
  Fix: remove, dedupe, or replace with a smaller/native alternative.

### Images & Media

- `I1 Oversized or unoptimized images`.
  Severity: `ROCK`.
  Detection: image dimensions or file size far exceed the rendered size, or no modern format is used.
  Fix: resize to actual display dimensions, compress, and serve AVIF/WebP with a fallback.
- `I2 Above-the-fold images lazy-loaded, or below-the-fold images eager`.
  Severity: `STONE`.
  Detection: `loading="lazy"` on the LCP image, or missing on offscreen images.
  Fix: eager-load (or priority-hint) the LCP image only; lazy-load the rest.

### Fonts

- `F1 Multiple static font weights/styles loaded when fewer would do`.
  Severity: `STONE`.
  Detection: several static weight/style files requested but only one or two actually used, or a design needs a range of weights.
  Fix: trim to the weights/styles actually in use, or replace multiple static files with a single variable font — one file covering the whole weight/style axis is usually lighter than two or more static cuts.
- `F2 No font-display strategy`.
  Severity: `STONE`.
  Detection: `@font-face` without `font-display`, causing invisible text or layout shift.
  Fix: set `font-display: swap` or `optional`.

### Third-Party Scripts & Tags

- `X1 Third-party script blocking the critical path`.
  Severity: `BOULDER`.
  Detection: a tag manager or widget script loaded synchronously in the document head.
  Fix: load it asynchronously/deferred, after first interaction/idle, or off the main thread via a worker proxy (e.g. Partytown).
- `X2 Third-party script with no clear product justification`.
  Severity: `STONE`.
  Detection: analytics/marketing/chat tags present without a stated owner or purpose.
  Fix: remove if unjustified; otherwise document why it's needed.

### CSS & Delivery

- `D1 No compression on text assets`.
  Severity: `BOULDER`.
  Detection: HTML/CSS/JS served without gzip/brotli.
  Fix: enable compression at the CDN/edge or server.
- `D2 Missing or short cache headers on static assets`.
  Severity: `STONE`.
  Detection: hashed static assets (JS/CSS/images/fonts) are re-fetched on every visit.
  Fix: use long `max-age` and immutable caching for hashed assets.

### Hosting

- `H1 No CDN/edge caching for static assets`.
  Severity: `STONE`.
  Detection: static assets served from origin on every request instead of an edge cache.
  Fix: front static assets with a CDN/edge cache and check cache hit rate.
- `H2 Renewable/green hosting not verified`.
  Severity: `PEBBLE`.
  Detection: the hosting provider's energy source hasn't been checked.
  Fix: verify with the Green Web Foundation's green-hosting check, or note it as an accepted tradeoff.

### Measurement

- `M1 No baseline measurement before optimizing`.
  Severity: `STONE`.
  Detection: changes are proposed without a measured before/after (bundle size, Lighthouse score, CO2 estimate).
  Fix: measure first — see "What Drives a CO2 Estimate" and [scripts/measure.sh](./scripts/measure.sh).
