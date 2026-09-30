(() => {
  const form = document.querySelector('#contact-form');
  if (!form) return;
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(entries => {
      document.body.classList.toggle('contact-active', entries[0].isIntersecting);
    }).observe(form.closest('.contact'));
  }
  const endpoint = 'https://mail.glixerp.com/api/glix-contact.php';
  const button = form.querySelector('button[type="submit"]');
  const label = button.querySelector('span');
  const status = form.querySelector('.contact-status');
  const success = document.querySelector('.contact-success');
  const header = document.querySelector('.contact-card-description');
  const title = document.querySelector('.contact-form-card > h3');
  let token = null;
  let issued = 0;
  let busy = false;
  const ready = () => { button.disabled = false; };
  async function prepare() {
    const response = await fetch(endpoint, { mode: 'cors', cache: 'no-store', credentials: 'omit', signal: AbortSignal.timeout(12000) });
    const data = await response.json();
    if (!response.ok || !data.token) throw new Error('No pudimos conectar el formulario. Podés reintentar o escribirnos a info@glixerp.com.');
    token = data.token;
    issued = Date.now();
  }
  // Prepare only as the visitor approaches the section.
  const load = () => prepare().catch(() => {}).finally(ready);
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) { observer.disconnect(); load(); }
    }, { rootMargin: '400px' });
    observer.observe(form);
  } else load();
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (busy || !form.reportValidity()) return;
    busy = true; button.disabled = true; label.textContent = 'Enviando consulta…';
    form.setAttribute('aria-busy', 'true'); status.textContent = '';
    try {
      if (!token || Date.now() - issued > 100 * 60 * 1000) await prepare();
      const wait = 3000 - (Date.now() - issued);
      if (wait > 0) await new Promise(resolve => setTimeout(resolve, wait));
      const payload = Object.fromEntries(new FormData(form));
      payload.token = token;
      const response = await fetch(endpoint, {
        method: 'POST', mode: 'cors', credentials: 'omit',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload), signal: AbortSignal.timeout(20000)
      });
      const data = await response.json();
      if (!response.ok || !data.ok) throw new Error(data.message || 'No pudimos enviar tu consulta. Intentá nuevamente o escribinos a info@glixerp.com.');
      form.hidden = true; header.hidden = true; title.hidden = true; success.hidden = false;
      success.focus({ preventScroll: true });
      success.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'nearest' });
      form.reset(); token = null;
    } catch (error) {
      status.textContent = error.name === 'TimeoutError' ? 'La conexión está demorando. Tu consulta no pudo confirmarse. Antes de reenviar, podés escribirnos a info@glixerp.com.' : (error instanceof TypeError ? 'No pudimos conectar. Revisá tu conexión o escribinos a info@glixerp.com.' : error.message);
      if (error.name !== 'TimeoutError' && !(error instanceof TypeError)) token = null;
    } finally {
      busy = false; button.disabled = false; label.textContent = 'Enviar consulta'; form.removeAttribute('aria-busy');
    }
  });
  document.querySelector('.contact-another').addEventListener('click', () => {
    success.hidden = true; form.hidden = false; header.hidden = false; title.hidden = false; status.textContent = '';
    form.querySelector('input').focus(); load();
  });
})();
