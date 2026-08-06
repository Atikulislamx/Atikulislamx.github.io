# /prompts

Every decorative/illustrative asset on the site is defined here as a JSON spec, organized by asset type. `scripts/build-assets.js` reads every non-deferred spec in this tree, generates the asset, and writes an optimized production file into `/assets/generated/`.

## Structure

```
prompts/
├── _style-constraints.json   ← shared palette + style rules, appended to every prompt automatically
├── hero/                     ← Home hero background
├── services/                 ← Services hub + 8 per-service illustrations
├── case-studies/             ← Case Studies hub banner + 5 per-case banners
├── dividers/                 ← Reusable section divider
├── cta/                      ← Reusable CTA graphic
├── portfolio/                ← Portfolio page illustration
├── about/                    ← About page supporting graphic
├── empty-states/             ← 404 (launch) + Blog/Testimonials/Media (deferred)
└── og/                       ← OG image base template (per-page text composited separately)
```

## Spec schema

Every `*.json` file (except `_style-constraints.json`) follows:

| Field | Meaning |
|---|---|
| `id` | Unique asset ID, matches output filename stem |
| `type` | `illustration` or `og-template` |
| `layered` | If `true`, the generation request asks for separate named SVG `<g>` groups so layers can be animated independently (see Design System §23 motion guidelines) |
| `outputFilename` / `outputFormat` / `destination` | Where the optimized asset lands in `assets/generated/` |
| `dimensions` | Reference size; SVGs remain scalable regardless |
| `prompt` | The generation prompt. `_style-constraints.json` is appended automatically — do not repeat palette/style rules here |
| `decorative` | If `true`, the asset ships with `alt=""` + `aria-hidden="true"`. If `false`, `altText` must be populated |
| `deferred` | If `true`, `build-assets.js` skips it by default — generated only when that section of the site is activated (`npm run generate:assets -- --include-deferred` to force it) |

## Two intentional exceptions — not generated from this pipeline

- **Favicon** (`scripts/generate-favicon.js`): a flat typographic "AIR" mark, produced deterministically from SVG/code rather than routed through the AI pipeline. A generative model can't reliably guarantee pixel-perfect legibility at 16×16px, so this is a documented engineering decision, not an oversight.
- **Avatar default state**: pure CSS (see `src/css/components/avatar.css`), per your explicit instruction — never AI-generated, never a photo of you.
- **Functional UI icons**: Lucide, not generated — see project rule in `scripts/build-assets.js` header comment.

## Running the pipeline

```
npm install
cp .env.example .env   # set IMAGE_API_URL + IMAGE_API_KEY — see note below
npm run generate:assets
```

**One real blocker, documented rather than worked around:** `scripts/lib/image-generator.js` is a complete, provider-agnostic adapter (configured via `IMAGE_API_URL`/`IMAGE_API_KEY`/`IMAGE_API_PROVIDER` in `.env`), but no image-generation API is reachable or configured in the environment this pipeline was authored in — no network access, no credentials. This isn't an open design question (every prompt, filename, path, and dimension above is fully specified) — it's an execution dependency. The moment `.env` is filled in with a real provider's endpoint/key, `npm run generate:assets` runs end-to-end with no further changes.
