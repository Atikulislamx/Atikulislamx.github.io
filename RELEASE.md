# Release notes: 2026 refresh

Branch `arena/807402c8-atikulislamx-github-io`, based on `main` at `b007a14`. Full findings and open items are in [docs/audit-2026.md](docs/audit-2026.md).

## What changed

- **Contact form works.** The honeypot bug that blocked every submission is fixed. Validation, submit states, and error handling are in place.
- **Fonts load.** Inter and Fraunces are self-hosted (SIL OFL 1.1).
- **Case study fixed.** The placeholder domain is gone from Zero Idea. Unverifiable attribution and overstated outcomes are removed or reworded.
- **Navigation.** The mobile menu hides its links while closed and supports Escape, focus return, and scroll lock. The desktop Services submenu supports Escape and `aria-expanded`.
- **Accessibility.** 3 px focus outlines. Solid text colours replace opacity-faded text. Content is visible without JavaScript. Motion is off under `prefers-reduced-motion`.
- **Content.** Unverifiable statistics and badges are removed (listed in `data/site.json`). Service pages gained who-it's-for, process, required information, and limitations sections. The homepage narrative now runs identity, expertise, services, proof, case studies, trust, and CTA.
- **Visuals.** Retired the blank hero, the identical OG and banner images, the generic illustrations, and the face-crop favicon. Added a monogram favicon and app icons, route motif, and one OG card per page.
- **SEO and structured data.** Per-page titles, descriptions, canonicals, OG and Twitter tags, breadcrumbs, and consistent JSON-LD. The sitemap lists 20 URLs and has no internal references.
- **Repository.** Removed `assets/generated/`, the avatar script and stylesheet, and the duplicate manifest. Added `npm run check`.

## What did not change

`CNAME`, the custom domain, every directory route, `robots.txt`, `google0a2814688d6877bf.html`, the GTM container, the Facebook app ID, and the Web3Forms access key. The service and case-study structure and the conversion paths are kept.

## Verified

- `npm run check`: no errors across 22 HTML files and 20 sitemap URLs.
- Chromium at nine widths (320–1440): no horizontal scroll on any of 21 pages.
- axe-core 4.14 (WCAG 2.2 AA and best practice): zero violations on all 21 pages.
- Interaction tests: mobile menu, desktop submenu, contact form (with Web3Forms mocked), no-JS fallbacks, reduced motion, focus.
- Visual review: homepage at 1440 px and 390 px.

## Not verified

Live Web3Forms delivery, hover on the desktop submenu, real devices, screen readers, other browsers, Lighthouse, Rich Results Test, Search Console, and the live domain after deployment. See audit section 7.

## Before merging

Owner decisions O1–O6 in [docs/audit-2026.md](docs/audit-2026.md) section 9, especially the profile photo, client permissions, legal review of one case-study line, and confirming form delivery.
