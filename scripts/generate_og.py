# -*- coding: utf-8 -*-
"""Render the 1200x630 Open Graph cards and the hero portrait for atikulislam.me.

    python3 scripts/generate_og.py

Requires Pillow and fontTools (build-time only; see package.json / docs).
The cards mirror the live design system: obsidian ground, cyan and emerald
ambient light, Inter display type, one kicker per page.
"""
import json
import os
import sys

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OG_DIR = os.path.join(ROOT, "assets", "img", "og")
FONT_WOFF2 = os.path.join(ROOT, "assets", "fonts", "inter-latin-var.woff2")
TMP_TTF = "/tmp/inter-var.ttf"

W, H = 1200, 630
BG = (7, 9, 14)
TEXT = (248, 250, 252)
MUTED = (148, 163, 184)
DIM = (124, 138, 160)
CYAN = (56, 189, 248)
EMERALD = (16, 185, 129)
LINE = (255, 255, 255, 26)


def ensure_ttf():
    if not os.path.exists(TMP_TTF):
        f = TTFont(FONT_WOFF2)
        f.flavor = None
        f.save(TMP_TTF)
    return TMP_TTF


def font(size, weight="SemiBold"):
    f = ImageFont.truetype(ensure_ttf(), size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def tracked(draw, xy, text, fnt, fill, tracking=2.2):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += fnt.getlength(ch) + tracking


def wrap(draw, text, fnt, max_width, max_lines=3):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
            if len(lines) == max_lines:
                break
    if current and len(lines) < max_lines:
        lines.append(current)
    if len(lines) == max_lines:
        # trim the last line with an ellipsis if content remains
        joined = " ".join(lines)
        if len(joined.split()) < len(words):
            last = lines[-1]
            while draw.textlength(last + "…", font=fnt) > max_width and len(last) > 4:
                last = last[:-1]
            lines[-1] = last.rstrip() + "…"
    return lines


def card(kicker, title, sub=None):
    img = Image.new("RGB", (W, H), BG)

    # Ambient light
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.ellipse([W - 520, -300, W + 220, 300], fill=CYAN + (66,))
    g.ellipse([-260, H - 260, 420, H + 240], fill=EMERALD + (40,))
    glow = glow.filter(ImageFilter.GaussianBlur(150))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")

    # Hairline grid
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for x in range(0, W, 72):
        gd.line([(x, 0), (x, H)], fill=(255, 255, 255, 8))
    for y in range(0, H, 72):
        gd.line([(0, y), (W, y)], fill=(255, 255, 255, 8))
    img = Image.alpha_composite(img.convert("RGBA"), grid).convert("RGB")

    d = ImageDraw.Draw(img)

    # Monogram
    d.rounded_rectangle([72, 64, 116, 108], radius=11, fill=(14, 22, 34), outline=(56, 189, 248, 120), width=1)
    d.text((82, 76), "AIR", font=font(15, "Bold"), fill=(224, 242, 254))

    tracked(d, (132, 78), "ATIKUL ISLAM RABBI", font(13, "SemiBold"), (203, 213, 225), 2.6)
    tracked(d, (132, 96), "ATIKULSLAM.ME", font(11, "Medium"), DIM, 2.2)

    # Kicker
    d.line([(72, 236), (104, 236)], fill=CYAN, width=2)
    tracked(d, (118, 224), kicker.upper(), font(14, "SemiBold"), CYAN, 3.4)

    # Title
    fnt = font(58, "SemiBold")
    lines = wrap(d, title, fnt, 980, 3)
    y = 268
    for line in lines:
        d.text((72, y), line, font=fnt, fill=TEXT)
        y += 68

    # Sub
    if sub:
        sfnt = font(24, "Regular")
        sub_lines = wrap(d, sub, sfnt, 900, 2)
        y += 8
        for line in sub_lines:
            d.text((72, y), line, font=sfnt, fill=MUTED)
            y += 34

    # Footer
    d.line([(72, H - 92), (W - 72, H - 92)], fill=LINE, width=1)
    d.text((72, H - 66), "atikulislam.me", font=font(18, "Medium"), fill=MUTED)
    tracked(d, (W - 372, H - 64), "SOCIAL MEDIA SECURITY", font(12, "SemiBold"), DIM, 2.4)

    return img


CARDS = []


def add(rel_path, kicker, title, sub=None):
    CARDS.append((rel_path, kicker, title, sub))


def build_manifest():
    from build_site import META, SERVICE_TITLES
    from site_lib import CASES, SERVICES
    from content_blog import POSTS

    kickers = {
        "/": "Social media security",
        "/about/": "About",
        "/services/": "Services",
        "/case-studies/": "Case studies",
        "/portfolio/": "Clients",
        "/faq/": "FAQ",
        "/contact/": "Contact",
        "/blog/": "Insights",
        "/privacy-policy/": "Legal",
        "/terms/": "Legal",
    }
    subs = {
        "/": "Social Media Security Expert · Founder & CEO, Cyber Infinity",
        "/portfolio/": "Social media security and management for brands worldwide",
        "/case-studies/": "Documented cases, with their limits stated",
        "/blog/": "Field notes on recovery and account security",
    }

    for path, (title, desc, og, lastmod) in META.items():
        clean = title.split(" | ")[0]
        add(og, kickers.get(path, "Insights"), clean, subs.get(path))

    for s in SERVICES:
        add("/assets/img/og/service-%s.jpg" % s["slug"], s["group"], s["title"], "Remote, worldwide")
    for c in CASES:
        short = c.get("shortTitle") or c["title"].split(":")[0]
        add("/assets/img/og/case-%s.jpg" % c["slug"], "Case study",
            short + ": " + (c.get("platform") or "Recovery"), c.get("clientType"))
    for p in POSTS:
        add("/assets/img/og/post-%s.jpg" % p["slug"], p["kicker"], p["title"], "atikulislam.me/insights")


def build_portrait():
    src = os.path.join(ROOT, "assets", "_source", "profile-original-512.png")
    out = os.path.join(ROOT, "assets", "img", "atikul-islam-rabbi-social-media-security-expert.jpg")
    if not os.path.exists(src):
        print("  ! source portrait missing, skipped")
        return
    img = Image.open(src).convert("RGB")
    if img.size[0] > 900:
        img = img.resize((900, int(900 * img.size[1] / img.size[0])), Image.LANCZOS)
    img.save(out, "JPEG", quality=90, optimize=True, progressive=True)
    print("  portrait ->", os.path.relpath(out, ROOT), img.size, os.path.getsize(out) // 1024, "KB")


def main():
    ensure_ttf()
    os.makedirs(OG_DIR, exist_ok=True)
    build_manifest()
    seen = set()
    for rel, kicker, title, sub in CARDS:
        if rel in seen:
            continue
        seen.add(rel)
        img = card(kicker, title, sub)
        out = os.path.join(ROOT, rel.lstrip("/"))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        img.save(out, "JPEG", quality=86, optimize=True, progressive=True)
    print("  %d OG cards written" % len(seen))
    build_portrait()


if __name__ == "__main__":
    main()
