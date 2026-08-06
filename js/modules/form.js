/**
 * js/modules/form.js
 * Contact form submission via Web3Forms (see docs/asset-pipeline.md's sibling
 * decision doc, Master-Blueprint-Final.md §Part 8 — Web3Forms confirmed).
 *
 * IMPORTANT: replace WEB3FORMS_ACCESS_KEY below with a real Web3Forms access
 * key before deployment (https://web3forms.com — free, no backend required).
 * This is a public, client-side key by design for this service; it is not a
 * secret and does not need to be hidden from the page source.
 */

const WEB3FORMS_ACCESS_KEY = '437ef875-ee27-44e0-9884-22910c26316b';
const WEB3FORMS_ENDPOINT = 'https://api.web3forms.com/submit';

function setFieldError(field, message) {
  const wrapper = field.closest('.form-field');
  if (!wrapper) return;
  wrapper.classList.add('has-error');
  const errorEl = wrapper.querySelector('.form-error');
  if (errorEl) errorEl.textContent = message;
  field.setAttribute('aria-invalid', 'true');
}

function clearFieldError(field) {
  const wrapper = field.closest('.form-field');
  if (!wrapper) return;
  wrapper.classList.remove('has-error');
  field.removeAttribute('aria-invalid');
}

function validateForm(form) {
  let isValid = true;
  const requiredFields = form.querySelectorAll('[required]');

  requiredFields.forEach((field) => {
    clearFieldError(field);
    if (!field.value.trim()) {
      setFieldError(field, 'This field is required.');
      isValid = false;
      return;
    }
    if (field.type === 'email') {
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailPattern.test(field.value.trim())) {
        setFieldError(field, 'Please enter a valid email address.');
        isValid = false;
      }
    }
  });

  return isValid;
}

async function handleSubmit(event, form, statusRegion) {
  event.preventDefault();

  // Honeypot check — a filled hidden field means a bot, not a real visitor.
  const honeypot = form.querySelector('input[name="botcheck"]');
  if (honeypot && honeypot.value) {
    return; // silently drop — no error shown, since this path is bot traffic
  }

  if (!validateForm(form)) {
    statusRegion.textContent = 'Please fix the highlighted fields and try again.';
    statusRegion.className = 'alert alert--danger';
    form.querySelector('[aria-invalid="true"]')?.focus();
    return;
  }

  const submitBtn = form.querySelector('[type="submit"]');
  const originalLabel = submitBtn.textContent;
  submitBtn.disabled = true;
  submitBtn.textContent = 'Sending…';

  try {
    const formData = new FormData(form);
    formData.append('access_key', WEB3FORMS_ACCESS_KEY);

    const response = await fetch(WEB3FORMS_ENDPOINT, {
      method: 'POST',
      body: formData,
    });
    const result = await response.json();

    if (result.success) {
      form.reset();
      form.hidden = true;
      statusRegion.textContent = "Thanks — your message has been sent. I'll get back to you as soon as I can.";
      statusRegion.className = 'alert alert--success';
      statusRegion.setAttribute('tabindex', '-1');
      statusRegion.focus();
    } else {
      throw new Error(result.message || 'Submission failed.');
    }
  } catch (err) {
    statusRegion.textContent =
      "Something went wrong sending your message. Please try again, or email help.atikulislam@gmail.com directly.";
    statusRegion.className = 'alert alert--danger';
    statusRegion.setAttribute('tabindex', '-1');
    statusRegion.focus();
    console.error('[contact-form]', err);
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = originalLabel;
  }
}

function initContactForm() {
  const form = document.querySelector('[data-contact-form]');
  if (!form) return;
  const statusRegion = document.querySelector('[data-form-status]');

  form.addEventListener('submit', (e) => handleSubmit(e, form, statusRegion));

  form.querySelectorAll('.form-input, .form-textarea').forEach((field) => {
    field.addEventListener('blur', () => {
      if (field.hasAttribute('required') && !field.value.trim()) {
        setFieldError(field, 'This field is required.');
      } else {
        clearFieldError(field);
      }
    });
  });
}

document.addEventListener('DOMContentLoaded', initContactForm);
