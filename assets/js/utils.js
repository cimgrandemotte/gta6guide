/* ═══════════════════════════════════════════════════════════════════════════
   utils.js — S3 / BUILD_CORE_PAGES
   Utilitaires zéro dépendance + playlist locale.

   Règles : aucun CDN, aucun localhost, aucun appel réseau externe. Les chemins
   sont résolus depuis `data-root` posé sur <html> ("." à la racine, ".." dans
   /en/). `research_data.json` n'est consulté qu'en relative URL, avec dégradation
   gracieuse si l'aperçu sandbox bloque fetch().
   ═══════════════════════════════════════════════════════════════════════════ */

export const ASSET_ROOT = document.documentElement.dataset.root || '.';

/** Construit une URL locale relative compatible racine FR et sous-dossier /en/. */
export function asset(path) {
  if (/^(?:[a-z]+:|\/\/|#|data:|mailto:|tel:)/i.test(path)) return path;
  return `${ASSET_ROOT}/${String(path).replace(/^\/+/, '')}`;
}

export const normalize = (value) => String(value || '')
  .normalize('NFD')
  .replace(/[\u0300-\u036f]/g, '')
  .toLocaleLowerCase('fr');

export const escapeHTML = (value) => String(value || '').replace(/[&<>"']/g, (c) => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[c]));

export const debounce = (fn, delay = 120) => {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
};

export const prefersReducedMotion = () =>
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

export const storage = {
  get(key, fallback = null) {
    try {
      const raw = localStorage.getItem(key);
      return raw === null ? fallback : JSON.parse(raw);
    } catch { return fallback; }
  },
  set(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); return true; }
    catch { return false; }
  }
};

export function announce(message) {
  let el = document.getElementById('gta6-live-region');
  if (!el) {
    el = document.createElement('div');
    el.id = 'gta6-live-region';
    el.className = 'sr-only';
    el.setAttribute('role', 'status');
    el.setAttribute('aria-live', 'polite');
    el.setAttribute('aria-atomic', 'true');
    document.body.appendChild(el);
  }
  el.textContent = '';
  window.setTimeout(() => { el.textContent = message; }, 30);
}

/** Formatte sans fabriquer de chiffre : retourne « — » si la valeur manque. */
export const metric = (value) =>
  Number.isFinite(Number(value)) ? Number(value).toLocaleString('fr-FR') : '—';

/* ── Playlist S3 : 10 MP3 S2 + 2 MP3 S3, tous locaux et non officiels ─────── */
const TRACKS = [
  ['Sunset Cruise · Ambiance S3', 'assets/audio/ambiances/homepage_ambiance_sunset_cruise_01.mp3'],
  ['Guide Intro · Jingle S3', 'assets/audio/jingles/homepage_jingle_guide_intro_01.mp3'],
  ['Vice City · Nuit néon', 'assets/audio/ambiances/homepage_ambiance_vicecity_night_01.mp3'],
  ['Leonida · Wetlands', 'assets/audio/ambiances/map_leonida_ambiance_01.mp3'],
  ['Moteur V8 · Démarrage', 'assets/audio/ambiances/vehicles_engine_v8_01.mp3'],
  ['Jason · Thème', 'assets/audio/jingles/characters_jason_theme_01.mp3'],
  ['Lucia · Thème', 'assets/audio/jingles/characters_lucia_theme_01.mp3'],
  ['UI · Survol', 'assets/audio/ui/homepage_ui_hover_01.mp3'],
  ['UI · Clic', 'assets/audio/ui/homepage_ui_click_01.mp3'],
  ['UI · Transition', 'assets/audio/ui/homepage_ui_transition_01.mp3'],
  ['Arme · Équipement', 'assets/audio/ui/weapons_equip_sound_01.mp3'],
  ['Quiz · Bonne réponse', 'assets/audio/ui/quiz_correct_answer_01.mp3']
].map(([label, src]) => ({ label, src: asset(src) }));

/** Vrai si la page courante est la racine du site (le lecteur audio y est monté). */
export const hasAudioPlayer = Boolean(document.querySelector('[data-audio-player]'));

/** Styles/scripts partagés absents : signale un environnement dégradé. */
window.GTA6_AUDIO_TRACKS = hasAudioPlayer ? TRACKS : [];
window.GTA6_UI_SOUNDS = false; // aucun son UI sans opt-in explicite
window.GTA6Utils = { asset, normalize, escapeHTML, debounce, prefersReducedMotion, storage, announce, metric };
