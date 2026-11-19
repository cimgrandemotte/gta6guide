/* ═══════════════════════════════════════════════════════════════════════════
   main.js — S3 / BUILD_CORE_PAGES
   Orchestrateur de la homepage définitive.

   Ordre d'évaluation des imports :
     1. utils.js   → playlist locale + helpers, avant auto-init des composants
     2. search.js  → window.GTA6_SEARCH_INDEX, avant initSearch()
     3. components.js / animations.js → auto-init S2 (ARIA, clavier, audio…)
     4. ce module  → raccourcis, métriques JSON, état post-lancement, fallbacks

   Aucun réseau externe, aucun localhost, aucune dépendance npm.
   ═══════════════════════════════════════════════════════════════════════════ */
import './utils.js';
import './search.js';
import './components.js';
import './animations.js';
import { initLeonidaMap } from './map_leonida.js';
import { initS5Checklists } from './s5_checklist.js';
import { initS5Quiz } from './s5_quiz.js';
import { asset, announce, metric, prefersReducedMotion } from './utils.js';

const RELEASE = new Date(2026, 10, 19, 0, 0, 0).getTime();
const LIVE = () => Date.now() >= RELEASE;

/** Valeurs de repli strictement recopiées depuis research_data.json (S3). */
const METRIC_FALLBACK = {
  facts: 577,
  sources: 292,
  sections: 20,
  missions: 93
};

function isTypingTarget(el) {
  return el && (/^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName) || el.isContentEditable);
}

function initKeyboardShortcuts() {
  document.addEventListener('keydown', (event) => {
    if (event.key === '/' && !isTypingTarget(event.target) && !event.ctrlKey && !event.metaKey && !event.altKey) {
      const input = document.querySelector('[data-search] input');
      if (input) {
        event.preventDefault();
        input.focus();
        announce('Recherche focalisée. Saisissez au moins deux caractères.');
      }
    }
    if (event.key.toLowerCase() === 'm' && event.altKey) {
      const audio = document.querySelector('[data-audio-toggle]');
      if (audio) { event.preventDefault(); audio.focus(); announce('Lecteur audio focalisé.'); }
    }
    if (event.key === 'Escape') {
      const active = document.activeElement;
      if (active && active.matches('[data-search] input')) active.blur();
    }
  });
}

async function hydrateMetrics() {
  try {
    const response = await fetch(asset('research_data.json'), { cache: 'no-cache' });
    if (!response.ok) return;
    const data = await response.json();
    const totals = data.meta?.totals || {};
    const values = {
      facts: totals.facts ?? METRIC_FALLBACK.facts,
      sources: totals.sources_registered ?? METRIC_FALLBACK.sources,
      sections: totals.sections ?? METRIC_FALLBACK.sections,
      missions: data.s2_press_mission_list?.total ?? METRIC_FALLBACK.missions
    };
    Object.entries(values).forEach(([key, value]) => {
      document.querySelectorAll(`[data-metric="${key}"]`).forEach((el) => {
        el.textContent = metric(value);
        el.dataset.metricSource = 'research_data.json';
      });
    });
  } catch {
    /* Le fallback HTML reste affiché : valeurs déjà validées par check_s3.py. */
  }
}

function initLaunchState() {
  if (!LIVE()) return;
  document.documentElement.classList.add('is-post-launch');
  document.querySelectorAll('[data-launch-cta]').forEach((el) => {
    el.textContent = 'Lancer le Guide';
    el.setAttribute('href', '#guide-demarrage');
  });
  document.querySelectorAll('[data-prelaunch-label]').forEach((el) => {
    el.textContent = 'Le guide est en service';
  });
}

function initImageFallback() {
  document.querySelectorAll('img[data-media]').forEach((img) => {
    img.addEventListener('error', () => {
      const frame = img.closest('[data-media-frame]');
      if (frame) frame.classList.add('media-fallback');
      img.hidden = true;
    }, { once: true });
  });
}

function initExternalLinks() {
  document.querySelectorAll('a[href^="http"]').forEach((a) => {
    if (!a.hasAttribute('rel')) a.setAttribute('rel', 'noopener noreferrer');
    a.dataset.external = 'true';
  });
}

/** Synchronise aria-expanded de chaque combobox avec l'état réel du panneau. */
function initSearchAria() {
  document.querySelectorAll('[data-search]').forEach((root) => {
    const input = root.querySelector('input');
    const panel = root.querySelector('[data-search-panel]');
    if (!input || !panel) return;
    const sync = () => input.setAttribute('aria-expanded', String(!panel.hidden));
    sync();
    new MutationObserver(sync).observe(panel, { attributes: true, attributeFilter: ['hidden'] });
  });
}

function initReducedMotionNotice() {
  if (prefersReducedMotion()) {
    document.documentElement.classList.add('reduced-motion');
  }
}

function ready(fn) {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fn, { once: true });
  } else fn();
}

ready(() => {
  document.documentElement.classList.add('has-js');
  initKeyboardShortcuts();
  hydrateMetrics();
  initLaunchState();
  initImageFallback();
  initExternalLinks();
  initSearchAria();
  initReducedMotionNotice();
});

/* ── S5 : modules interactifs (carte, checklists, quiz) ───────────────────── */
function initS5() {
  initLeonidaMap();
  initS5Checklists();
  initS5Quiz();
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initS5, { once: true });
else initS5();
