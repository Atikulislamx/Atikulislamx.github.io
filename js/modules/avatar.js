/** Optional photo override from data/site.json. Static HTML already contains the
 * current portrait, so it stays visible if JSON is unavailable or JS is off.
 * Only supply a genuine photograph here; never synthesize a replacement face.
 */
async function initAvatars(siteDataUrl = '/data/site.json') {
  const containers = document.querySelectorAll('[data-avatar]');
  if (!containers.length) return;
  try {
    const res = await fetch(siteDataUrl);
    if (!res.ok) return;
    const { profilePhoto } = await res.json();
    if (typeof profilePhoto !== 'string' || !profilePhoto.trim()) return;
    containers.forEach(container => {
      const image = container.querySelector('img');
      if (!image || image.getAttribute('src') === profilePhoto) return;
      // Do not replace the known-good portrait until a future replacement loads.
      const candidate = new Image();
      candidate.onload = () => { image.src = profilePhoto; };
      candidate.src = profilePhoto;
    });
  } catch (_) { /* Static photo remains a functional fallback. */ }
}

initAvatars();
export { initAvatars };
