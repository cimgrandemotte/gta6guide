/* ==========================================================================
   S5 — Checklists 100 % persistées (localStorage), accessibles au clavier.
   Chaque liste porte un data-checklist="slug" et chaque item un data-key.
   Le composant historique de components.js gère déjà ce contrat ; ce module
   ajoute le filtrage par catégorie, la barre de progression et la remise à zéro.
   ========================================================================== */

const KEY_PREFIX = 'gta6guide.checklist.';

function readStore(key) {
  try {
    return JSON.parse(localStorage.getItem(KEY_PREFIX + key) || '{}');
  } catch {
    return {};
  }
}

function writeStore(key, state) {
  try {
    localStorage.setItem(KEY_PREFIX + key, JSON.stringify(state));
  } catch {
    /* Mode privé ou quota : on continue en mémoire. */
  }
}

export function initS5Checklists() {
  document.querySelectorAll('[data-s5-checklist]').forEach(root => {
    const storeKey = root.dataset.s5Checklist || 's5';
    const state = readStore(storeKey);
    const items = Array.from(root.querySelectorAll('[data-check-item]'));
    const fill = root.querySelector('[data-check-fill]');
    const label = root.querySelector('[data-check-label]');
    const chips = Array.from(root.querySelectorAll('[data-check-filter]'));
    const clear = root.querySelector('[data-check-clear]');
    const empty = root.querySelector('[data-check-empty]');
    let filter = 'all';

    const render = () => {
      let visible = 0;
      let done = 0;
      items.forEach(item => {
        const key = item.dataset.checkItem;
        const cat = item.dataset.category || 'all';
        const isDone = state[key] === true;
        if (isDone) done += 1;
        const show = filter === 'all' || cat === filter;
        item.hidden = !show;
        if (show) visible += 1;
        item.setAttribute('role', 'checkbox');
        item.setAttribute('tabindex', '0');
        item.setAttribute('aria-checked', String(isDone));
        item.classList.toggle('is-checked', isDone);
      });
      const total = items.length;
      const pct = total ? Math.round((done / total) * 100) : 0;
      if (fill) fill.style.width = pct + '%';
      if (label) label.textContent = `${done} / ${total} validés · ${pct} %`;
      root.querySelector('[data-check-bar]')?.setAttribute('aria-valuenow', String(pct));
      if (empty) empty.hidden = visible !== 0;
    };

    const toggle = (item) => {
      const key = item.dataset.checkItem;
      state[key] = !(state[key] === true);
      writeStore(storeKey, state);
      render();
    };

    items.forEach(item => {
      item.addEventListener('click', () => toggle(item));
      item.addEventListener('keydown', (e) => {
        if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); toggle(item); }
      });
    });

    chips.forEach(chip => chip.addEventListener('click', () => {
      filter = chip.dataset.checkFilter;
      chips.forEach(c => c.setAttribute('aria-pressed', String(c === chip)));
      render();
    }));

    if (clear) {
      clear.addEventListener('click', () => {
        items.forEach(item => { delete state[item.dataset.checkItem]; });
        writeStore(storeKey, state);
        render();
        if (label) label.textContent = `0 / ${items.length} validés · 0 %`;
      });
    }

    render();
  });

  // Compteur global des collectibles (page collectibles, bloc de synthèse).
  document.querySelectorAll('[data-collect-total]').forEach(el => {
    const root = document.querySelector('[data-s5-checklist]');
    if (!root) return;
    const items = Array.from(root.querySelectorAll('[data-check-item]'));
    const state = readStore(root.dataset.s5Checklist || 's5');
    const done = items.filter(i => state[i.dataset.checkItem] === true).length;
    el.textContent = `${done} / ${items.length}`;
  });
}
