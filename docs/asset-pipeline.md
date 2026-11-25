# Asset pipeline

Everything the browser loads is a committed static file. There is no runtime build; the Python scripts run on a workstation and their output is committed.

## Fonts and icons

- `assets/fonts/inter-latin-var.woff2` — Inter variable (SIL OFL 1.1, `LICENSE-Inter.txt`). One file covers 400–800, so a second family was dropped.
- `assets/icons/sprite.svg` — Lucide (ISC), `<symbol id="i-…" viewBox="0 0 24 24">`. Referenced as `<svg class="icon"><use href="/assets/icons/sprite.svg#i-play"></use></svg>`. Adding an icon means adding a symbol; the markup only ever references existing ids (checked by `check-site.mjs`).
- `assets/brand/` — the AIR monogram favicon (SVG source), 16/32 PNG, 180 Apple touch icon, 192 and 512 maskable icons, plus `/favicon.ico` at the root for legacy clients.

## Open Graph cards

`scripts/generate_og.py` renders every card and the hero portrait:

```bash
pip install Pillow fontTools brotli   # build-time only
python3 scripts/generate_og.py
```

- 1200×630 JPEGs in `assets/img/og/` — one per page, service, case study and blog post (29 in total).
- The card list is derived from the same metadata the pages use (`META`, `SERVICES`, `CASES`, `POSTS`), so a title change is picked up on the next run.
- Type is Inter (converted from the site's woff2 at build time), against an obsidian ground with cyan and emerald ambient light and a hairline grid — the same language as the site.
- The portrait is exported from `assets/_source/profile-original-512.png` to `assets/img/atikul-islam-rabbi-social-media-security-expert.jpg`. Do not retouch the face.

## What was removed

The Fraunces display font, the second WebP portrait set, the route motif, the duplicate brand `favicon.ico`, five stylesheets and the Node/sharp asset scripts. They were superseded by the design system, by one portrait and one CSS file, and by the Python renderer above.
