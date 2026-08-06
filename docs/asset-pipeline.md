# Visual Asset Pipeline
## `/docs/asset-pipeline.md`

This is the operational reference for the automated visual asset generation system. It complements (not replaces) `prompts/README.md`, `Image-Asset-Policy-v1.md`, and `Asset-Manifest-v1.md` — those define *what* to generate and in what style; this document defines *how the pipeline runs*.

---

## 1. Architecture

```
prompts/                        Asset specs (JSON) — the single source of truth for
                                 what gets generated, organized by category/directory
  _style-constraints.json       Shared palette + "avoid" rules, appended to every prompt
  hero/ services/ case-studies/
  dividers/ cta/ portfolio/
  about/ empty-states/ og/

scripts/
  lib/
    image-generator.js          Provider-agnostic AI image API adapter
    shared-style.js              Loads _style-constraints.json
    svg-optimizer.js             SVGO wrapper (preserves layer IDs)
    raster-optimizer.js          sharp wrapper (WebP + JPEG output)
    validator.js                  Dimension/format/size-budget/well-formedness checks
    manifest.js                   Builds assets-manifest.json with checksums
  generate-illustrations.js     Generates every SVG/banner asset under /prompts (except og/)
  generate-og-images.js          Generates the OG base template once + per-page composites
  generate-favicon.js            Deterministic favicon generation (no AI call)
  build-assets.js                Top-level orchestrator — the single entry point

data/
  site.json                     profilePhoto field + site metadata
  pages.json                    Real page titles/slugs, used to generate accurate per-page OG images

src/
  css/components/avatar.css     CSS monogram avatar (default, non-AI)
  js/modules/avatar.js           Swaps monogram → real photo when site.json.profilePhoto is set

assets/generated/               Pipeline output (gitignored raw intermediates; final optimized
                                 assets + assets-manifest.json are the build artifacts)
```

**Data flow for one asset:** `prompts/<category>/<id>.json` → `image-generator.js` (calls the configured provider, with style constraints auto-appended) → format-specific optimizer (`svg-optimizer.js` or `raster-optimizer.js`) → `validator.js` (gate) → written to `assets/generated/<destination>/` → recorded → included in `assets-manifest.json`.

**OG images are the one deliberate exception** to "one spec = one generation call": a single AI-generated base template is reused for every page, with each page's real title composited on top *deterministically* (not by the AI model) — see `prompts/og/base-template.json` for the reasoning.

**Favicon and the avatar default are the other two exceptions** — both produced without any AI call, documented in `prompts/README.md`.

---

## 2. Workflow

### Running the full pipeline

```bash
npm install
cp .env.example .env      # configure your provider — see Section 4
npm run generate:assets
```

This runs, in order: favicon → illustrations/banners → OG images, then validates and writes the manifest.

### Incremental behavior

By default, an asset already present on disk is **skipped**, not regenerated — the pipeline is safe and fast to re-run repeatedly (e.g., after adding a tenth service page, only that new asset generates).

```bash
npm run generate:assets                    # incremental — only missing assets generate
npm run generate:assets -- --force         # regenerate everything
npm run generate:assets -- --type=services # only the services category
npm run generate:assets -- --type=og --force
npm run generate:assets -- --include-deferred   # also generate reserved future-phase assets
```

Valid `--type` values match the `/prompts` subdirectory names: `hero`, `services`, `case-studies`, `dividers`, `cta`, `portfolio`, `about`, `empty-states`, `og`, `favicon`, or `all`.

### What "deferred" means in practice

Assets belonging to not-yet-launched sections (Blog, Resources, Testimonials, Media & Recognition) have `"deferred": true` in their spec and are skipped by default — they do not block a build and are not counted as "missing required assets." Run with `--include-deferred` only when that section of the site is actually being built.

---

## 3. Validation Gate

Every generated asset is checked before the build accepts it:

| Check | Applies to | Failure behavior |
|---|---|---|
| Dimensions match spec | Raster (banners, OG) | Record marked `failed` |
| Well-formed SVG / has `viewBox` | SVG | Record marked `failed` |
| Named layer groups present (`layer-bg`, `layer-mid`, `layer-accent`) | SVGs with `"layered": true` | Record marked `failed` |
| File size within budget (SVG 20KB / banner 130KB / OG 150KB / favicon 10KB) | All | Record marked `failed` |
| Output file(s) actually exist | All | Record marked `failed` / triggers the missing-required-asset build failure |

A `failed` record is never silently swapped for a placeholder. `build-assets.js` exits with a non-zero status and prints exactly which asset(s) failed and why.

---

## 4. Configuration

Set in `.env` (see `.env.example`):

| Variable | Purpose |
|---|---|
| `IMAGE_API_PROVIDER` | Free-text label for logging only |
| `IMAGE_API_URL` | Full endpoint URL for your chosen provider's image generation API |
| `IMAGE_API_KEY` | Bearer token / API key |

If either `IMAGE_API_URL` or `IMAGE_API_KEY` is unset, `image-generator.js` throws immediately with an actionable error — it never falls back to producing a blank/placeholder file for a required asset.

---

## 5. Supported Providers

`scripts/lib/image-generator.js` is intentionally provider-agnostic: it POSTs a normalized `{ prompt, format, width, height }` request and expects a normalized `{ data, contentType }` response. **No specific vendor SDK is imported anywhere in the pipeline** — this satisfies the "provider replaceable through configuration only" requirement.

The one place that is necessarily provider-specific is the response-parsing block inside `generateImage()`, marked with a comment (`// Expected response contract...`). Different providers return results in different shapes (base64 payload vs. hosted URL vs. multipart), so this block should be adjusted to match whichever provider you configure — that's a few lines, not an architecture change, and every other file in the pipeline (optimizer, validator, manifest, orchestrator) is unaffected by which provider is chosen.

---

## 6. Adding a New Asset Type

1. Create `prompts/<category>/<new-id>.json` following the schema documented in `prompts/README.md`.
2. If it's a new *category* (new subdirectory), no code change is required — `generate-illustrations.js` walks `/prompts` recursively and derives the category from the directory name automatically, which also makes it immediately usable as a `--type=` filter value.
3. Run `npm run generate:assets -- --type=<new-category>`.
4. The new asset appears in `assets-manifest.json` automatically on the next full build.

If the new asset needs special handling (e.g., another deterministic/non-AI exception like the favicon), add a small dedicated script following the pattern in `generate-favicon.js` (build a record object with the same shape, call it from `build-assets.js`) rather than overloading `generate-illustrations.js`'s generic path.

---

## 7. Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| `IMAGE_API_URL and IMAGE_API_KEY must be set` | `.env` missing or not filled in — copy `.env.example` and configure your provider |
| Provider request fails with a 4xx/5xx | Check the logged status/body; likely an auth or malformed-request issue specific to your provider — see the response-parsing note in Section 5 |
| `Validation failed: Width mismatch...` | The provider returned an image at the wrong size — either request the correct size explicitly in your provider integration, or add a resize step before optimization |
| `Validation failed: ... layer group id="layer-bg" not found` | The provider didn't honor the layered-SVG instruction appended by `image-generator.js` — some providers need layer/group requests phrased differently; adjust the `layeredInstruction` string in `prompts/_style-constraints.json` |
| `SVG exceeds 20KB budget` | Source artwork is too detailed for an icon/illustration at this scale — simplify the prompt or increase the budget in `scripts/lib/validator.js` if the added detail is a deliberate choice |
| Build fails with "required launch assets are missing" | One or more non-deferred assets failed generation or validation — check the itemized list printed above the failure banner, fix the underlying issue, re-run |
| Want to regenerate just one asset | `npm run generate:assets -- --type=<category> --force` regenerates that whole category; deleting the specific output file(s) under `assets/generated/` and re-running without `--force` also works, since the pipeline is incremental |

---

## 8. Maintenance

- **Style changes** (palette, "avoid" list): edit `prompts/_style-constraints.json` once — every future generation call picks it up automatically, no per-spec edits needed.
- **New pages needing OG images**: add an entry to `data/pages.json`; `npm run generate:assets -- --type=og` picks it up on the next run.
- **Manifest drift checks**: `assets-manifest.json` includes a SHA-256 checksum per file — a CI step can re-hash files on disk and diff against the manifest to catch any asset edited outside the pipeline.
- **Provider migration**: update `.env` and the response-parsing block in `image-generator.js`; nothing else in the pipeline changes.
- **Every asset this pipeline can produce is enumerated in `Asset-Manifest-v1.md`** — that document stays the planning-level reference; this file and the code are the execution-level implementation of it. If the two ever disagree, treat that as a bug to reconcile, not a reason to trust one over the other silently.
