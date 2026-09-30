const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.primary-nav');
const siteHeader = document.querySelector('.site-header');

function updateHeader() {
  siteHeader?.classList.toggle('is-scrolled', window.scrollY > 24);
}

updateHeader();
window.addEventListener('scroll', updateHeader, { passive: true });

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
    // Keep initial content visible; animate headings reached by scrolling.
    if (target.getBoundingClientRect().top < window.innerHeight) return;
    target.classList.add('reveal');
    observer.observe(target);
  });
  document.body.classList.add('js-ready');
}

// Only animate visible sequences; stop timers in background tabs and reduced motion.
const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
document.querySelectorAll('[data-frame-sequence]').forEach((sequence) => {
  const frames = [...sequence.querySelectorAll('img')];
  if (frames.length < 2) return;
  const requestedInterval = Number(sequence.dataset.interval);
  const interval = Number.isFinite(requestedInterval) && requestedInterval >= 1000
    ? requestedInterval : 2000;
  let active = 0;
  let visible = false;
  let timer;

  function stop() {
    window.clearInterval(timer);
    timer = undefined;
  }

  function updatePlayback() {
    stop();
    if (motionPreference.matches) {
      frames.forEach((frame, index) => frame.classList.toggle('is-active', index === 0));
      active = 0;
      return;
    }
    if (!visible || document.hidden) return;
    timer = window.setInterval(() => {
      const next = (active + 1) % frames.length;
      // Keep the current frame when another image has not loaded or failed.
      if (!frames[next].complete || !frames[next].naturalWidth) return;
      frames[active].classList.remove('is-active');
      frames[next].classList.add('is-active');
      active = next;
    }, interval);
  }

  if ('IntersectionObserver' in window) {
    const visibilityObserver = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      updatePlayback();
    });
    visibilityObserver.observe(sequence);
  } else {
    visible = true;
    updatePlayback();
  }
  document.addEventListener('visibilitychange', updatePlayback);
  motionPreference.addEventListener('change', updatePlayback);
  window.addEventListener('pagehide', stop);
  window.addEventListener('pageshow', updatePlayback);
});

// Pause decorative animation outside the viewport without changing its visible design.
if ('IntersectionObserver' in window) {
  const animationObserver = new IntersectionObserver((entries) => {
    entries.forEach(({ target, isIntersecting }) => {
      target.classList.toggle('animation-paused', !isIntersecting);
    });
  });
  document.querySelectorAll('.tic-button, .client-marquee__track, .solution-still img').forEach((target) => {
    target.classList.add('animation-paused');
    animationObserver.observe(target);
  });
}
