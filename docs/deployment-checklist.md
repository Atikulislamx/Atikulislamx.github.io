# GitHub Pages deployment checklist (October 2026)

The static assets are committed. **No image API, font download, npm install, build step, or server-side runtime is needed for Pages.** See [site-audit-2026.md](site-audit-2026.md) for the completed code audit and test coverage.

- [ ] Merge the changes to the branch actually configured as the Pages source. Keep `CNAME` (`atikulislam.me`) and the `/` root deployment intact.
- [ ] Confirm DNS, TLS and custom-domain configuration in GitHub Pages. Verify the live homepage plus all service and case-study routes (including the custom 404 page).
- [ ] Send one **non-sensitive** contact form test from the deployed domain, verify its arrival, and configure Web3Forms allowed domains, spam controls and notifications. Do not share passwords/one-time codes through the form.
- [ ] Confirm published client names, case outcomes, externally linked profiles and the older statements in `data/case-studies.json`; keep the UAE case anonymized without explicit approval.
- [ ] Review Google Tag Manager's privacy/consent settings for the homepage; do not assume the analytics configuration is complete.
- [ ] Run Lighthouse/Core Web Vitals on the live domain and manually verify keyboard, screen-reader, touch and viewport behavior on physical devices. Submit `https://atikulislam.me/sitemap.xml` to Search Console.
- [ ] If the portrait is replaced, use only an authentic photo provided/approved by the owner. Update both `data/site.json` and the static HTML fallback; do not generate a synthetic likeness.

Run `python3 scripts/check-site.py` before merging. Do not run the legacy image pipeline with `--force` on the new artwork.
