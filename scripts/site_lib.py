# -*- coding: utf-8 -*-
"""Shared framework for atikulislam.me — head, schema graph, header, footer.

The generated HTML is committed and is what GitHub Pages serves. This module is
build-time only and is excluded from the published site by _config.yml.
"""
import base64
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE = "https://atikulislam.me"

SITE = {
    "name": "Atikul Islam Rabbi",
    "first": "Atikul",
    "role": "Social Media Security Expert",
    "role_full": "Social Media Security Expert | Founder & CEO of Cyber Infinity",
    "company": "Cyber Infinity",
    "handle": "atikulislamx",
    "email": "help.atikulislam@gmail.com",
    "whatsapp_display": "+880 1300 228105",
    "whatsapp_url": "https://wa.me/8801300228105",
    "gbp": "https://g.co/kgs/RUh5c5i",
    "portrait": "/assets/img/atikul-islam-rabbi-social-media-security-expert.jpg",
    "profile_small": "/assets/img/profile-96.webp",
    "updated": "2026-11-25",
}

SAME_AS = [
    "https://www.linkedin.com/in/atikul-islam-rabbi-275975386/",
    "https://www.facebook.com/atikulislamx",
    "https://www.instagram.com/atikulislamx/",
    "https://x.com/atikulislamx",
    "https://github.com/Atikulislamx",
    "https://atikulislamx.medium.com/",
    "https://www.crunchbase.com/person/atikul-islam-rabbi",
    "https://about.me/atikulislamrabbi",
    "https://atikulislamrabbi.bio.link/",
    "https://en.everybodywiki.com/Atikul_Islam_Rabbi",
    "https://wikialpha.co/wiki/Atikul_Islam_Rabbi",
    "https://g.co/kgs/RUh5c5i",
]

PROFILES = [
    ("LinkedIn", "in", "https://www.linkedin.com/in/atikul-islam-rabbi-275975386/"),
    ("X", "X", "https://x.com/atikulislamx"),
    ("Facebook", "f", "https://www.facebook.com/atikulislamx"),
    ("Instagram", "IG", "https://www.instagram.com/atikulislamx/"),
    ("GitHub", "GH", "https://github.com/Atikulislamx"),
    ("Medium", "M", "https://atikulislamx.medium.com/"),
    ("Crunchbase", "CB", "https://www.crunchbase.com/person/atikul-islam-rabbi"),
    ("about.me", "AM", "https://about.me/atikulislamrabbi"),
    ("bio.link", "BL", "https://atikulislamrabbi.bio.link/"),
    ("EverybodyWiki", "EW", "https://en.everybodywiki.com/Atikul_Islam_Rabbi"),
    ("WikiAlpha", "WA", "https://wikialpha.co/wiki/Atikul_Islam_Rabbi"),
    ("Google Business", "G", "https://g.co/kgs/RUh5c5i"),
]

KNOWS_ABOUT = [
    "Facebook Page recovery",
    "Facebook account recovery",
    "Instagram account recovery",
    "Meta Business Manager recovery",
    "Meta business verification",
    "Admin dispute resolution",
    "Social media security audits",
    "Digital asset protection",
    "Social media management",
    "Account takeover response",
]

EMAIL_B64 = base64.b64encode(SITE["email"].encode()).decode()

# --------------------------------------------------------------------------
# Build-time data
# --------------------------------------------------------------------------


def read_json(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return json.load(fh)


SERVICES = read_json("data/services.json")["services"]
CASES = read_json("data/case-studies.json")["caseStudies"]
FAQS = read_json("data/faq.json")["faqs"]

SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}
CASE_BY_SLUG = {c["slug"]: c for c in CASES}

GROUPS = []
for _s in SERVICES:
    if _s["group"] not in [g for g, _ in GROUPS]:
        GROUPS.append((_s["group"], []))
    for _g, _items in GROUPS:
        if _g == _s["group"]:
            _items.append(_s)

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------


def esc(value):
    return html.escape(str(value), quote=True)


def icon(name, cls=""):
    c = ("icon " + cls).strip()
    return ('<svg class="%s" aria-hidden="true" focusable="false">'
            '<use href="/assets/icons/sprite.svg#i-%s"></use></svg>' % (c, name))


def ext_icon():
    return icon("arrow-up-right")


def badge(text, kind=""):
    k = (" badge--" + kind) if kind else ""
    return '<span class="badge%s">%s</span>' % (k, esc(text))


def abs_url(path):
    return BASE + path


# --------------------------------------------------------------------------
# Schema (@graph)
# --------------------------------------------------------------------------


def person_node():
    return {
        "@type": "Person",
        "@id": BASE + "/#person",
        "name": SITE["name"],
        "alternateName": ["atikulislamx", "Atikul Islam Rabbi (atikulislamx)"],
        "url": BASE + "/",
        "mainEntityOfPage": BASE + "/",
        "image": {"@id": BASE + "/#portrait"},
        "jobTitle": SITE["role"],
        "description": ("Social Media Security Expert and Founder & CEO of Cyber Infinity. "
                        "Recovery, verification and security for Facebook, Instagram and "
                        "Meta Business Manager assets."),
        "worksFor": {"@id": BASE + "/#organization"},
        "founderOf": {"@id": BASE + "/#organization"},
        "knowsAbout": KNOWS_ABOUT,
        "knowsLanguage": [
            {"@type": "Language", "name": "English"},
            {"@type": "Language", "name": "Bengali"},
        ],
        "address": {"@type": "PostalAddress", "addressCountry": "BD"},
        "sameAs": SAME_AS,
    }


def org_node():
    return {
        "@type": "Organization",
        "@id": BASE + "/#organization",
        "name": SITE["company"],
        "url": BASE + "/about/#company",
        "description": ("A digital security practice for social media recovery, Meta Business "
                        "Manager support, digital asset protection and cybersecurity consulting."),
        "founder": {"@id": BASE + "/#person"},
        "foundingLocation": {"@type": "Place", "name": "Dhaka, Bangladesh"},
        "areaServed": {"@type": "Place", "name": "Worldwide"},
        "logo": {
            "@type": "ImageObject",
            "url": BASE + "/assets/brand/icon-512.png",
            "width": 512,
            "height": 512,
        },
        "contactPoint": [{
            "@type": "ContactPoint",
            "contactType": "client enquiries",
            "email": SITE["email"],
            "url": BASE + "/contact/",
            "availableLanguage": ["English", "Bengali"],
            "areaServed": "Worldwide",
        }],
        "knowsAbout": KNOWS_ABOUT[:6],
    }


def website_node():
    return {
        "@type": "WebSite",
        "@id": BASE + "/#website",
        "url": BASE + "/",
        "name": SITE["name"],
        "alternateName": "atikulislam.me",
        "inLanguage": "en",
        "publisher": {"@id": BASE + "/#person"},
        "about": {"@id": BASE + "/#person"},
    }


def portrait_node():
    return {
        "@type": "ImageObject",
        "@id": BASE + "/#portrait",
        "url": BASE + SITE["portrait"],
        "contentUrl": BASE + SITE["portrait"],
        "width": 512,
        "height": 512,
        "caption": "Atikul Islam Rabbi, Social Media Security Expert and Founder & CEO of Cyber Infinity",
        "representativeOfPage": True,
    }


def breadcrumb_node(path, label, parents=None):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"}]
    pos = 2
    for name, href in (parents or []):
        items.append({"@type": "ListItem", "position": pos, "name": name, "item": BASE + href})
        pos += 1
    if path != "/":
        items.append({"@type": "ListItem", "position": pos, "name": label, "item": BASE + path})
    return {"@type": "BreadcrumbList", "@id": BASE + path + "#breadcrumb",
            "itemListElement": items}


def webpage_node(path, title, desc, page_type="WebPage", og=None):
    node = {
        "@type": page_type,
        "@id": BASE + path + "#webpage",
        "url": BASE + path,
        "name": title,
        "description": desc,
        "isPartOf": {"@id": BASE + "/#website"},
        "about": {"@id": BASE + "/#person"},
        "inLanguage": "en",
        "dateModified": SITE["updated"],
        "primaryImageOfPage": {
            "@type": "ImageObject",
            "url": BASE + og if og else BASE + "/assets/img/og/home.jpg",
        },
    }
    return node


def graph(*nodes):
    data = {"@context": "https://schema.org", "@graph": list(nodes)}
    return ('<script type="application/ld+json">' +
            json.dumps(data, ensure_ascii=False, separators=(",", ":")) +
            "</script>")


# --------------------------------------------------------------------------
# Head
# --------------------------------------------------------------------------


def head(title, desc, path, og="/assets/img/og/home.jpg", schema="", noindex=False,
         extra_head="", verify_google=False):
    canonical = BASE + path
    # A noindex page (404, redirect stub) must not declare a canonical: the
    # signal pair is contradictory and Search Console reports it as such.
    canonical_tag = "" if noindex else ('  <link rel="canonical" href="%s">' % canonical)
    robots = ("noindex, follow" if noindex
              else "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1")
    verification = ('\n  <meta name="google-site-verification" content="9LfSMTrxIRXCKl_mf6eKHWW6lcNpd7CMY6IFT_Bk1FU">'
                    if verify_google else "")
    parts = [
        "<!doctype html>",
        '<html lang="en" class="no-js">',
        "<head>",
        '  <meta charset="utf-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1">',
        "  <script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>",
        "  <title>%s</title>" % esc(title),
        '  <meta name="description" content="%s">' % esc(desc),
        canonical_tag,
        '  <meta name="robots" content="%s">' % robots,
        '  <meta name="author" content="Atikul Islam Rabbi">',
        '  <meta name="theme-color" content="#07090E">',
        '  <meta name="color-scheme" content="dark">',
        '  <meta property="fb:app_id" content="1765803794607971">' + verification,
        "",
        '  <meta property="og:type" content="%s">' % ("article" if "/blog/" in path and path != "/blog/" else "website"),
        '  <meta property="og:site_name" content="Atikul Islam Rabbi">',
        '  <meta property="og:title" content="%s">' % esc(title),
        '  <meta property="og:description" content="%s">' % esc(desc),
        '  <meta property="og:url" content="%s">' % canonical,
        '  <meta property="og:image" content="%s">' % (BASE + og),
        '  <meta property="og:image:type" content="image/jpeg">',
        '  <meta property="og:image:width" content="1200">',
        '  <meta property="og:image:height" content="630">',
        '  <meta property="og:image:alt" content="%s">' % esc(title),
        '  <meta property="og:locale" content="en_US">',
        '  <meta name="twitter:card" content="summary_large_image">',
        '  <meta name="twitter:site" content="@atikulislamx">',
        '  <meta name="twitter:creator" content="@atikulislamx">',
        '  <meta name="twitter:title" content="%s">' % esc(title),
        '  <meta name="twitter:description" content="%s">' % esc(desc),
        '  <meta name="twitter:image" content="%s">' % (BASE + og),
        '  <meta name="twitter:image:alt" content="%s">' % esc(title),
        "",
        '  <link rel="icon" href="/assets/brand/favicon.svg" type="image/svg+xml">',
        '  <link rel="icon" href="/favicon.ico" sizes="any">',
        '  <link rel="icon" href="/assets/brand/favicon-32.png" type="image/png" sizes="32x32">',
        '  <link rel="icon" href="/assets/brand/favicon-16.png" type="image/png" sizes="16x16">',
        '  <link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png" sizes="180x180">',
        '  <link rel="manifest" href="/site.webmanifest">',
        '  <link rel="preload" href="/assets/fonts/inter-latin-var.woff2" as="font" type="font/woff2" crossorigin>',
        '  <link rel="stylesheet" href="/css/site.css">',
    ]
    if schema:
        parts.append("  " + schema)
    if extra_head:
        parts.append("  " + extra_head)
    parts += [
        "  <!-- Google Tag Manager (loaded last in head so metadata parses first) -->",
        "  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':",
        "  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],",
        "  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=",
        "  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);",
        "  })(window,document,'script','dataLayer','GTM-PHVGHCMT');</script>",
        "  <!-- End Google Tag Manager -->",
        "</head>",
    ]
    return "\n".join(parts)


# --------------------------------------------------------------------------
# Header / navigation
# --------------------------------------------------------------------------

NAV = [
    ("Services", "/services/"),
    ("Clients", "/portfolio/"),
    ("Case Studies", "/case-studies/"),
    ("Insights", "/blog/"),
    ("About", "/about/"),
]


def is_active(active, path):
    if not active:
        return False
    if path == "/":
        return active.startswith("/") and active == "/"
    return active.startswith(path)


def nav_link(label, path, active, cls="nav__link"):
    cur = ' aria-current="page"' if is_active(active, path) else ""
    return '<li><a class="%s" href="%s"%s>%s</a></li>' % (cls, path, cur, esc(label))


def mega_groups():
    out = []
    for group, items in GROUPS:
        links = []
        for s in items:
            links.append(
                '<li><a class="mega__link" href="/services/%s/">'
                '<strong>%s</strong><span>%s</span></a></li>' % (
                    s["slug"], esc(s["title"]), esc(s["cardSummary"]))
            )
        out.append(
            '<div class="mega__group"><p class="mega__group-title">%s</p>'
            '<ul class="mega__list">%s</ul></div>' % (esc(group), "".join(links))
        )
    out.append(
        '<div class="mega__promo">'
        '<p class="mega__group-title">Not sure where you fit?</p>'
        '<p>Describe what happened. I will tell you which route applies and whether it is realistic — before any work starts.</p>'
        '<a class="btn btn--primary btn--sm" href="/contact/">Request an assessment %s</a>'
        '<a class="link-arrow" href="/services/">All eight services %s</a>'
        '</div>' % (icon("arrow-right"), icon("arrow-right"))
    )
    return "".join(out)


def header(active):
    nav_items = []
    for label, path in NAV:
        if path == "/services/":
            cur = ' aria-current="page"' if active.startswith("/services/") else ""
            nav_items.append(
                '<li><button class="nav__trigger" type="button" data-mega-trigger '
                'aria-expanded="false" aria-controls="mega-services"%s>%s %s</button></li>' % (
                    cur, esc(label), icon("chevron-down"))
            )
        else:
            nav_items.append(nav_link(label, path, active))

    drawer_services = []
    for group, items in GROUPS:
        drawer_services.append('<p class="drawer__label">%s</p>' % esc(group))
        for s in items:
            drawer_services.append('<a href="/services/%s/">%s</a>' % (s["slug"], esc(s["title"])))

    drawer_items = []
    for label, path in NAV:
        if path == "/services/":
            drawer_items.append(
                '<li><details class="drawer__sub"><summary class="drawer__summary">Services %s</summary>'
                '<div class="drawer__sub-list"><a href="/services/">All services</a>%s</div>'
                '</details></li>' % (icon("chevron-down"), "".join(drawer_services))
            )
        else:
            drawer_items.append('<li><a class="drawer__link" href="%s">%s</a></li>' % (path, esc(label)))

    return """
<a class="skip" href="#main">Skip to content</a>
<header class="site-header" data-header>
  <div class="container header-inner">
    <a class="brand" href="/" aria-label="Atikul Islam Rabbi — home">
      <span class="brand__mark" aria-hidden="true">AIR</span>
      <span class="brand__text">
        <span class="brand__name">Atikul Islam Rabbi</span>
        <span class="brand__role">Social Media Security Expert</span>
      </span>
    </a>

    <nav class="nav" aria-label="Primary">
      <ul class="nav__list">%s</ul>
      <a class="btn btn--primary btn--sm nav__cta" href="/contact/">Request recovery</a>
    </nav>

    <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="mobile-drawer">
      <span data-nav-label>Menu</span>%s
    </button>

    <div class="mega" id="mega-services" data-mega data-open="false">
      <div class="container">
        <div class="mega__panel">%s</div>
      </div>
    </div>
  </div>
</header>

<div class="drawer" id="mobile-drawer" data-drawer aria-label="Mobile navigation" data-open="false">
  <ul class="drawer__list">%s</ul>
  <div class="drawer__cta">
    <a class="btn btn--primary btn--block" href="/contact/">Request recovery</a>
    <a class="btn btn--secondary btn--block" href="/faq/">Read the FAQ</a>
  </div>
  <div class="drawer__meta">
    <span>Remote support worldwide · Dhaka, Bangladesh (UTC+6)</span>
    <span>No passwords are ever requested.</span>
  </div>
</div>
""" % ("".join(nav_items), icon("menu"), mega_groups(), "".join(drawer_items))


# --------------------------------------------------------------------------
# Footer
# --------------------------------------------------------------------------


def footer():
    profile_links = "".join(
        '<li><a href="%s" target="_blank" rel="noopener noreferrer me">%s</a></li>' % (url, esc(name))
        for name, mark, url in PROFILES[:7]
    )
    service_links = "".join(
        '<li><a href="/services/%s/">%s</a></li>' % (s["slug"], esc(s["title"]))
        for s in SERVICES[:5]
    )
    return """
<footer class="site-footer" data-inert-when-open>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="/" aria-label="Atikul Islam Rabbi — home">
          <span class="brand__mark" aria-hidden="true">AIR</span>
          <span class="brand__text">
            <span class="brand__name">Atikul Islam Rabbi</span>
            <span class="brand__role">Founder &amp; CEO, Cyber Infinity</span>
          </span>
        </a>
        <p>Social media security, Meta account recovery and digital asset protection for founders, agencies and brands worldwide.</p>
        <p class="footer-status"><span class="dot" aria-hidden="true"></span><span>Accepting new cases · replies within one business day</span></p>
        <p><a class="link-arrow" href="/contact/">Start a confidential assessment %s</a></p>
      </div>

      <div>
        <p class="footer-title">Services</p>
        <ul class="footer-list">%s
          <li><a href="/services/">All eight services</a></li>
        </ul>
      </div>

      <div>
        <p class="footer-title">Company</p>
        <ul class="footer-list">
          <li><a href="/about/">About</a></li>
          <li><a href="/portfolio/">Clients &amp; work</a></li>
          <li><a href="/case-studies/">Case studies</a></li>
          <li><a href="/blog/">Insights</a></li>
          <li><a href="/faq/">FAQ</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
      </div>

      <div>
        <p class="footer-title">Verified profiles</p>
        <ul class="footer-list">%s</ul>
      </div>
    </div>

    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> Atikul Islam Rabbi · Cyber Infinity</span>
      <span class="footer-legal">
        <a href="/privacy-policy/">Privacy</a>
        <a href="/terms/">Terms</a>
        <a href="/.well-known/security.txt">Security</a>
        <a href="/sitemap.xml">Sitemap</a>
      </span>
    </div>

    <p class="footer-disclaimer">Recovery outcomes depend on platform review and the evidence available; no outcome is guaranteed. Passwords, one-time codes and recovery codes are never requested. This site is independent and is not affiliated with, endorsed by, or sponsored by Meta Platforms, Inc. Facebook, Instagram, WhatsApp and Meta Business Manager are trademarks of Meta Platforms, Inc.</p>
  </div>
</footer>
""" % (icon("arrow-right"), service_links, profile_links)


# --------------------------------------------------------------------------
# Page shell
# --------------------------------------------------------------------------


def page(title, desc, path, body, active=None, og="/assets/img/og/home.jpg",
         schema="", noindex=False, extra_head="", verify_google=False, body_class=""):
    cls = (' class="%s"' % body_class) if body_class else ""
    return "\n".join([
        head(title, desc, path, og, schema, noindex, extra_head, verify_google),
        "<body%s>" % cls,
        '<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PHVGHCMT" '
        'height="0" width="0" style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>',
        header(active or path),
        '<main id="main" data-inert-when-open>',
        body,
        "</main>",
        footer(),
        '<script src="/js/main.js" defer></script>',
        "</body>",
        "</html>",
        "",
    ])


# --------------------------------------------------------------------------
# Small UI builders
# --------------------------------------------------------------------------


def crumbs(items):
    """items: list of (label, href) — last item rendered as current."""
    out = []
    for i, (label, href) in enumerate(items):
        if i == len(items) - 1:
            out.append('<li aria-current="page">%s</li>' % esc(label))
        else:
            out.append('<li><a href="%s">%s</a></li>' % (href, esc(label)))
    return ('<nav class="crumbs" aria-label="Breadcrumb"><div class="container">'
            '<ol>%s</ol></div></nav>' % "".join(out))


def section_head(eyebrow, title, lead=None, tid="", row=False, action=""):
    tid_attr = ' id="%s"' % tid if tid else ""
    cls = "section-head section-head--row" if row else "section-head"
    label = (' aria-labelledby="%s"' % tid) if tid else ""
    lead_html = '<p class="lead">%s</p>' % lead if lead else ""
    return ('<div class="%s" data-reveal%s>' % (cls, label) +
            '<div><span class="eyebrow">%s</span><h2%s>%s</h2></div>%s%s</div>' % (
                esc(eyebrow), tid_attr, esc(title), lead_html, action))


def cta_band(title, text, primary=("Request priority asset recovery", "/contact/"),
             secondary=("Read the FAQ", "/faq/")):
    return """
<section class="section section--tight">
  <div class="container">
    <div class="cta" data-reveal>
      <div>
        <span class="eyebrow">Next step</span>
        <h2>%s</h2>
        <p>%s</p>
      </div>
      <div class="cta__actions">
        <a class="btn btn--primary" href="%s">%s %s</a>
        <a class="btn btn--secondary" href="%s">%s</a>
      </div>
    </div>
  </div>
</section>""" % (esc(title), text, primary[1], esc(primary[0]), icon("arrow-right"),
                 secondary[1], esc(secondary[0]))


def service_card(svc, reveal=True):
    return """
<article class="card card--link service-card"%(rev)s>
  <div class="card__top">
    <span class="icon-badge">%(icon)s</span>
    <span class="service-card__group">%(group)s</span>
  </div>
  <h3 class="card__title mt-4"><a href="/services/%(slug)s/">%(title)s</a></h3>
  <p class="card__text">%(summary)s</p>
  <span class="card__foot"><span class="link-arrow">Read the process %(arrow)s</span></span>
</article>""" % {
        "rev": " data-reveal" if reveal else "",
        "icon": icon(svc["icon"]),
        "group": esc(svc["group"]),
        "slug": svc["slug"],
        "title": esc(svc["title"]),
        "summary": esc(svc["cardSummary"]),
        "arrow": icon("arrow-right"),
    }


def case_card(case, reveal=True):
    return """
<article class="card card--link case-card"%(rev)s>
  <div class="card__top">
    <span class="badge">%(platform)s</span>
    <span class="case-card__platform">%(client)s</span>
  </div>
  <h3 class="card__title mt-4"><a href="/case-studies/%(slug)s/">%(title)s</a></h3>
  <p class="card__text">%(problem)s</p>
  <p class="case-card__result">%(check)s<span>%(result)s</span></p>
  <span class="card__foot"><span class="link-arrow">Read the case study %(arrow)s</span></span>
</article>""" % {
        "rev": " data-reveal" if reveal else "",
        "platform": esc(case["platform"]),
        "client": esc(case["clientType"]),
        "slug": case["slug"],
        "title": esc(case["title"]),
        "problem": esc(case["problem"]),
        "result": esc(first_sentence(case["result"])),
        "check": icon("circle-check"),
        "arrow": icon("arrow-right"),
    }


def first_sentence(text):
    text = text.strip()
    for sep in (". ", "。"):
        if sep in text:
            return text.split(sep)[0] + "."
    return text
