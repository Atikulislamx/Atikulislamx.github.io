/** Shared progressive enhancements; static links and content remain usable without JS. */
function initHeaderScrollState() {
  const header = document.querySelector('.site-header');
  if (!header) return;
  const update = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
  update();
  window.addEventListener('scroll', update, { passive: true });
}

function initMobileNav() {
  const toggle = document.querySelector('[data-nav-toggle]');
  const panel = document.querySelector('[data-mobile-nav]');
  if (!toggle || !panel) return;
  panel.inert = true;
  const closeButton = panel.querySelector('[data-nav-close]');
  const header = document.querySelector('.site-header');
  let previousOverflow = '';
  let previousFocus = null;
  const isOpen = () => panel.classList.contains('is-open');

  function close(restoreFocus = true) {
    if (!isOpen()) return;
    panel.classList.remove('is-open');
    panel.inert = true;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
    document.body.style.overflow = previousOverflow;
    if (header) header.inert = false;
    if (restoreFocus) (previousFocus?.isConnected && previousFocus !== document.body ? previousFocus : toggle).focus();
  }
  function open() {
    previousFocus = document.activeElement;
    previousOverflow = document.body.style.overflow;
    panel.inert = false;
    panel.classList.add('is-open');
    toggle.setAttribute('aria-expanded', 'true');
    toggle.setAttribute('aria-label', 'Close menu');
    document.body.style.overflow = 'hidden';
    if (header) header.inert = true;
    (closeButton || panel.querySelector('a, summary'))?.focus();
  }

  toggle.addEventListener('click', () => isOpen() ? close() : open());
  closeButton?.addEventListener('click', () => close());
  panel.addEventListener('click', event => {
    if (event.target.closest('a')) close(false);
  });
  document.addEventListener('keydown', event => {
    if (!isOpen()) return;
    if (event.key === 'Escape') { event.preventDefault(); close(); return; }
    if (event.key !== 'Tab') return;
    const focusable = [...panel.querySelectorAll('a, button, summary')]
      .filter(el => el.getClientRects().length && !el.closest('details:not([open])'));
    if (!focusable.length) return;
    const first = focusable[0], last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  });
  // Breakpoint changes should never leave a hidden overlay or locked document.
  const desktop = window.matchMedia('(min-width: 1024px)');
  desktop.addEventListener('change', event => { if (event.matches) close(false); });
}

function initDesktopServices() {
  document.querySelectorAll('.has-submenu').forEach(item => {
    item.addEventListener('keydown', event => {
      if (event.key !== 'Escape') return;
      event.preventDefault();
      item.classList.add('is-dismissed');
      item.querySelector('.site-nav__link')?.focus();
    });
    item.addEventListener('focusout', event => {
      if (!item.contains(event.relatedTarget)) item.classList.remove('is-dismissed');
    });
    item.addEventListener('mouseleave', () => {
      if (!item.contains(document.activeElement)) item.classList.remove('is-dismissed');
    });
  });
}

initHeaderScrollState();
initMobileNav();
initDesktopServices();
