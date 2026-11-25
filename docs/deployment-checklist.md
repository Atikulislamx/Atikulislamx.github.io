# Deployment checklist

GitHub Pages, branch `main`, folder `/` (legacy Jekyll build). The committed HTML is what gets published — nothing is compiled at deploy time. `_config.yml` only scopes what is allowed through.

## Before merging

- [ ] `python3 scripts/build_site.py` runs clean and the generated HTML is committed with the source change.
- [ ] `node scripts/check-site.mjs` prints `no errors`.
- [ ] `python3 scripts/preview.py 8000`, then check `/`, `/services/`, one service page, `/case-studies/`, `/portfolio/`, `/blog/`, `/contact/`, `/nope/` (404) and `/Atikulislamx/` (redirect).
- [ ] **YouTube IDs.** Paste the real 11-character IDs into `TESTIMONIALS[].yt` in `scripts/build_site.py`, set `wide` for 16:9 clips, rebuild. Until then a click shows the "publishing shortly" note instead of a broken embed.
- [ ] **O5 Contact form.** Confirm the Web3Forms access key `437ef875-ee27-44e0-9884-22910c26316b` is active for `help.atikulislam@gmail.com`, then send one test message after deploy.
- [ ] **O2 Legal review.** The Dinajpur case study now says the reports "were disputed" and that the review turned on proof of ownership and on how the claims were made. No allegation about the reporting party remains. Confirm the wording with the owner.
- [ ] **O3 Client permissions.** Confirm permission to name Zero Idea, Delicious Food by Arpa, and the seven clients on `/portfolio/`. The brand links point at their public sites only.
- [ ] **O4** Confirm the UAE verification result with a screenshot or written confirmation.
- [ ] **Portrait.** `assets/img/atikul-islam-rabbi-social-media-security-expert.jpg` is the owner photo at 512 px. The 4:5 frame crops it with `object-fit: cover`; replace the source at `assets/_source/profile-original-512.png` and re-run `python3 scripts/generate_og.py` if a better photograph arrives. Do not retouch.

## After merging

- [ ] Confirm the custom domain and HTTPS still point at `atikulislam.me` (`CNAME` unchanged).
- [ ] Confirm the internal documents are gone: `https://atikulislam.me/docs/audit-2026-11.md`, `/README.md`, `/RELEASE.md`, `/scripts/build_site.py`, `/data/services.json`, `/prompts/base.json` must all return **404**.
- [ ] Confirm `/.well-known/security.txt`, `/privacy-policy/`, `/terms/`, `/blog/`, `/Atikulislamx/`, `/sitemap.xml`, `/robots.txt`, `/site.webmanifest` all resolve.
- [ ] Search Console: resubmit `sitemap.xml`, and request removal of the old `/docs/` and `/README.md` URLs.
- [ ] GTM `GTM-PHVGHCMT`: preview the site, submit the contact form, confirm `generate_lead` fires with the `service` parameter, and map it to a conversion.
- [ ] Rich Results Test on `/`, `/faq/` and one `/blog/` post: expect Person, Organization, WebSite, WebPage, BreadcrumbList and FAQPage without errors.
- [ ] Share `/` and one case study through the Facebook and LinkedIn debuggers; confirm the 1200×630 card.

## Operational notes

- Content changes: edit `scripts/build_site.py`, `scripts/content_blog.py` or the JSON in `data/`, then rebuild. Never hand-edit generated HTML.
- New or removed pages: the builder writes `sitemap.xml` from the same list; the checker fails when an indexable page is missing from it.
- OG cards: re-render with `python3 scripts/generate_og.py` after a title change (needs Pillow and fontTools).
- Do not add statistics, client names, testimonials, badges or partnerships without evidence and permission.
