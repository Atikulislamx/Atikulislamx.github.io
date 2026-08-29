# atikulislamx.github.io

Personal portfolio and agency site for Atikul Islam Rabbi — Founder & CEO of Cyber Infinity. This repository contains the static site sources (HTML/CSS/JS) plus a small Node-based build-time asset pipeline for generating favicons and Open Graph images.

Live site: https://atikulislam.me/ (CNAME present)

## Features
- Static, fast, and accessible HTML/CSS/vanilla JS (no framework runtime)
- Build-time image generation & optimization (sharp, svgo)
- Structured data (JSON-LD), Open Graph & Twitter Card metadata
- Responsive design, accessible navigation, and small client-side interactions (mobile nav, scroll reveal)
- Case studies, services, and contact pages for lead generation

## Quick start (local)
Requirements: Node.js >= 18, npm

1. Install dependencies
   ```
   npm ci
   ```

2. Generate build-time assets (favicons, OG images):
   ```
   npm run generate:assets
   ```

3. Serve the directory (any static server). Example:
   ```
   npx http-server -c-1 . -p 8080
   ```

Visit http://localhost:8080 to preview.

## Scripts
- `npm run generate:assets` — runs `scripts/build-assets.js` to generate images.
- `npm run generate:assets:force` — force re-generate assets.
- `npm run generate:favicon` — generate favicons.
- `npm run generate:og` — generate Open Graph images.

## Repo layout
- `index.html`, `about/`, `case-studies/`, `services/` — static HTML pages
- `css/` — stylesheets (base, layout, components)
- `js/` — client JavaScript modules
- `data/` — site data used by client scripts (e.g., `site.json`)
- `scripts/` — Node scripts for build-time asset generation
- `assets/` — generated images & favicons (output)

## Deployment
This project is designed for GitHub Pages:
- Push to the default branch (main) — GitHub Pages will serve the site.
- A `CNAME` file is included for the custom domain `atikulislam.me`.

If you prefer to build assets on CI instead of committing generated files:
- Add a GitHub Actions workflow that runs the generate script and commits the assets to the branch used for Pages, or deploy to a static hosting provider after generation.

## Contributing
- Open an issue for discussion before making major changes.
- For minor fixes, fork and submit a pull request.
- If you change code that affects `scripts/` or `package.json`, include a short note about the Node.js version and commands used to test.

## License
Add your preferred license here (e.g., MIT). If the repository contains business-sensitive content you don't want to license, keep the repository's default terms and document them here.

## Contact
- Email: help.atikulislam@gmail.com
- WhatsApp: https://wa.me/8801300228105
- GitHub: https://github.com/atikulislamx
