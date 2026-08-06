/**
 * src/js/modules/avatar.js
 *
 * Reads data/site.json's `profilePhoto` field. Both a local relative path
 * and a full URL are valid <img src> values, so no branching on "which
 * kind" is needed — if the field is a non-empty string, it's used directly.
 *
 * When absent/null: every [data-avatar] container keeps rendering the
 * CSS monogram already in the markup (see avatar.css) — nothing to do.
 * When present: the monogram content is replaced with a real <img>, inside
 * the exact same .avatar container/classes, so no HTML structure, CSS, or
 * layout changes either way.
 *
 * Markup contract:
 *   <span class="avatar avatar--lg" data-avatar>
 *     <span aria-hidden="true">AIR</span>
 *   </span>
 */

async function initAvatars(siteDataUrl = '/data/site.json') {
  let site;
  try {
    const res = await fetch(siteDataUrl);
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    site = await res.json();
  } catch (err) {
    console.warn('[avatar] Could not load site.json — keeping monogram placeholder.', err);
    return;
  }

  const photo = site.profilePhoto;
  if (typeof photo !== 'string' || photo.trim() === '') {
    return; // no real photo yet — CSS monogram default stands as-is
  }

  document.querySelectorAll('[data-avatar]').forEach((container) => {
    const img = document.createElement('img');
    img.src = photo;
    img.alt = site.profilePhotoAlt || 'Atikul Islam Rabbi, Founder & CEO of Cyber Infinity';
    img.className = 'avatar__image';
    img.loading = 'lazy';
    container.replaceChildren(img);
  });
}

document.addEventListener('DOMContentLoaded', () => initAvatars());

export { initAvatars };
