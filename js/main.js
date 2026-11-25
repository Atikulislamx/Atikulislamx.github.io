/* ==========================================================================
   main.js — atikulislam.me
   Vanilla JS, no dependencies, every block guarded. Content and navigation
   work without JavaScript; this file adds polish, not access.
   ========================================================================== */
(function () {
  'use strict';

  var doc = document;
  var root = doc.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var desktop = window.matchMedia('(min-width: 1024px)');

  function push(event, data) {
    window.dataLayer = window.dataLayer || [];
    var payload = { event: event };
    if (data) { Object.keys(data).forEach(function (k) { payload[k] = data[k]; }); }
    window.dataLayer.push(payload);
  }

  /* 1. Sticky header hairline ------------------------------------------------ */
  var header = doc.querySelector('[data-header]');
  if (header) {
    var ticking = false;
    var onScroll = function () {
      header.classList.toggle('is-scrolled', window.scrollY > 6);
      ticking = false;
    };
    window.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(onScroll); ticking = true; }
    }, { passive: true });
    onScroll();
  }

  /* 2. Desktop mega-menu ----------------------------------------------------- */
  var mega = doc.querySelector('[data-mega]');
  var trigger = doc.querySelector('[data-mega-trigger]');
  if (mega && trigger) {
    var hoverTimer = null;
    var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');

    var setMega = function (open) {
      mega.setAttribute('data-open', open ? 'true' : 'false');
      trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
    };

    trigger.addEventListener('click', function () {
      setMega(mega.getAttribute('data-open') !== 'true');
    });

    if (finePointer.matches) {
      var host = trigger.closest('li') || trigger;
      var openSoon = function () {
        window.clearTimeout(hoverTimer);
        hoverTimer = window.setTimeout(function () { setMega(true); }, 90);
      };
      var closeSoon = function () {
        window.clearTimeout(hoverTimer);
        hoverTimer = window.setTimeout(function () {
          if (!mega.contains(doc.activeElement)) { setMega(false); }
        }, 160);
      };
      host.addEventListener('mouseenter', openSoon);
      host.addEventListener('mouseleave', closeSoon);
      mega.addEventListener('mouseenter', function () { window.clearTimeout(hoverTimer); });
      mega.addEventListener('mouseleave', closeSoon);
    }

    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mega.getAttribute('data-open') === 'true') {
        setMega(false);
        trigger.focus();
      }
    });

    doc.addEventListener('click', function (e) {
      if (mega.getAttribute('data-open') === 'true' &&
          !mega.contains(e.target) && !trigger.contains(e.target)) {
        setMega(false);
      }
    });

    doc.addEventListener('focusin', function (e) {
      if (mega.getAttribute('data-open') === 'true' &&
          !mega.contains(e.target) && !trigger.contains(e.target)) {
        setMega(false);
      }
    });

    desktop.addEventListener('change', function (e) { if (e.matches) setMega(false); });
  }

  /* 3. Mobile drawer --------------------------------------------------------- */
  var drawer = doc.querySelector('[data-drawer]');
  var navToggle = doc.querySelector('[data-nav-toggle]');
  if (drawer && navToggle) {
    var pageRegions = doc.querySelectorAll('[data-inert-when-open]');
    var lastFocus = null;
    var scrollY = 0;

    var setDrawer = function (open) {
      drawer.setAttribute('data-open', open ? 'true' : 'false');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      var label = navToggle.querySelector('[data-nav-label]');
      if (label) { label.textContent = open ? 'Close' : 'Menu'; }

      Array.prototype.forEach.call(pageRegions, function (el) {
        if (open) { el.setAttribute('inert', ''); } else { el.removeAttribute('inert'); }
      });

      if (open) {
        lastFocus = doc.activeElement;
        scrollY = window.scrollY;
        doc.body.style.top = '-' + scrollY + 'px';
        doc.body.classList.add('is-locked');
        var first = drawer.querySelector('a, button, summary');
        if (first) { first.focus(); }
      } else {
        doc.body.classList.remove('is-locked');
        doc.body.style.top = '';
        window.scrollTo(0, scrollY);
        if (lastFocus && typeof lastFocus.focus === 'function') { lastFocus.focus(); }
      }
    };

    navToggle.addEventListener('click', function () {
      setDrawer(drawer.getAttribute('data-open') !== 'true');
    });

    drawer.addEventListener('click', function (e) {
      if (e.target.closest('a')) { setDrawer(false); }
    });

    doc.addEventListener('keydown', function (e) {
      if (drawer.getAttribute('data-open') !== 'true') { return; }
      if (e.key === 'Escape') { e.preventDefault(); setDrawer(false); return; }
      if (e.key !== 'Tab') { return; }

      var focusable = drawer.querySelectorAll('a[href], button:not([disabled]), summary, input, select, textarea');
      if (!focusable.length) { return; }
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (e.shiftKey && doc.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    desktop.addEventListener('change', function (e) {
      if (e.matches && drawer.getAttribute('data-open') === 'true') { setDrawer(false); }
    });
  }

  /* 4. Scroll reveal --------------------------------------------------------- */
  var revealItems = doc.querySelectorAll('[data-reveal]');
  if (revealItems.length && !reduce.matches && 'IntersectionObserver' in window) {
    root.classList.add('reveal-ready');
    var io = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          obs.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.06 });
    Array.prototype.forEach.call(revealItems, function (el) { io.observe(el); });
  }

  /* 5. YouTube facade — no iframe until the visitor asks for it -------------- */
  var facades = doc.querySelectorAll('[data-youtube-id], [data-video-id]');
  Array.prototype.forEach.call(facades, function (btn) {
    var card = btn.closest('.video-card');
    btn.addEventListener('click', function () {
      var id = (btn.getAttribute('data-youtube-id') || btn.getAttribute('data-video-id') || '').trim();
      var note = card ? card.querySelector('[data-video-note]') : null;

      if (!id || id === 'YOUR_VIDEO_ID_HERE') {
        if (note) {
          note.hidden = false;
          note.textContent = 'Testimonial video publishing shortly — the written reference below stands.';
        }
        return;
      }

      var frame = doc.createElement('iframe');
      frame.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) +
                  '?autoplay=1&rel=0&modestbranding=1&playsinline=1';
      frame.title = btn.getAttribute('data-video-title') || 'Client video testimonial';
      frame.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      frame.setAttribute('allowfullscreen', '');
      frame.setAttribute('loading', 'lazy');
      frame.referrerPolicy = 'strict-origin-when-cross-origin';

      var media = btn.parentNode;
      btn.remove();
      media.appendChild(frame);
      frame.focus();
      push('video_play', { video_id: id });
    });
  });

  /* 6. Email links (assembled in the browser, not in the HTML) --------------- */
  var mailNodes = doc.querySelectorAll('[data-email]');
  Array.prototype.forEach.call(mailNodes, function (node) {
    var encoded = node.getAttribute('data-email');
    if (!encoded) { return; }
    var address;
    try { address = window.atob(encoded); } catch (err) { return; }

    if (node.tagName === 'A') {
      node.setAttribute('href', 'mailto:' + address);
      var slot = node.querySelector('.js-email');
      if (slot) { slot.textContent = address; }
      else if (!node.getAttribute('data-keep-text')) { node.textContent = address; }
    } else {
      node.textContent = address;
    }
  });

  /* 7. Channel tracking ------------------------------------------------------ */
  doc.addEventListener('click', function (e) {
    var link = e.target.closest('[data-channel]');
    if (!link) { return; }
    push('contact_channel', { channel: link.getAttribute('data-channel') });
  });

  /* 8. Contact form ---------------------------------------------------------- */
  (function () {
    var form = doc.querySelector('[data-contact-form]');
    if (!form) { return; }

    var ENDPOINT = 'https://api.web3forms.com/submit';
    var ACCESS_KEY = '437ef875-ee27-44e0-9884-22910c26316b';
    var TIMEOUT = 15000;
    var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

    var RULES = {
      name: function (v) { return v.trim().length < 2 ? 'Please enter your name.' : ''; },
      email: function (v) {
        if (!v.trim()) { return 'Please enter your email address.'; }
        return EMAIL_RE.test(v.trim()) ? '' : 'Enter an email address like name@example.com.';
      },
      service: function (v) { return v ? '' : 'Choose the closest service.'; },
      message: function (v) {
        var t = v.trim();
        if (!t) { return 'Please describe what is happening.'; }
        return t.length < 20 ? 'Add a little more detail — at least 20 characters.' : '';
      },
      consent: function (_, input) { return input && input.checked ? '' : 'Please accept the privacy note so I can reply.'; }
    };

    function fieldOf(input) { return input.closest('.field') || input.closest('.check'); }
    function errorNode(input) { var f = fieldOf(input); return f ? f.querySelector('.field__error') : null; }

    function setError(input, message) {
      var node = errorNode(input);
      if (node) { node.textContent = message; }
      var field = fieldOf(input);
      if (field) { field.classList.toggle('has-error', Boolean(message)); }
      if (message) { input.setAttribute('aria-invalid', 'true'); } else { input.removeAttribute('aria-invalid'); }
    }

    function validate(input) {
      var rule = RULES[input.name];
      if (!rule) { return ''; }
      var msg = rule(input.value || '', input);
      setError(input, msg);
      return msg;
    }

    function validateAll() {
      var firstBad = null;
      Object.keys(RULES).forEach(function (name) {
        var input = form.elements.namedItem(name);
        if (!input) { return; }
        if (validate(input) && !firstBad) { firstBad = input; }
      });
      return firstBad;
    }

    function setBusy(busy) {
      var btn = form.querySelector('[data-submit]');
      if (!btn) { return; }
      var label = btn.querySelector('[data-submit-label]');
      var spinner = btn.querySelector('.spinner');
      btn.disabled = busy;
      btn.setAttribute('aria-busy', busy ? 'true' : 'false');
      if (label) { label.textContent = busy ? 'Sending…' : btn.getAttribute('data-label'); }
      if (spinner) { spinner.hidden = !busy; }
    }

    var wrap = form.closest('[data-form-wrap]') || form;

    function showError() {
      var box = wrap.querySelector('[data-form-error]');
      if (!box) { return; }
      box.hidden = false;
      box.focus();
    }

    function hideError() {
      var box = wrap.querySelector('[data-form-error]');
      if (box) { box.hidden = true; }
    }

    function showSuccess(serviceName) {
      var success = wrap.querySelector('[data-form-success]');
      form.hidden = true;
      if (success) {
        success.hidden = false;
        success.focus();
      }
      push('generate_lead', { form: 'contact', service: serviceName || 'unspecified' });
    }

    function serviceLabel() {
      var sel = form.elements.namedItem('service');
      if (!sel || sel.selectedIndex < 0) { return 'General enquiry'; }
      return sel.options[sel.selectedIndex].text;
    }

    function send() {
      var data = new FormData(form);
      var name = String(data.get('name') || '').trim();
      var consent = form.elements.namedItem('consent');
      var serviceName = data.get('service') || 'unspecified';

      data.delete('botcheck');
      data.set('access_key', ACCESS_KEY);
      data.set('from_name', name ? 'Website: ' + name : 'Website contact form');
      data.set('subject', 'New enquiry: ' + serviceLabel());
      data.set('privacy_consent', consent && consent.checked ? 'yes' : 'no');

      var controller = typeof AbortController === 'function' ? new AbortController() : null;
      var timer = controller ? window.setTimeout(function () { controller.abort(); }, TIMEOUT) : null;

      setBusy(true);

      fetch(ENDPOINT, {
        method: 'POST',
        body: data,
        headers: { Accept: 'application/json' },
        signal: controller ? controller.signal : undefined
      })
        .then(function (res) {
          return res.json().catch(function () { return {}; })
            .then(function (json) { return { ok: res.ok, json: json }; });
        })
        .then(function (result) {
          if (result.ok && result.json && result.json.success) {
            showSuccess(serviceName);
          } else {
            throw new Error('rejected');
          }
        })
        .catch(function () { showError(); })
        .then(function () {
          if (timer) { window.clearTimeout(timer); }
          setBusy(false);
        });
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      hideError();
      form.setAttribute('data-attempted', 'true');

      var bad = validateAll();
      if (bad) { bad.focus(); return; }

      var hp = form.elements.namedItem('botcheck');
      if (hp && hp.checked) { showSuccess(); return; }

      send();
    });

    var revalidate = function (e) {
      if (form.getAttribute('data-attempted') !== 'true') { return; }
      if (e.target.name && RULES[e.target.name]) { validate(e.target); }
    };
    form.addEventListener('blur', revalidate, true);
    form.addEventListener('change', revalidate, true);

    var wanted = new URLSearchParams(window.location.search).get('service');
    if (wanted) {
      var select = form.elements.namedItem('service');
      if (select) {
        Array.prototype.forEach.call(select.options, function (opt) {
          if (opt.value === wanted) { select.value = wanted; }
        });
      }
    }
  }());

  /* 9. Current year ---------------------------------------------------------- */
  var yearNodes = doc.querySelectorAll('[data-year]');
  Array.prototype.forEach.call(yearNodes, function (n) {
    n.textContent = String(new Date().getFullYear());
  });
}());
