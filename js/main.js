/**
 * js/main.js
 * Site-wide behavior: sticky header shadow, mobile nav toggle, scroll-reveal.
 * No framework, no build step — plain ES modules loaded via <script type="module">.
 */

function initHeaderScrollState() {
  const header = document.querySelector('.site-header');
  if (!header) return;
  const onScroll = () => {
    header.classList.toggle('is-scrolled', window.scrollY > 8);
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}

function initMobileNav() {
  const toggle = document.querySelector('[data-nav-toggle]');
  const panel = document.querySelector('[data-mobile-nav]');
  const closeBtn = document.querySelector('[data-nav-close]');
  if (!toggle || !panel) return;

  const open = () => {
    panel.classList.add('is-open');
    toggle.setAttribute('aria-expanded', 'true');
    panel.querySelector('a, button')?.focus();
    document.body.style.overflow = 'hidden';
  };
  const close = () => {
    panel.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.focus();
    document.body.style.overflow = '';
  };

  toggle.addEventListener('click', () => {
    const isOpen = panel.classList.contains('is-open');
    isOpen ? close() : open();
  });
  closeBtn?.addEventListener('click', close);

  panel.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') close();
  });

  // Close the panel when a nav link inside it is activated
  panel.querySelectorAll('a').forEach((link) => link.addEventListener('click', close));
}

function initScrollReveal() {
  const targets = document.querySelectorAll('[data-reveal]');
  if (!targets.length) return;

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReducedMotion) {
    targets.forEach((el) => el.classList.add('is-visible'));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );

  targets.forEach((el) => observer.observe(el));
}

function initServicesSubmenuKeyboard() {
  // Ensure the desktop mega-menu opens on focus (keyboard), not just hover.
  document.querySelectorAll('.has-submenu').forEach((item) => {
    const submenu = item.querySelector('.submenu');
    if (!submenu) return;
    item.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        item.querySelector('a')?.focus();
      }
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initHeaderScrollState();
  initMobileNav();
  initScrollReveal();
  initServicesSubmenuKeyboard();
});
