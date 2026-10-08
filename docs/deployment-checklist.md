# Deployment checklist

The site deploys from the repository through GitHub Pages. No build step runs at deploy time. Committed HTML is published as it is.

## Before merging

- [ ] `npm run check` reports no errors.
- [ ] **O5 Contact form:** confirm the Web3Forms access key `437ef875-ee27-44e0-9884-22910c26316b` is active for `help.atikulislam@gmail.com`. After deployment, send one test message from `/contact/` and confirm it arrives. The sandbox could not test delivery.
- [ ] **O1 Profile photo:** replace the owner photo with a neutral, real headshot if one is available. Re-export `assets/img/profile-96.webp` (96 px) and `assets/img/profile-480.webp` (480 px) from the original. Keep the alt text. Do not generate, beautify, or retouch.
- [ ] **O2 Legal review:** the Dinajpur line "reporting party allegedly demanded money" (`case-studies/dinajpur-image/`).
- [ ] **O3 Client permissions:** confirm permission to name Zero Idea and Delicious Food by Arpa, or anonymize them. Confirm the Zero Idea follower count and video reference, and the Delicious Food outcomes.
- [ ] **O4:** confirm the UAE verification result with a screenshot or written confirmation.
- [ ] **O6 Wording:** confirm "I reply by email", "I don't ask for passwords", and the reworded vision statement.

## After merging

- [ ] Confirm the custom domain and HTTPS still point at `atikulislam.me` (`CNAME` is unchanged).
- [ ] Open `https://atikulislam.me/`, one service page, one case study, `/contact/`, and an unknown URL (404 page).
- [ ] Check `https://atikulislam.me/sitemap.xml`, `/robots.txt`, `/site.webmanifest`, and `/google0a2814688d6877bf.html`.
- [ ] In Search Console, resubmit `sitemap.xml`. Request re-indexing for the homepage and the case studies.
- [ ] Share one page on Facebook and LinkedIn with a debugger, and confirm the OG card and title.
- [ ] Optional: run Lighthouse on mobile for the homepage and one case study. Run the Rich Results Test on the FAQ and one case study.

## Operational notes

- Content changes: edit the HTML and keep `data/*.json` in step. Run `npm run check`.
- New or removed pages: update `sitemap.xml`. The checker fails when an indexable page is missing from it.
- Changed copy on an OG card: re-render the card (see `design/README.md`) and commit the JPG.
- Do not add statistics, client names, testimonials, or partnerships without evidence and permission.
