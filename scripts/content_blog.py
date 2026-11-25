# -*- coding: utf-8 -*-
"""Editorial content for /blog/. Imported by build_site.py.

Each post: slug, title (<=60 chars), description, kicker, date, updated,
read (minutes), body (HTML). Body uses .prose styles and <h2>/<h3>.
"""

POSTS = [
    {
        "slug": "recover-hacked-facebook-page",
        "title": "How to Recover a Hacked Facebook Page",
        "kicker": "Recovery",
        "date": "2026-11-18",
        "updated": "2026-11-18",
        "read": 8,
        "description": "A structured process for taking back a Facebook Page after admin access is removed: what to document, which Meta routes to use, and what makes a case fail.",
        "body": """
<p class="lead">A Page takeover is rarely a single event. Access is usually lost in one of three ways: an admin is removed by someone who still holds a role, the personal profile behind the admin role is itself compromised, or the Page is absorbed into a Business Manager that the attacker now controls. The route back is different in each case, which is why "just use the recovery form" fails so often.</p>

<div class="callout"><svg class="icon" aria-hidden="true"><use href="/assets/icons/sprite.svg#i-info"></use></svg><span><strong>First rule:</strong> do not delete the Page, do not create a duplicate, and do not pay anyone who guarantees recovery. Both actions make a legitimate claim harder to prove.</span></div>

<h2>1. Establish what actually happened</h2>
<p>Before contacting Meta, write down the sequence of events. A support team, and a reviewer, needs a timeline that can be checked:</p>
<ul>
  <li>The last time you had working admin access, with a date.</li>
  <li>Any email or notification about an admin change, a login from a new device, or a policy notice.</li>
  <li>Whether the Page is linked to a Business Manager, and who is listed as its owner.</li>
  <li>Whether the email address or phone number on your personal profile was changed.</li>
</ul>
<p>If your personal profile still works but the Page is gone from your list, the problem is a role change. If your profile is also locked out, the problem starts there — <a href="/services/facebook-account-recovery/">account recovery comes first</a>, because every Page route depends on a profile that Meta can verify.</p>

<h2>2. Check Business Manager before the Page</h2>
<p>Most high-value Pages are attached to a Business Manager. Open <em>Business settings → Accounts → Pages</em> and look at who holds admin or full control. If an unknown person appears, remove them first, then claim the Page back into your own portfolio. If you cannot open that Business Manager at all, you are dealing with a <a href="/services/meta-business-manager-recovery/">Business Manager takeover</a>, which needs its own claim.</p>

<h2>3. Use the recovery routes in the right order</h2>
<ol>
  <li><strong>Page roles route.</strong> From the Page's help menu, request admin access and complete identity verification. This works when ownership evidence still points to you.</li>
  <li><strong>Account recovery route.</strong> If the admin profile is compromised, restore the profile using the identity documents attached to that account, then return to the Page.</li>
  <li><strong>Business Manager ownership route.</strong> Where a Business Manager holds the Page, the claim is filed against the business, not the Page. Proof of legal entity matters more than a profile here.</li>
  <li><strong>Support inbox escalation.</strong> Only after a case exists — an escalation without a case number and a clean evidence set tends to be closed as duplicate.</li>
</ol>

<h2>4. Build the evidence file</h2>
<p>Reviewers decide on documents, not explanations. A strong file contains:</p>
<ul>
  <li>Government ID matching the name on the admin profile (never sent over chat or a form to a third party).</li>
  <li>Business registration or a tax document matching the Page's name.</li>
  <li>Older admin invitations, screenshots of the Page's dashboard from before the loss, or Meta emails addressed to you.</li>
  <li>Domain or website control, if the Page represents a business with a site.</li>
</ul>
<p>Redact everything that is not needed. A reviewer does not need your home address, payment details, or audience data.</p>

<h2>5. What makes a case fail</h2>
<ul>
  <li><strong>Conflicting claims.</strong> Two people filing for the same Page slows both.</li>
  <li><strong>Mismatched identity.</strong> The name on the ID, the profile, and the business documents do not agree.</li>
  <li><strong>Unresolved policy strikes.</strong> A Page under a content or trademark restriction is reviewed differently from one that was only hijacked.</li>
  <li><strong>Repeated duplicate tickets.</strong> Each new ticket without a case number resets the context.</li>
</ul>

<h2>6. Secure the Page the moment it returns</h2>
<p>Recovery without hardening invites a second takeover. Within the first hour: remove every unrecognised admin, switch on two-factor authentication for all remaining admins, review connected apps and business integrations, confirm the recovery email and phone, and check scheduled posts and payment methods before they are used.</p>

<h2>Realistic expectations</h2>
<p>Some recoveries close in days. Others take weeks of review, and some are not recoverable — for example where the Page was deleted, or where ownership genuinely cannot be evidenced. A professional assessment should tell you which of those you are looking at before any work starts. If you want that review, <a href="/contact/?service=facebook-page-recovery">describe the situation</a> and I will tell you plainly what is realistic.</p>
""",
    },
    {
        "slug": "facebook-account-disabled-appeal",
        "title": "Facebook Account Disabled: How to Appeal",
        "kicker": "Recovery",
        "date": "2026-11-11",
        "updated": "2026-11-11",
        "read": 7,
        "description": "Why Facebook accounts get disabled, how the appeal and identity-verification routes work, and the mistakes that get a second appeal rejected.",
        "body": """
<p class="lead">A disabled personal account is usually a bigger business problem than it looks. Pages, ad accounts, pixels, catalogs and Business Manager roles all hang off a personal profile. When that profile is disabled, the assets do not disappear — but the person who can administer them does.</p>

<h2>Why accounts are disabled</h2>
<p>The notice you receive is deliberately short. In practice, disabling follows one of these triggers:</p>
<ul>
  <li><strong>Identity suspicion.</strong> A new device, a new country, or a name that does not look consistent with the account history.</li>
  <li><strong>Impersonation reports.</strong> Someone reports the profile as fake, often the same attacker who took it over.</li>
  <li><strong>Automated behaviour flags.</strong> Bulk messaging, rapid friend requests, or automation tools.</li>
  <li><strong>Policy enforcement.</strong> Content or advertising violations, sometimes inherited from a Page you administer.</li>
</ul>

<h2>The appeal is a document problem</h2>
<p>Most rejected appeals are rejected for one of three reasons: the submitted ID does not match the account name, the photo is unreadable, or the appeal is submitted from a device and network that do not resemble the account's history. Before you submit:</p>
<ol>
  <li>Use the device and connection you normally use for that account.</li>
  <li>Submit a clear, colour photo of a government ID where the name matches the profile name.</li>
  <li>If the account name is a variation (for example a middle name or a transliteration), explain that in the appeal text — do not guess.</li>
  <li>Submit once, then wait. Repeated submissions create duplicate cases that are closed automatically.</li>
</ol>

<div class="callout"><svg class="icon" aria-hidden="true"><use href="/assets/icons/sprite.svg#i-info"></use></svg><span>Never send identity documents to a person offering recovery in a direct message. Meta does not ask for documents by chat, and a document set is enough to impersonate you convincingly.</span></div>

<h2>If your Business Manager depends on the profile</h2>
<p>Do not wait for the appeal to resolve before protecting the business. Two immediate moves:</p>
<ul>
  <li>Ask another trusted admin in the Business Manager to add a second admin profile, so the business is not single-threaded.</li>
  <li>Record the asset inventory now — Page IDs, ad account IDs, pixel IDs, domains — while you can still see them. That inventory is what a claim needs later.</li>
</ul>
<p>If nobody else holds admin rights, the business side becomes a <a href="/services/meta-business-manager-recovery/">Business Manager recovery</a> question rather than an appeal question.</p>

<h2>Timelines, honestly</h2>
<p>Appeals are time-sensitive, but the review queue is not something an applicant can speed up. Some cases resolve in 48 hours; some sit for weeks; some are refused with no explanation and can only be re-opened with additional evidence. Anyone who promises a fixed timeline is guessing.</p>

<h2>Prevention that actually works</h2>
<ul>
  <li>Two-factor authentication with an app or hardware key, not SMS.</li>
  <li>Two trusted contacts configured in Meta Accounts Center.</li>
  <li>A recovery email on a domain you control, not a second free mailbox.</li>
  <li>At least two admins on every business asset, both with 2FA.</li>
</ul>
<p>The <a href="/services/social-media-security-audit/">security audit</a> exists precisely to find these gaps before an attacker does. If your account is disabled now, <a href="/contact/?service=facebook-account-recovery">start with a case review</a>.</p>
""",
    },
    {
        "slug": "instagram-account-hacked-recovery",
        "title": "Instagram Account Hacked: Recovery Steps",
        "kicker": "Recovery",
        "date": "2026-11-04",
        "updated": "2026-11-04",
        "read": 7,
        "description": "What to do in the first hour after an Instagram takeover, which verification route fits creator and business accounts, and how to stop a second breach.",
        "body": """
<p class="lead">Instagram takeovers follow a pattern. The attacker changes the email, adds two-factor authentication to a device you do not control, and often posts or messages your audience before you notice. Speed matters, but the order of the steps matters more.</p>

<h2>Minute one: protect the recovery path</h2>
<ul>
  <li><strong>Do not delete the app or the account.</strong> Deletion removes the history a reviewer needs.</li>
  <li><strong>Try "Secure your account".</strong> The login screen flow can revert a changed email if your device is recognised.</li>
  <li><strong>Check the linked Facebook Page.</strong> If the Instagram account is connected to a Page or Business Manager, an admin there may be able to reclaim it through Meta Business Suite.</li>
  <li><strong>Tell your audience, once.</strong> A short story or pinned comment prevents the attacker from monetising your trust.</li>
</ul>

<h2>Pick the route that matches the account type</h2>
<table>
  <thead><tr><th>Account type</th><th>Primary route</th><th>Strongest evidence</th></tr></thead>
  <tbody>
    <tr><td>Personal / creator</td><td>Login help → identity verification</td><td>Video selfie, original email, device history</td></tr>
    <tr><td>Business, linked to a Page</td><td>Meta Business Suite → asset claim</td><td>Page admin role, business documents</td></tr>
    <tr><td>Creator with a verified badge</td><td>Support form + verification review</td><td>ID, prior notices, brand documentation</td></tr>
    <tr><td>Managed by an agency</td><td>Business Manager ownership</td><td>Written authorisation from the brand</td></tr>
  </tbody>
</table>

<div class="callout callout--warn"><svg class="icon" aria-hidden="true"><use href="/assets/icons/sprite.svg#i-triangle-alert"></use></svg><span>If the attacker has posted a "recovery service" contact in your bio, your audience is now the target. Warn them explicitly and ask them to report the impostor account rather than message it.</span></div>

<h2>What reviewers look for</h2>
<p>Instagram reviews are evidence-driven. A case is stronger when the original email address, an older device, and an identity document all point to the same person. Cases are weaker when the account was created recently, when the name on documents differs from the profile, or when multiple people submit competing claims for the same handle.</p>

<h2>After you are back in</h2>
<ul>
  <li>Remove every unrecognised login session and connected app.</li>
  <li>Replace SMS two-factor with an authenticator app or a passkey.</li>
  <li>Change the email to a mailbox you control with its own 2FA.</li>
  <li>Check linked ad accounts, shops and creator tools for unknown connections.</li>
  <li>Review the "download your information" export for actions taken during the takeover.</li>
</ul>

<h2>When it is not a hack</h2>
<p>Some "hacked" accounts are actually disabled for policy reasons, or were deactivated by a former team member who still had the password. The distinction changes the route entirely, and misdiagnosing it wastes the one clean appeal you get. If you are unsure which situation you are in, <a href="/contact/?service=instagram-account-recovery">send the timeline</a> and get a read before you file anything.</p>
""",
    },
    {
        "slug": "meta-business-manager-hacked",
        "title": "Meta Business Manager Hacked: What to Do",
        "kicker": "Security",
        "date": "2026-10-27",
        "updated": "2026-10-27",
        "read": 8,
        "description": "A Business Manager takeover puts Pages, ad accounts and pixels under someone else's control. Here is the containment order and the claim process that works.",
        "body": """
<p class="lead">A compromised Business Manager is the most expensive social media incident a company can have, because it controls everything at once: Pages, ad accounts, pixels, catalogs, domains, Instagram accounts and payment methods. The instinct is to change passwords. That is not the first step.</p>

<h2>1. Contain the money</h2>
<p>Before anything else, ask the finance owner to check the payment method attached to the ad account and to watch for new charges. If a card is exposed, freeze it with the bank rather than removing it in Business Manager — an attacker with full control can re-add it.</p>

<h2>2. Map who holds control</h2>
<p>From a surviving admin account, open <em>Business settings → People</em> and record every name, email and role. Look specifically for:</p>
<ul>
  <li>New admins added in the last 30 days.</li>
  <li>Former employees or agencies who were never removed.</li>
  <li>Unknown "system user" or API integrations.</li>
  <li>Ownership transfers of Pages or ad accounts.</li>
</ul>
<p>Screenshot the list before removing anyone. If the case becomes a claim, that record is evidence.</p>

<h2>3. Decide which problem you have</h2>
<table>
  <thead><tr><th>Situation</th><th>What it means</th><th>Realistic route</th></tr></thead>
  <tbody>
    <tr><td>You still hold admin, an intruder was added</td><td>Contained intrusion</td><td>Remove access, rotate credentials, audit integrations</td></tr>
    <tr><td>You were removed, but another admin remains</td><td>Role dispute</td><td>Internal re-add, then formal dispute if refused</td></tr>
    <tr><td>No legitimate admin remains</td><td>Full takeover</td><td>Business ownership claim with legal-entity evidence</td></tr>
    <tr><td>Business Manager is restricted, not stolen</td><td>Policy / verification issue</td><td>Verification or appeal, not recovery</td></tr>
  </tbody>
</table>

<h2>4. The claim is about the business, not the profile</h2>
<p>When no legitimate admin remains, Meta reviews the claim against the legal entity. Prepare the documents that match the business name exactly as it appears on the Business Manager:</p>
<ul>
  <li>Company registration or incorporation certificate.</li>
  <li>A recent utility bill or bank statement showing the registered address.</li>
  <li>A phone number on the business record that can receive a verification code.</li>
  <li>Domain control: a DNS record or an email on the company domain.</li>
  <li>Authorisation letter if an agency is filing on the brand's behalf.</li>
</ul>
<p>Name mismatches are the single most common reason a claim stalls — a trading name versus a registered name, an abbreviation, or a translated entity name.</p>

<h2>5. Recover the assets in order</h2>
<ol>
  <li><strong>Pages</strong> — reclaim admin, then remove unknown roles.</li>
  <li><strong>Instagram</strong> — relink to the recovered Page.</li>
  <li><strong>Ad accounts</strong> — restore access, then review billing and campaign history for unauthorised spend.</li>
  <li><strong>Pixels and catalogs</strong> — reinstall or rotate if the attacker could have copied them.</li>
  <li><strong>Domains</strong> — verify domain ownership and remove unknown verification tokens.</li>
</ol>

<h2>6. Rebuild so it cannot repeat</h2>
<p>Two admins minimum, both on app-based two-factor. No shared logins. Remove agency access the day a contract ends. Review <em>Business settings → People</em> and connected apps quarterly — this is one of the checks in the <a href="/services/social-media-security-audit/">security audit</a>.</p>

<div class="callout"><svg class="icon" aria-hidden="true"><use href="/assets/icons/sprite.svg#i-lock"></use></svg><span>I never ask for your password, a one-time code, or recovery codes. Any assessor who does is a risk, not a resource.</span></div>

<p>If the Business Manager is currently outside your control, <a href="/contact/?service=meta-business-manager-recovery">send the timeline and the asset list</a>. The first answer you need is which of the four situations above you are in.</p>
""",
    },
    {
        "slug": "meta-business-verification-documents",
        "title": "Meta Business Verification: What Passes",
        "kicker": "Verification",
        "date": "2026-10-20",
        "updated": "2026-10-20",
        "read": 6,
        "description": "The documents, name matching and domain checks that decide a Meta business verification — and the recurring reasons applications are rejected.",
        "body": """
<p class="lead">Business verification is not a formality and it is not discretionary. It is a document-matching exercise. When the legal name, address, phone and domain all point to the same entity, approval is routine. When they do not, applications fail repeatedly with no useful explanation.</p>

<h2>The four things Meta is checking</h2>
<ol>
  <li><strong>Legal existence.</strong> The business is registered somewhere, and the document shows it.</li>
  <li><strong>Name match.</strong> The name on the document matches the name in Business Manager.</li>
  <li><strong>Address match.</strong> A document shows the address entered in the business profile.</li>
  <li><strong>Control.</strong> You can act for the business — typically proven by domain or phone control.</li>
</ol>

<h2>Documents that are usually accepted</h2>
<table>
  <thead><tr><th>Purpose</th><th>Examples</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>Legal entity</td><td>Certificate of incorporation, trade licence, tax registration</td><td>Must show the registered name and, ideally, an address</td></tr>
    <tr><td>Address</td><td>Utility bill, bank statement, lease</td><td>Recent (usually within 90 days), full document, not cropped</td></tr>
    <tr><td>Phone</td><td>Number able to receive SMS or a call</td><td>Use a business line, not a personal mobile that changes</td></tr>
    <tr><td>Domain</td><td>DNS TXT record, meta tag, or a file on the site</td><td>Domain should match the business, not a free subdomain</td></tr>
  </tbody>
</table>

<h2>The seven reasons applications fail</h2>
<ul>
  <li><strong>Trading name vs legal name.</strong> "Arpa Foods" on the site, "Arpa Food Products Ltd" on the certificate. Use the legal name in Business Manager.</li>
  <li><strong>Translated documents.</strong> A certified translation is often required; a photo of a document in another script may be refused.</li>
  <li><strong>Old address proofs.</strong> Statements older than the accepted window are treated as missing.</li>
  <li><strong>Cropped or watermarked documents.</strong> Submit the whole page, unedited.</li>
  <li><strong>Shared infrastructure.</strong> A free website builder subdomain or a generic email domain weakens the control signal.</li>
  <li><strong>Mismatched phone.</strong> The number entered does not match the business record.</li>
  <li><strong>Retrying without changes.</strong> Resubmitting identical documents produces identical results.</li>
</ul>

<div class="callout callout--ok"><svg class="icon" aria-hidden="true"><use href="/assets/icons/sprite.svg#i-check"></use></svg><span><strong>Do this first:</strong> write the legal name, registered address, business phone and domain on one page. Every field in Business Manager must match that page exactly before you submit.</span></div>

<h2>Before and after verification</h2>
<p>Verification unlocks ad spend limits, certain features and a stronger footing in disputes — but it does not fix a restricted ad account, and it does not remove policy strikes. If a restriction exists, that is a separate appeal with its own evidence. The <a href="/services/business-verification-guidance/">verification service</a> exists to prepare the file once, correctly, rather than learning the rules through rejections.</p>

<h2>If you have already been rejected</h2>
<p>Do not resubmit the same file. Send the rejection notice, the documents used, and the exact business details in Business Manager for a review. <a href="/contact/?service=business-verification-guidance">Ask for an assessment</a> — usually the mismatch is visible in a few minutes.</p>
""",
    },
    {
        "slug": "social-media-security-audit-checklist",
        "title": "Social Media Security Audit Checklist",
        "kicker": "Security",
        "date": "2026-10-13",
        "updated": "2026-10-13",
        "read": 9,
        "description": "A practical 30/60/90-day checklist for auditing access, admin roles, two-factor authentication and asset ownership across Meta and other social platforms.",
        "body": """
<p class="lead">Most social media incidents are not sophisticated. They are an old employee who still had admin rights, a shared password in a spreadsheet, two-factor authentication switched off on the one profile that controls everything, or an agency that was never removed. An audit finds those before an attacker does.</p>

<h2>The inventory (start here)</h2>
<p>You cannot secure what you have not listed. Build one table with a row per asset:</p>
<ul>
  <li>Facebook Pages, Instagram accounts, ad accounts, pixels, catalogs and domains.</li>
  <li>The Business Manager that owns each asset, and its business ID.</li>
  <li>Every person with access, their role, and why they have it.</li>
  <li>Recovery email and phone for each personal profile that holds admin.</li>
  <li>Connected third-party apps and scheduling tools.</li>
</ul>
<p>If a single personal profile appears as the only admin for most assets, that is your biggest finding on day one.</p>

<h2>Access and roles</h2>
<ul>
  <li>Minimum two admins per business asset, on separate people.</li>
  <li>No shared logins; agency access granted through Business Manager, never by password.</li>
  <li>Former team members removed on the day they leave, with a written check.</li>
  <li>Quarterly review of <em>Business settings → People</em> and connected apps.</li>
</ul>

<h2>Authentication</h2>
<ul>
  <li>App-based two-factor or a passkey on every admin profile — SMS is the weakest option and is vulnerable to SIM swap.</li>
  <li>Recovery email on a domain the business controls.</li>
  <li>Trusted contacts configured, so a lockout is survivable.</li>
  <li>No one-time codes sent over chat, ever.</li>
</ul>

<div class="callout callout--warn"><svg class="icon" aria-hidden="true"><use href="/assets/icons/sprite.svg#i-triangle-alert"></use></svg><span>The most common breach path in small businesses is not malware. It is a message that says "I'm from Meta support, send the code". Train the person who answers the inbox.</span></div>

<h2>Asset ownership</h2>
<ul>
  <li>Every Page and ad account sits inside a Business Manager owned by the business, not by an agency or a freelancer.</li>
  <li>Business verification completed, with documents stored somewhere the company controls.</li>
  <li>Domains verified in Business Manager; unknown verification tokens removed.</li>
  <li>Pixel and catalog ownership confirmed, with no legacy tokens from former vendors.</li>
</ul>

<h2>Monitoring and response</h2>
<ul>
  <li>Login alerts enabled and routed to a monitored inbox.</li>
  <li>A one-page incident plan: who calls the bank, who contacts Meta, who speaks to the audience, who keeps the evidence log.</li>
  <li>An offline copy of the asset inventory and key documents.</li>
</ul>

<h2>30 / 60 / 90 days</h2>
<table>
  <thead><tr><th>Window</th><th>Outcome</th></tr></thead>
  <tbody>
    <tr><td>Days 1–30</td><td>Inventory complete, unknown admins removed, 2FA enforced on every admin profile</td></tr>
    <tr><td>Days 31–60</td><td>Ownership consolidated into the company Business Manager, verification filed, domain and pixel ownership confirmed</td></tr>
    <tr><td>Days 61–90</td><td>Offboarding process documented, incident plan tested, quarterly review scheduled</td></tr>
  </tbody>
</table>

<p>A <a href="/services/social-media-security-audit/">structured audit</a> compresses this into a prioritised report — what is exposed now, what it would take to fix, and what to do first. If you would rather start with a conversation, <a href="/contact/?service=social-media-security-audit">describe your setup</a>.</p>
""",
    },
]
