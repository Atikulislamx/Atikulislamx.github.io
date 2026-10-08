# Site audit and QA — October 2026

## Architecture and scope

20 indexable HTML routes plus `404.html`; no client framework or deployment build. `index.html` links to the same service, case-study, FAQ and contact directories as the shared header/footer. Eight service pages and five case-study pages are authored HTML, **not rendered from JSON at runtime**. `data/services.json` and `data/case-studies.json` are editorial references; `data/pages.json` and the `prompts/` collection belong to the legacy asset pipeline. `data/site.json` is read by the optional avatar override; `data/faq.json` is not fetched by the live site. CSS is split into base tokens/reset, layout, components, avatar, homepage, and shared detail-page rules. JS modules handle navigation, avatar override and contact form. No server routes. Root-relative links require deployment at the domain root, matching the existing `CNAME`.

## Findings and priority

| Priority | Evidence | Action |
|---|---|---|
| Critical | Zero Idea case study had placeholder domain in canonical, OG URL/image and JSON-LD; 20 other routes used the custom domain. | Replaced all placeholder references. Sitemap and canonicals now agree. |
| High | 20 pages referenced a missing `favicon.svg`; CSS referenced two missing WOFF2 fonts. | Unified page icons/manifest and system font stack. Root favicon now matches the icon set. |
| High | Closed mobile nav was visually off-screen but keyboard-focusable; menu had no focus loop or breakpoint cleanup. Desktop submenu claimed application-menu semantics without application-menu behavior. | Inert/visibility closed state, focus return/trap, Escape, scroll restoration, native details, ordinary link semantics. |
| High | Hero was nearly all white. Five case banners were byte-identical generic placeholders; most social cards were byte-identical and did not show the page title. | Replaced with a consistent editorial system and page-specific social cards. |
| Medium | Header/footer avatar mixed a portrait with AIR text, while JSON claimed null. Portrait had been used as tiny favicon. | Reused the existing face without alteration in a 17 KB WebP on every route; distinct monogram tab icon. About photo gets descriptive alt; repeated header/footer photos are decorative beside the name. |
| Medium | The homepage showed unsourced numerical counters and an Upwork success metric. | Removed those claims from prominent UI; linked to the actual profile and replaced counters with a process explanation. No new proof claims. |
| Medium | The form validated required fields but did not validate malformed email on blur; status/field description wiring was incomplete. | Added validity feedback, field error associations, focus/status/busy states, network failure fallback, and a warning not to share credentials. |
| Polish | Overspecified menu ARIA, repeated visual placeholders, fixed button white-space and several image slots lacking dimensions. | Simplified semantics, reserved image space, wrapped buttons, cleaned unused assets, and adjusted breakpoints. |

## Visual asset decisions

| Asset group | Previous use / issue | Decision |
|---|---|---|
| Existing portrait (formerly inside 512px favicon PNG) | Shown in some headers/about, replaced by AIR text elsewhere; saturated magenta lighting. Identity cannot be inferred or synthesized. | Preserve the original bytes as `/assets/images/atikul-islam-rabbi-source.png`; encode the served `/assets/images/atikul-islam-rabbi.webp` without retouching, use one image everywhere. **Recommend a genuine, neutrally lit professional photograph from the owner** when available. |
| Home `hero-home.png` | Nearly blank white 1920×1080 background without informative content. | Removed; HTML/CSS process card is meaningful, legible, and crops without image loading. |
| Eight service SVGs, services hub SVG | All were minor variations of two circles and a line, unrelated to specific recovery tasks. | Removed from live site; page-specific semantic process graphics replace them. |
| Five case banners | Five identical 1600×600 files with two circles, regardless of client or situation. | Replaced the *used* WebPs at the same paths with distinct titled, labeled 1600×600 banners; narrow viewports crop only the decorative right geometry while keeping the left title readable. Deleted unused JPEG variants. |
| Case-studies hub banner | Unreferenced. | Deleted. Hub cards use numbered case-file treatment rather than unnecessary images. |
| 20 OG cards | Most were the same title-less 1200×630 generic card; home PNG was 921 KB. | Replaced with per-route titled 1200×630 graphics; home PNG ~40 KB. OG and Twitter image URLs point to actual files. |
| Favicons, Apple/Android icons, root ICO, manifests | Favicon referred to missing SVG on most routes, while duplicate manifests disagreed. | Coordinated deterministic A monogram, one active manifest, root + linked ICO. |
| Portfolio/CTA/divider/about-support SVGs | Generic shapes without meaningful subject; most unused. | Removed; portfolio foregrounds actual stated skills. |
| 404 SVG | Simple directional arrow was appropriate and small. | Kept. |

Do not use an image model to invent a new portrait, client scene, platform dashboard or credential. The editorial artwork is reproducible with `scripts/render-editorial-assets.py` (optional authoring dependencies only; no Pages build).

## SEO, accessibility, performance, and security

- All 20 indexable routes have distinct titles/descriptions, canonicals, OG and Twitter metadata, JSON-LD and sitemap entries. Case-study URLs now use the custom domain. Existing Person/Organization/WebSite, Service, Article and BreadcrumbList schema retained. `robots.txt` and `CNAME` remain unchanged. Article claims are still the repository's authored claims, not independently substantiated.
- Semantic headings and skip links retained; menu semantics corrected; form errors linked with `aria-describedby`; visible focus outline; content visible without JS; native `details` preserved. Reduced motion disables transitions via CSS. Keyboard tests were run for navigation and form behavior.
- Removed missing font requests and blank hero image; optimized the existing portrait; reduced OG home from ~921 KB to ~40 KB; case banners now ~17–23 KB each. PNG favicon source no longer doubles as the portrait file on every page. No client-side framework.
- All `target="_blank"` links use `noopener noreferrer`. Contact uses a public Web3Forms identifier in client JS (not a secret). Never ask visitors to submit passwords or OTPs. Google Tag Manager remains on the homepage; its privacy/consent configuration is a site-owner decision. No live message was sent during QA.

## Verification performed

- `python3 scripts/check-site.py` passed: 20 indexable pages + 404, local routes/assets, canonical/OG/Twitter, JSON-LD parse, sitemap, manifest icons, target security and CSS URLs.
- `git diff --check` and `node --check` passed for the three browser modules. Automated axe-core checks on all 21 routes at 390px and 1280px, plus the opened mobile menu, reported zero violations after improving footer-label contrast and underlining in-text links. This does not replace a manual screen-reader audit.
- Served locally with `python -m http.server` and used headless Chromium for **all 21 HTML routes at 320, 360, 375, 390, 414, 768, 1024, 1280 and 1440px** (189 viewport-route combinations): no document horizontal scroll, missing decoded images, local HTTP 404 or page exceptions. Desktop and mobile homepage screenshots reviewed. Checked menu open, native service disclosure, Escape, focus return, scroll unlock, desktop focus submenu, validation of empty and invalid-email form states, and mocked success/error response paths. Browser/network service delivery and screen-reader behavior were **not** tested against production.

## Remaining owner tasks

1. Provide a genuine neutral-lighting portrait, if desired; verify published profile, case-study, follower-count and outcome claims and obtain explicit permission for named references. The UAE study remains anonymized.
2. Send a real **non-sensitive** test contact message after deployment; configure Web3Forms domain restrictions, notifications and spam controls. The simulated network test is not delivery confirmation.
3. Confirm external social links, analytics/consent needs, and the homepage Google Tag Manager configuration; outbound third-party sites were not live-verified in this sandbox.
4. Run Lighthouse/Core Web Vitals and a screen-reader/manual device pass on the public deployment, and submit the sitemap to Search Console. The static and headless checks do not replace these real-user tests.
5. Keep `docs/asset-pipeline.md` in view before invoking the legacy image generator: its force option would overwrite this visual system.
