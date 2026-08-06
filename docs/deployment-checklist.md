# Deployment Checklist — GitHub Pages

Everything code-side is complete and QA-verified (see `RELEASE.md`). These are the remaining **manual, external** steps — none require further code changes.

## 1. Visual assets (blocking — pages will show broken images without this)
- [ ] `npm install` inside the project root
- [ ] Copy `.env.example` → `.env`, fill in a real image-generation provider's `IMAGE_API_URL` / `IMAGE_API_KEY`
- [ ] Adjust the response-parsing block in `scripts/lib/image-generator.js` to match that provider's actual response shape (the one documented provider-specific integration point — see `docs/asset-pipeline.md` §5)
- [ ] Run `npm run generate:assets`
- [ ] Confirm the run ends with "✔ Asset pipeline completed successfully." and `assets/generated/assets-manifest.json` lists ~43 files

## 2. Fonts
- [ ] Either supply real `.woff2` files at `assets/fonts/inter-variable.woff2` and `assets/fonts/fraunces-variable.woff2` (referenced in `css/base.css`), or replace the `@font-face` blocks with a Google Fonts `<link>` in every page's `<head>`

## 3. Contact form
- [ ] Create a free Web3Forms account and access key at web3forms.com
- [ ] Replace `WEB3FORMS_ACCESS_KEY` in `js/modules/form.js` with the real key
- [ ] Submit a real test message from `/contact/` once deployed and confirm it arrives

## 4. Domain
- [ ] Every canonical URL, Open Graph URL, JSON-LD `@id`, `robots.txt`, and `sitemap.xml` currently uses the placeholder `REPLACE-WITH-YOUR-DOMAIN.example` — find-and-replace with the real domain across all files before going live
- [ ] If using a custom domain: add a `CNAME` file at the project root containing the domain
- [ ] If staying on `<username>.github.io`: update the placeholder to that URL instead

## 5. GitHub Pages setup
- [ ] Push the repository to GitHub
- [ ] Repo Settings → Pages → set source to the branch/folder this site lives in
- [ ] If using a custom domain, configure DNS (A records or CNAME per GitHub's docs) and confirm HTTPS is enforced once the cert issues

## 6. Post-deploy verification
- [ ] Load every one of the 21 pages live and confirm no 404s on CSS/JS/images
- [ ] Validate structured data on a few key pages (Home, one service, one case study) with Google's Rich Results Test
- [ ] Submit `sitemap.xml` in Google Search Console
- [ ] Run Lighthouse against the live Home page (Performance / Accessibility / SEO / Best Practices)
- [ ] Confirm the favicon renders correctly in a browser tab

## 7. Optional, not blocking launch
- [ ] Replace the CSS monogram avatar with a real profile photo via `data/site.json`'s `profilePhoto` field (local path or URL — no code change needed)
- [ ] Add real testimonials once available (component is built, simply unused until content exists)
- [ ] Confirm client approval on the anonymized Business Manager Verification (UAE) case study, or keep it anonymized indefinitely
