/** Web3Forms client-side submission. The access key is a public form identifier,
 * not a secret; configure domain restrictions and notifications in Web3Forms.
 */
const WEB3FORMS_ACCESS_KEY = '437ef875-ee27-44e0-9884-22910c26316b';
const WEB3FORMS_ENDPOINT = 'https://api.web3forms.com/submit';

function setError(field, message) {
  const wrapper = field.closest('.form-field');
  if (!wrapper) return;
  wrapper.classList.toggle('has-error', Boolean(message));
  field.setAttribute('aria-invalid', message ? 'true' : 'false');
  const error = wrapper.querySelector('.form-error');
  if (error) error.textContent = message;
}
function errorFor(field) {
  const value = field.value.trim();
  if (field.required && !value) return 'This field is required.';
  if (field.type === 'email' && value && !field.validity.valid) return 'Please enter a valid email address.';
  return '';
}
function validate(form) {
  let firstInvalid;
  form.querySelectorAll('.form-input, .form-textarea').forEach(field => {
    const error = errorFor(field);
    setError(field, error);
    if (error && !firstInvalid) firstInvalid = field;
  });
  firstInvalid?.focus();
  return !firstInvalid;
}
function status(region, message, kind) {
  region.textContent = message;
  region.className = `alert alert--${kind}`;
  region.hidden = false;
  region.focus();
}
function initContactForm() {
  const form = document.querySelector('[data-contact-form]');
  const region = document.querySelector('[data-form-status]');
  if (!form || !region) return;
  const button = form.querySelector('[type="submit"]');
  if (!button) return;
  form.querySelectorAll('.form-input, .form-textarea').forEach(field => {
    field.addEventListener('blur', () => setError(field, errorFor(field)));
    field.addEventListener('input', () => {
      if (field.getAttribute('aria-invalid') === 'true') setError(field, errorFor(field));
    });
  });
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (button.disabled) return;
    region.hidden = true;
    if (!validate(form)) {
      // Move focus to the first field; the inline message gives the specific reason.
      region.textContent = 'Please correct the highlighted fields before sending.';
      return;
    }
    if (form.elements.botcheck?.checked) {
      status(region, 'Thanks for your message.', 'success');
      return;
    }
    const label = button.textContent;
    button.disabled = true;
    button.textContent = 'Sending…';
    form.setAttribute('aria-busy', 'true');
    try {
      const payload = new FormData(form);
      payload.append('access_key', WEB3FORMS_ACCESS_KEY);
      const response = await fetch(WEB3FORMS_ENDPOINT, { method: 'POST', body: payload });
      if (!response.ok) throw new Error('Submission service unavailable');
      const result = await response.json();
      if (!result.success) throw new Error('Submission rejected');
      form.reset();
      form.hidden = true;
      status(region, "Thanks — your message has been sent. I'll get back to you as soon as I can.", 'success');
    } catch (_) {
      status(region, 'Your message could not be sent. Please try again, or email help.atikulislam@gmail.com directly.', 'danger');
    } finally {
      button.disabled = false;
      button.textContent = label;
      form.removeAttribute('aria-busy');
    }
  });
}
initContactForm();
