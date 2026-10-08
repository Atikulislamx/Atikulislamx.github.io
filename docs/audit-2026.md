# Audit and 2026 modernization: atikulislam.me

Branch `arena/807402c8-atikulislamx-github-io` (base `b007a14`). Review date: 2026-10-08.

## 1. Summary

The site had launch-blocking defects. The contact form could not submit. Every custom font returned 404. The Zero Idea case study shipped a placeholder domain. Keyboard users could reach links inside the closed mobile menu. Most brand images were blank, duplicated, or generic.

This pass fixes those defects and rebuilds the homepage narrative, the service and case-study templates, and the contact flow on one visual system. It also removes claims that cannot be verified from the repository. The site is still static HTML, CSS, vanilla JavaScript, and JSON, with no framework and no build step needed to deploy.

Items that need owner decisions are listed in section 9. They include the profile photo, client permissions, one legal-review line, and confirming the form delivery key.

## 2. Method

- Read every HTML, CSS, JS, JSON, manifest, sitemap, robots, CNAME, and documentation file. Searched for placeholders and broken references. Hashed every image to find duplicates. Measured dimensions.
- Headless Chromium 153 with axe-core 4.14, run at nine widths (320, 360, 375, 390, 414, 768, 1024, 1280, 1440) across 21 pages. Interaction tests were run separately.
- `npm run check` (`scripts/check-site.mjs`) runs the static rules.
- Not run: Lighthouse, real devices, screen readers, other browsers, and live Web3Forms delivery. See section 7.

## 3. Findings and status

Status key: **Fixed** (changed in this pass, verified where noted), **Owner** (needs a decision, section 9), **Flagged** (kept, with a note).

### Critical

| ID | Finding | Status |
|---|---|---|
| C1 | Contact form never submitted. The honeypot test read `.value`, which is always `"on"`, so the handler returned before validation. | Fixed. `form.js` checks `.checked`. Verified: empty, invalid, honeypot, success, and failure paths. |
| C2 | Font files were missing. `@font-face` pointed to two woff2 files that were never committed, so all text used fallbacks. | Fixed. Self-hosted Inter and Fraunces (SIL OFL 1.1) with licence files in `assets/fonts/`. |
| C3 | Placeholder domain `REPLACE-WITH-YOUR-DOMAIN.example` in the Zero Idea case study: canonical, `og:url`, `og:image`, and JSON-LD `@id`/`item` (8 occurrences). | Fixed. Page rebuilt. The checker fails the build on any `REPLACE-WITH`. |
| C4 | Mobile menu exposed 15 links to the keyboard while closed. Escape did not close it, there was no scroll lock, and the toggle label stayed "Open menu". | Fixed. Native `<details>` menu with Escape, focus return, scroll lock, and close-on-tab-out. Verified. |
| C5 | Unverifiable claims: "300+ clients", "20+ countries", "100+ accounts recovered", "30+ Business Managers recovered", Upwork "100% Job Success", "globally recognized" vision, and "direct experience recovering Business Managers" in service copy. | Fixed. Removed or reworded. Each is listed in `data/site.json` under `unverifiedClaims`. See section 5. |
| C6 | Case study said the attacker was "based in Vietnam" (unverifiable, and it attributes conduct to a third party). | Fixed. Attribution removed. |
| C7 | Dinajpur case says the reporting party "allegedly demanded money". | Flagged. Kept at the owner's wording. Needs legal review (O2). |
| C8 | Case-study overstatement: "recoverable" in three takeaways, and "All requested objectives were successfully completed" as the Delicious Food result. | Fixed. Takeaways reworded. The result lists the outcomes already recorded in the case text. Owner to confirm (O3). |

### High

| ID | Finding | Status |
|---|---|---|
| H1 | Brand imagery: the hero image was a blank white PNG. The 20 OG images were byte-identical generic cards. Banners were identical. The favicon was a face crop that is unreadable at 16 px. Eleven illustrations were generic circles. | Fixed. Per-page OG cards with no face. AIR monogram favicon and app icons. Route motif. `assets/generated/` removed. |
| H2 | Two conflicting web manifests (root and `assets/generated/favicon/`). No 192 px or 512 px icons. | Fixed. One manifest, with 192 px and 512 px icons. |
| H3 | `favicon.svg` was referenced on every page and did not exist. | Fixed. Brand `favicon.svg` committed. 404 page corrected. |
| H4 | Missing `og:site_name`, `twitter:title`, and `twitter:image`. One shared `og:image` across pages. | Fixed. Every page has its own image, alt text, and Twitter tags. |
| H5 | Four titles over 70 characters. Nine meta descriptions outside 70–160. | Fixed. Checker warns above 65 characters for titles and outside 70–160 for descriptions. |
| H6 | 20 pages had `target="_blank"` without `rel="noopener noreferrer"`. | Fixed. No new-tab links remain. The checker enforces the rule. |
| H7 | Focus indicator was `outline: none` with a faint 45% box-shadow. | Fixed. 3 px solid focus outline from tokens, on light and dark surfaces. |
| H8 | Footer labels at 75% opacity failed WCAG AA contrast (axe `color-contrast`). | Fixed. Solid muted token, 8.4:1 on navy. QA caught and fixed one regression on navy cards. |
| H9 | Without JavaScript, all scroll-reveal sections were invisible (opacity 0). | Fixed. Content is hidden only when JS runs and motion is allowed. |
| H10 | Service pages had no "who it's for", process, required information, or limitations. | Fixed. All eight pages now have these, built from the existing copy. No guarantees. |
| H11 | Homepage first screen did not say who it is for or why to trust it. | Fixed. Hero names the person, the work, the audience, the limits, and the next step. Narrative: identity, trust band, expertise, services, proof, case studies, trust, CTA. |
| H12 | Structured data gaps: Article had no image or URL, no breadcrumbs, and inconsistent entity markup. | Fixed. One consistent `@graph` per page. `datePublished` omitted because dates are unknown (O7). |
| H13 | Contact form did not disclose third-party processing. | Fixed. Form footnote, notice, and FAQ state that Web3Forms processes messages. No passwords requested. |
| H14 | Owner photo: identity cannot be verified from the repo, and the magenta and violet lighting conflicts with the brief. | Flagged. Kept unaltered, resized only. Replacement recommended (O1). |
| H15 | `RELEASE.md` claimed "audited", "all links resolve", and "21 pages". Findings above contradict these. | Fixed. Rewritten with an accurate verification list. |
| H16 | Client names (Zero Idea, Delicious Food by Arpa) published with no recorded permission. | Flagged. Kept, since this is the owner's choice. Permission needed (O3). |

### Medium

| ID | Finding | Status |
|---|---|---|
| M1 | CSS: duplicated and dead selectors, avatar-only rules, opacity-based colour, and `!important` workarounds. | Fixed. Five stylesheets on one token set. `avatar.css` removed. Unminified CSS grew from about 24 KB to about 56 KB (gzip 5.8 KB to 10.7 KB) because of new components and comments (section 6). |
| M2 | Mobile navigation differed between the homepage (accordion) and other pages (flat list). | Fixed. One structure everywhere. |
| M3 | Desktop Services submenu: Escape did not close it and there was no `aria-expanded`. | Fixed. Disclosure button with `aria-expanded`, Escape, and click-outside. Hover opens on pointer devices (CSS). |
| M4 | 36 images lacked `loading="lazy"`; 42 lacked width and height. | Fixed. Lazy loading on all images. Width and height on every image. |
| M5 | Google Fonts preconnect remained after self-hosting. | Fixed. Removed. |
| M6 | `.vscode/launch.json` pointed at another machine's absolute path. | Fixed. Points to localhost. |
| M7 | `scripts/generate-og-images.js` and `generate-illustrations.js` produced the retired assets. | Fixed. Both exit with a message pointing to `design/README.md`. `generate:favicon` now rebuilds PNG and ICO from the committed SVG. |
| M8 | Sitemap comment referenced `Master-Blueprint-Final.md`, which is not in the repo. | Fixed. Sitemap regenerated: 20 URLs with `lastmod`. |
| M9 | Technical skills risked looking like the primary positioning. | Fixed. Positioned as supporting, in About, the homepage expertise note, and the portfolio copy. Header navigation unchanged. Portfolio stays in the footer. |
| M10 | `data/*.json` were not used by the site, so they drifted. | Flagged. Now the content record, updated to match the pages. HTML is canonical (O8). |

### Polish

| ID | Finding | Status |
|---|---|---|
| P1 | Typography. | Fixed. Fraunces for display, Inter for UI and body, fluid scale, balanced headline wrapping. |
| P2 | Visual direction. | Fixed. Navy, steel, and teal palette, neutral shadows, route motif. No neon, glow, padlocks, Matrix effects, masks, or fake terminals. |
| P3 | Motion. | Fixed. Subtle reveal, hover lift, header hairline on scroll. All motion is off under `prefers-reduced-motion`. |
| P4 | Inner pages had no breadcrumbs or quick facts. | Fixed. Breadcrumbs with structured data. "At a glance" panels. |
| P5 | Footer had no trademark or independence note. | Fixed. States the site is independent and not affiliated with Meta Platforms, Inc. |
| P6 | `prompts/` describes the retired image pipeline. | Flagged. Marked as superseded. |

## 4. What changed

- **Fixed:** items C1–C8, H1–H16, M1–M10, P4–P5 above.
- **Redesigned:** homepage narrative, service template, case-study template (one system for all five), contact page, navigation (mobile and desktop), FAQ and About layout.
- **Regenerated:** 20 OG cards (`assets/img/og/*.jpg`, from `design/og-template.html`). Brand icon set (`assets/brand/`). Root and brand `favicon.ico`. `sitemap.xml`, `robots.txt`, `site.webmanifest`, `404.html`, and the 21 HTML pages.
- **Replaced:** the header and footer logo (now a 96 px WebP of the owner photo, with a monogram for favicons and app icons). The hero image (now a route motif SVG). Fonts (now self-hosted).
- **Removed:** `assets/generated/` (blank, duplicate, generic images and a second manifest). `css/components/avatar.css`. `js/modules/avatar.js`. The owner's original photo is archived, unchanged, at `assets/source/profile-original-512.png` and is not referenced by the site.
- **Kept:** `CNAME`, the custom domain, every directory route, `robots.txt`, `google0a2814688d6877bf.html` (byte-identical), the GTM container `GTM-PHVGHCMT`, the Facebook app ID, the Web3Forms access key, and the existing service and case-study structure.

## 5. Claims removed or changed

| Claim (old site) | Action | Reason |
|---|---|---|
| 300+ clients served | Removed | Cannot be verified from the repository. |
| 20+ countries worked with | Removed | Cannot be verified. |
| 100+ accounts recovered | Removed | Cannot be verified. Also implies outcome rates. |
| 30+ Business Managers recovered | Removed | Cannot be verified. |
| Upwork 100% Job Success | Removed | A platform metric that changes. The profile link is kept. |
| "Globally recognized" digital security brand (vision) | Reworded | Superlative. |
| "Direct experience recovering hacked and restricted Business Managers" | Reworded | Experience claim that needs owner confirmation (O6). |
| Attacker "based in Vietnam" (Zero Idea) | Removed | Unverifiable attribution. |
| "Recoverable" outcomes in takeaways | Reworded | Overpromise. |
| UAE client in Dubai, reference to a "Master Blueprint" | Generalized to "Middle East", confidentiality note | Identifying detail and an internal document reference. |
| Zero Idea: over 400,000 followers; public video | Kept, flagged | Owner's record. Evidence needed before republishing (O3). |
| Delicious Food: "All requested objectives…" | Replaced with the specific outcomes already in the case text | Vague outcome. Owner to confirm (O3). |

## 6. Weight and performance (measured)

| Asset | Before | After |
|---|---|---|
| Fonts | 2 requests returned 404 (fallback fonts) | 81.7 KB, preloaded (Inter 48 KB, Fraunces 33 KB) |
| CSS | 23.8 KB unminified, 5.8 KB gzipped | 55.7 KB unminified, 10.7 KB gzipped (new components, comments, and a page stylesheet) |
| JavaScript | 8.6 KB unminified, 3.2 KB gzipped (3 files) | 11.0 KB unminified, 3.6 KB gzipped (2 files) |
| Homepage HTML | 20.6 KB | 32.8 KB (adds structured data and sections) |
| Service page HTML | 14.8 KB | 27.8 KB |
| Header and footer image | 378 KB 512 px PNG on every page | 2.7 KB WebP (96 px) in the header; 21.8 KB WebP (480 px) for the About page and homepage teaser |
| Hero image | 10 KB blank PNG | 1 KB SVG |
| OG images | 1.1 MB total: 20 JPGs byte-identical, plus a 943 KB portrait card | 1.4 MB total, 20 distinct cards. Only social crawlers fetch them. |

Lazy loading is set on all images. Fonts are preloaded. There are no third-party requests except GTM. The GTM container was kept as it was.

## 7. Verification

**Performed:**

- `npm run check`: 22 HTML files, 20 sitemap URLs, every local reference, canonical, `og:url`, and absolute URL resolves to a file, JSON-LD parses, one `<h1>` per page, no heading level skips, alt on every image, no duplicate IDs, every `aria-*` and label reference resolves, no inline event handlers, no placeholder text, CSS `url()` assets exist, JSON files parse. Result: no errors.
- Browser audit at nine widths (320–1440) across 21 pages: **no horizontal scroll** at any width. **axe-core 4.14: 0 violations** (WCAG 2.2 AA and best-practice rules). Console errors come only from the blocked GTM request, because this sandbox blocks external hosts. One automated check flags `favicon.svg` by substring; the file exists at `/assets/brand/favicon.svg` and the checker resolves it.
- Interaction tests in Chromium: mobile menu (open, close, Escape, focus return, scroll lock, Tab out of an open menu, and Tab from a closed menu leaves it); desktop submenu (click opens, Escape closes, focus returns); contact form (empty submit shows four errors and focuses the first field; invalid email and short message show specific text; honeypot bot-path sends nothing and shows success; valid submit sends the access key and subject with no honeypot field and shows success; mocked server failure shows the error alert and keeps the form; `?service=` pre-selects the service); no-JavaScript fallbacks (form hidden, email and WhatsApp shown, content visible, mobile menu opens); reduced motion (no hidden reveal state); 3 px focus outline after keyboard navigation; no JavaScript errors.
- Visual review: homepage at 1440 px and 390 px.

**Not performed:**

- Live delivery through Web3Forms. The sandbox cannot reach `api.web3forms.com`, so the mock was used.
- Hover opening of the desktop submenu. Headless Chromium reports no hover capability, so this path is verified by reading the CSS only.
- Real devices (iOS Safari, Android Chrome), Firefox, Safari, and other engines.
- Screen reader testing (NVDA, JAWS, VoiceOver).
- Lighthouse and PageSpeed scores, Google Rich Results Test, and Search Console.
- The live domain after deployment.
- Visual review of templates other than the homepage. They passed automated checks, not a manual look.

## 8. Visual direction and AI-image audit

**Direction.** Calm, precise, and human: navy `#0F2A4A` for text, bands, and buttons; steel `#1B4965` for hover states; teal `#2EC4B6` as an accent on dark surfaces, with `#0B6E65` for teal text on light surfaces. Off-white backgrounds. Fraunces for headlines, which reads as human and editorial. Inter for interface and body text, which reads as precise. A faint dot grid and a route motif suggest a process without cyber clichés.

**AI-image audit.**

| Asset | Finding | Decision |
|---|---|---|
| `hero-home.png` | Blank white (one colour). | Retired. Replaced by a route-motif SVG. |
| `og-home.png` | Stylized portrait with magenta and blue rim light, glowing circle, serif text. Identity unverifiable. Conflicts with the brief. | Retired. |
| 20 OG JPGs | Byte-identical generic navy card. | Replaced by 20 distinct cards rendered from `design/og-template.html`. No face, no AI imagery. |
| Banners (case-studies hub and 5 case studies) | Identical navy gradients with circles. | Retired. |
| 11 service and about illustrations | Generic circles and lines, not specific to any service. | Retired. |
| `android-chrome-512x512.png` (header, footer, about) | Owner photo, circle-cropped. Identity cannot be verified from the repo. | **Kept unaltered** (resize and compress only). Replacement recommended (O1). |

No AI-generated image of the owner was created. No face was generated, retouched, or altered. The owner's photo is the only person image on the site.

**Photo policy.** Use only a real photo of the owner. Resize and compress only. Do not generate, beautify, or alter the face, skin, hair, or proportions. Recommended replacement: a neutral, well-lit, recent headshot on a plain background, supplied by the owner.

## 9. Owner decisions and open items

| ID | Priority | Decision needed |
|---|---|---|
| O1 | High | Replace the profile photo with a neutral, real headshot. Re-export `assets/img/profile-96.webp` and `profile-480.webp`, and keep the alt text. |
| O2 | High | Legal review of the Dinajpur line "reporting party allegedly demanded money". It is kept at the owner's wording. |
| O3 | High | Confirm permission to name Zero Idea and Delicious Food by Arpa. If not confirmed, anonymize them the way the UAE case is anonymized. Also confirm the Zero Idea follower count and video reference, and the Delicious Food outcomes list. |
| O4 | Medium | Confirm the UAE result ("The Business Manager was verified") with a screenshot or written confirmation. |
| O5 | High | Confirm the Web3Forms access key is active for `help.atikulislam@gmail.com`, then send one test message from the live site. |
| O6 | Medium | Confirm the wording of process and experience statements: "I reply by email", "I don't ask for passwords", the "direct experience" line (removed), and the reworded vision. |
| O7 | Low | Provide publication dates for the case studies. Article `datePublished` is currently omitted. |
| O8 | Medium | **Proposal, not implemented:** make `data/*.json` the source for the HTML through a small generator, instead of keeping them in sync by hand. This is a stack and tooling decision, so it needs approval. |
| O9 | Medium | **Proposal, not implemented:** restore any headline statistic only with a documented source. The four counters are not restored. |
| O10 | Low | **Proposal, not implemented:** a testimonials or client-logos section. None exist in the repo, and none were created. Add only with written consent. |

## 10. Next steps

1. Owner decisions O1–O6, in priority order.
2. Merge the branch, deploy through GitHub Pages, then check `https://atikulislam.me`, the 404 page, `sitemap.xml`, `robots.txt`, and that `google0a2814688d6877bf.html` is still served. Resubmit the sitemap in Search Console.
3. Run `npm run check` before every content change. Test the contact form once on the live site.
4. Optional: run Lighthouse on the live homepage and one case study on mobile, and the Rich Results Test on the FAQ and a case study.
5. If the owner approves O8, plan the generator as a separate change.

## Files most affected

`index.html`, `about/`, `services/` (hub and 8 pages), `case-studies/` (hub and 5 pages), `faq/`, `contact/`, `portfolio/`, `404.html`, `css/` (5 files), `js/main.js`, `js/modules/form.js`, `data/` (5 files), `assets/brand/`, `assets/fonts/`, `assets/icons/`, `assets/img/`, `design/`, `scripts/check-site.mjs`, `scripts/generate-favicon.js`, `sitemap.xml`, `robots.txt`, `site.webmanifest`, `favicon.ico`, `README.md`, `RELEASE.md`, `docs/`.
