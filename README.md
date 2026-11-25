# atikulislam.me

Personal and company site for **Atikul Islam Rabbi** — Social Media Security Expert, Founder & CEO of Cyber Infinity. Published with GitHub Pages at <https://atikulislam.me> (see `CNAME`).

The published site is plain HTML, one CSS file, one JavaScript file and static assets. The HTML is **generated** from a small Python build so that navigation, schema, metadata and card markup stay identical on every page — the committed output is what GitHub Pages serves (no build step runs at deploy time).

## The five commands

```bash
python3 scripts/build_site.py     # regenerate every page, sitemap, robots, manifest
python3 scripts/preview.py 8000   # preview with the _config.yml excludes enforced
python3 scripts/generate_og.py    # re-render the 29 OG cards + hero portrait (needs Pillow, fontTools)
node   scripts/check-site.mjs     # pre-publish validation — must print "no errors"
npm run release                   # build + check in one step
```

`check-site.mjs` fails on a broken local link, a missing or mismatched canonical, a sitemap entry without a file, a JSON-LD block without `@context`, an `@graph` reference that does not resolve, missing Open Graph or Twitter tags, a skipped heading level, a duplicate title or description, a raw `mailto:` link, a banned junior framing, or any published link into `docs/`, `prompts/`, `scripts/`, `data/` or `design/`.

## Structure

| Path | What it is |
|---|---|
| `scripts/site_lib.py` | Design-system and schema library: tokens, `head()`, header, footer, cards, `@graph` node builders |
| `scripts/build_site.py` | Page builders: home, about, services (8), case studies (5), portfolio, FAQ, contact, blog (6 posts), legal, 404, redirect, sitemap, robots, manifest |
| `scripts/content_blog.py` | Long-form article content for the insights hub |
| `scripts/generate_og.py` | Renders the 1200×630 OG cards and the hero portrait from `assets/_source/` |
| `scripts/check-site.mjs` | Pre-publish validator (zero dependencies) |
| `scripts/preview.py` | Local server that mimics GitHub Pages with the `_config.yml` excludes |
| `css/site.css` | The whole design system in one file: tokens, layout, components, pages, print |
| `js/main.js` | Header hairline, mega-menu, mobile drawer, reveal, YouTube facade, email obfuscation, contact form, channel tracking |
| `data/*.json` | Content sources: services, case studies, FAQ |
| `assets/` | Fonts (Inter, OFL), icons (Lucide, ISC), brand icons, portrait, OG cards |
| `_config.yml` | GitHub Pages publishing rules — keeps `docs/`, `prompts/`, `scripts/`, `data/` off the web |

Generated routes: `/`, `/about/`, `/services/` + 8 service pages, `/case-studies/` + 5 case files, `/portfolio/`, `/blog/` + 6 guides, `/faq/`, `/contact/`, `/privacy-policy/`, `/terms/`, `/404.html`, `/Atikulislamx/` (redirect stub).

## How publishing is scoped

`_config.yml` runs at deploy time on GitHub Pages and excludes the build inputs:

```yaml
exclude: [docs, prompts, scripts, design, data, README.md, RELEASE.md, package.json, ...]
include: [.well-known]
```

`assets/_source/` is ignored automatically (leading underscore) and also listed in the exclude block. `scripts/preview.py` applies the same rules locally, so a path that 404s in the preview will 404 in production.

## Client video testimonials

Four facade cards ship on the homepage and four on `/portfolio/`. Nothing loads from YouTube until the visitor presses play; the click swaps in a `youtube-nocookie` embed with `autoplay=1&rel=0`.

**To add a real video**, edit the `TESTIMONIALS` list in `scripts/build_site.py` and replace the placeholder:

```python
{"initials": "ZI", "client": "...", "brand": "...", "service": "...",
 "quote": "...", "yt": "YOUR_VIDEO_ID_HERE", "wide": False},
```

`yt` takes the 11-character ID from the watch URL (`youtube.com/watch?v=**dQw4w9WgXcQ**`). Set `"wide": True` for a 16:9 clip; leave it `False` for 9:16 Shorts. Then run `python3 scripts/build_site.py`.

Until an ID is set, clicking a card shows "Testimonial video publishing shortly — the written reference below stands" instead of a broken embed. You can also patch `data-youtube-id="..."` directly in the generated HTML, but the next build overwrites it.

## Contact form

`js/main.js` posts JSON to Web3Forms with the access key `437ef875-ee27-44e0-9884-22910c26316b`, a honeypot (`botcheck`), a 15-second `AbortController` timeout, and a `generate_lead` event pushed to `dataLayer` on success (with the chosen service). `?service=<slug>` preselects the topic; the generator and the script both honour it.

Email is base64-encoded in `data-email` attributes and assembled in the browser, which keeps harvesters from reading it out of the HTML. Without JavaScript the form is hidden and the direct channels remain.

## Editing content

1. Change the copy in `scripts/build_site.py` / `scripts/content_blog.py`, or the JSON in `data/`.
2. `python3 scripts/build_site.py`
3. `node scripts/check-site.mjs`
4. Commit the generated HTML with the source change.

Never hand-edit the generated pages: the next build replaces them.

## Deployment

GitHub Pages, `main`, `/` (legacy Jekyll build). `CNAME` keeps `atikulislam.me`; HTTPS is enforced. No plugins, no themes, no dependencies at runtime. See [docs/deployment-checklist.md](docs/deployment-checklist.md) for the post-deploy checks, and [docs/audit-2026-11.md](docs/audit-2026-11.md) for the audit this rebuild answers.

## Licences

Inter is licensed under the SIL OFL 1.1 (`assets/fonts/LICENSE-Inter.txt`). The icon sprite is derived from Lucide (ISC). All photographs and client marks belong to their respective owners.
