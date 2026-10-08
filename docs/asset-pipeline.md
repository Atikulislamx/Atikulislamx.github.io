# Asset pipeline

The site no longer uses the AI image-generation pipeline. The provider-based scripts (`scripts/build-assets.js`, `scripts/lib/`) remain in the repo for reference, but nothing in the current site depends on them, and `assets/generated/` has been removed.

## Where each asset comes from

| Asset | Source | How to regenerate |
|---|---|---|
| Favicons, app icons, `favicon.ico` | `assets/brand/favicon.svg` (monogram with outlined letterforms) | `npm install` then `npm run generate:favicon`. Copy `assets/brand/favicon.ico` to the repo root. |
| OG cards (`assets/img/og/*.jpg`) | `design/og-template.html` with `design/og-cards.json` | See `design/README.md`. |
| Profile photo (`assets/img/profile-96.webp`, `profile-480.webp`) | Owner photo, archived at `assets/source/profile-original-512.png` | Resize and compress only, with sharp or any image editor. Do not alter the face. |
| Route motif (`assets/img/route-motif.svg`) | Hand-written SVG | Edit the file directly. |
| Icon sprite (`assets/icons/sprite.svg`) | Lucide icons (ISC licence, `assets/icons/LICENSE-Lucide.txt`) | Rebuild from the Lucide package if icons are added. |
| Fonts (`assets/fonts/*.woff2`) | Fontsource packages `@fontsource-variable/inter` and `@fontsource-variable/fraunces` (SIL OFL 1.1) | Re-subset only if the character set changes. Licence files are in the same folder. |

## Retired

- `scripts/build-assets.js`, `npm run generate:assets`, and `npm run generate:assets:force`: the provider-based image pipeline. They need `IMAGE_API_URL` and `IMAGE_API_KEY` and write to `assets/generated/`, which no longer exists.
- `scripts/generate-og-images.js` (`npm run generate:og`) and `scripts/generate-illustrations.js`: retired. They exit with a message.
- `prompts/`: image specifications for the retired pipeline. Kept for reference only.

## Rules that still apply

- No AI-generated images of the owner. No generated or retouched faces.
- Images are resized and compressed, never restyled.
- Every image has alt text (decorative images use `alt=""`). Every image has width and height, and is lazy-loaded unless it is the header avatar.
- Colour follows `css/base.css` and `prompts/_style-constraints.json`: navy, steel, teal. No neon, glow, padlocks, Matrix effects, masks, or stock imagery.
