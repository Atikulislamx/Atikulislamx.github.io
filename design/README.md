# Design sources

## Open Graph cards

`assets/img/og/*.jpg` are 1200 × 630 cards used for social previews. Each page has its own card. There is no photo and no AI imagery on the cards.

- `og-template.html`: the card layout. It reads `kicker`, `title`, and `sub` from the query string. It is marked `noindex`. The template is not linked from the site.
- `og-cards.json`: the card list (slug, kicker, title, sub). It is written by the page build, so the text matches each page.

**To re-render a card**, open the template in Chromium at 1200 × 630, with the same query string as the card, and save a JPG at quality 88:

```
design/og-template.html?kicker=Services&title=Social%20media%20security%20and%20recovery%20services&sub=...
```

The card file name is the card's `slug` in `og-cards.json`. Use the same name in `assets/img/og/`. Then run `npm run check`.

Fonts and the route motif load from `/assets`, so render from the site root (for example, `python3 -m http.server 8080` from the repo root).

## Route motif

`assets/img/route-motif.svg`: a dot grid, two thin circles, and a dashed teal route with three nodes. It is used at low opacity in the homepage hero, the OG template, and the 404 page. Keep it abstract. Do not add figures, faces, or neon effects.
