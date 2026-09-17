const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.primary-nav');

function setMenu(open) {
  menuButton?.setAttribute('aria-expanded', String(open));
  menuButton?.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
  nav?.classList.toggle('is-open', open);
  document.body.classList.toggle('menu-open', open);
}

menuButton?.addEventListener('click', () => {
  const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
  setMenu(!isOpen);
});

nav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => {
  setMenu(false);
}));

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && menuButton?.getAttribute('aria-expanded') === 'true') {
    setMenu(false);
    menuButton.focus();
  }
});

window.matchMedia('(min-width: 1151px)').addEventListener('change', (event) => {
  if (event.matches) setMenu(false);
});

const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!prefersReducedMotion && 'IntersectionObserver' in window) {
  const revealTargets = document.querySelectorAll('main h1, main h2, main h3, .section-cta-title');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px 60px 0px' });
  revealTargets.forEach((target) => {
    target.classList.add('reveal');
    observer.observe(target);
  });
  document.body.classList.add('js-ready');
}

const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();

// Cambios de cuadro sin fundido: las carcasas permanecen inmóviles.
document.querySelectorAll('[data-frame-sequence]').forEach((sequence) => {
  const frames = [...sequence.querySelectorAll('img')];
  if (frames.length < 2 || prefersReducedMotion) return;

  const interval = Number(sequence.dataset.interval) || 2000;
  const ready = frames.map((frame) => frame.decode?.().catch(() => {}) ?? Promise.resolve());

  Promise.all(ready).then(() => {
    let active = 0;
    window.setInterval(() => {
      if (document.hidden) return;
      frames[active].classList.remove('is-active');
      active = (active + 1) % frames.length;
      frames[active].classList.add('is-active');
    }, interval);
  });
});
