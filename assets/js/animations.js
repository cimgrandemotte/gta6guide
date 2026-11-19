/* ═══════════════════════════════════════════════════════════════════════════
   animations.js — S2 / DESIGN_SYSTEM
   Moteur d'animations Vanilla ES6+ : LoadingScreen, GlitchText, TypewriterIntro,
   ParallaxHero, FloatingParticles (Canvas), CardHover3D, CounterAnimation,
   ScrollReveal, SmoothScroll, CursorCustom, ScanLines, WantedStars.

   • Aucune dépendance externe (GSAP reste OPTIONNEL : window.gsap est utilisé
     s'il est déjà présent, sinon fallback natif).
   • Aucun SVG / PNG / GIF : particules dessinées dans un <canvas> CSS.
   • Respect strict de prefers-reduced-motion et désactivation sur écran tactile.
   ═══════════════════════════════════════════════════════════════════════════ */

const $  = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
const reduced = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const finePointer = () => window.matchMedia('(hover: hover) and (pointer: fine)').matches;

/* ── LoadingScreen ────────────────────────────────────────────────────────── */
export function initLoadingScreen() {
  const screen = $('[data-loading]');
  if (!screen) { document.body.classList.add('is-ready'); return; }
  const bar = $('[data-loading-bar]', screen);
  const pct = $('[data-loading-pct]', screen);
  const skip = $('[data-loading-skip]', screen);
  let value = 0;
  let done = false;

  const finish = () => {
    if (done) return;
    done = true;
    if (bar) bar.style.width = '100%';
    if (pct) pct.textContent = '100 %';
    screen.classList.add('is-done');
    document.body.classList.add('is-ready');
    setTimeout(() => screen.remove(), 600);
  };

  const duration = reduced() ? 200 : 1350;
  const step = 40;
  const timer = setInterval(() => {
    value = Math.min(100, value + (100 * step / duration) * (0.7 + Math.random() * 0.8));
    if (bar) bar.style.width = value.toFixed(1) + '%';
    if (pct) pct.textContent = Math.floor(value) + ' %';
    if (value >= 100) { clearInterval(timer); setTimeout(finish, 180); }
  }, step);

  skip?.addEventListener('click', finish);
  window.addEventListener('load', () => setTimeout(finish, reduced() ? 0 : 400), { once: true });
  setTimeout(finish, duration + 1000); // filet de sécurité si un asset bloque
}

/* ── GlitchText : déclenché au survol / focus / entrée en scène ───────────── */
export function initGlitchText() {
  $$('.glitch[data-text]').forEach(el => {
    if (!el.hasAttribute('tabindex')) el.setAttribute('tabindex', '0');
    const burst = () => {
      if (reduced()) return;
      el.classList.add('glitch--active');
      setTimeout(() => el.classList.remove('glitch--active'), 900);
    };
    el.addEventListener('mouseenter', burst);
    el.addEventListener('focus', burst);
    el.addEventListener('click', burst);
  });
}

/* ── TypewriterIntro ──────────────────────────────────────────────────────── */
export function initTypewriter() {
  $$('[data-typewriter]').forEach(el => {
    const text = el.dataset.typewriter || el.textContent.trim();
    const speed = Number(el.dataset.typewriterSpeed || 46);
    if (reduced()) { el.textContent = text; return; }
    el.textContent = '';
    let i = 0;
    const caret = document.createElement('span');
    caret.className = 'typewriter__caret';
    caret.textContent = '▌';
    caret.setAttribute('aria-hidden', 'true');
    const type = () => {
      if (i <= text.length) {
        el.textContent = text.slice(0, i++);
        el.appendChild(caret);
        setTimeout(type, speed + Math.random() * 34);
      }
    };
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting) { type(); io.disconnect(); }
      }, { threshold: .3 });
      io.observe(el);
    } else type();
  });
}

/* ── ParallaxHero (rAF + transform GPU) ───────────────────────────────────── */
export function initParallax() {
  if (reduced()) return;
  const layers = $$('[data-parallax]');
  if (!layers.length) return;
  let ticking = false;
  const update = () => {
    const y = window.scrollY;
    layers.forEach(layer => {
      const speed = Number(layer.dataset.parallax || 0.18);
      layer.style.transform = `translate3d(0, ${(y * speed).toFixed(1)}px, 0)`;
    });
    ticking = false;
  };
  window.addEventListener('scroll', () => {
    if (!ticking) { requestAnimationFrame(update); ticking = true; }
  }, { passive: true });
  update();
}

/* ── FloatingParticles (canvas 100 % JS, zéro image) ──────────────────────── */
export function initParticles() {
  if (reduced()) return;
  let canvas = $('#particles-canvas');
  if (!canvas) {
    canvas = document.createElement('canvas');
    canvas.id = 'particles-canvas';
    canvas.setAttribute('aria-hidden', 'true');
    document.body.prepend(canvas);
  }
  const ctx = canvas.getContext('2d', { alpha: true });
  if (!ctx) return;
  const colors = ['255,45,120', '0,212,255', '255,215,0', '139,92,246'];
  let w = 0, h = 0, dpr = 1, particles = [], raf = 0;

  const resize = () => {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = canvas.clientWidth = window.innerWidth;
    h = canvas.clientHeight = window.innerHeight;
    canvas.width = w * dpr; canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const count = Math.min(90, Math.round(w * h / 22000));
    particles = Array.from({ length: count }, () => ({
      x: Math.random() * w, y: Math.random() * h,
      r: .6 + Math.random() * 1.9,
      vx: (Math.random() - .5) * .22, vy: -.12 - Math.random() * .38,
      a: .16 + Math.random() * .55,
      c: colors[Math.floor(Math.random() * colors.length)]
    }));
  };
  const draw = () => {
    ctx.clearRect(0, 0, w, h);
    for (const p of particles) {
      p.x += p.vx; p.y += p.vy;
      if (p.y < -8) { p.y = h + 8; p.x = Math.random() * w; }
      if (p.x < -8) p.x = w + 8; else if (p.x > w + 8) p.x = -8;
      ctx.beginPath();
      ctx.fillStyle = `rgba(${p.c},${p.a})`;
      ctx.shadowBlur = 8; ctx.shadowColor = `rgba(${p.c},.55)`;
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
    }
    ctx.shadowBlur = 0;
    raf = requestAnimationFrame(draw);
  };
  const stop = () => { cancelAnimationFrame(raf); raf = 0; };
  const start = () => { if (!raf) raf = requestAnimationFrame(draw); };

  resize();
  window.addEventListener('resize', resize, { passive: true });
  document.addEventListener('visibilitychange', () => document.hidden ? stop() : start());
  start();
}

/* ── CardHover3D ──────────────────────────────────────────────────────────── */
export function initTiltCards() {
  if (reduced() || !finePointer()) return;
  $$('.tilt-card').forEach(card => {
    card.addEventListener('pointermove', (e) => {
      const r = card.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width - .5;
      const py = (e.clientY - r.top) / r.height - .5;
      card.style.transform = `perspective(900px) rotateX(${(-py * 8).toFixed(2)}deg) rotateY(${(px * 8).toFixed(2)}deg) translateY(-4px)`;
    });
    card.addEventListener('pointerleave', () => { card.style.transform = ''; });
  });
}

/* ── CounterAnimation (CountUp-like natif) ────────────────────────────────── */
export function initCounters() {
  const els = $$('[data-count]');
  if (!els.length) return;
  const run = (el) => {
    const target = Number(el.dataset.count) || 0;
    const duration = Number(el.dataset.countDuration || 1600);
    const prefix = el.dataset.countPrefix || '';
    const suffix = el.dataset.countSuffix || '';
    if (reduced()) { el.textContent = prefix + target.toLocaleString('fr-FR') + suffix; return; }
    const t0 = performance.now();
    const frame = (now) => {
      const p = Math.min(1, (now - t0) / duration);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = prefix + Math.round(target * eased).toLocaleString('fr-FR') + suffix;
      if (p < 1) requestAnimationFrame(frame);
    };
    requestAnimationFrame(frame);
  };
  if (!('IntersectionObserver' in window)) { els.forEach(run); return; }
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { run(e.target); io.unobserve(e.target); }
  }), { threshold: .4 });
  els.forEach(el => io.observe(el));
}

/* ── ScrollReveal ─────────────────────────────────────────────────────────── */
export function initReveal() {
  const els = $$('[data-reveal]');
  if (!els.length) return;
  els.forEach(el => el.classList.add('reveal'));
  if (reduced() || !('IntersectionObserver' in window)) { els.forEach(el => el.classList.add('is-visible')); return; }
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); }
  }), { threshold: .12, rootMargin: '0px 0px -40px 0px' });
  els.forEach(el => io.observe(el));
}

/* ── CursorCustom (div, aucun SVG) ────────────────────────────────────────── */
export function initCursor() {
  if (reduced() || !finePointer()) return;
  let dot = $('.cursor-reticle');
  if (!dot) {
    dot = document.createElement('div');
    dot.className = 'cursor-reticle';
    dot.setAttribute('aria-hidden', 'true');
    document.body.appendChild(dot);
    document.body.classList.add('has-custom-cursor');
  }
  let x = -100, y = -100, tx = -100, ty = -100, raf = 0;
  const loop = () => {
    x += (tx - x) * .22; y += (ty - y) * .22;
    dot.style.transform = `translate3d(${x - 15}px, ${y - 15}px, 0)`;
    raf = requestAnimationFrame(loop);
  };
  document.addEventListener('pointermove', (e) => {
    tx = e.clientX; ty = e.clientY;
    dot.classList.add('is-active');
    const interactive = e.target.closest('a, button, input, select, [role="checkbox"]');
    dot.classList.toggle('is-hover', Boolean(interactive));
  }, { passive: true });
  document.addEventListener('pointerleave', () => dot.classList.remove('is-active'));
  raf = requestAnimationFrame(loop);
}

/* ── ScanLines (overlay pure CSS activé par JS) ───────────────────────────── */
export function initScanLines() {
  if ($('.scanlines')) return;
  const layer = document.createElement('div');
  layer.className = 'scanlines';
  layer.setAttribute('aria-hidden', 'true');
  layer.innerHTML = '<div class="scanlines__beam"></div>';
  document.body.appendChild(layer);
  const vignette = document.createElement('div');
  vignette.className = 'vignette';
  vignette.setAttribute('aria-hidden', 'true');
  document.body.appendChild(vignette);
}

/* ── WantedStars : rendu dynamique du niveau de recherche ─────────────────── */
export function initWantedStars() {
  $$('[data-wanted]').forEach(el => {
    const n = Math.max(0, Math.min(6, Number(el.dataset.wanted) || 0));
    el.innerHTML = Array.from({ length: n }, (_, i) =>
      `<span class="star" style="animation-delay:${i * .12}s" aria-hidden="true">★</span>`).join('');
    el.classList.toggle('wanted-stars--red', n === 6);
    el.setAttribute('aria-label', `${n} étoile${n > 1 ? 's' : ''} de recherche`);
    el.setAttribute('role', 'img');
  });
}

/* ── SmoothScroll / ScrollProgress ────────────────────────────────────────── */
export function initSmoothScroll() {
  // Le scroll natif est déjà fluide en CSS ; ici on pilote uniquement l'overlay
  // et on expose une API réutilisable par S3/S4/S5.
  window.GTA6Scroll = {
    to(target, offset = 72) {
      const el = typeof target === 'string' ? document.querySelector(target) : target;
      if (!el) return;
      const top = el.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: reduced() ? 'auto' : 'smooth' });
    }
  };
}

/* ── Intégration GSAP optionnelle (si chargé par une page) ────────────────── */
export function initGsapHooks() {
  if (!window.gsap || reduced()) return;
  const gsap = window.gsap;
  $$('[data-gsap-parallax]').forEach(el => {
    gsap.to(el, {
      yPercent: Number(el.dataset.gsapParallax || 12),
      ease: 'none',
      scrollTrigger: window.ScrollTrigger ? { trigger: el, scrub: true, start: 'top bottom', end: 'bottom top' } : undefined
    });
  });
}

/* ── Initialisation ───────────────────────────────────────────────────────── */
export function initAnimations() {
  initLoadingScreen();
  initGlitchText();
  initTypewriter();
  initParallax();
  initParticles();
  initTiltCards();
  initCounters();
  initReveal();
  initCursor();
  initScanLines();
  initWantedStars();
  initSmoothScroll();
  initGsapHooks();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initAnimations, { once: true });
} else initAnimations();
