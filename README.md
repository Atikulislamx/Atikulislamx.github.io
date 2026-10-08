# Atikul Islam Rabbi — professional portfolio

Static personal authority site for **Atikul Islam Rabbi**, Social Media Security & Recovery Specialist and Founder & CEO of Cyber Infinity. Production domain: https://atikulislam.me/ (`CNAME`).

## Site map and deployment

The committed `index.html`, `about/`, `services/` (eight detail pages), `case-studies/` (five detail pages), `portfolio/`, `faq/`, `contact/`, and `404.html` are directory-based routes. Shared CSS lives in `css/`, JavaScript in `js/`, source content in `data/`. `sitemap.xml`, `robots.txt`, and `site.webmanifest` are served directly. GitHub Pages needs **no Node install, framework, backend, or build step**; leave the custom domain and root-relative asset paths intact.

To preview locally: `python3 -m http.server 8080 --bind 0.0.0.0`, then visit http://localhost:8080/. The contact form submits to Web3Forms through `js/modules/form.js`; its public access key is not a private API secret. Set form domain restrictions and notifications in Web3Forms, and use an email link as fallback if the service is down.

## Editing

- Keep service outcomes conditional on Meta's decisions and available evidence. Avoid claims that have not been substantiated.
- The existing photograph is reused without identity modification. `data/site.json` can point to a genuine replacement image, but the HTML static fallback should also be updated.
- Editorial images are already committed. `docs/asset-pipeline.md` explains the visual system and the optional reproducible artwork script. **Do not run the legacy AI asset pipeline with `--force` on production artwork.**
- `docs/site-audit-2026.md` records the audit, fixes, limitations, and QA checklist.

## Contact

Email: help.atikulislam@gmail.com · WhatsApp: https://wa.me/8801300228105
