# Visual assets — current site

The deployed site is plain HTML/CSS/JS. All artwork is committed; GitHub Pages **does not run a build**.

## Current art direction

Navy / mineral teal / warm off-white; restrained typography, deliberate access-path geometry. No generated people, platform logos, hacker imagery, or fabricated product screenshots. The repository's original 512px avatar photograph is retained unchanged as `assets/images/atikul-islam-rabbi-source.png`. The served `assets/images/atikul-islam-rabbi.webp` is only re-encoded from it; it has **not** been retouched. Ask the owner before replacing it with a new genuine photograph. The 16px browser icon uses a brand monogram instead of a miniature face.

- Home visual: semantic HTML and CSS process graphic (`index.html`, `css/pages/home.css`), replacing a nearly blank white PNG.
- Service visual: semantic HTML and CSS steps (`services/*/index.html`, `css/pages/detail.css`), replacing eight virtually identical anonymous SVG networks. Text is page-specific and is not a platform promise.
- Case studies: five distinct, titled WebP banners (`assets/generated/banners/`), reusing one editorial layout with case-specific labels. 1600×600; on narrow screens only the decorative right geometry is cropped, keeping the left title readable. No client photographs are implied.
- Social cards: page-specific 1200×630 JPEG/PNG titles in `assets/generated/og/`; all OG URLs in HTML resolve to these assets.
- 404: the small directional-arrow SVG remains useful. Unused placeholder CTA, divider, supporting illustration, and duplicate JPEG banners were removed.
- Favicon: a coordinated A monogram set plus `favicon.ico` at the root and in `assets/generated/favicon/`; one active manifest at `/site.webmanifest`.

## Reproducing the committed editorial assets (optional)

Use Python 3 with Pillow and Beautiful Soup installed locally, then run `python3 scripts/render-editorial-assets.py` (or `npm run generate:assets` with Python dependencies available). It reads actual site titles/cases and writes the committed banners, OG cards, and icons. It does **not** create or modify the profile photograph. No key or remote AI provider is required. To manually optimize a replacement authentic profile photo, keep an unaltered copy and update `data/site.json` and the HTML fallback image consistently.

## Legacy pipeline

The preexisting `scripts/build-assets.js`, `scripts/generate-illustrations.js`, `scripts/generate-og-images.js`, and `scripts/generate-favicon.js` and their JSON prompts remain for historical reference. They rely on an optional image API and use the old generic visual direction. The package scripts for them are prefixed `legacy:`. Do **not** run `legacy:generate:assets:force` against the production assets without reviewing outputs: it can overwrite the new editorial system. Neither pipeline runs in GitHub Pages.
