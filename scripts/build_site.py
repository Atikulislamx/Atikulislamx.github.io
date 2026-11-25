# -*- coding: utf-8 -*-
"""Build every page of atikulislam.me.

    python3 scripts/build_site.py

Writes committed HTML into the repository root. GitHub Pages serves that HTML
directly; no build step runs at deploy time.
"""
import json
import os
import re

from content_blog import POSTS
from site_lib import (
    BASE, CASES, CASE_BY_SLUG, EMAIL_B64, FAQS, GROUPS, PROFILES, ROOT, SERVICES,
    SERVICE_BY_SLUG, SITE, SAME_AS, badge, breadcrumb_node, case_card, cta_band,
    crumbs, esc, graph, icon, org_node, page, person_node, portrait_node,
    read_json, section_head, service_card, website_node, webpage_node,
)

DATE = SITE["updated"]

# --------------------------------------------------------------------------
# Page metadata: path -> title, description, og image, lastmod
# --------------------------------------------------------------------------
META = {
    "/": (
        "Atikul Islam Rabbi | Social Media Security Expert & Founder",
        "Atikul Islam Rabbi is a social media security expert and Founder & CEO of Cyber Infinity. "
        "Meta recovery and account security for brands worldwide.",
        "/assets/img/og/home.jpg", "2026-11-25",
    ),
    "/about/": (
        "About Atikul Islam Rabbi — Social Media Security Expert",
        "Founder & CEO of Cyber Infinity. 40+ critical Meta and social assets recovered, with client "
        "retainers across the UK, UAE, South Asia and global digital brands.",
        "/assets/img/og/about.jpg", "2026-11-25",
    ),
    "/services/": (
        "Social Media Security & Meta Recovery Services",
        "Eight services for Facebook Pages, Instagram, personal accounts and Meta Business Manager: "
        "recovery, verification, admin disputes and security audits.",
        "/assets/img/og/services.jpg", "2026-11-25",
    ),
    "/case-studies/": (
        "Meta Recovery Case Studies | Atikul Islam Rabbi",
        "Documented Facebook Page, Instagram and Business Manager cases: the problem, the approach, "
        "the result and the limits. Recovery is never guaranteed.",
        "/assets/img/og/case-studies.jpg", "2026-11-25",
    ),
    "/portfolio/": (
        "Clients & Global Work | Atikul Islam Rabbi",
        "International brands and agencies supported with social media security and management, from "
        "Edinburgh and London to the UAE and global eCommerce.",
        "/assets/img/og/portfolio.jpg", "2026-11-25",
    ),
    "/faq/": (
        "FAQ: Recovery, Privacy & Working Together | Atikul Islam Rabbi",
        "Straight answers on recovery timelines, what to send, how information is handled, and what "
        "working together actually involves.",
        "/assets/img/og/faq.jpg", "2026-11-25",
    ),
    "/contact/": (
        "Contact: Priority Asset Recovery | Atikul Islam Rabbi",
        "Request a confidential assessment for a hacked Page, account or Business Manager. No passwords "
        "requested. Replies within one business day.",
        "/assets/img/og/contact.jpg", "2026-11-25",
    ),
    "/blog/": (
        "Insights: Meta & Social Media Security | Atikul Islam Rabbi",
        "Field notes on Facebook Page recovery, account appeals, Business Manager takeovers, "
        "verification and social media security audits.",
        "/assets/img/og/blog.jpg", "2026-11-25",
    ),
    "/privacy-policy/": (
        "Privacy Policy | Atikul Islam Rabbi",
        "How enquiry data is collected, used, stored and protected, which processors are involved, and "
        "how to exercise your rights.",
        "/assets/img/og/privacy.jpg", "2026-11-25",
    ),
    "/terms/": (
        "Terms & Service Scope | Atikul Islam Rabbi",
        "The basis on which recovery, verification and security work is provided, including scope, "
        "confidentiality, no-guarantee terms and acceptable use.",
        "/assets/img/og/terms.jpg", "2026-11-25",
    ),
}

SERVICE_TITLES = {
    "facebook-page-recovery": "Hacked Facebook Page Recovery | Atikul Islam Rabbi",
    "facebook-account-recovery": "Facebook Account Recovery | Atikul Islam Rabbi",
    "instagram-account-recovery": "Instagram Account Recovery | Atikul Islam Rabbi",
    "meta-business-manager-recovery": "Meta Business Manager Recovery | Atikul Islam Rabbi",
    "business-verification-guidance": "Business Verification Guidance | Atikul Islam Rabbi",
    "admin-dispute-resolution": "Admin Dispute Resolution | Atikul Islam Rabbi",
    "security-consultation": "Security Consultation | Atikul Islam Rabbi",
    "social-media-security-audit": "Social Media Security Audit | Atikul Islam Rabbi",
}

SERVICE_DESCS = {
    "facebook-page-recovery": "Recover a hacked, hijacked or lost Facebook Page. An evidence-led review of ownership and Meta's recovery routes, then hardening so it holds.",
    "facebook-account-recovery": "Regain access to a hacked, locked or disabled personal Facebook account — and therefore to the Pages and ad accounts behind it.",
    "instagram-account-recovery": "Recover a hacked or locked Instagram account for creators and businesses, including accounts managed inside Meta Business Manager.",
    "meta-business-manager-recovery": "Restore control of a hacked or restricted Meta Business Manager and the Pages, ad accounts, pixels and catalogs attached to it.",
    "business-verification-guidance": "Prepare a Meta business verification that matches on the first submission: legal name, address, phone and domain evidence.",
    "admin-dispute-resolution": "Resolve admin and ownership disputes over Pages and Business Managers through evidence, correct routing and clean escalation.",
    "security-consultation": "A focused review of access, admin roles, two-factor authentication and ownership across your social accounts, with prioritised fixes.",
    "social-media-security-audit": "A structured audit of Facebook, Instagram and Meta Business Manager exposure, delivered as a prioritised report with a 30/60/90 plan.",
}

CASE_TITLES = {
    "zero-idea-facebook-page-recovery": "Zero Idea: Facebook Page Recovery Case Study | Atikul Islam Rabbi",
    "dinajpur-image": "Dinajpur Image: Page Restoration Case Study | Atikul Islam Rabbi",
    "santali-ari-chari": "Santali Ari-Chari: Page Recovery Case Study | Atikul Islam Rabbi",
    "business-manager-verification-uae": "Business Manager Verification Case Study | Atikul Islam Rabbi",
    "delicious-food-by-arpa": "Delicious Food by Arpa: Case Study | Atikul Islam Rabbi",
}


def meta_for(path):
    if path in META:
        return META[path]
    if path.startswith("/services/") and path != "/services/":
        slug = path.strip("/").split("/")[-1]
        svc = SERVICE_BY_SLUG[slug]
        return (SERVICE_TITLES[slug], SERVICE_DESCS[slug],
                "/assets/img/og/service-%s.jpg" % slug, "2026-11-25")
    if path.startswith("/case-studies/") and path != "/case-studies/":
        slug = path.strip("/").split("/")[-1]
        case = CASE_BY_SLUG[slug]
        desc = case["problem"].strip()
        if len(desc) < 120:  # short problems: add the outcome sentence
            result = case["result"].strip()
            extra = result.split(". ")[0].rstrip(".") + "."
            desc = (desc + " " + extra).strip()
        desc = desc[:152].rsplit(" ", 1)[0].rstrip(",;:-")
        if not desc.endswith("."):
            desc += "."
        return (CASE_TITLES[slug], desc,
                "/assets/img/og/case-%s.jpg" % slug, "2026-11-25")
    if path.startswith("/blog/") and path != "/blog/":
        slug = path.strip("/").split("/")[-1]
        post = next(p for p in POSTS if p["slug"] == slug)
        return (post["title"] + " | Atikul Islam Rabbi", post["description"],
                "/assets/img/og/post-%s.jpg" % slug, post["updated"])
    raise KeyError(path)


# --------------------------------------------------------------------------
# Home
# --------------------------------------------------------------------------
CLIENTS = [
    {
        "name": "Sanatorium Tattoo", "mark": "ST",
        "industry": "Tattoo & permanent make-up", "region": "Edinburgh, UK",
        "desc": "An award-winning Edinburgh studio covering tattoo, permanent make-up, piercing and laser removal. Social media security and day-to-day management where most booking conversations begin.",
        "scope": "Social media security & management",
    },
    {
        "name": "I AM BEING", "mark": "IB",
        "industry": "Cacao & wellbeing", "region": "London, UK",
        "desc": "A London ceremonial cacao and wellbeing brand running ceremonies, sound baths and facilitator training. Security and management across a five-platform presence.",
        "scope": "Social media security & management",
    },
    {
        "name": "Afghan Carpet", "mark": "AC",
        "industry": "Luxury rug retail", "region": "South Asia & UAE",
        "desc": "The region's largest hand-woven carpet retailer, with showrooms and a Dubai branch. Social channel management and account protection for a multi-currency luxury retailer.",
        "scope": "Social media security & management",
    },
    {
        "name": "Ingram Investments", "mark": "II",
        "industry": "Investment & venture building", "region": "UK & UAE",
        "desc": "An investment firm backing and building ventures from early-stage startups to turnarounds. Social media security and management for a corporate brand whose principals appear on camera.",
        "scope": "Account security & management",
    },
    {
        "name": "NOTFIT", "mark": "NF",
        "industry": "Fitness app & membership", "region": "Global",
        "desc": "An anti-fitness training app with programmes, community and member stories. Account security and social management for a product whose growth runs through short-form video.",
        "scope": "Social media security & management",
    },
    {
        "name": "Upseeks Media", "mark": "UM",
        "industry": "App development & growth", "region": "Global agency",
        "desc": "A build-and-grow agency spanning apps, web development and paid media. Social presence management and account protection for a team that sells social services itself.",
        "scope": "Social media security & management",
    },
    {
        "name": "PinClever", "mark": "PC",
        "industry": "Pinterest ads for DTC", "region": "Global eCommerce",
        "desc": "A Pinterest advertising agency for DTC and eCommerce brands. Social media security and content management for a performance brand competing on creative volume.",
        "scope": "Social media security & management",
    },
]

TESTIMONIALS = [
    {
        "name": "Zero Idea", "who": "Page owner · science & education",
        "tag": "Facebook Page recovery", "yt": "YOUR_VIDEO_ID_HERE", "wide": False,
        "line": "A 400,000+ follower Page recovered after a two-month lockout. The owner later shared a public video about it.",
    },
    {
        "name": "Sanatorium Tattoo", "who": "Founder · Edinburgh, UK",
        "tag": "Security & management", "yt": "YOUR_VIDEO_ID_HERE", "wide": False,
        "line": "An award-winning studio with 1,000+ reviews, protected across Instagram, Facebook and TikTok.",
    },
    {
        "name": "Ingram Investments", "who": "Principal · UK & UAE",
        "tag": "Account security", "yt": "YOUR_VIDEO_ID_HERE", "wide": False,
        "line": "A corporate presence with on-camera principals, secured across five platforms.",
    },
    {
        "name": "I AM BEING", "who": "Founder · London, UK",
        "tag": "Instagram & TikTok", "yt": "YOUR_VIDEO_ID_HERE", "wide": False,
        "line": "A multi-platform wellbeing brand: shop, classes and journal, managed and protected.",
    },
]


def video_card(t):
    wide = " video-card--wide" if t["wide"] else ""
    return """
<article class="video-card%(wide)s">
  <div class="video-card__media">
    <div class="video-card__grain" aria-hidden="true"></div>
    <div class="video-card__initials" aria-hidden="true">%(initials)s</div>
    <button class="video-card__poster" type="button" data-youtube-id="%(yt)s"
            data-video-title="%(title_attr)s" aria-label="Play client video: %(name)s">
      <span class="video-card__play">%(play)s</span>
      <span class="video-card__time">0:30</span>
      <span class="video-card__badge badge">%(tag)s</span>
    </button>
  </div>
  <div class="video-card__body">
    <p class="video-card__quote">%(line)s</p>
    <p class="video-card__who"><strong>%(name)s</strong><br>%(who)s</p>
  </div>
  <p class="video-card__note" data-video-note hidden></p>
</article>""" % {
        "wide": wide,
        "initials": esc("".join(w[0] for w in t["name"].split()[:2])),
        "yt": esc(t["yt"]),
        "name": esc(t["name"]),
        "title_attr": esc("Client video testimonial: " + t["name"]),
        "play": icon("play"),
        "tag": esc(t["tag"]),
        "line": esc(t["line"]),
        "who": esc(t["who"]),
    }


def clients_grid(limit=None, reveal=True):
    items = CLIENTS[:limit] if limit else CLIENTS
    out = []
    for i, c in enumerate(items):
        wide = " client--wide" if i == 0 else ""
        out.append("""
<article class="client%(wide)s"%(rev)s>
  <div class="client__head">
    <span class="client__mark" aria-hidden="true">%(mark)s</span>
    <div>
      <p class="client__name">%(name)s</p>
      <p class="client__region">%(region)s</p>
    </div>
  </div>
  <div class="client__tags">%(industry)s%(retainer)s</div>
  <p class="client__desc">%(desc)s</p>
  <div class="client__foot">
    <span class="client__scope">%(scope)s</span>
    <a class="client__visit" href="%(url)s" target="_blank" rel="noopener noreferrer nofollow">Visit site %(ext)s</a>
  </div>
</article>""" % {
            "wide": wide,
            "rev": " data-reveal" if reveal else "",
            "mark": esc(c["mark"]),
            "name": esc(c["name"]),
            "region": esc(c["region"]),
            "industry": badge(c["industry"]),
            "retainer": badge("Ongoing retainer", "emerald"),
            "desc": esc(c["desc"]),
            "scope": esc(c["scope"]),
            "url": {"Sanatorium Tattoo": "https://sanatorium.tattoo/",
                    "I AM BEING": "https://iambeing.co.uk/",
                    "Afghan Carpet": "https://www.afghancarpet.com/",
                    "Ingram Investments": "https://ingraminvestments.com/",
                    "NOTFIT": "https://notfit.io/",
                    "Upseeks Media": "https://upseeksmedia.com/",
                    "PinClever": "https://www.pinclever.com/"}[c["name"]],
            "ext": icon("arrow-up-right"),
        })
    return "".join(out)


def credentials_list():
    creds = [
        ("badge", "Founder &amp; CEO, Cyber Infinity",
         "A digital security practice for recovery, verification and social media protection."),
        ("circle-check", "40+ critical assets recovered",
         "Meta and social media assets returned to their legitimate owners."),
        ("globe", "International retainers",
         "Client relationships across the UK, UAE, South Asia and global digital brands."),
        ("map-pin", "Based in Dhaka, working worldwide",
         "Remote delivery in English and Bengali, UTC+6."),
        ("lock", "Evidence-led, password-free process",
         "No passwords, one-time codes or recovery codes are ever requested."),
        ("file-text", "Written plans before action",
         "Every case starts with a documented review and realistic options."),
    ]
    out = []
    for ic, title, text in creds:
        out.append('<div class="cred"><span class="cred__icon">%s</span><div><strong>%s</strong><span>%s</span></div></div>'
                   % (icon(ic), title, text))
    out.append('<a class="cred" href="%s" target="_blank" rel="noopener noreferrer nofollow">'
               '<span class="cred__icon">%s</span><div><strong>Verified Google Business Profile</strong>'
               '<span>Reviews and business details verified by Google.</span></div></a>'
               % (SITE["gbp"], icon("badge-check")))
    return "".join(out)


def social_hub():
    chips = []
    for name, mark, url in PROFILES:
        chips.append('<a class="social-chip" href="%s" target="_blank" rel="noopener noreferrer me">'
                     '<span class="social-chip__mark" aria-hidden="true">%s</span>%s</a>'
                     % (url, esc(mark), esc(name)))
    return '<div class="social-hub">%s</div>' % "".join(chips)


def build_home():
    path = "/"
    title, desc, og, lastmod = META[path]
    tags = [badge("40+ assets recovered", "emerald"), badge("Founder & CEO", "cyan")]
    schema = graph(
        website_node(), person_node(), org_node(),portrait_node(),
        webpage_node(path, title, desc, "WebPage", og),
        breadcrumb_node(path, "Home"),
        {
            "@type": "ItemList",
            "name": "Services",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": s["title"],
                 "url": BASE + "/services/" + s["slug"] + "/"}
                for i, s in enumerate(SERVICES)
            ],
        },
    )

    body = """
<section class="hero">
  <div class="container">
    <div class="hero__grid">
      <div class="hero__copy">
        <div class="hero__pill">
          <span class="pill pill--verified"><span class="dot" aria-hidden="true"></span>Verified Social Media Security Expert &amp; Founder</span>
        </div>
        <h1 class="hero__title">
          <span class="hero__name">Atikul Islam Rabbi</span>
          <span class="hero__role">Social Media Security Expert · <em>Founder &amp; CEO of Cyber Infinity</em></span>
        </h1>
        <p class="hero__lead">I protect and recover high-value social media assets for founders, agencies and brands — Facebook Pages, Instagram accounts and Meta Business Managers — with evidence-led recovery and security work that holds after the case closes.</p>
        <div class="hero__actions">
          <a class="btn btn--primary" href="/contact/">Request Priority Asset Recovery %s</a>
          <a class="btn btn--secondary" href="/about/#credentials">Verify Credentials &amp; Work %s</a>
        </div>
        <p class="hero__micro">
          <span>%s No passwords requested</span>
          <span>%s Remote worldwide</span>
          <span>%s Reply within one business day</span>
        </p>
      </div>
      <div class="portrait">
        <div class="portrait__frame">
          <img src="%s" width="512" height="512"
               alt="Atikul Islam Rabbi, Social Media Security Expert and Founder &amp; CEO of Cyber Infinity"
               fetchpriority="high" decoding="async">
        </div>
        <span class="portrait__tag portrait__tag--tl">%s Verified by Google</span>
        <span class="portrait__tag portrait__tag--br">%s 40+ assets recovered</span>
        <p class="portrait__caption">Atikul Islam Rabbi · Dhaka, Bangladesh · working worldwide</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight" aria-label="At a glance">
  <div class="container">
    <div class="bento">
      <div class="bento__tile" data-reveal>
        <p class="bento__num">40<span>+</span></p>
        <p class="bento__label"><strong>Critical assets recovered</strong>Meta &amp; social media accounts returned to their legitimate owners</p>
      </div>
      <div class="bento__tile" data-reveal>
        <p class="bento__num">5<span>+</span></p>
        <p class="bento__label"><strong>Global &amp; domestic retainers</strong>Ongoing security and management for brands in the UK, UAE and South Asia</p>
      </div>
      <div class="bento__tile" data-reveal>
        <p class="bento__num" style="font-size:1.25rem;line-height:1.25">Founder &amp; CEO</p>
        <p class="bento__label"><strong>Cyber Infinity</strong>A digital security practice for recovery, verification and protection</p>
      </div>
      <a class="bento__tile bento__tile--accent" href="%s" target="_blank" rel="noopener noreferrer nofollow" data-reveal>
        <p class="bento__num" style="font-size:1.25rem;line-height:1.25">%s Verified</p>
        <p class="bento__label"><strong>Google Business Profile</strong>Business details and reviews verified by Google</p>
        <span class="bento__link">View the profile %s</span>
      </a>
    </div>
  </div>
</section>

<section class="section" id="services">
  <div class="container">
    %s
    <div class="grid grid--4">%s</div>
    <p class="mt-6"><a class="link-arrow" href="/services/">All eight services %s</a></p>
  </div>
</section>

<section class="section" id="clients">
  <div class="container">
    %s
    <div class="grid grid--3">%s</div>
    <p class="mt-6"><a class="link-arrow" href="/portfolio/">Clients, retainers and technical work %s</a></p>
  </div>
</section>

<section class="section" id="testimonials">
  <div class="container">
    %s
    <div class="video-grid">%s</div>
    <p class="aspect-note mt-4">Short client videos are published with written consent. Names shown are clients on retainer.</p>
  </div>
</section>

<section class="section" id="proof">
  <div class="container">
    %s
    <article class="featured" data-reveal>
      <div>
        <div class="cluster">%s%s</div>
        <h3 class="featured__title">Zero Idea: Facebook Page Recovery</h3>
        <p>Zero Idea publishes science and educational content to more than 400,000 followers. The Page was taken over and the legitimate administrator was locked out for about two months.</p>
        <p>I investigated how the compromise happened, confirmed the administrator's ownership, then worked the recovery route with the platform and secured the Page once control returned.</p>
        <p class="mt-5"><a class="btn btn--secondary btn--sm" href="/case-studies/zero-idea-facebook-page-recovery/">Read the full case study %s</a></p>
      </div>
      <dl class="featured__side">
        <div class="fact"><dt>Result</dt><dd>The Page was recovered and the legitimate administrator regained control.</dd></div>
        <div class="fact"><dt>Scale</dt><dd>400,000+ followers · science and education</dd></div>
        <div class="fact"><dt>Limits</dt><dd>One Page, one set of circumstances. It does not predict another case.</dd></div>
        <div class="fact"><dt>Service</dt><dd><a href="/services/facebook-page-recovery/">Facebook Page Recovery</a></dd></div>
      </dl>
    </article>
    <div class="grid grid--2 mt-6">%s</div>
  </div>
</section>

<section class="section" id="credentials">
  <div class="container">
    %s
    <div class="split">
      <div>
        <div class="cred-grid">%s</div>
        <p class="mt-6"><a class="link-arrow" href="/about/">Read the full background %s</a></p>
      </div>
      <aside class="split__aside glass" style="padding:var(--s5)">
        <p class="footer-title">Identity &amp; profiles</p>
        <p class="t-sm dim mb-4">Every profile below is the same person, verified across platforms.</p>
        %s
      </aside>
    </div>
  </div>
</section>

<section class="section" id="insights">
  <div class="container">
    %s
    <div class="grid grid--3">%s</div>
  </div>
</section>
""" % (
        icon("arrow-right"), icon("arrow-right"),
        icon("lock"), icon("globe"), icon("clock"),
        SITE["portrait"],
        icon("badge-check"), icon("circle-check"),
        SITE["gbp"], icon("badge-check"), icon("arrow-up-right"),
        section_head("Services", "Recovery, verification and security for Meta assets",
                     "Each service page states who it is for, the process, what to send and the limits — before you commit to anything.",
                     "services-title"),
        "".join(service_card(s) for s in SERVICES),
        icon("arrow-right"),
        section_head("Clients", "Global brands & international clients",
                     "Social media security and management for brands across the UK, the UAE and global eCommerce.",
                     "clients-title"),
        clients_grid(),
        icon("arrow-right"),
        section_head("Testimonials", "30-second client stories",
                     "Short, unscripted videos from clients — recovery cases and long-term retainers.",
                     "testimonials-title"),
        "".join(video_card(t) for t in TESTIMONIALS),
        section_head("Proof", "A recent case, with its limits stated",
                     "Results depend on platform review and the evidence available. Limits are part of the record.",
                     "proof-title"),
        badge("Facebook Page"), badge("400,000+ followers"),
        icon("arrow-right"),
        "".join(case_card(c) for c in CASES[1:5]),
        section_head("Authority", "Verified credentials & identity",
                     "The record a client can check before handing over access to a business asset.",
                     "credentials-title"),
        credentials_list(),
        icon("arrow-right"),
        social_hub(),
        section_head("Insights", "Field notes on recovery & security",
                     "Practical guidance written from live cases, not from templates.",
                     "insights-title",
                     action='<a class="link-arrow" href="/blog/">All insights %s</a>' % icon("arrow-right")),
        "".join(post_card(p, compact=True) for p in POSTS[:3]),
    ) + cta_band(
        "A compromised asset is a business problem, not a support ticket.",
        "Describe what happened. You will get a realistic assessment of the routes open to you — and an honest answer if recovery is unlikely.",
        ("Request priority asset recovery", "/contact/"),
        ("Verify credentials first", "/about/#credentials"),
    )

    return page(title, desc, path, body, active="/", og=og, schema=schema, verify_google=True)


# --------------------------------------------------------------------------
# About
# --------------------------------------------------------------------------


def build_about():
    path = "/about/"
    title, desc, og, lastmod = META[path]
    schema = graph(
        website_node(), person_node(), org_node(),portrait_node(),
        {
            "@type": "ProfilePage",
            "@id": BASE + path + "#webpage",
            "url": BASE + path,
            "name": title,
            "description": desc,
            "isPartOf": {"@id": BASE + "/#website"},
            "mainEntity": {"@id": BASE + "/#person"},
            "about": {"@id": BASE + "/#person"},
            "primaryImageOfPage": {"@id": BASE + "/#portrait"},
            "inLanguage": "en",
            "dateModified": DATE,
        },
        breadcrumb_node(path, "About"),
    )

    body = """
%(crumbs)s
<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <span class="eyebrow">About</span>
      <h1>Atikul Islam Rabbi</h1>
      <p class="lead">Social Media Security Expert and Founder &amp; CEO of Cyber Infinity. I recover and protect the Meta assets that businesses cannot afford to lose.</p>
      <div class="page-hero__actions">
        <a class="btn btn--primary" href="/contact/">Request an assessment %(arrow)s</a>
        <a class="btn btn--secondary" href="#credentials">Credentials &amp; verification</a>
      </div>
      <div class="page-hero__meta">
        <span>%(pin)s Dhaka, Bangladesh (UTC+6)</span>
        <span>%(globe)s Remote worldwide</span>
        <span>%(check)s 40+ critical assets recovered</span>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split">
      <div class="prose">
        <p>I run a digital security practice built around one narrow, high-stakes problem: what happens when a business loses control of its social media assets. A Facebook Page that carries the brand. An Instagram account with the audience. A Meta Business Manager that holds the Pages, ad accounts, pixels and catalogs of an entire company.</p>
        <p>Most of these incidents are not sophisticated attacks. They are an old administrator who was never removed, a profile without two-factor authentication, an agency handover that was never completed, or a shared password in a spreadsheet. The recovery is technical; the cause is usually operational.</p>
        <p>That is why the work has two halves. The first is recovery: establishing what actually happened, assembling the evidence that proves legitimate ownership, and working the correct Meta route instead of repeating the same rejected appeal. The second is hardening: removing the access paths that made the takeover possible, so the same case does not return in six months.</p>
        <p>I founded Cyber Infinity to deliver that work for founders, agencies and brands internationally. Clients range from a 400,000-follower education Page and an award-winning Edinburgh studio to investment firms and eCommerce brands operating across several markets.</p>
        <p>I do not guarantee outcomes, because the final decision always sits with the platform. What I do guarantee is a structured review, a written assessment of the realistic routes, and no request for a password, a one-time code or a recovery code — ever.</p>
      </div>
      <aside class="split__aside">
        <div class="glass" style="padding:var(--s4)">
          <img src="%(portrait)s" width="512" height="512" loading="lazy" decoding="async"
               alt="Portrait of Atikul Islam Rabbi, Social Media Security Expert"
               style="width:100%%;height:auto;border-radius:var(--r-md)">
        </div>
        <dl class="glass mt-4" style="padding:var(--s5)">
          <div class="fact"><dt>Role</dt><dd>Social Media Security Expert · Founder &amp; CEO, Cyber Infinity</dd></div>
          <div class="fact"><dt>Focus</dt><dd>Facebook, Instagram and Meta Business Manager</dd></div>
          <div class="fact"><dt>Base</dt><dd>Dhaka, Bangladesh · UTC+6</dd></div>
          <div class="fact"><dt>Languages</dt><dd>English, Bengali</dd></div>
          <div class="fact"><dt>Response</dt><dd>Within one business day</dd></div>
        </dl>
      </aside>
    </div>
  </div>
</section>

<section class="section" id="credentials">
  <div class="container">
    %(cred_head)s
    <div class="split">
      <div>
        <div class="cred-grid">%(creds)s</div>
        <div class="callout callout--ok mt-6">
          %(check_icon)s
          <span><strong>Verify before you engage.</strong> Check the Google Business Profile, the LinkedIn record and the case studies. Every claim on this site is something you can inspect.</span>
        </div>
      </div>
      <aside class="split__aside glass" style="padding:var(--s5)">
        <p class="footer-title">Identity graph</p>
        <p class="t-sm dim mb-4">The same person across twelve verified properties — the record search engines use to confirm an identity.</p>
        %(hub)s
      </aside>
    </div>
  </div>
</section>

<section class="section section--line" id="company">
  <div class="container">
    %(company_head)s
    <div class="grid grid--3">
      <div class="card"><h3>What Cyber Infinity does</h3><p class="card__text">Recovery of hacked, hijacked or restricted Meta assets; business verification preparation; admin dispute resolution; and security audits for social infrastructure.</p></div>
      <div class="card"><h3>How engagements run</h3><p class="card__text">A confidential intake, a written assessment of the routes available, then either a scoped recovery engagement or a security workplan. Fees are agreed in writing before work starts.</p></div>
      <div class="card"><h3>What it will not do</h3><p class="card__text">No guaranteed outcomes, no password collection, no work against accounts you cannot prove you own, and no engagement that depends on deceiving a platform's review process.</p></div>
    </div>
  </div>
</section>
""" % {
        "crumbs": crumbs([("Home", "/"), ("About", "/about/")]),
        "arrow": icon("arrow-right"),
        "pin": icon("map-pin"),
        "globe": icon("globe"),
        "check": icon("check"),
        "portrait": SITE["portrait"],
        "cred_head": section_head("Credentials", "The record you can check",
                                  "Authority here is not a badge on a page. It is a verified profile, a documented case and a client list you can visit.",
                                  "credentials-title"),
        "creds": credentials_list(),
        "check_icon": icon("check"),
        "hub": social_hub(),
        "company_head": section_head("Company", "Cyber Infinity",
                                     "A digital security practice for social media recovery, Meta Business Manager support and digital asset protection.",
                                     "company-title"),
    } + cta_band(
        "Working on a compromised asset right now?",
        "Send the timeline and the asset list. The first reply tells you which situation you are in and what is realistically open.",
        ("Request priority asset recovery", "/contact/"),
        ("Read client outcomes", "/case-studies/"),
    )

    return page(title, desc, path, body, active="/about/", og=og, schema=schema)


# --------------------------------------------------------------------------
# Services
# --------------------------------------------------------------------------


def build_services_hub():
    path = "/services/"
    title, desc, og, lastmod = META[path]
    schema = graph(
        website_node(), person_node(), org_node(),
        portrait_node(),
        webpage_node(path, title, desc, "CollectionPage", og),
        breadcrumb_node(path, "Services"),
        {
            "@type": "ItemList",
            "name": "Social media security and recovery services",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": s["title"],
                 "url": BASE + "/services/" + s["slug"] + "/"}
                for i, s in enumerate(SERVICES)
            ],
        },
        {
            "@type": "ProfessionalService",
            "@id": BASE + path + "#service",
            "name": SITE["company"],
            "description": "Social media recovery, Meta Business Manager support, business verification and cybersecurity consulting.",
            "url": BASE + "/",
            "areaServed": {"@type": "Place", "name": "Worldwide"},
            "provider": {"@id": BASE + "/#organization"},
            "founder": {"@id": BASE + "/#person"},
        },
    )

    groups_html = []
    for group, items in GROUPS:
        groups_html.append(
            '<div class="mt-7"><h2 class="t-sm" style="letter-spacing:0.14em;text-transform:uppercase;color:var(--text-faint)">'
            '%s</h2><div class="grid grid--4 mt-4">%s</div></div>' % (
                esc(group), "".join(service_card(s) for s in items))
        )

    body = """
%s
<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <span class="eyebrow">Services</span>
      <h1>Social media security and recovery services</h1>
      <p class="lead">Eight services across three fronts: recovering assets that are already compromised, clearing verification and disputes, and hardening access so it does not happen twice.</p>
      <div class="page-hero__actions">
        <a class="btn btn--primary" href="/contact/">Request an assessment %s</a>
        <a class="btn btn--secondary" href="/case-studies/">See documented cases</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    %s
  </div>
</section>

<section class="section section--line">
  <div class="container">
    %s
    <div class="grid grid--2">
      <ol class="steps">
        <li class="step"><span class="step__n">1</span><div><p class="step__title">Tell me what happened</p><p class="step__text">Use the contact form. Add the timeline, the platform and any notices you received. No passwords.</p></div></li>
        <li class="step"><span class="step__n">2</span><div><p class="step__title">I review the evidence</p><p class="step__text">Ownership proof, admin history and the route that is actually open for your case.</p></div></li>
      </ol>
      <ol class="steps" start="3">
        <li class="step"><span class="step__n">3</span><div><p class="step__title">You get a written plan</p><p class="step__text">The options, what each one needs from you, and my recommendation. You decide.</p></div></li>
        <li class="step"><span class="step__n">4</span><div><p class="step__title">We work the case and secure it</p><p class="step__text">Recovery first, then access hardening so the same failure cannot repeat.</p></div></li>
      </ol>
    </div>
    <div class="callout callout--warn mt-6">%s<span><strong>What I will not do:</strong> ask for a password or one-time code, promise a guaranteed recovery, or take on an account you cannot show is yours.</span></div>
  </div>
</section>
""" % (
        crumbs([("Home", "/"), ("Services", "/services/")]),
        icon("arrow-right"),
        "".join(groups_html),
        section_head("Process", "How an engagement runs", "The same four steps for every service, so you always know what happens next and what it needs from you.", "process-title"),
        icon("lock"),
    ) + cta_band(
        "Not sure which service fits?",
        "Describe the situation in a few lines. I will point you to the right route — including when the right answer is that nothing can be done.",
        ("Request an assessment", "/contact/"),
        ("Read the FAQ", "/faq/"),
    )
    return page(title, desc, path, body, active="/services/", og=og, schema=schema)


def build_service(svc):
    slug = svc["slug"]
    path = "/services/%s/" % slug
    title, desc, og, lastmod = META.get(path) or meta_for(path)
    schema = graph(
        website_node(), person_node(), org_node(),
        portrait_node(),
        {
            "@type": "Service",
            "@id": BASE + path + "#service",
            "name": svc["title"],
            "serviceType": svc["title"],
            "description": svc["summary"],
            "url": BASE + path,
            "provider": {"@id": BASE + "/#organization"},
            "areaServed": {"@type": "Place", "name": "Worldwide"},
            "audience": {"@type": "Audience", "audienceType": "; ".join(svc["whoFor"])},
        },
        webpage_node(path, title, desc, "WebPage", og),
        breadcrumb_node(path, svc["title"], [("Services", "/services/")]),
    )

    who = "".join("<li>%s</li>" % esc(w) for w in svc["whoFor"])
    send = "".join("<li>%s</li>" % esc(w) for w in svc["send"])
    limits = "".join("<li>%s</li>" % esc(w) for w in svc["limitations"])
    steps = "".join(
        '<li class="step"><span class="step__n">%d</span><div><p class="step__title">%s</p><p class="step__text">%s</p></div></li>'
        % (i + 1, esc(p["title"]), esc(p["text"]))
        for i, p in enumerate(svc["process"])
    )
    related_cases = [CASE_BY_SLUG[s] for s in svc.get("caseStudySlugs", []) if s in CASE_BY_SLUG]
    related_services = [SERVICE_BY_SLUG[s] for s in svc.get("related", []) if s in SERVICE_BY_SLUG]
    cases_html = "".join(case_card(c) for c in related_cases) if related_cases else ""
    related_html = "".join(
        '<li><a class="link-arrow" href="/services/%s/">%s %s</a></li>' % (s["slug"], esc(s["title"]), icon("arrow-right"))
        for s in related_services
    )

    body = """
%(crumbs)s
<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <div class="cluster">%(badge_group)s%(badge_request)s</div>
      <h1>%(title)s</h1>
      <p class="lead">%(summary)s</p>
      <div class="page-hero__actions">
        <a class="btn btn--primary" href="/contact/?service=%(slug)s">Request this service %(arrow)s</a>
        <a class="btn btn--secondary" href="/services/">All services</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split">
      <div class="prose">
        <h2>The problem it solves</h2>
        <p>%(problem)s</p>

        <h2>Who it is for</h2>
        <ul>%(who)s</ul>

        <h2>My approach</h2>
        <p>%(approach)s</p>

        <h2>How the process works</h2>
        <ol class="steps mt-4">%(steps)s</ol>

        <h2>What to send</h2>
        <p>Only send what is needed for your case. Never send passwords, one-time codes or recovery codes.</p>
        <ul>%(send)s</ul>

        <h2>Limitations</h2>
        <ul>%(limits)s</ul>

        <div class="callout callout--warn">%(lock)s<span><strong>No guarantees.</strong> The final decision sits with the platform. What I control is the quality of the evidence and the correctness of the route.</span></div>
      </div>

      <aside class="split__aside">
        <div class="glass" style="padding:var(--s5)">
          <p class="footer-title">At a glance</p>
          <dl>
            <div class="fact"><dt>Service</dt><dd>%(title)s</dd></div>
            <div class="fact"><dt>Category</dt><dd>%(group)s</dd></div>
            <div class="fact"><dt>Delivery</dt><dd>Remote, worldwide</dd></div>
            <div class="fact"><dt>First reply</dt><dd>Within one business day</dd></div>
            <div class="fact"><dt>Handled by</dt><dd><a href="/about/">Atikul Islam Rabbi</a></dd></div>
          </dl>
          <a class="btn btn--primary btn--block mt-4" href="/contact/?service=%(slug)s">Start a confidential assessment</a>
        </div>
        %(related_box)s
      </aside>
    </div>
  </div>
</section>

%(cases_section)s
""" % {
        "crumbs": crumbs([("Home", "/"), ("Services", "/services/"), (svc["title"], path)]),
        "badge_group": badge(svc["group"], "cyan"),
        "badge_request": badge("No passwords requested", "emerald"),
        "title": esc(svc["title"]),
        "summary": esc(svc["summary"]),
        "slug": slug,
        "arrow": icon("arrow-right"),
        "problem": esc(svc["problem"]),
        "who": who,
        "approach": esc(svc["approach"]),
        "steps": steps,
        "send": send,
        "limits": limits,
        "lock": icon("lock"),
        "group": esc(svc["group"]),
        "related_box": ('<div class="glass mt-4" style="padding:var(--s5)"><p class="footer-title">Related services</p><ul class="stack stack--sm">%s</ul></div>' % related_html) if related_html else "",
        "cases_section": ("""
<section class="section section--line">
  <div class="container">
    %s
    <div class="grid grid--2">%s</div>
  </div>
</section>""" % (section_head("Proof", "Related case studies", "Documented cases that used this service, with their limits stated.", "cases-title"), cases_html)) if cases_html else "",
    } + cta_band(
        "Ready to start?",
        "Send the timeline and what you have already tried. The reply tells you whether this service applies and what it would take.",
        ("Request %s" % svc["title"], "/contact/?service=" + slug),
        ("All services", "/services/"),
    )
    return page(title, desc, path, body, active="/services/", og=og, schema=schema)


# --------------------------------------------------------------------------
# Case studies
# --------------------------------------------------------------------------


def build_cases_hub():
    path = "/case-studies/"
    title, desc, og, lastmod = META[path]
    schema = graph(
        website_node(), person_node(), org_node(),
        portrait_node(),
        webpage_node(path, title, desc, "CollectionPage", og),
        breadcrumb_node(path, "Case Studies"),
        {
            "@type": "ItemList",
            "@id": BASE + path + "#itemlist",
            "name": "Case studies",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": c["title"],
                 "url": BASE + "/case-studies/" + c["slug"] + "/"}
                for i, c in enumerate(CASES)
            ],
        },
    )

    body = """
%s
<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <span class="eyebrow">Case studies</span>
      <h1>Documented cases, with the limits stated</h1>
      <p class="lead">Each case sets out the problem, the situation, the approach, the work, the result and what it does not prove. Where a client asked not to be named, the details are generalised.</p>
      <div class="page-hero__actions">
        <a class="btn btn--primary" href="/contact/">Discuss a similar situation %s</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="bento mb-6">
      <div class="bento__tile bento__tile--wide"><p class="bento__num">5</p><p class="bento__label"><strong>Documented cases</strong>Pages, accounts and Business Managers across four countries</p></div>
      <div class="bento__tile"><p class="bento__num">4</p><p class="bento__label"><strong>Platforms involved</strong>Facebook, Instagram, Business Manager, ad accounts</p></div>
      <div class="bento__tile"><p class="bento__num">0</p><p class="bento__label"><strong>Guarantees given</strong>Every outcome depended on platform review</p></div>
    </div>
    <h2 class="h3 mb-4" data-reveal>All case files</h2>
    <div class="grid grid--2">%s</div>
  </div>
</section>
""" % (
        crumbs([("Home", "/"), ("Case Studies", "/case-studies/")]),
        icon("arrow-right"),
        "".join(case_card(c) for c in CASES),
    ) + cta_band(
        "Your case will not be identical.",
        "That is the point of an assessment: to see which parts of a documented case actually apply to yours.",
        ("Request an assessment", "/contact/"),
        ("Read the services", "/services/"),
    )
    return page(title, desc, path, body, active="/case-studies/", og=og, schema=schema)


def build_case(case):
    slug = case["slug"]
    path = "/case-studies/%s/" % slug
    title, desc, og, lastmod = META.get(path) or meta_for(path)
    schema = graph(
        website_node(), person_node(), org_node(),
        portrait_node(),
        {
            "@type": "Article",
            "@id": BASE + path + "#article",
            "headline": case["title"],
            "description": case["problem"],
            "url": BASE + path,
            "mainEntityOfPage": {"@id": BASE + path + "#webpage"},
            "image": {"@type": "ImageObject", "url": BASE + og, "width": 1200, "height": 630},
            "inLanguage": "en",
            "datePublished": "2026-10-08",
            "dateModified": DATE,
            "author": {"@id": BASE + "/#person"},
            "publisher": {"@id": BASE + "/#organization"},
            "about": [{"@type": "Service", "name": SERVICE_BY_SLUG[s]["title"]}
                      for s in case["services"] if s in SERVICE_BY_SLUG],
        },
        webpage_node(path, title, desc, "WebPage", og),
        breadcrumb_node(path, case["shortTitle"], [("Case Studies", "/case-studies/")]),
    )

    work = "".join("<li>%s</li>" % esc(w) for w in case["work"])
    limits = "".join("<li>%s</li>" % esc(w) for w in case["limitations"])
    services_links = "".join(
        '<li><a class="link-arrow" href="/services/%s/">%s %s</a></li>' % (s, esc(SERVICE_BY_SLUG[s]["title"]), icon("arrow-right"))
        for s in case["services"] if s in SERVICE_BY_SLUG
    )
    others = [c for c in CASES if c["slug"] != slug][:2]

    body = """
%(crumbs)s
<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <div class="cluster">%(badge_platform)s%(badge_client)s</div>
      <h1>%(title)s</h1>
      <p class="lead">%(problem)s</p>
      <div class="page-hero__actions">
        <a class="btn btn--primary" href="/contact/">Discuss a similar situation %(arrow)s</a>
        <a class="btn btn--secondary" href="/case-studies/">All case studies</a>
      </div>
      <div class="page-hero__meta"><span>Case study</span><span>Updated %(updated)s</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split">
      <div class="prose">
        <h2>Problem</h2><p>%(problem)s</p>
        <h2>Situation</h2><p>%(situation)s</p>
        <h2>Challenge</h2><p>%(challenge)s</p>
        <h2>Approach</h2><p>%(approach)s</p>
        <h2>Work</h2><ul>%(work)s</ul>
        <h2>Result</h2><p>%(result)s</p>
        <h2>Key takeaway</h2><p>%(takeaway)s</p>
        <h2>Limitations</h2><ul>%(limits)s</ul>
      </div>
      <aside class="split__aside">
        <div class="glass" style="padding:var(--s5)">
          <p class="footer-title">At a glance</p>
          <dl>
            <div class="fact"><dt>Platform</dt><dd>%(platform)s</dd></div>
            <div class="fact"><dt>Client type</dt><dd>%(client)s</dd></div>
            %(location_fact)s
            <div class="fact"><dt>Service</dt><dd>%(service_names)s</dd></div>
            <div class="fact"><dt>Result</dt><dd>%(result_short)s</dd></div>
          </dl>
          <a class="btn btn--primary btn--block mt-4" href="/contact/">Request an assessment</a>
        </div>
        %(anon)s
      </aside>
    </div>
  </div>
</section>

<section class="section section--line">
  <div class="container">
    %(other_head)s
    <div class="grid grid--2">%(others)s</div>
  </div>
</section>
""" % {
        "crumbs": crumbs([("Home", "/"), ("Case Studies", "/case-studies/"), (case["shortTitle"], path)]),
        "badge_platform": badge(case["platform"], "cyan"),
        "badge_client": badge(case["clientType"]),
        "title": esc(case["title"]),
        "problem": esc(case["problem"]),
        "arrow": icon("arrow-right"),
        "updated": DATE,
        "situation": esc(case["situation"]),
        "challenge": esc(case["challenge"]),
        "approach": esc(case["approach"]),
        "work": work,
        "result": esc(case["result"]),
        "takeaway": esc(case["keyTakeaway"]),
        "limits": limits,
        "platform": esc(case["platform"]),
        "client": esc(case["clientType"]),
        "location_fact": ('<div class="fact"><dt>Region</dt><dd>%s</dd></div>' % esc(case["location"])) if case.get("location") else "",
        "service_names": ", ".join(esc(SERVICE_BY_SLUG[s]["title"]) for s in case["services"] if s in SERVICE_BY_SLUG),
        "result_short": esc(case["result"].split(". ")[0] + "."),
        "anon": ('<div class="callout mt-4">%s<span>%s</span></div>' % (icon("info"), esc(case["anonymizationNote"]))) if case.get("anonymizationNote") else "",
        "other_head": section_head("More cases", "Other documented work", None, "more-cases"),
        "others": "".join(case_card(c) for c in others),
    } + cta_band(
        "Facing something similar?",
        "Send the timeline. You will get a straight answer on which parts of this case apply to yours.",
        ("Request an assessment", "/contact/"),
        ("See the services", "/services/"),
    )
    return page(title, desc, path, body, active="/case-studies/", og=og, schema=schema)


# --------------------------------------------------------------------------
# Portfolio / clients
# --------------------------------------------------------------------------


def build_portfolio():
    path = "/portfolio/"
    title, desc, og, lastmod = META[path]
    schema = graph(
        website_node(), person_node(), org_node(),
        portrait_node(),
        webpage_node(path, title, desc, "CollectionPage", og),
        breadcrumb_node(path, "Clients"),
        {
            "@type": "ItemList",
            "name": "Clients and engagements",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": c["name"],
                 "description": "%s · %s" % (c["industry"], c["region"])}
                for i, c in enumerate(CLIENTS)
            ],
        },
    )

    body = """
%(crumbs)s
<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <span class="eyebrow">Clients &amp; work</span>
      <h1>Global brands and the work behind them</h1>
      <p class="lead">Social media security and management for brands that depend on their social presence — a tattoo studio in Edinburgh, a wellbeing brand in London, an investment firm operating across the UK and UAE, and eCommerce teams selling worldwide.</p>
      <div class="page-hero__actions">
        <a class="btn btn--primary" href="/contact/">Discuss a retainer %(arrow)s</a>
        <a class="btn btn--secondary" href="/case-studies/">Recovery case studies</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    %(clients_head)s
    <div class="grid grid--3">%(clients)s</div>
    <p class="aspect-note mt-5">Domestic corporate clients and additional international brands are covered under confidentiality and are not listed here. Client names are published with permission.</p>
  </div>
</section>

<section class="section" id="testimonials">
  <div class="container">
    %(testi_head)s
    <div class="video-grid">%(videos)s</div>
    <p class="aspect-note mt-4">Thirty-second videos, published with written consent. Nothing loads from YouTube until you press play.</p>
  </div>
</section>

<section class="section section--line" id="systems">
  <div class="container">
    %(systems_head)s
    <div class="grid grid--3">
      <article class="card"><span class="icon-badge">%(scan)s</span><h3 class="mt-4">Recovery &amp; OSINT workflows</h3><p class="card__text">Structured evidence collection and asset-mapping for takeover cases: admin graphs, ownership trails, registrar and domain checks, and the documentation a platform review can follow.</p></article>
      <article class="card"><span class="icon-badge">%(terminal)s</span><h3 class="mt-4">Automation &amp; tooling</h3><p class="card__text">Python and API automation for routine checks — access inventories, permission drift, and repeated audit steps that should not depend on memory.</p></article>
      <article class="card"><span class="icon-badge">%(globe)s</span><h3 class="mt-4">Secure static delivery</h3><p class="card__text">This site is hand-built: no framework, no database, no runtime dependencies, and a hardened publish scope. A security practice should not be the weakest site in its own portfolio.</p></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    %(retainer_head)s
    <div class="grid grid--2">
      <div class="card"><h3>Security &amp; management retainer</h3><p class="card__text">Ongoing social media security and account management: access reviews, admin hygiene, incident response and day-to-day channel operations.</p><p class="card__text"><strong>Typical fit:</strong> brands with multiple channels and a team that changes.</p></div>
      <div class="card"><h3>Recovery engagement</h3><p class="card__text">A scoped case: assessment, evidence file, route selection and recovery work, followed by hardening of the recovered asset.</p><p class="card__text"><strong>Typical fit:</strong> a Page, account or Business Manager already compromised.</p></div>
    </div>
  </div>
</section>
""" % {
        "crumbs": crumbs([("Home", "/"), ("Clients", "/portfolio/")]),
        "arrow": icon("arrow-right"),
        "clients_head": section_head("Clients", "Brands on retainer",
                                     "Each engagement covers both halves of the work: the day-to-day channel, and the security of the account behind it.",
                                     "clients-title"),
        "clients": clients_grid(),
        "testi_head": section_head("Testimonials", "30-second client stories",
                                   "Short videos from clients across recovery cases and long-term retainers.",
                                   "testimonials-title"),
        "videos": "".join(video_card(t) for t in TESTIMONIALS),
        "systems_head": section_head("Systems", "The technical layer behind the work",
                                     "Tools and workflows built to make recovery repeatable and audits measurable.",
                                     "systems-title"),
        "scan": icon("scan-search"),
        "terminal": icon("terminal"),
        "globe": icon("globe"),
        "retainer_head": section_head("Engagements", "Two ways to work together",
                                      "Both start with an assessment, and both are agreed in writing before any work begins.",
                                      "engagements-title"),
    } + cta_band(
        "Protecting a brand with more than one channel?",
        "A retainer covers the security and the day-to-day, so incidents are caught before they become recoveries.",
        ("Discuss a retainer", "/contact/"),
        ("Read the services", "/services/"),
    )
    return page(title, desc, path, body, active="/portfolio/", og=og, schema=schema)


# --------------------------------------------------------------------------
# FAQ
# --------------------------------------------------------------------------


def build_faq():
    path = "/faq/"
    title, desc, og, lastmod = META[path]
    schema = graph(
        website_node(), person_node(), org_node(),
        portrait_node(),
        {
            "@type": "FAQPage",
            "@id": BASE + path + "#faq",
            "url": BASE + path,
            "name": title,
            "mainEntity": [
                {"@type": "Question", "name": q["question"],
                 "acceptedAnswer": {"@type": "Answer", "text": q["answer"]}}
                for q in FAQS
            ],
        },
        webpage_node(path, title, desc, "WebPage", og),
        breadcrumb_node(path, "FAQ"),
    )

    cats = []
    for q in FAQS:
        if q["category"] not in cats:
            cats.append(q["category"])

    blocks = []
    for cat in cats:
        items = [q for q in FAQS if q["category"] == cat]
        rows = "".join("""
<details class="faq__item">
  <summary class="faq__q">%s %s</summary>
  <div class="faq__a"><p>%s</p></div>
</details>""" % (esc(q["question"]), icon("plus"), esc(q["answer"])) for q in items)
        blocks.append('<p class="faq__cat">%s</p><div class="faq">%s</div>' % (esc(cat), rows))

    body = """
%s
<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <span class="eyebrow">FAQ</span>
      <h1>Frequently asked questions</h1>
      <p class="lead">Short answers on recovery, evidence, privacy and what working together involves. If your question is not here, the contact form reaches me directly.</p>
      <div class="page-hero__actions">
        <a class="btn btn--primary" href="/contact/">Ask a question %s</a>
        <a class="btn btn--secondary" href="/services/">Browse services</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split">
      <div>%s</div>
      <aside class="split__aside">
        <div class="glass" style="padding:var(--s5)">
          <p class="footer-title">Before you send anything</p>
          <ul class="stack stack--sm t-sm">
            <li>%s Never send a password or one-time code.</li>
            <li>%s Share the timeline, not the whole account history.</li>
            <li>%s Redact customer data from screenshots.</li>
            <li>%s Ask about confidentiality if the brand cannot be named.</li>
          </ul>
          <a class="btn btn--secondary btn--block mt-4" href="/privacy-policy/">Privacy policy</a>
        </div>
      </aside>
    </div>
  </div>
</section>
""" % (
        crumbs([("Home", "/"), ("FAQ", "/faq/")]),
        icon("arrow-right"),
        "".join(blocks),
        icon("lock"), icon("file-text"), icon("scan-search"), icon("shield"),
    ) + cta_band(
        "Still unsure?",
        "A short, specific question usually gets a short, specific answer. No obligation.",
        ("Ask directly", "/contact/"),
        ("See case studies", "/case-studies/"),
    )
    return page(title, desc, path, body, active="/faq/", og=og, schema=schema)


# --------------------------------------------------------------------------
# Contact
# --------------------------------------------------------------------------


def build_contact():
    path = "/contact/"
    title, desc, og, lastmod = META[path]
    schema = graph(
        website_node(), person_node(), org_node(),
        portrait_node(),
        {
            "@type": "ContactPage",
            "@id": BASE + path + "#webpage",
            "url": BASE + path,
            "name": title,
            "description": desc,
            "isPartOf": {"@id": BASE + "/#website"},
            "about": {"@id": BASE + "/#person"},
            "inLanguage": "en",
            "dateModified": DATE,
        },
        breadcrumb_node(path, "Contact"),
    )

    options = []
    for s in SERVICES:
        options.append('<option value="%s">%s</option>' % (s["slug"], esc(s["title"])))
    options.append('<option value="social-media-management">Social media management retainer</option>')
    options.append('<option value="not-sure">Not sure yet</option>')

    body = """
%(crumbs)s
<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <span class="eyebrow">Contact</span>
      <h1>Request a confidential assessment</h1>
      <p class="lead">Describe what happened in your own words. You will get a reply within one business day with the realistic routes and the next step — or a straight answer if recovery is unlikely.</p>
      <div class="page-hero__meta">
        <span>%(clock)s Reply within one business day</span>
        <span>%(lock)s No passwords requested</span>
        <span>%(globe)s Remote worldwide</span>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split">
      <div class="glass" style="padding:clamp(var(--s4),3vw,var(--s6))" data-form-wrap>
        <div class="alert alert--danger" role="alert" tabindex="-1" data-form-error hidden>
          %(warn)s <span>Your message could not be sent. Please try again, or reach me on WhatsApp.</span>
        </div>

        <form class="form js-only" data-contact-form novalidate>
          <div class="hp" aria-hidden="true">
            <label for="botcheck">Leave this unchecked</label>
            <input type="checkbox" id="botcheck" name="botcheck" tabindex="-1" autocomplete="off">
          </div>

          <div class="form-grid form-grid--2">
            <div class="field">
              <label class="field__label" for="name">Name <span class="field__req">(required)</span></label>
              <input class="input" type="text" id="name" name="name" required autocomplete="name" aria-describedby="name-error">
              <p class="field__error" id="name-error"></p>
            </div>
            <div class="field">
              <label class="field__label" for="email">Email <span class="field__req">(required)</span></label>
              <input class="input" type="email" id="email" name="email" required autocomplete="email" inputmode="email" aria-describedby="email-error">
              <p class="field__error" id="email-error"></p>
            </div>
          </div>

          <div class="form-grid form-grid--2">
            <div class="field">
              <label class="field__label" for="service">Service <span class="field__req">(required)</span></label>
              <select class="select" id="service" name="service" required aria-describedby="service-hint service-error">
                <option value="">Choose a service</option>
                %(options)s
              </select>
              <p class="field__hint" id="service-hint">Not sure? Choose “Not sure yet”.</p>
              <p class="field__error" id="service-error"></p>
            </div>
            <div class="field">
              <label class="field__label" for="urgency">Urgency</label>
              <select class="select" id="urgency" name="urgency" aria-describedby="urgency-hint">
                <option value="">Optional</option>
                <option value="active-incident">Active incident — access lost now</option>
                <option value="this-week">This week</option>
                <option value="planning">Planning ahead</option>
              </select>
              <p class="field__hint" id="urgency-hint">Helps me triage honestly.</p>
            </div>
          </div>

          <div class="field">
            <label class="field__label" for="asset">Page, account or business name <span class="field__req">(optional)</span></label>
            <input class="input" type="text" id="asset" name="asset" autocomplete="off" placeholder="Name, handle or Business Manager ID">
          </div>

          <div class="field">
            <label class="field__label" for="message">What is happening? <span class="field__req">(required)</span></label>
            <textarea class="textarea" id="message" name="message" required maxlength="4000" aria-describedby="message-hint message-error" placeholder="When did it start? What have you already tried? Any notices from Meta?"></textarea>
            <p class="field__hint" id="message-hint">At least 20 characters. Do not include passwords, one-time codes or recovery codes.</p>
            <p class="field__error" id="message-error"></p>
          </div>

          <div class="field">
            <label class="check" for="consent">
              <input type="checkbox" id="consent" name="consent" required aria-describedby="consent-error">
              <span>I agree to the <a href="/privacy-policy/">privacy policy</a> and understand this message is processed by Web3Forms and delivered by email.</span>
            </label>
            <p class="field__error" id="consent-error"></p>
          </div>

          <button class="btn btn--primary btn--block" type="submit" data-submit data-label="Send message">
            <span data-submit-label>Send message</span>
            <span class="spinner" aria-hidden="true" hidden></span>
          </button>
          <p class="form-foot">No outcome is guaranteed. Every case is reviewed individually before any work is agreed.</p>
        </form>

        <div class="form-success" data-form-success role="status" tabindex="-1" hidden>
          <h2>Message received</h2>
          <p>Thank you. I will reply to the email address you gave, within one business day.</p>
          <p>If access is actively compromised, message me on WhatsApp and reference this enquiry.</p>
          <p><a class="btn btn--secondary btn--sm" href="https://wa.me/8801300228105" target="_blank" rel="noopener noreferrer" data-channel="whatsapp">WhatsApp %(ext)s</a></p>
        </div>

        <noscript>
          <div class="callout mt-4">%(info)s<span>The form needs JavaScript. You can still reach me directly on <a href="https://wa.me/8801300228105">WhatsApp</a>, or send the details to my email address listed beside this form.</span></div>
        </noscript>
      </div>

      <aside class="split__aside">
        <div class="glass" style="padding:var(--s5)">
          <p class="footer-title">Direct channels</p>
          <div class="methods">
            <a class="method" href="https://wa.me/8801300228105" target="_blank" rel="noopener noreferrer" data-channel="whatsapp">
              <span class="method__icon">%(msg)s</span>
              <span><strong>WhatsApp</strong><span>%(wa)s · fastest for active incidents</span></span>
            </a>
            <a class="method" href="/contact/" data-email="%(mail)s" data-channel="email" data-keep-text="1">
              <span class="method__icon">%(mailicon)s</span>
              <span><strong>Email</strong><span class="js-email">Available after JavaScript loads</span></span>
            </a>
            <a class="method" href="%(gbp)s" target="_blank" rel="noopener noreferrer nofollow" data-channel="google">
              <span class="method__icon">%(badge)s</span>
              <span><strong>Google Business Profile</strong><span>Verified business details and reviews</span></span>
            </a>
          </div>
        </div>

        <div class="glass mt-4" style="padding:var(--s5)">
          <p class="footer-title">What happens next</p>
          <ol class="steps">
            <li class="step"><span class="step__n">1</span><div><p class="step__title">I read it myself</p><p class="step__text">No sales team, no chatbot.</p></div></li>
            <li class="step"><span class="step__n">2</span><div><p class="step__title">You get a written response</p><p class="step__text">Which routes are open, what each needs, and whether I can help.</p></div></li>
            <li class="step"><span class="step__n">3</span><div><p class="step__title">You decide</p><p class="step__text">Scope and fees are agreed in writing before any work starts.</p></div></li>
          </ol>
        </div>

        <div class="callout mt-4">%(lockicon)s<span>Never send passwords, one-time codes or recovery codes — by form, email or WhatsApp. I will never ask for them.</span></div>
      </aside>
    </div>
  </div>
</section>
""" % {
        "crumbs": crumbs([("Home", "/"), ("Contact", "/contact/")]),
        "clock": icon("clock"), "lock": icon("lock"), "globe": icon("globe"),
        "warn": icon("triangle-alert"),
        "options": "".join(options),
        "ext": icon("arrow-up-right"),
        "info": icon("info"),
        "msg": icon("message-circle"),
        "wa": esc(SITE["whatsapp_display"]),
        "mail": EMAIL_B64,
        "mailicon": icon("mail"),
        "gbp": SITE["gbp"],
        "badge": icon("badge-check"),
        "lockicon": icon("lock"),
    }
    return page(title, desc, path, body, active="/contact/", og=og, schema=schema)


# --------------------------------------------------------------------------
# Blog
# --------------------------------------------------------------------------


def post_card(post, compact=False):
    return """
<article class="card card--link"%(rev)s>
  <div class="card__top"><span class="badge badge--cyan">%(kicker)s</span><span class="t-xs faint">%(read)s min read</span></div>
  <h3 class="card__title mt-4"><a href="/blog/%(slug)s/">%(title)s</a></h3>
  <p class="card__text">%(desc)s</p>
  <span class="card__foot"><time datetime="%(date)s">%(pretty)s</time><span class="link-arrow">Read %(arrow)s</span></span>
</article>""" % {
        "rev": " data-reveal" if not compact else "",
        "kicker": esc(post["kicker"]),
        "read": post["read"],
        "slug": post["slug"],
        "title": esc(post["title"]),
        "desc": esc(post["description"]),
        "date": post["date"],
        "pretty": pretty_date(post["date"]),
        "arrow": icon("arrow-right"),
    }


def pretty_date(iso):
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    y, m, d = [int(x) for x in iso.split("-")]
    return "%d %s %d" % (d, months[m - 1], y)


def build_blog_hub():
    path = "/blog/"
    title, desc, og, lastmod = META[path]
    schema = graph(
        website_node(), person_node(), org_node(),
        portrait_node(),
        webpage_node(path, title, desc, "CollectionPage", og),
        breadcrumb_node(path, "Insights"),
        {
            "@type": "ItemList",
            "name": "Insights",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": p["title"],
                 "url": BASE + "/blog/" + p["slug"] + "/"}
                for i, p in enumerate(POSTS)
            ],
        },
    )
    first = POSTS[0]
    rest = POSTS[1:]

    body = """
%s
<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <span class="eyebrow">Insights</span>
      <h1>Field notes on recovery and social media security</h1>
      <p class="lead">Practical guidance on Facebook Page recovery, account appeals, Business Manager takeovers, verification and access audits — written from live cases rather than templates.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <article class="featured" data-reveal>
      <div>
        <div class="cluster">%s<span class="t-xs faint">%s · %d min read</span></div>
        <h2 class="featured__title"><a href="/blog/%s/" style="color:inherit;text-decoration:none">%s</a></h2>
        <p>%s</p>
        <p class="mt-5"><a class="btn btn--primary btn--sm" href="/blog/%s/">Read the guide %s</a></p>
      </div>
      <dl class="featured__side">
        <div class="fact"><dt>Category</dt><dd>%s</dd></div>
        <div class="fact"><dt>Updated</dt><dd>%s</dd></div>
        <div class="fact"><dt>Written by</dt><dd><a href="/about/">Atikul Islam Rabbi</a></dd></div>
      </dl>
    </article>

    <div class="grid grid--3 mt-7">%s</div>
  </div>
</section>
""" % (
        crumbs([("Home", "/"), ("Insights", "/blog/")]),
        badge(first["kicker"], "cyan"), pretty_date(first["date"]), first["read"],
        first["slug"], esc(first["title"]), esc(first["description"]),
        first["slug"], icon("arrow-right"),
        esc(first["kicker"]), pretty_date(first["updated"]),
        "".join(post_card(p) for p in rest),
    ) + cta_band(
        "Need this applied to your own accounts?",
        "Guides are general. A case review is specific to your assets, your evidence and your platform history.",
        ("Request an assessment", "/contact/"),
        ("See the services", "/services/"),
    )
    return page(title, desc, path, body, active="/blog/", og=og, schema=schema)


def build_post(post):
    path = "/blog/%s/" % post["slug"]
    title, desc, og, lastmod = META.get(path) or meta_for(path)
    related = [p for p in POSTS if p["slug"] != post["slug"]][:3]
    schema = graph(
        website_node(), person_node(), org_node(),portrait_node(),
        {
            "@type": "Article",
            "@id": BASE + path + "#article",
            "headline": post["title"],
            "description": post["description"],
            "url": BASE + path,
            "mainEntityOfPage": {"@id": BASE + path + "#webpage"},
            "image": {"@type": "ImageObject", "url": BASE + og, "width": 1200, "height": 630},
            "datePublished": post["date"],
            "dateModified": post["updated"],
            "inLanguage": "en",
            "author": {"@id": BASE + "/#person"},
            "publisher": {"@id": BASE + "/#organization"},
            "about": {"@id": BASE + "/#person"},
            "keywords": ", ".join([post["kicker"], "Meta", "social media security", "account recovery"]),
        },
        webpage_node(path, title, desc, "WebPage", og),
        breadcrumb_node(path, post["title"], [("Insights", "/blog/")]),
    )

    body = """
%(crumbs)s
<article>
  <section class="page-hero">
    <div class="container">
      <div class="page-hero__inner">
        <div class="cluster">%(badge)s<span class="t-xs faint">%(pretty)s · %(read)d min read</span></div>
        <h1>%(title)s</h1>
        <p class="lead">%(desc)s</p>
        <div class="page-hero__meta">
          <span>By <a href="/about/">Atikul Islam Rabbi</a></span>
          <span>Last updated %(updated)s</span>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="split">
        <div class="prose">%(body)s</div>
        <aside class="split__aside">
          <div class="glass" style="padding:var(--s5)">
            <img src="%(portrait)s" width="512" height="512" loading="lazy" decoding="async" alt="Atikul Islam Rabbi"
                 style="width:64px;height:64px;border-radius:50%%;object-fit:cover;object-position:50%% 22%%">
            <p class="footer-title mt-3">Written by</p>
            <p class="t-sm"><strong>Atikul Islam Rabbi</strong><br><span class="dim">Social Media Security Expert · Founder &amp; CEO, Cyber Infinity</span></p>
            <p class="t-xs dim mt-3">Recovery and security work for Facebook Pages, Instagram accounts and Meta Business Managers across the UK, UAE, South Asia and beyond.</p>
            <a class="btn btn--primary btn--block mt-4" href="/contact/?service=not-sure">Request an assessment</a>
          </div>
          <div class="callout mt-4">%(lock)s<span>Never send passwords or one-time codes. Not to me, not to anyone claiming to be platform support.</span></div>
        </aside>
      </div>
    </div>
  </section>
</article>

<section class="section section--line">
  <div class="container">
    %(related_head)s
    <div class="grid grid--3">%(related)s</div>
  </div>
</section>
""" % {
        "crumbs": crumbs([("Home", "/"), ("Insights", "/blog/"), (post["title"], path)]),
        "badge": badge(post["kicker"], "cyan"),
        "pretty": pretty_date(post["date"]),
        "read": post["read"],
        "title": esc(post["title"]),
        "desc": esc(post["description"]),
        "updated": pretty_date(post["updated"]),
        "body": post["body"],
        "portrait": SITE["portrait"],
        "lock": icon("lock"),
        "related_head": section_head("Keep reading", "Related guides", None, "related-title"),
        "related": "".join(post_card(p) for p in related),
    } + cta_band(
        "Want your own setup reviewed?",
        "A security audit maps every admin, integration and recovery path — then tells you what to fix first.",
        ("Request an audit", "/contact/?service=social-media-security-audit"),
        ("Read the services", "/services/"),
    )
    return page(title, desc, path, body, active="/blog/", og=og, schema=schema)


# --------------------------------------------------------------------------
# Legal
# --------------------------------------------------------------------------


def build_privacy():
    path = "/privacy-policy/"
    title, desc, og, lastmod = META[path]
    schema = graph(
        website_node(), person_node(), org_node(),
        portrait_node(),
        webpage_node(path, title, desc, "WebPage", og),
        breadcrumb_node(path, "Privacy Policy"),
    )
    body = """
%(crumbs)s
<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <span class="eyebrow">Legal</span>
      <h1>Privacy policy</h1>
      <p class="lead">How enquiry information is collected, used, stored and protected — in plain language.</p>
      <div class="page-hero__meta"><span>Last updated %(date)s</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="prose">
      <h2>Who is responsible</h2>
      <p>This site is operated by Atikul Islam Rabbi, Founder &amp; CEO of Cyber Infinity, based in Dhaka, Bangladesh. For any privacy question, use the <a href="/contact/">contact form</a>.</p>

      <h2>What is collected</h2>
      <ul>
        <li><strong>Enquiry details you submit</strong> — name, email address, selected service, urgency, asset name (optional) and the message you write.</li>
        <li><strong>Technical data</strong> — standard analytics such as pages viewed, approximate region, device type and referral source, if analytics is enabled and you consent where required.</li>
        <li><strong>Communication records</strong> — the email or WhatsApp correspondence that follows an enquiry.</li>
      </ul>
      <p>Passwords, one-time codes and recovery codes are never requested and should never be sent.</p>

      <h2>Why it is processed</h2>
      <ul>
        <li>To answer your enquiry and assess whether the service applies (legitimate interest, and steps taken at your request).</li>
        <li>To deliver agreed work and keep records of it (contract).</li>
        <li>To meet legal and accounting obligations (legal obligation).</li>
        <li>To measure site performance and improve it (consent, where required).</li>
      </ul>

      <h2>Processors</h2>
      <table>
        <thead><tr><th>Processor</th><th>Purpose</th><th>Data involved</th></tr></thead>
        <tbody>
          <tr><td>Web3Forms</td><td>Delivers the contact form to email</td><td>Form fields you submit</td></tr>
          <tr><td>Google (Tag Manager / Analytics)</td><td>Aggregate traffic measurement</td><td>Usage data, cookie identifiers</td></tr>
          <tr><td>GitHub Pages</td><td>Static hosting</td><td>Server request logs</td></tr>
          <tr><td>Email and messaging providers</td><td>Correspondence</td><td>Messages you send</td></tr>
        </tbody>
      </table>
      <p>These providers may process data outside your country. Where required, transfers rely on the providers' standard contractual safeguards.</p>

      <h2>How long it is kept</h2>
      <p>Enquiries that do not become engagements are kept for up to 12 months, then deleted. Engagement records are kept for as long as the relationship continues and for the period required by law afterwards. Analytics data is retained according to the analytics provider's settings.</p>

      <h2>Cookies and analytics</h2>
      <p>The site itself sets no cookies. Google Tag Manager and any analytics tags it loads may set cookies or read identifiers. Where consent is required, tags should only run after consent; you can block them at any time using your browser settings or a content blocker.</p>

      <h2>Your rights</h2>
      <p>Depending on where you live, you may request access to your data, correction, deletion, restriction, portability, or object to processing. Use the <a href="/contact/">contact form</a> and state what you need. You also have the right to complain to your local data protection authority.</p>

      <h2>Security</h2>
      <p>This site is served over HTTPS, publishes no databases or credentials, and keeps the intake surface deliberately small. Access to enquiry correspondence is limited to the operator. No system is perfectly secure, and no method of transmission is guaranteed, but the practical exposure is kept to what is necessary to answer you.</p>

      <h2>Client confidentiality</h2>
      <p>Case details are published only with permission. Where a client cannot be named, identifying details are generalised. Screenshots and documents are redacted before they are stored or shared.</p>

      <h2>Children</h2>
      <p>The services are intended for businesses and adults. The site is not directed at children and does not knowingly collect their data.</p>

      <h2>Changes</h2>
      <p>This policy may be updated. The date above always reflects the current version.</p>
    </div>
  </div>
</section>
""" % {
        "crumbs": crumbs([("Home", "/"), ("Privacy Policy", "/privacy-policy/")]),
        "date": "25 November 2026",
    }
    return page(title, desc, path, body, active="", og=og, schema=schema)


def build_terms():
    path = "/terms/"
    title, desc, og, lastmod = META[path]
    schema = graph(
        website_node(), person_node(), org_node(),
        portrait_node(),
        webpage_node(path, title, desc, "WebPage", og),
        breadcrumb_node(path, "Terms"),
    )
    body = """
%(crumbs)s
<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <span class="eyebrow">Legal</span>
      <h1>Terms &amp; service scope</h1>
      <p class="lead">The basis on which recovery, verification and security work is provided.</p>
      <div class="page-hero__meta"><span>Last updated %(date)s</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="prose">
      <h2>1. What is provided</h2>
      <p>Advisory and technical work relating to social media account security, recovery, verification and disputes — principally for Facebook, Instagram and Meta Business Manager. The scope of each engagement is agreed in writing before work begins.</p>

      <h2>2. No guaranteed outcome</h2>
      <p>Recovery, verification, dispute and appeal decisions are made by the platform, not by me. Nothing on this site or in any communication is a guarantee of recovery, reinstatement, verification or timing. Any statement about typical outcomes is descriptive, not predictive.</p>

      <h2>3. Your responsibilities</h2>
      <ul>
        <li>You must be the legitimate owner, or authorised to act for the owner, of every asset you ask me to work on.</li>
        <li>You must provide accurate information and genuine documents.</li>
        <li>You must not ask me to misrepresent ownership, submit false evidence, or circumvent a platform decision.</li>
        <li>You are responsible for keeping your own copies of documents you send.</li>
      </ul>

      <h2>4. Credentials and sensitive data</h2>
      <p>Passwords, one-time codes and recovery codes are never requested. If any third party requests them while claiming to act for this practice, treat it as fraud and report it. Where a platform process genuinely requires account access, it is discussed explicitly and handled through a method you control.</p>

      <h2 id="security">5. Confidentiality</h2>
      <p>Case information is treated as confidential. Details are published only with written permission, and identifying details are generalised where a client cannot be named. Client names, screenshots and documents are never published without consent.</p>

      <h2>6. Fees and payment</h2>
      <p>Fees are quoted per engagement and agreed in writing in advance. Work outside the agreed scope is quoted separately. Payment terms are set out in the engagement letter.</p>

      <h2>7. Limitation of liability</h2>
      <p>To the extent permitted by law, liability is limited to the fees paid for the specific engagement. I am not liable for platform decisions, account suspensions, lost revenue, loss of audience or indirect losses arising from an incident that predates the engagement.</p>

      <h2>8. Intellectual property</h2>
      <p>The content of this site, including text and design, belongs to Atikul Islam Rabbi. It may not be republished commercially without permission. Client trademarks remain the property of their owners.</p>

      <h2>9. Independence</h2>
      <p>This site and the services described are independent. They are not affiliated with, endorsed by, sponsored by or otherwise connected to Meta Platforms, Inc. Facebook, Instagram, WhatsApp and Meta Business Manager are trademarks of Meta Platforms, Inc.</p>

      <h2>10. Reporting a security issue</h2>
      <p>If you believe you have found a vulnerability in this site, please report it through the <a href="/contact/">contact form</a> with enough detail to reproduce it. Responsible disclosure is welcome and will be acknowledged. The machine-readable policy is at <a href="/.well-known/security.txt">/.well-known/security.txt</a>.</p>

      <h2>11. Governing law</h2>
      <p>These terms are governed by the laws of Bangladesh. Disputes are subject to the jurisdiction of the courts of Dhaka, without prejudice to any mandatory consumer protection rights you may have where you live.</p>

      <h2>12. Changes</h2>
      <p>These terms may be updated. The date above reflects the current version.</p>
    </div>
  </div>
</section>
""" % {
        "crumbs": crumbs([("Home", "/"), ("Terms", "/terms/")]),
        "date": "25 November 2026",
    }
    return page(title, desc, path, body, active="", og=og, schema=schema)


# --------------------------------------------------------------------------
# 404 + legacy redirect
# --------------------------------------------------------------------------


def build_404():
    title = "Page not found | Atikul Islam Rabbi"
    desc = "The page you requested does not exist. Start from the homepage, the services list or the case studies."
    schema = graph(breadcrumb_node("/404.html", "Page not found"))
    body = """
<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <span class="eyebrow">Error 404</span>
      <h1>This page does not exist</h1>
      <p class="lead">The link may be out of date, or the page may have moved. These are the routes most people are looking for.</p>
      <div class="page-hero__actions">
        <a class="btn btn--primary" href="/">Back to the homepage %s</a>
        <a class="btn btn--secondary" href="/contact/">Report a broken link</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid--4">
      <a class="card card--link" href="/services/"><span class="icon-badge">%s</span><h2 class="card__title mt-4">Services</h2><p class="card__text">Recovery, verification and security for Meta assets.</p></a>
      <a class="card card--link" href="/case-studies/"><span class="icon-badge">%s</span><h2 class="card__title mt-4">Case studies</h2><p class="card__text">Documented cases with their limits stated.</p></a>
      <a class="card card--link" href="/blog/"><span class="icon-badge">%s</span><h2 class="card__title mt-4">Insights</h2><p class="card__text">Guides on recovery, appeals and account security.</p></a>
      <a class="card card--link" href="/contact/"><span class="icon-badge">%s</span><h2 class="card__title mt-4">Contact</h2><p class="card__text">Request a confidential assessment.</p></a>
    </div>
  </div>
</section>
""" % (icon("arrow-right"), icon("life-buoy"), icon("file-text"), icon("clipboard-list"), icon("mail"))
    return page(title, desc, "/404.html", body, active="", schema=schema, noindex=True)


def build_redirect():
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Redirecting to atikulislam.me</title>
  <meta name="robots" content="noindex, follow">
  <link rel="canonical" href="https://atikulislam.me/">
  <meta http-equiv="refresh" content="0; url=https://atikulislam.me/">
  <meta name="description" content="This legacy address has moved. You are being redirected to atikulislam.me.">
  <script>window.location.replace('https://atikulislam.me/');</script>
  <style>body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:#07090E;color:#CBD5E1;display:grid;place-items:center;min-height:100vh;margin:0;text-align:center;padding:24px}a{color:#38BDF8}</style>
</head>
<body>
  <main>
    <h1 style="color:#F8FAFC">This address has moved</h1>
    <p>The current site is at <a href="https://atikulislam.me/">atikulislam.me</a>.</p>
    <p><a href="https://atikulislam.me/">Continue to atikulislam.me</a></p>
  </main>
</body>
</html>
"""


# --------------------------------------------------------------------------
# Site-level files
# --------------------------------------------------------------------------


def build_sitemap():
    urls = []
    for path in ["/", "/about/", "/services/", "/portfolio/", "/case-studies/", "/blog/",
                 "/faq/", "/contact/", "/privacy-policy/", "/terms/"]:
        urls.append((path, META[path][3]))
    for s in SERVICES:
        p = "/services/%s/" % s["slug"]
        urls.append((p, "2026-11-25"))
    for c in CASES:
        urls.append(("/case-studies/%s/" % c["slug"], "2026-11-25"))
    for p in POSTS:
        urls.append(("/blog/%s/" % p["slug"], p["updated"]))

    rows = []
    for path, lastmod in urls:
        if path == "/":
            image = "/assets/img/atikul-islam-rabbi-social-media-security-expert.jpg"
        else:
            image = meta_for(path)[2] if path in META or path.startswith(("/services/", "/case-studies/", "/blog/")) else None
            if path in META:
                image = META[path][2]
        img = ('\n    <image:image>\n      <image:loc>%s%s</image:loc>\n    </image:image>' % (BASE, image)) if image else ""
        rows.append("  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>%s\n  </url>" % (BASE, path, lastmod, img))

    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
            + "\n".join(rows) + "\n</urlset>\n")


def build_robots():
    return """# atikulislam.me
User-agent: *
Allow: /
Disallow: /Atikulislamx/
Disallow: /docs/
Disallow: /prompts/
Disallow: /scripts/
Disallow: /design/
Disallow: /data/
Disallow: /*.md$

# Crawl-delay is not needed; this is a static site.
Sitemap: https://atikulislam.me/sitemap.xml
"""


def build_config():
    return """# Jekyll configuration for GitHub Pages.
# The repository root is the web root, so anything not listed here would be
# published. Keep build inputs and internal documents out of the live site.

title: Atikul Islam Rabbi
description: Social media security, Meta recovery and digital asset protection.

exclude:
  - docs
  - prompts
  - scripts
  - design
  - data
  - README.md
  - RELEASE.md
  - package.json
  - package-lock.json
  - node_modules
  - .vscode
  - .env.example
  # Source photo for the hero portrait; underscore dirs are ignored by Jekyll,
  # this is belt and braces (and documents the intent).
  - assets/_source
  - .gitignore

# .well-known starts with a dot, so Jekyll excludes it unless it is included.
include:
  - .well-known

plugins: []
"""


def build_security_txt():
    return """Contact: mailto:help.atikulislam@gmail.com
Expires: 2027-11-25T00:00:00.000Z
Preferred-Languages: en, bn
Canonical: https://atikulislam.me/.well-known/security.txt
Policy: https://atikulislam.me/terms/#security
Acknowledgements: https://atikulislam.me/contact/
# Please report vulnerabilities privately and allow reasonable time to fix
# before public disclosure.
"""


def build_manifest():
    return json.dumps({
        "id": "/",
        "name": "Atikul Islam Rabbi — Social Media Security Expert",
        "short_name": "A. I. Rabbi",
        "description": "Recovery, verification and security for Facebook, Instagram and Meta Business Manager assets.",
        "lang": "en",
        "dir": "ltr",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "background_color": "#07090E",
        "theme_color": "#07090E",
        "icons": [
            {"src": "/assets/brand/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/brand/icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "/assets/brand/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }, indent=2) + "\n"


# --------------------------------------------------------------------------
# Write
# --------------------------------------------------------------------------


def write(rel, content):
    full = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)
    print("  wrote", rel, "(%d KB)" % (len(content.encode()) // 1024 or 1))


def main():
    print("Building pages…")
    write("index.html", build_home())
    write("about/index.html", build_about())
    write("services/index.html", build_services_hub())
    for svc in SERVICES:
        write("services/%s/index.html" % svc["slug"], build_service(svc))
    write("case-studies/index.html", build_cases_hub())
    for case in CASES:
        write("case-studies/%s/index.html" % case["slug"], build_case(case))
    write("portfolio/index.html", build_portfolio())
    write("faq/index.html", build_faq())
    write("contact/index.html", build_contact())
    write("blog/index.html", build_blog_hub())
    for post in POSTS:
        write("blog/%s/index.html" % post["slug"], build_post(post))
    write("privacy-policy/index.html", build_privacy())
    write("terms/index.html", build_terms())
    write("404.html", build_404())
    write("Atikulislamx/index.html", build_redirect())

    print("Building site files…")
    write("sitemap.xml", build_sitemap())
    write("robots.txt", build_robots())
    write("_config.yml", build_config())
    write(".well-known/security.txt", build_security_txt())
    write("site.webmanifest", build_manifest())
    print("Done.")


if __name__ == "__main__":
    main()
