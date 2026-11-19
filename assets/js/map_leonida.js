/* ==========================================================================
   S5 — Carte interactive de Leonida (schéma SVG maison, zéro dépendance)
   Aucun appel réseau, aucun CDN, aucun localhost : l'aperçu sandbox
   fonctionne exactement comme le fichier ouvert en local.
   ========================================================================== */

const REGIONS = {
  vicecity: 'Vice City',
  keys: 'Leonida Keys',
  grassrivers: 'Grassrivers',
  portgellhorn: 'Port Gellhorn',
  ambrosia: 'Ambrosia',
  kalaga: 'Mount Kalaga'
};

const KINDS = {
  collectible: 'Collectible',
  activity: 'Activité',
  landmark: 'Repère',
  danger: 'Zone à risque'
};

/* Coordonnées exprimées dans le viewBox 0 0 400 300 du schéma.
   Aucune position n'est officielle : toutes sont des placements éditoriaux. */
const PLACES = [
  { id: 'vice-beach', name: 'Vice Beach', region: 'vicecity', kind: 'landmark', x: 268, y: 196, note: 'Front de mer Art déco, Ocean Drive' },
  { id: 'downtown', name: 'Downtown Vice City', region: 'vicecity', kind: 'landmark', x: 236, y: 168, note: 'Tours, bayfront, banques' },
  { id: 'stockyard', name: 'Stockyard', region: 'vicecity', kind: 'landmark', x: 208, y: 150, note: 'Entrepôts, fresques, galeries' },
  { id: 'la-perle', name: 'La Perle', region: 'vicecity', kind: 'collectible', x: 226, y: 132, note: 'Quartier haïtien au nord du centre' },
  { id: 'design', name: 'Design District', region: 'vicecity', kind: 'collectible', x: 250, y: 142, note: 'Commerce de luxe, vitrines' },
  { id: 'flamingo', name: 'Série de cartes Flamingos', region: 'vicecity', kind: 'collectible', x: 282, y: 214, note: '24 cartes — voir la checklist' },
  { id: 'marina', name: 'Marina de Vice Beach', region: 'vicecity', kind: 'activity', x: 292, y: 178, note: 'Bateaux, plongée, sorties en mer' },
  { id: 'k9', name: 'Roadblock de nuit', region: 'vicecity', kind: 'danger', x: 214, y: 186, note: 'Éviter 4 étoiles ici : peu de fuite' },

  { id: 'keys-north', name: 'Key Lento', region: 'keys', kind: 'landmark', x: 214, y: 258, note: 'La plus grande île de la chaîne' },
  { id: 'keys-boat', name: "Brian's Boat Works", region: 'keys', kind: 'activity', x: 186, y: 276, note: 'Atelier et marina du sud' },
  { id: 'keys-bridge', name: 'Pont des Keys', region: 'keys', kind: 'landmark', x: 250, y: 268, note: 'Liaison routière principale' },
  { id: 'keys-shell', name: 'Coquillages et jetées', region: 'keys', kind: 'collectible', x: 232, y: 284, note: 'Chasse en bord de mer' },

  { id: 'grass-airboat', name: 'Airboat des marais', region: 'grassrivers', kind: 'activity', x: 178, y: 200, note: 'Everglades, faune, eau peu profonde' },
  { id: 'grass-rv', name: 'Sunrise RV Park', region: 'grassrivers', kind: 'landmark', x: 156, y: 214, note: 'Camping-car, relais routier' },
  { id: 'grass-gator', name: 'Zone à alligators', region: 'grassrivers', kind: 'danger', x: 168, y: 226, note: 'Nager ici coûte cher' },
  { id: 'grass-cards', name: 'Cartes éparpillées', region: 'grassrivers', kind: 'collectible', x: 148, y: 196, note: 'Série locale, 24 cartes' },

  { id: 'pg-port', name: 'Port de Gellhorn', region: 'portgellhorn', kind: 'landmark', x: 108, y: 138, note: 'Industrie, grues, conteneurs' },
  { id: 'pg-motel', name: 'Starlet Motel', region: 'portgellhorn', kind: 'landmark', x: 120, y: 122, note: 'Point de rendez-vous discret' },
  { id: 'pg-race', name: 'Circuit de Gellhorn', region: 'portgellhorn', kind: 'activity', x: 96, y: 118, note: 'Courses, véhicules rapides' },
  { id: 'pg-crate', name: 'Conteneurs à fouiller', region: 'portgellhorn', kind: 'collectible', x: 86, y: 148, note: 'Butin et cartes' },

  { id: 'amb-mill', name: 'Raffinerie Allied Crystal', region: 'ambrosia', kind: 'landmark', x: 118, y: 84, note: 'Sucre, cheminées, paysage plat' },
  { id: 'amb-raceway', name: 'Ambrosia Raceway', region: 'ambrosia', kind: 'activity', x: 138, y: 92, note: 'Piste, paris, véhicules' },
  { id: 'amb-baseball', name: 'Terrain de baseball', region: 'ambrosia', kind: 'activity', x: 152, y: 74, note: 'Activité de quartier' },
  { id: 'amb-cane', name: 'Champs de canne', region: 'ambrosia', kind: 'collectible', x: 104, y: 68, note: 'Collectibles en zone rurale' },

  { id: 'mk-summit', name: 'Mont Kalaga', region: 'kalaga', kind: 'landmark', x: 74, y: 52, note: 'Point culminant, vue sur l\'État' },
  { id: 'mk-falls', name: 'Cascade et réservoir', region: 'kalaga', kind: 'activity', x: 92, y: 40, note: 'Randonnée, saut de base' },
  { id: 'mk-trail', name: 'Sentiers et faune rare', region: 'kalaga', kind: 'collectible', x: 62, y: 36, note: 'Espèces légendaires à photographier' },
  { id: 'mk-camp', name: 'Camp isolé', region: 'kalaga', kind: 'danger', x: 80, y: 62, note: 'Rencontres hostiles hors sentier' }
];

function normalise(v) {
  return v.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
}

export function initLeonidaMap() {
  const root = document.querySelector('[data-leonida-map]');
  if (!root) return;

  const pins = Array.from(root.querySelectorAll('[data-pin]'));
  const items = Array.from(root.querySelectorAll('[data-place-item]'));
  const chips = Array.from(root.querySelectorAll('[data-map-filter]'));
  const input = root.querySelector('[data-map-search]');
  const count = root.querySelector('[data-map-count]');
  const empty = root.querySelector('[data-map-empty]');
  const detail = root.querySelector('[data-map-detail]');
  const reset = root.querySelector('[data-map-reset]');

  let activeFilter = 'all';
  let query = '';

  const matches = (place) => {
    const okFilter = activeFilter === 'all' || place.region === activeFilter || place.kind === activeFilter;
    if (!okFilter) return false;
    if (!query) return true;
    const hay = normalise(`${place.name} ${REGIONS[place.region]} ${KINDS[place.kind]} ${place.note}`);
    return hay.includes(query);
  };

  const apply = () => {
    let visible = 0;
    PLACES.forEach(place => {
      const ok = matches(place);
      if (ok) visible += 1;
      const pin = root.querySelector(`[data-pin="${place.id}"]`);
      const item = root.querySelector(`[data-place-item="${place.id}"]`);
      if (pin) pin.hidden = !ok;
      if (item) item.hidden = !ok;
    });
    if (count) count.textContent = `${visible} / ${PLACES.length} lieux affichés`;
    if (empty) empty.hidden = visible !== 0;
    if (detail) {
      detail.textContent = visible === 0
        ? 'Aucun lieu ne correspond à ce filtre.'
        : 'Sélectionnez un point sur la carte ou dans la liste pour voir son détail.';
    }
  };

  const select = (place) => {
    if (detail) {
      detail.innerHTML = `<strong>${place.name}</strong> — ${REGIONS[place.region]} · ${KINDS[place.kind]}. ${place.note}.`;
    }
    const pin = root.querySelector(`[data-pin="${place.id}"]`);
    if (pin) {
      pin.setAttribute('aria-current', 'true');
      root.querySelectorAll('[data-pin][aria-current]').forEach(p => { if (p !== pin) p.removeAttribute('aria-current'); });
    }
  };

  chips.forEach(chip => chip.addEventListener('click', () => {
    activeFilter = chip.dataset.mapFilter;
    chips.forEach(c => c.setAttribute('aria-pressed', String(c === chip)));
    apply();
  }));

  if (input) {
    input.addEventListener('input', () => { query = normalise(input.value); apply(); });
  }

  if (reset) {
    reset.addEventListener('click', () => {
      activeFilter = 'all';
      query = '';
      if (input) input.value = '';
      chips.forEach((c, i) => c.setAttribute('aria-pressed', String(i === 0)));
      if (detail) detail.textContent = 'Sélectionnez un point sur la carte ou dans la liste pour voir son détail.';
      apply();
      if (input) input.focus();
    });
  }

  [...pins, ...items].forEach(el => {
    const id = el.dataset.pin || el.dataset.placeItem;
    const place = PLACES.find(p => p.id === id);
    if (!place) return;
    el.addEventListener('click', () => select(place));
    el.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); select(place); }
    });
  });

  apply();

  // Copie de la fiche lieu dans le presse-papier (dégradation silencieuse).
  const copyBtn = root.querySelector('[data-map-copy]');
  if (copyBtn) {
    copyBtn.addEventListener('click', async () => {
      const text = PLACES.map(p => `${p.name} (${REGIONS[p.region]} · ${KINDS[p.kind]}) — ${p.note}`).join('\n');
      try {
        await navigator.clipboard.writeText(text);
        copyBtn.textContent = 'Liste copiée ✓';
        setTimeout(() => { copyBtn.textContent = 'Copier la liste des 28 lieux'; }, 2200);
      } catch {
        copyBtn.textContent = 'Copie indisponible ici';
      }
    });
  }
}
