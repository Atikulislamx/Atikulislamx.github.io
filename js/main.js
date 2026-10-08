/* ==========================================================================
   main.js — site-wide behaviour (vanilla JS, no dependencies)

   Every feature here is an enhancement. The mobile menu, FAQ, and service
   links work with JavaScript disabled because they use <details> and <a>.
   Each block checks for its own elements and does nothing if they are absent.
   ========================================================================== */
(function () {
  'use strict';

  var doc = document;
  var html = doc.documentElement;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var desktop = window.matchMedia('(min-width: 1024px)');

  /* 1. Header: hairline border once the page has scrolled ------------------ */
  var header = doc.querySelector('[data-site-header]');
  if (header) {
    var ticking = false;
    var updateHeader = function () {
      header.classList.toggle('is-scrolled', window.scrollY > 8);
      ticking = false;
    };
    window.addEventListener('scroll', function () {
      if (!ticking) {
        window.requestAnimationFrame(updateHeader);
        ticking = true;
      }
    }, { passive: true });
    updateHeader();
  }

  /* 2. Scroll reveal: only when motion is allowed and observers exist ------- */
  var revealItems = doc.querySelectorAll('[data-reveal]');
  if (revealItems.length && !reduceMotion.matches && 'IntersectionObserver' in window) {
    html.classList.add('reveal-ready');
    var observer = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealItems.forEach(function (el) { observer.observe(el); });
  }

  /* 3. Desktop Services submenu: disclosure button with aria-expanded ------- */
  doc.querySelectorAll('[data-submenu]').forEach(function (item) {
    var toggle = item.querySelector('.site-nav__sub-toggle');
    if (!toggle) return;

    var setOpen = function (open) {
      item.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    };

    toggle.addEventListener('click', function () {
      setOpen(!item.classList.contains('is-open'));
    });

    item.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && item.classList.contains('is-open')) {
        setOpen(false);
        toggle.focus();
      }
    });

    item.addEventListener('focusout', function (event) {
      if (event.relatedTarget && !item.contains(event.relatedTarget)) setOpen(false);
    });

    doc.addEventListener('click', function (event) {
      if (!item.contains(event.target)) setOpen(false);
    });
  });

  /* 4. Mobile menu (<details>): scroll lock, Escape, focus leaving the menu - */
  var mobileNav = doc.querySelector('[data-nav-mobile]');
  if (mobileNav) {
    var mobileSummary = mobileNav.querySelector('summary');

    mobileNav.addEventListener('toggle', function () {
      html.classList.toggle('nav-locked', mobileNav.open);
    });

    mobileNav.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && mobileNav.open) {
        mobileNav.open = false;
        if (mobileSummary) mobileSummary.focus();
      }
    });

    mobileNav.addEventListener('focusout', function (event) {
      if (mobileNav.open && event.relatedTarget && !mobileNav.contains(event.relatedTarget)) {
        mobileNav.open = false;
      }
    });

    mobileNav.addEventListener('click', function (event) {
      if (mobileNav.open && event.target.closest('a')) mobileNav.open = false;
    });

    doc.addEventListener('click', function (event) {
      if (mobileNav.open && !mobileNav.contains(event.target)) mobileNav.open = false;
    });

    desktop.addEventListener('change', function (event) {
      if (event.matches) mobileNav.open = false;
    });
  }
}());
