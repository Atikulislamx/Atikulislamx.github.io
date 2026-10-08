/* ==========================================================================
   form.js — contact form: validation, honeypot, submit state, errors

   - The Web3Forms access key is public by design (it is sent from the browser
     and only accepts submissions to the owner's inbox). It is not a secret.
   - Nothing is stored in the browser (no localStorage, no cookies).
   - Without JavaScript the form is hidden and the email/WhatsApp fallback
     is shown instead (see contact/index.html).
   ========================================================================== */
(function () {
  'use strict';

  var FORM_SELECTOR = '[data-contact-form]';
  var ENDPOINT = 'https://api.web3forms.com/submit';
  var ACCESS_KEY = '437ef875-ee27-44e0-9884-22910c26316b';
  var TIMEOUT_MS = 15000;
  var EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  var RULES = {
    name: function (value) {
      return value.trim().length < 2 ? 'Please enter your name.' : '';
    },
    email: function (value) {
      var v = value.trim();
      if (!v) return 'Please enter your email address.';
      return EMAIL_PATTERN.test(v) ? '' : 'Enter an email address in the format name@example.com.';
    },
    service: function (value) {
      return value ? '' : 'Choose the service closest to your situation.';
    },
    message: function (value) {
      var v = value.trim();
      if (!v) return 'Please describe what is happening.';
      return v.length < 20 ? 'Add a little more detail, at least 20 characters.' : '';
    }
  };

  /* Field error handling ---------------------------------------------------- */
  function setFieldError(input, message) {
    var field = input.closest('.field');
    var errorEl = field && field.querySelector('.field__error');
    if (!field || !errorEl) return;
    errorEl.textContent = message;
    field.classList.toggle('has-error', Boolean(message));
    if (message) {
      input.setAttribute('aria-invalid', 'true');
    } else {
      input.removeAttribute('aria-invalid');
    }
  }

  function validateField(input) {
    var rule = RULES[input.name];
    if (!rule) return '';
    var message = rule(input.value || '');
    setFieldError(input, message);
    return message;
  }

  function validateForm(form) {
    var firstInvalid = null;
    Object.keys(RULES).forEach(function (name) {
      var input = form.elements.namedItem(name);
      if (!input) return;
      if (validateField(input) && !firstInvalid) firstInvalid = input;
    });
    return firstInvalid;
  }

  /* Status panels ------------------------------------------------------------ */
  function setBusy(form, busy) {
    var button = form.querySelector('[data-submit]');
    if (!button) return;
    var label = button.querySelector('[data-submit-label]');
    var spinner = button.querySelector('.spinner');
    button.disabled = busy;
    button.setAttribute('aria-busy', busy ? 'true' : 'false');
    if (label) label.textContent = busy ? 'Sending…' : button.getAttribute('data-label');
    if (spinner) spinner.hidden = !busy;
  }

  // The error alert sits beside the form (inside the wrapper), so search the wrapper.
  function errorBox(form) {
    var wrap = form.closest('[data-form-wrap]') || form;
    return wrap.querySelector('[data-form-error]');
  }

  function showError(form) {
    var box = errorBox(form);
    if (!box) return;
    box.hidden = false;
    box.focus();
    box.scrollIntoView({ block: 'nearest' });
  }

  function hideError(form) {
    var box = errorBox(form);
    if (box) box.hidden = true;
  }

  function showSuccess(form) {
    var wrap = form.closest('[data-form-wrap]');
    var success = wrap && wrap.querySelector('[data-form-success]');
    form.hidden = true;
    if (success) {
      success.hidden = false;
      success.focus();
    }
  }

  /* Submission ----------------------------------------------------------------- */
  function serviceLabel(form) {
    var select = form.elements.namedItem('service');
    if (!select || select.selectedIndex < 0) return 'General enquiry';
    return select.options[select.selectedIndex].text;
  }

  function send(form) {
    var data = new FormData(form);
    var name = String(data.get('name') || '').trim();

    data.delete('botcheck');
    data.set('access_key', ACCESS_KEY);
    data.set('from_name', name ? 'Website: ' + name : 'Website contact form');
    data.set('subject', 'New enquiry: ' + serviceLabel(form));

    var controller = typeof AbortController === 'function' ? new AbortController() : null;
    var timer = controller ? window.setTimeout(function () { controller.abort(); }, TIMEOUT_MS) : null;

    setBusy(form, true);

    fetch(ENDPOINT, {
      method: 'POST',
      body: data,
      headers: { Accept: 'application/json' },
      signal: controller ? controller.signal : undefined
    })
      .then(function (response) {
        return response.json()
          .catch(function () { return {}; })
          .then(function (json) { return { ok: response.ok, json: json }; });
      })
      .then(function (result) {
        if (result.ok && result.json && result.json.success) {
          showSuccess(form);
        } else {
          throw new Error('Submission was not accepted');
        }
      })
      .catch(function () {
        showError(form);
      })
      .then(function () {
        if (timer) window.clearTimeout(timer);
        setBusy(form, false);
      });
  }

  function onSubmit(event) {
    event.preventDefault();
    var form = event.currentTarget;
    form.setAttribute('data-submitted', 'true');
    hideError(form);

    var firstInvalid = validateForm(form);
    if (firstInvalid) {
      firstInvalid.focus();
      return;
    }

    // Honeypot: the checkbox is hidden from people, so a checked box means a bot.
    // Bots get a success message, but nothing is sent.
    var honeypot = form.elements.namedItem('botcheck');
    if (honeypot && honeypot.checked) {
      showSuccess(form);
      return;
    }

    send(form);
  }

  /* Prefill from ?service=slug (linked from service pages) ------------------- */
  function prefillService(form) {
    var select = form.elements.namedItem('service');
    var wanted = new URLSearchParams(window.location.search).get('service');
    if (!select || !wanted) return;
    var match = Array.prototype.find.call(select.options, function (option) {
      return option.value === wanted;
    });
    if (match) select.value = wanted;
  }

  function init() {
    var form = document.querySelector(FORM_SELECTOR);
    if (!form) return;

    prefillService(form);
    form.addEventListener('submit', onSubmit);

    // After a failed attempt, re-check each field as the user corrects it.
    var revalidate = function (event) {
      if (form.getAttribute('data-submitted') === 'true') validateField(event.target);
    };
    form.addEventListener('blur', revalidate, true);
    form.addEventListener('change', revalidate, true);
  }

  init();
}());
