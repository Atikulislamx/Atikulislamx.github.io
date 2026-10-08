# atikulislam.me

Personal and company site for **Atikul Islam Rabbi**, Social Media Security & Recovery Specialist and Founder & CEO of Cyber Infinity. Published with GitHub Pages at <https://atikulislam.me> (see `CNAME`).

The site is plain static files: HTML, CSS, vanilla JavaScript, and JSON. There is no framework and no build step needed for deployment. The committed HTML is what gets published.

## Quick start

```bash
# Preview locally (any static server works)
python3 -m http.server 8080      # then open http://localhost:8080

# Optional: install dev tools for the asset scripts
npm install
npm run check                    # validate links, metadata, sitemap, JSON-LD, headings, and alt text
```

Run `npm run check` before every commit. It exits with an error when a local link is broken, a canonical or sitemap entry is wrong, JSON-LD does not parse, a heading level is skipped, an image has no alt text, a new-tab link lacks `rel="noopener noreferrer"`, or placeholder text remains.

## Structure

| Path | What it is |
|---|---|
| `index.html` | Homepage: identity, expertise, services, proof, case studies, trust, CTA |
| `about/`, `faq/`, `portfolio/`, `contact/` | Inner pages |
| `services/` | Service hub and eight service pages (same template) |
| `case-studies/` | Case-study hub and five case studies (same template) |
| `404.html` | Not-found page (`noindex`) |
| `css/base.css` | Design tokens (colour, type, spacing, radius, motion), fonts, focus, reduced motion |
| `css/layout.css` | Containers, grids, header and navigation, breadcrumbs, footer |
| `css/components.css` | Buttons, cards, chips, alerts, forms, FAQ disclosure, steps, facts, CTA band |
| `css/pages/home.css`, `css/pages/content.css` | Homepage-only styles; styles for all other pages |
| `js/main.js` | Header state, scroll reveal, desktop submenu, mobile menu. Each part is optional. |
| `js/modules/form.js` | Contact form: validation, honeypot, submit states, prefill from `?service=` |
| `assets/brand/` | Favicons, app icons, and the AIR monogram (`favicon.svg` is the source) |
| `assets/fonts/` | Self-hosted Inter and Fraunces (SIL OFL 1.1) with licences |
| `assets/icons/` | Icon sprite built from Lucide (ISC licence) |
| `assets/img/` | Profile photo (WebP), route motif, Open Graph cards (`og/`) |
| `assets/source/` | Original owner photo, archived. Not referenced by the site. |
| `design/` | OG card template and card list. See `design/README.md`. |
| `data/` | Content record: site identity, services, case studies, FAQ, pages. HTML is canonical; keep these in step. |
| `docs/` | Audit report, deployment checklist, asset notes |
| `scripts/` | `check-site.mjs` (validator), `generate-favicon.js` (rebuilds PNG and ICO from the SVG) |
| `prompts/` | Retired image-generation specs, kept for reference |
| `CNAME`, `robots.txt`, `sitemap.xml`, `site.webmanifest`, `favicon.ico` | Site-level files. Do not rename or move. |
| `google0a2814688d6877bf.html` | Search Console verification file. Keep unchanged. |

## Editing content

- **Edit the HTML directly.** The pages are canonical.
- **Keep `data/*.json` in step.** It is the content record for services, case studies, and FAQ.
- **Adding a page:** add it to `sitemap.xml`, give it a canonical, and run `npm run check`.
- **Adding a case study:** follow the eight-part structure (Problem, Situation, Challenge, Approach, Work, Result, Service, Limitations). Name no client without permission, or anonymize. Do not publish results you cannot document.
- **Claims:** do not add statistics, testimonials, client names, certifications, or partnerships without evidence. `data/site.json` lists the claims that were removed and why.
- **Colour and type:** change tokens in `css/base.css`, not individual rules.
- **Images:** use real photos of the owner only, resized and compressed, never generated or retouched. See `docs/audit-2026.md` section 8.

## Contact form

The form posts to Web3Forms with a public access key (`js/modules/form.js`). The key is designed for browser use and is not a secret. Nothing is stored in the browser. Without JavaScript, the form is hidden and the email and WhatsApp details are shown instead.

## Limits

- This site describes services. It does not guarantee any recovery outcome.
- It is independent and not affiliated with Meta Platforms, Inc.
