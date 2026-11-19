/* ═══════════════════════════════════════════════════════════════════════════
   components.js — S2 / DESIGN_SYSTEM
   Composants globaux réutilisables en JavaScript ES6+ VANILLA (0 dépendance).

   Initialisation automatique au DOMContentLoaded + exports nommés pour S3/S4/S5.
   Accessibilité : ARIA, navigation clavier, focus visible, annonces via aria-live.
   Aucun appel réseau externe, aucun localhost, aucun SVG/PNG : les icônes sont
   des glyphes Unicode et les formes sont dessinées en CSS.
   ═══════════════════════════════════════════════════════════════════════════ */

/* ── Données de démonstration (remplacées par research_data.json en S5) ───── */
export const AUDIO_TRACKS = [
  { label: 'Vice City · Nuit néon',       src: 'assets/audio/ambiances/homepage_ambiance_vicecity_night_01.mp3' },
  { label: 'Leonida · Wetlands',          src: 'assets/audio/ambiances/map_leonida_ambiance_01.mp3' },
  { label: 'Moteur V8 · Démarrage',       src: 'assets/audio/ambiances/vehicles_engine_v8_01.mp3' },
  { label: 'Jason · Thème',               src: 'assets/audio/jingles/characters_jason_theme_01.mp3' },
  { label: 'Lucia · Thème',               src: 'assets/audio/jingles/characters_lucia_theme_01.mp3' },
  { label: 'UI · Survol',                 src: 'assets/audio/ui/homepage_ui_hover_01.mp3' },
  { label: 'UI · Clic',                   src: 'assets/audio/ui/homepage_ui_click_01.mp3' },
  { label: 'UI · Transition',             src: 'assets/audio/ui/homepage_ui_transition_01.mp3' },
  { label: 'Arme · Équipement',           src: 'assets/audio/ui/weapons_equip_sound_01.mp3' },
  { label: 'Quiz · Bonne réponse',        src: 'assets/audio/ui/quiz_correct_answer_01.mp3' }
];

export const SEARCH_INDEX = [
  { title: 'Accueil',                 section: 'Hub',        url: 'index.html',                         thumb: 'assets/images/heroes/homepage_hero_vicecity_night_01.jpg' },
  { title: 'Vice City',               section: 'Carte',      url: '#',                                  thumb: 'assets/images/heroes/vicecity_districts_night_01.jpg', soon: 'S4' },
  { title: 'Leonida Keys',            section: 'Carte',      url: '#',                                  thumb: 'assets/images/map/leonida_keys_paradise_01.jpg', soon: 'S4' },
  { title: 'Mount Kalaga',            section: 'Carte',      url: '#',                                  thumb: 'assets/images/map/mount_kalaga_epic_01.jpg', soon: 'S4' },
  { title: 'Carte de Leonida',        section: 'Carte',      url: '#',                                  thumb: 'assets/images/map/map_leonida_aerial_01.jpg', soon: 'S5' },
  { title: 'Jason Duval',             section: 'Personnage', url: '#',                                  thumb: 'assets/images/characters/characters_jason_fullbody_01.jpg', soon: 'S4' },
  { title: 'Lucia Caminos',           section: 'Personnage', url: '#',                                  thumb: 'assets/images/characters/characters_lucia_fullbody_01.jpg', soon: 'S4' },
  { title: 'Arsenal',                 section: 'Armes',      url: '#',                                  thumb: 'assets/images/weapons/weapons_arsenal_cinematic_01.jpg', soon: 'S4' },
  { title: 'Garage',                   section: 'Véhicules', url: '#',                                  thumb: 'assets/images/vehicles/vehicles_lineup_vicecity_01.jpg', soon: 'S4' },
  { title: 'Missions & braquages',    section: 'Gameplay',   url: '#',                                  thumb: 'assets/images/missions/gameplay_action_scene_01.jpg', soon: 'S4' },
  { title: 'Données de recherche S1', section: 'Projet',     url: 'research_data.json',                 thumb: '' },
  { title: 'Workflowmaster',           section: 'Projet',     url: 'workflow_master.yaml',               thumb: '' }
];

/* ── Utilitaires ───────────────────────────────────────────────────────────── */
const $  = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
const reduceMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

let toastTimer;
export function toast(message, kind = 'success') {
  let el = $('#gta-toast');
  if (!el) {
    el = document.createElement('div');
    el.id = 'gta-toast';
    el.className = 'toast';
    el.setAttribute('role', 'status');
    el.setAttribute('aria-live', 'polite');
    document.body.appendChild(el);
  }
  el.textContent = message;
  el.style.color = kind === 'error' ? 'var(--c-danger)' : 'var(--c-success)';
  el.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.hidden = true; }, 2600);
}

/* ── Navbar : burger, drawer, scroll progress ─────────────────────────────── */
export function initNavbar() {
  const burger = $('[data-nav-burger]');
  const drawer = $('[data-nav-drawer]');
  const navbar = $('.navbar');
  const progress = $('.navbar__scroll');

  if (burger && drawer) {
    const setOpen = (open) => {
      burger.setAttribute('aria-expanded', String(open));
      drawer.classList.toggle('is-open', open);
      if (open) $('a, input', drawer)?.focus();
    };
    burger.addEventListener('click', () => setOpen(burger.getAttribute('aria-expanded') !== 'true'));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setOpen(false); });
    document.addEventListener('click', (e) => {
      if (navbar && !navbar.contains(e.target)) setOpen(false);
    });
    $$('a', drawer).forEach(a => a.addEventListener('click', () => setOpen(false)));
  }

  if (progress) {
    const update = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + '%';
    };
    window.addEventListener('scroll', update, { passive: true });
    update();
  }

  // Marquer la page courante dans les liens de navigation.
  const here = location.pathname.split('/').pop() || 'index.html';
  $$('[data-nav-current]').forEach(a => {
    if (a.getAttribute('href') === here) a.setAttribute('aria-current', 'page');
  });
}

/* ── SearchEngine : autocomplete clavier ──────────────────────────────────── */
export function initSearch() {
  $$('[data-search]').forEach(root => {
    const input  = $('input', root);
    const panel  = $('[data-search-panel]', root);
    if (!input || !panel) return;
    // S3 : l'index peut être enrichi de façon asynchrone par research_data.json.
    // On le relit à chaque saisie plutôt que de figer une référence locale.
    let active = -1;
    let results = [];

    const render = (items) => {
      results = items;
      active = -1;
      panel.innerHTML = '';
      if (!items.length) {
        panel.innerHTML = '<p class="search__empty">Aucun résultat — essayez « Vice City », « Jason », « armes »…</p>';
      } else {
        items.forEach((item, i) => {
          const a = document.createElement('a');
          a.className = 'search__item';
          a.href = item.url || '#';
          a.dataset.index = String(i);
          a.setAttribute('role', 'option');
          const thumb = item.thumb
            ? `<img class="search__item-thumb" src="${item.thumb}" alt="" width="38" height="38" loading="lazy">`
            : '<span class="search__item-thumb" aria-hidden="true"></span>';
          a.innerHTML = `${thumb}<span><span class="search__item-meta">${item.section}${item.soon ? ' · ' + item.soon : ''}</span>${item.title}</span>`;
          a.addEventListener('click', (e) => {
            if (item.soon) { e.preventDefault(); toast(`Page « ${item.title} » prévue en ${item.soon}`); close(); }
          });
          panel.appendChild(a);
        });
      }
      panel.hidden = false;
    };
    const close = () => { panel.hidden = true; active = -1; };
    const highlight = (i) => {
      $$('.search__item', panel).forEach((el, n) => el.classList.toggle('is-active', n === i));
      active = i;
      if (i >= 0) $$('.search__item', panel)[i]?.scrollIntoView({ block: 'nearest' });
    };

    input.addEventListener('input', () => {
      const q = input.value.trim().toLocaleLowerCase('fr');
      if (q.length < 2) { close(); return; }
      const index = window.GTA6_SEARCH_INDEX || SEARCH_INDEX;
      render(index.filter(x => (x.title + ' ' + x.section).toLocaleLowerCase('fr').includes(q)).slice(0, 8));
    });
    input.addEventListener('keydown', (e) => {
      if (panel.hidden) return;
      if (e.key === 'ArrowDown') { e.preventDefault(); highlight(Math.min(active + 1, results.length - 1)); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); highlight(Math.max(active - 1, 0)); }
      else if (e.key === 'Enter' && active >= 0) { e.preventDefault(); $$('.search__item', panel)[active].click(); }
      else if (e.key === 'Escape') { close(); input.blur(); }
    });
    document.addEventListener('click', (e) => { if (!root.contains(e.target)) close(); });
  });
}

/* ── StatBar : remplissage au scroll ──────────────────────────────────────── */
export function initStatBars() {
  const bars = $$('[data-stat-value]');
  if (!bars.length) return;
  const fill = (bar) => {
    const v = Math.max(0, Math.min(100, Number(bar.dataset.statValue) || 0));
    $('.stat-bar__fill', bar).style.width = v + '%';
  };
  if (!('IntersectionObserver' in window) || reduceMotion()) { bars.forEach(fill); return; }
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) { fill(entry.target); io.unobserve(entry.target); }
    });
  }, { threshold: .3 });
  bars.forEach(bar => io.observe(bar));
}

/* ── TooltipSystem ────────────────────────────────────────────────────────── */
export function initTooltips() {
  $$('.tooltip[data-tooltip]').forEach(el => {
    const bubble = document.createElement('span');
    bubble.className = 'tooltip__bubble';
    bubble.setAttribute('role', 'tooltip');
    bubble.textContent = el.dataset.tooltip;
    document.body.appendChild(bubble);
    const show = () => {
      const r = el.getBoundingClientRect();
      bubble.style.left = Math.min(r.left, window.innerWidth - 290) + 'px';
      bubble.style.top = (r.bottom + window.scrollY + 10) + 'px';
      bubble.classList.add('is-shown');
    };
    const hide = () => bubble.classList.remove('is-shown');
    el.addEventListener('mouseenter', show);
    el.addEventListener('focus', show);
    el.addEventListener('mouseleave', hide);
    el.addEventListener('blur', hide);
  });
}

/* ── SpoilerToggle ────────────────────────────────────────────────────────── */
export function initSpoilers() {
  $$('[data-spoiler-toggle]').forEach(btn => {
    const content = document.getElementById(btn.getAttribute('aria-controls'));
    if (!content) return;
    btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      content.hidden = open;
    });
  });
}

/* ── CopyButton ───────────────────────────────────────────────────────────── */
export function initCopyButtons() {
  $$('[data-copy]').forEach(btn => {
    btn.addEventListener('click', async () => {
      const text = btn.dataset.copy || $(btn.dataset.copyTarget || '')?.textContent?.trim() || '';
      if (!text) return;
      try {
        if (navigator.clipboard?.writeText) await navigator.clipboard.writeText(text);
        else {
          const ta = document.createElement('textarea');
          ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
          document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove();
        }
        const original = btn.textContent;
        btn.textContent = '✓ Copié';
        btn.classList.add('is-copied');
        toast('Copié dans le presse-papiers');
        setTimeout(() => { btn.textContent = original; btn.classList.remove('is-copied'); }, 1800);
      } catch { toast('Copie impossible — sélectionnez le texte', 'error'); }
    });
  });
}

/* ── BackToTop avec indicateur de progression ─────────────────────────────── */
export function initBackToTop() {
  const btn = $('[data-back-to-top]');
  if (!btn) return;
  const update = () => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    const pct = max > 0 ? Math.min(100, (window.scrollY / max) * 100) : 0;
    btn.style.setProperty('--scroll-progress', pct + '%');
    btn.classList.toggle('is-shown', window.scrollY > 420);
    btn.setAttribute('aria-label', `Retour en haut (${Math.round(pct)} % de la page)`);
  };
  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: reduceMotion() ? 'auto' : 'smooth' }));
  window.addEventListener('scroll', update, { passive: true });
  update();
}

/* ── CookieBanner (RGPD minimal, localStorage) ────────────────────────────── */
export function initCookieBanner() {
  const banner = $('[data-cookie-banner]');
  if (!banner) return;
  const KEY = 'gta6guide.cookie.choice';
  let stored = null;
  try { stored = localStorage.getItem(KEY); } catch { /* stockage indisponible */ }
  if (stored) { banner.hidden = true; return; }
  $$('[data-cookie-choice]', banner).forEach(btn => btn.addEventListener('click', () => {
    try { localStorage.setItem(KEY, btn.dataset.cookieChoice); } catch { /* ignore */ }
    banner.hidden = true;
    toast('Préférence enregistrée');
  }));
}

/* ── AudioPlayer : 10 MP3 originaux, aucun sample sous licence ─────────────── */
export function initAudioPlayer() {
  const root = $('[data-audio-player]');
  if (!root) return;
  const tracks = window.GTA6_AUDIO_TRACKS || AUDIO_TRACKS;
  const audio = new Audio();
  audio.preload = 'none';
  let current = 0;
  let playing = false;

  const toggleBtn = $('[data-audio-toggle]', root);
  const titleEl   = $('[data-audio-title]', root);
  const trackEl   = $('[data-audio-track]', root);
  const listEl    = $('[data-audio-list]', root);
  const progEl    = $('[data-audio-progress]', root);
  const muteBtn   = $('[data-audio-mute]', root);
  const volInput  = $('[data-audio-volume]', root);
  const listBtn   = $('[data-audio-list-toggle]', root);

  if (listEl) {
    tracks.forEach((t, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'audio-player__item';
      b.textContent = `${String(i + 1).padStart(2, '0')} · ${t.label}`;
      b.addEventListener('click', () => load(i, true));
      listEl.appendChild(b);
    });
  }

  function load(i, autoplay = false) {
    current = (i + tracks.length) % tracks.length;
    audio.src = tracks[current].src;
    if (trackEl) trackEl.textContent = tracks[current].label;
    if (titleEl) titleEl.textContent = playing || autoplay ? 'Lecture' : 'Ambiances Leonida';
    $$('.audio-player__item', root).forEach((el, n) => el.classList.toggle('is-current', n === current));
    if (autoplay) play();
  }
  async function play() {
    try {
      await audio.play();
      playing = true;
      if (toggleBtn) { toggleBtn.textContent = '❚❚'; toggleBtn.setAttribute('aria-label', 'Mettre en pause'); }
      if (titleEl) titleEl.textContent = 'Lecture';
    } catch {
      playing = false;
      toast('Lecture bloquée par le navigateur — cliquez à nouveau', 'error');
    }
  }
  function pause() {
    audio.pause(); playing = false;
    if (toggleBtn) { toggleBtn.textContent = '▶'; toggleBtn.setAttribute('aria-label', 'Lire'); }
    if (titleEl) titleEl.textContent = 'Ambiances Leonida';
  }
  toggleBtn?.addEventListener('click', () => playing ? pause() : (audio.src ? play() : load(0, true)));
  $('[data-audio-next]', root)?.addEventListener('click', () => load(current + 1, playing));
  $('[data-audio-prev]', root)?.addEventListener('click', () => load(current - 1, playing));
  muteBtn?.addEventListener('click', () => {
    audio.muted = !audio.muted;
    muteBtn.textContent = audio.muted ? '🔇' : '🔊';
    muteBtn.setAttribute('aria-label', audio.muted ? 'Réactiver le son' : 'Couper le son');
  });
  volInput?.addEventListener('input', () => { audio.volume = Number(volInput.value); audio.muted = false; });
  listBtn?.addEventListener('click', () => {
    if (!listEl) return;
    listEl.hidden = !listEl.hidden;
    listBtn.setAttribute('aria-expanded', String(!listEl.hidden));
  });
  audio.addEventListener('timeupdate', () => {
    if (progEl && audio.duration) progEl.style.width = (audio.currentTime / audio.duration * 100) + '%';
  });
  audio.addEventListener('ended', () => load(current + 1, true));
  audio.addEventListener('error', () => toast('Piste audio indisponible', 'error'));
  load(0, false);
}

/* ── Breadcrumbs (générés depuis l'URL) ───────────────────────────────────── */
export function initBreadcrumbs() {
  const el = $('[data-breadcrumbs]');
  if (!el) return;
  const list = $('ol', el);
  // S4 : les pages de contenu fournissent leur propre fil d'Ariane statique
  // (data-breadcrumbs="static") pour rester justes et accessibles sans JS.
  if (el.dataset.breadcrumbs === 'static' || !list) return;
  const parts = location.pathname.split('/').filter(Boolean).map(decodeURIComponent);
  const labels = {
    'index.html': 'Accueil', 'histoire': 'Histoire', 'personnages': 'Personnages',
    'carte': 'Carte', 'armes': 'Armes', 'vehicules': 'Véhicules', 'gameplay': 'Gameplay',
    'guide': 'Guide', 'online': 'Online', 'news': 'News', 'quiz': 'Quiz'
  };
  const crumbs = ['<li><a href="index.html">Accueil</a></li>'];
  parts.forEach((p, i) => {
    if (p === 'index.html' && i === parts.length - 1) return;
    const label = labels[p] || p.replace(/-/g, ' ').replace(/\.html$/, '');
    crumbs.push(i === parts.length - 1
      ? `<li aria-current="page">${label}</li>`
      : `<li><a href="#">${label}</a></li>`);
  });
  list.innerHTML = crumbs.join('');
}

/* ── Countdown : 19/11/2026 minuit, bascule après sortie ──────────────────── */
export function initCountdown() {
  $$('[data-countdown]').forEach(root => {
    // S3 : la homepage fournit un fallback inline autonome pour l'aperçu sandbox.
    // Quand data-countdown-inline="managed", on évite un double timer.
    if (root.dataset.countdownInline === 'managed') return;
    const target = new Date(2026, 10, 19, 0, 0, 0).getTime();
    const fields = ['d', 'h', 'm', 's'].map(k => $(`[data-cd-${k}]`, root));
    const label = $('[data-cd-label]', root);
    const pad = n => String(n).padStart(2, '0');
    const tick = () => {
      const left = target - Date.now();
      if (left <= 0) {
        root.classList.add('is-live');
        if (label) label.textContent = 'GTA VI EST DISPONIBLE · 19 novembre 2026';
        const digits = $('.countdown__digits', root);
        if (digits) digits.innerHTML = '<a class="btn btn--primary countdown__launch" href="#guide-demarrage">Lancer le Guide</a>';
        return;
      }
      const s = Math.floor(left / 1000);
      [Math.floor(s / 86400), Math.floor(s % 86400 / 3600), Math.floor(s % 3600 / 60), s % 60]
        .forEach((v, i) => { if (fields[i]) fields[i].textContent = pad(v); });
      setTimeout(tick, 1000);
    };
    tick();
  });
}

/* ── Filtres (armes / véhicules / carte) ──────────────────────────────────── */
export function initFilters() {
  $$('[data-filter-group]').forEach(group => {
    const buttons = $$('[data-filter]', group);
    const targets = $$('[data-filter-target]', document);
    buttons.forEach(btn => btn.addEventListener('click', () => {
      const value = btn.dataset.filter;
      buttons.forEach(b => b.classList.toggle('is-active', b === btn));
      targets.forEach(t => {
        const tags = (t.dataset.tags || '').split(/\s+/);
        const show = value === 'all' || tags.includes(value);
        t.hidden = !show;
      });
      const live = $('[data-filter-live]', group);
      if (live) live.textContent = `${targets.filter(t => !t.hidden).length} résultat(s)`;
      toast(`Filtre : ${btn.textContent.trim()}`);
    }));
  });
}

/* ── Checklist 100 % persistée (localStorage) ─────────────────────────────── */
export function initChecklist() {
  $$('[data-checklist]').forEach(list => {
    const KEY = 'gta6guide.checklist.' + (list.dataset.checklist || 'default');
    let state = {};
    try { state = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch { state = {}; }
    const items = $$('.checklist__item', list);
    const progress = $('[data-checklist-progress]', list);
    const save = () => { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch { /* ignore */ } };
    const refresh = () => {
      const done = items.filter(i => state[i.dataset.key] === true).length;
      if (progress) progress.textContent = `${done} / ${items.length}`;
    };
    items.forEach(item => {
      const key = item.dataset.key;
      item.setAttribute('role', 'checkbox');
      item.setAttribute('tabindex', '0');
      item.setAttribute('aria-checked', String(state[key] === true));
      item.classList.toggle('is-checked', state[key] === true);
      const toggle = () => {
        state[key] = !state[key];
        item.classList.toggle('is-checked', state[key]);
        item.setAttribute('aria-checked', String(state[key]));
        save(); refresh();
      };
      item.addEventListener('click', toggle);
      item.addEventListener('keydown', e => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); toggle(); } });
    });
    refresh();
  });
}

/* ── Quiz (moteur de démo S2 ; 30 questions en S5) ────────────────────────── */
const DEMO_QUIZ = [
  { q: 'Combien de régions officielles compte Leonida ?', options: ['4', '6', '8', '11'], answer: 1, tip: 'Vice City, Leonida Keys, Grassrivers, Port Gellhorn, Ambrosia, Mount Kalaga.' },
  { q: 'Quel est le nombre maximal d’étoiles de recherche ?', options: ['5', '6', '4', '8'], answer: 1, tip: 'Le sixième niveau revient après GTA V qui plafonnait à 5.' },
  { q: 'Combien d’armes longues peut-on porter sur soi ?', options: ['1', '2', '4', 'Illimité'], answer: 1, tip: '2 longues + 2 poings ; le reste dans le coffre du véhicule.' },
  { q: 'Qui compose la score originale de GTA VI ?', options: ['Justice', 'Daft Punk', 'Hans Zimmer', 'Trent Reznor'], answer: 0, tip: 'Annonce Rockstar Newswire du 29 octobre 2026.' },
  { q: 'Quelle est la date de sortie officielle ?', options: ['26 mai 2026', '19 novembre 2026', '19 novembre 2025', '10 novembre 2026'], answer: 1, tip: 'Deux reports avant la date définitive.' }
];
export function initQuiz() {
  const root = $('[data-quiz]');
  if (!root) return;
  const qEl = $('[data-quiz-question]', root);
  const oEl = $('[data-quiz-options]', root);
  const fEl = $('[data-quiz-feedback]', root);
  const sEl = $('[data-quiz-score]', root);
  const nEl = $('[data-quiz-count]', root);
  const nxt = $('[data-quiz-next]', root);
  let i = 0, score = 0;
  const render = () => {
    const item = DEMO_QUIZ[i];
    if (!item) { qEl.textContent = 'Quiz terminé !'; oEl.innerHTML = ''; fEl.textContent = `Score final : ${score} / ${DEMO_QUIZ.length}`; return; }
    qEl.textContent = item.q;
    nEl.textContent = `Question ${i + 1} / ${DEMO_QUIZ.length}`;
    sEl.textContent = `Score ${score}`;
    fEl.textContent = '';
    oEl.innerHTML = '';
    item.options.forEach((opt, n) => {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'quiz__option'; b.textContent = opt;
      b.addEventListener('click', () => {
        if (oEl.dataset.locked === '1') return;
        oEl.dataset.locked = '1';
        const correct = n === item.answer;
        if (correct) score++;
        b.classList.add(correct ? 'is-correct' : 'is-wrong');
        $$('.quiz__option', oEl)[item.answer]?.classList.add('is-correct');
        fEl.textContent = (correct ? '✓ Correct — ' : '✕ Raté — ') + item.tip;
        sEl.textContent = `Score ${score}`;
        nxt.disabled = false;
      });
      oEl.appendChild(b);
    });
    oEl.dataset.locked = '0';
    nxt.disabled = true;
  };
  nxt?.addEventListener('click', () => { i++; render(); });
  render();
}

/* ── Divers : année du footer, ancres douces, sons UI ─────────────────────── */
export function initMisc() {
  $$('[data-year]').forEach(el => { el.textContent = String(new Date().getFullYear()); });
  $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    const id = a.getAttribute('href').slice(1);
    const target = id && document.getElementById(id);
    if (target) { e.preventDefault(); target.scrollIntoView({ behavior: reduceMotion() ? 'auto' : 'smooth', block: 'start' }); }
  }));
  // Sons UI : uniquement après une première interaction utilisateur (autoplay policy).
  if (window.GTA6_UI_SOUNDS === true) {
    let armed = false;
    const arm = () => {
      if (armed) return; armed = true;
      const click = new Audio('assets/audio/ui/homepage_ui_click_01.mp3');
      $$('.btn, .navbar__links a, .filter-btn').forEach(el => el.addEventListener('click', () => {
        click.currentTime = 0; click.play().catch(() => {});
      }));
    };
    document.addEventListener('pointerdown', arm, { once: true });
  }
}

/* ── Initialisation automatique ───────────────────────────────────────────── */
export function initComponents() {
  initNavbar();
  initSearch();
  initStatBars();
  initTooltips();
  initSpoilers();
  initCopyButtons();
  initBackToTop();
  initCookieBanner();
  initAudioPlayer();
  initBreadcrumbs();
  initCountdown();
  initFilters();
  initChecklist();
  initQuiz();
  initMisc();
}

function ready(fn) {
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn, { once: true });
  else fn();
}
ready(initComponents);
