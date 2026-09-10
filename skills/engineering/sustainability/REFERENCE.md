# Sustainability Reference

Comprehensive guidance for auditing and reducing the environmental and performance footprint of web pages. Use this file as a review and remediation reference.

## Severity Levels

- `CRITICAL`: materially bloats every page load or blocks rendering; fix before merge
- `IMPORTANT`: meaningful, fixable waste; fix in the same sprint
- `SUGGESTION`: marginal saving; schedule deliberately

## Byte-Budget Guidance

Ground specific numbers in a measured baseline (see Measurement below) rather than asserting them from memory.

- Total transferred weight per page: investigate anything well over ~500KB–1MB; the right number depends on the page's purpose.
- JS shipped to the client: prefer under ~150KB compressed for a typical content page; more requires justification.
- Largest Contentful Paint image: compressed, correctly sized, modern format (AVIF/WebP with a fallback).
- Web fonts: 1–2 families, subset to used characters/scripts, `font-display: swap` or `optional`.
- Third-party scripts: each one is a request, a parse cost, and often a privacy/consent cost — justify every single one.

## Platform-First Replacement Table

| Instead of (JS) | Use (native) |
|---|---|
| Accordion/disclosure library | `<details>` / `<summary>` |
| Modal/dialog library | `<dialog>` |
| Tooltip library for simple hints | `title` attribute or the native popover API |
| Tab library | Native semantics first; fall back to the ARIA tabs pattern only when a real requirement demands it |
| Carousel library for simple cases | CSS scroll-snap |
| Smooth-scroll polyfill | CSS `scroll-behavior: smooth` |
| Lazy-load-on-scroll library for images/iframes | `loading="lazy"` |
| Intersection-observer for reveal-on-scroll | CSS scroll-driven animations / `@starting-style` where support allows |
| JS-based form validation for basic checks | Native HTML validation attributes (`required`, `pattern`, `type="email"`) |
| JS conditional styling on state/attribute | CSS `:has()`, `:is()`, attribute selectors |
| Client-side templating for static content | Server/build-time rendering (static site generation / pre-rendering) |
| Custom video/audio player chrome for basic playback | Native `<video controls>` / `<audio controls>` |
| JS-driven responsive images | `<picture>` / `srcset` + `sizes` |

Only reach past this table when the native option genuinely can't meet a real requirement — not for a marginal visual preference.

## Anti-Pattern Catalog

### Platform Use

- `P1 JS reimplements a native element or behaviour`.
  Severity: `CRITICAL`.
  Detection: a custom component duplicates `<details>`, `<dialog>`, native form validation, or native lazy-loading.
  Fix: replace with the native element/attribute; see the table above.
- `P2 CSS-only interaction implemented in JS`.
  Severity: `IMPORTANT`.
  Detection: JS toggles a class for something achievable with `:hover`, `:focus-within`, `:has()`, or `:checked`.
  Fix: move the interaction to CSS.
- `P3 Client-side rendering for static/build-time content`.
  Severity: `CRITICAL`.
  Detection: content that doesn't depend on runtime user state is rendered client-side instead of at build time.
  Fix: render at build time (static output) and hydrate only the interactive parts.
- `P4 Over-hydration of interactive islands`.
  Severity: `IMPORTANT`.
  Detection: a hydration directive makes a component interactive immediately when it doesn't need to be, or at all.
  Fix: use the least eager hydration directive that satisfies the interaction, or none.

### JavaScript & Bundles

- `J1 Unused or duplicate dependencies shipped to the client`.
  Severity: `IMPORTANT`.
  Detection: bundle analysis shows dead code, duplicate versions of a library, or a large library used for one small utility.
  Fix: remove, dedupe, or replace with a smaller/native alternative.
- `J2 Whole-library imports instead of targeted imports`.
  Severity: `SUGGESTION`.
  Detection: importing an entire package for one function.
  Fix: import only the needed function, or replace with a native equivalent.
- `J3 Render-blocking synchronous scripts in the document head`.
  Severity: `CRITICAL`.
  Detection: a `<script>` without `defer`, `async`, or `type="module"` blocking parse.
  Fix: defer or move non-critical scripts; keep only what first paint actually needs blocking.
- `J4 No code-splitting for route/page-specific logic`.
  Severity: `IMPORTANT`.
  Detection: one JS bundle shipped on every page regardless of what that page uses.
  Fix: split by route/component so pages only load what they use.
- `J5 Polyfills shipped to modern browsers unconditionally`.
  Severity: `SUGGESTION`.
  Detection: polyfills bundled without a differential/targeted delivery strategy.
  Fix: serve polyfills conditionally, or drop support for the browsers that need them per the project's baseline.

### Images & Media

- `I1 Oversized or unoptimized images`.
  Severity: `CRITICAL`.
  Detection: image dimensions or file size far exceed the rendered size, or no modern format is used.
  Fix: resize to actual display dimensions, compress, and serve AVIF/WebP with a fallback.
- `I2 Missing responsive images`.
  Severity: `IMPORTANT`.
  Detection: one image size served to all viewports.
  Fix: use `<picture>` / `srcset` / `sizes` so small viewports don't download desktop-sized images.
- `I3 Above-the-fold images lazy-loaded, or below-the-fold images eager`.
  Severity: `IMPORTANT`.
  Detection: `loading="lazy"` on the LCP image, or missing on offscreen images.
  Fix: eager-load (or priority-hint) the LCP image only; lazy-load the rest.
- `I4 Autoplaying video without necessity`.
  Severity: `IMPORTANT`.
  Detection: autoplay video used purely decoratively.
  Fix: use a poster image, or a small muted looping clip only if genuinely essential.
- `I5 Uncompressed SVGs`.
  Severity: `SUGGESTION`.
  Detection: SVG assets carry editor cruft (metadata, hidden layers, unnecessary precision).
  Fix: run through an SVG optimizer.

### Fonts

- `T-F1 Multiple font families/weights loaded when one would do`.
  Severity: `IMPORTANT`.
  Detection: several weights/styles requested but only one or two actually used.
  Fix: trim to the weights/styles actually in use.
- `T-F2 Unsubsetted web fonts`.
  Severity: `SUGGESTION`.
  Detection: font files include full glyph sets for scripts/characters the site never uses.
  Fix: subset to the used character set.
- `T-F3 No font-display strategy`.
  Severity: `IMPORTANT`.
  Detection: `@font-face` without `font-display`, causing invisible text or layout shift.
  Fix: set `font-display: swap` or `optional`.
- `T-F4 Third-party font host adds a blocking round trip`.
  Severity: `SUGGESTION`.
  Detection: fonts loaded from an external host with a separate connection/DNS cost.
  Fix: self-host fonts where feasible.

### Third-Party Scripts & Tags

- `X1 Third-party script with no clear product justification`.
  Severity: `IMPORTANT`.
  Detection: analytics/marketing/chat tags present without a stated owner or purpose.
  Fix: remove if unjustified; otherwise document why it's needed.
- `X2 Third-party script blocking the critical path`.
  Severity: `CRITICAL`.
  Detection: a tag manager or widget script loaded synchronously in the document head.
  Fix: load it asynchronously/deferred, or after first interaction/idle.
- `X3 Duplicate tracking/analytics tags`.
  Severity: `IMPORTANT`.
  Detection: more than one tool measuring the same thing.
  Fix: consolidate to one.
- `X4 Third-party embeds loaded eagerly`.
  Severity: `IMPORTANT`.
  Detection: heavy iframe embeds (video, maps, social) load on every page view regardless of visibility or interaction.
  Fix: use a lightweight facade placeholder and swap in the real embed on interaction or visibility.

### CSS & Delivery

- `D1 Unused CSS shipped to every page`.
  Severity: `SUGGESTION`.
  Detection: a global stylesheet includes rules for components not present on most pages.
  Fix: scope CSS per component/route where the build tooling supports it.
- `D2 Render-blocking CSS for below-the-fold content`.
  Severity: `SUGGESTION`.
  Detection: a full stylesheet blocks render for styles that only apply far down the page.
  Fix: inline critical CSS and defer the rest.
- `D3 No compression on text assets`.
  Severity: `CRITICAL`.
  Detection: HTML/CSS/JS served without gzip/brotli.
  Fix: enable compression at the CDN/edge (CloudFront) or server.
- `D4 Missing or short cache headers on static assets`.
  Severity: `IMPORTANT`.
  Detection: hashed static assets (JS/CSS/images/fonts) are re-fetched on every visit.
  Fix: use long `max-age` and immutable caching for hashed assets via CloudFront cache behaviours.

### Hosting & Delivery Infrastructure

- `H1 No CDN/edge caching for static assets`.
  Severity: `IMPORTANT`.
  Detection: static assets served from origin on every request instead of an edge cache.
  Fix: front static assets with a CDN/edge cache (e.g., CloudFront) and check cache hit rate.
- `H2 Renewable/green hosting not verified`.
  Severity: `SUGGESTION`.
  Detection: the hosting provider's energy source hasn't been checked.
  Fix: verify the AWS region's renewable energy commitments, or note it as an accepted tradeoff.

### Measurement

- `M1 No baseline measurement before optimizing`.
  Severity: `IMPORTANT`.
  Detection: changes are proposed without a measured before/after (bundle size, Lighthouse score, CO2 estimate).
  Fix: measure first. If the repo provides a CO2/Lighthouse report script or CI artifact, use it; otherwise use Lighthouse, WebPageTest, or a bundle analyzer, plus build output size.
- `M2 Impact not quantified in the report`.
  Severity: `SUGGESTION`.
  Detection: recommendations given without an estimated bytes/requests saved.
  Fix: estimate impact per fix so effort can be prioritized.

## Review Checklist

### Platform-First Review

- [ ] Every JS-based UI pattern was checked against a native HTML/CSS equivalent.
- [ ] Hydration is scoped to only what's actually interactive.

### Weight Review

- [ ] JS bundle size and third-party script count were checked first.
- [ ] Images are correctly sized, compressed, and in a modern format.
- [ ] Fonts are limited, subsetted, and use a `font-display` strategy.
- [ ] Critical-path rendering isn't blocked by unnecessary scripts or styles.

### Delivery Review

- [ ] Static assets are compressed and cached at the edge.
- [ ] No duplicate third-party tags are present.

### Reporting Review

- [ ] Each finding cites a core principle and an estimated impact.
- [ ] A baseline measurement was taken or explicitly noted as unavailable.
