/* ==========================================================================
   S5 — Quiz GTA VI : 30 questions, 3 niveaux, chronomètre, score, rejouer.
   Aucune question ne porte sur du contenu interne non vérifié : uniquement
   calendrier, distribution, géographie nommée, chiffres publiés par la presse
   post-embargo. Chaque réponse porte sa référence de fait (research_data.json).
   ========================================================================== */

const QUESTIONS = [
  // ── Facile (10) ───────────────────────────────────────────────────────────
  { level: 'facile', q: 'Quel État fictif sert de cadre à GTA VI ?', options: ['Leonida', 'San Andreas', 'Liberty', 'Alderney'], answer: 0, tip: 'Leonida est la version fictive de la Floride. <code>REL-01</code>' },
  { level: 'facile', q: 'Quelle ville fait son retour dans GTA VI ?', options: ['Liberty City', 'Vice City', 'Los Santos', 'Carcer City'], answer: 1, tip: 'Premier retour à Vice City depuis 2002. <code>MAP-01</code>' },
  { level: 'facile', q: 'Quelle est la date de sortie officielle ?', options: ['26 mai 2026', '19 novembre 2026', '19 novembre 2025', '10 novembre 2026'], answer: 1, tip: 'Date verrouillée après deux reports. <code>REL-02</code>' },
  { level: 'facile', q: 'Quels sont les deux protagonistes ?', options: ['Jason et Lucia', 'Michael et Franklin', 'Tommy et Lance', 'Niko et Roman'], answer: 0, tip: 'Jason Duval et Lucia Caminos. <code>CHA-01</code>' },
  { level: 'facile', q: 'Combien de régions Rockstar a-t-il nommées officiellement ?', options: ['4', '6', '8', '11'], answer: 1, tip: 'Vice City, Keys, Grassrivers, Port Gellhorn, Ambrosia, Mount Kalaga. <code>MAP-16</code>' },
  { level: 'facile', q: 'Sur quelles consoles le jeu sort-il au lancement ?', options: ['PS5 et Xbox Series X|S', 'PS4 et Xbox One', 'PC uniquement', 'Switch 2 et PS5'], answer: 0, tip: 'Aucune version PC, PS4, Xbox One ou Switch 2. <code>FAQ-02</code>' },
  { level: 'facile', q: 'Combien coûte l’édition Standard ?', options: ['59,99 $', '69,99 $', '79,99 $', '89,99 $'], answer: 2, tip: 'Ultimate à 99,99 $, soit 20 $ de plus. <code>FAQ-03</code>' },
  { level: 'facile', q: 'Que contient la version physique vendue en boîte ?', options: ['Un disque', 'Un code de téléchargement', 'Deux disques', 'Une carte SD'], answer: 1, tip: 'Pas de disque : un code, point. <code>FAQ-04</code>' },
  { level: 'facile', q: 'Quelle est la cible de fréquence d’images annoncée ?', options: ['30 fps', '40 fps', '60 fps', '120 fps'], answer: 0, tip: '30 fps sur toutes les consoles, PS5 Pro incluse. <code>FAQ-07</code>' },
  { level: 'facile', q: 'Combien d’espace faut-il au maximum pour le préchargement ?', options: ['98 Go', '148 Go', '212 Go', '312 Go'], answer: 2, tip: 'Jusqu’à 212 Go selon la machine. <code>FAQ-05</code>' },

  // ── Moyen (10) ────────────────────────────────────────────────────────────
  { level: 'moyen', q: 'Quel quartier de Vice City correspond au Wynwood de Miami ?', options: ['Stockyard', 'La Perle', 'Vice Beach', 'Bayside'], answer: 0, tip: 'Stockyard : entrepôts, fresques, galeries.', ref: 'MAP-17' },
  { level: 'moyen', q: 'Combien de trophées compte GTA VI ?', options: ['42', '50', '55', '60'], answer: 2, tip: '55 trophées, dont 28 cachés. <code>TRO-17</code>' },
  { level: 'moyen', q: 'Quel est le nom du trophée platine ?', options: ['A Long Road', 'Vice Got a Price!', 'One Last Thing', 'Leonida Legend'], answer: 1, tip: '« Vice Got a Price! » — Leonida Legend. <code>TRO-18</code>' },
  { level: 'moyen', q: 'Combien de challenges compte le jeu ?', options: ['50', '60', '80', '100'], answer: 2, tip: '80 challenges, 8 catégories de 10. <code>TRO-29</code>' },
  { level: 'moyen', q: 'Combien de challenges faut-il pour la checklist 100 % ?', options: ['40 sur 80', '50 sur 80', '70 sur 80', 'Les 80'], answer: 2, tip: '50 débloque un trophée, 70 sont exigés pour le 100 %. <code>TRO-29</code>' },
  { level: 'moyen', q: 'Combien de séries de cartes à collectionner existent ?', options: ['12', '15', '18', '24'], answer: 2, tip: '18 séries, 480 cartes uniques. <code>TRO-31</code>' },
  { level: 'moyen', q: 'Combien de séries complètes faut-il pour le 100 % ?', options: ['3', '8', '12', '15'], answer: 3, tip: '3 donnent un trophée, 15 sont exigées pour le 100 %. <code>TRO-31</code>' },
  { level: 'moyen', q: 'Quelle résolution interne Digital Foundry mesure-t-il sur PS5 ?', options: ['1080p', '1440p', '1800p', '4K natif'], answer: 1, tip: '1440p, upscalé ensuite (PSSR sur Pro). <code>FAQ-08</code>' },
  { level: 'moyen', q: 'Quel avantage la PS5 Pro ajoute-t-elle ?', options: ['Un mode 60 fps', 'Les ombres ray-tracées et le PSSR', 'Une carte étendue', 'Le multijoueur'], answer: 1, tip: 'PSSR et ombres RT, mais pas de gain de fréquence. <code>FAQ-09</code>' },
  { level: 'moyen', q: 'Combien d’espèces animales le jeu compte-t-il ?', options: ['70', '120', '170', '250'], answer: 2, tip: 'Plus de 170 espèces, classées Rare / Découvrable / Légendaire. <code>MAP-21</code>' },

  // ── Difficile (10) ────────────────────────────────────────────────────────
  { level: 'difficile', q: 'Quel chiffre avance la communauté pour la surface de terres de Leonida ?', options: ['≈ 48 km²', '≈ 83 km²', '≈ 128 km²', '≈ 210 km²'], answer: 1, tip: 'Estimation communautaire ≈ 83 km², jamais confirmée par Rockstar. <code>MAP-19</code>' },
  { level: 'difficile', q: 'Comment s’appelle la base cartographique communautaire utilisée par les cartes de fans ?', options: ['YANIS', 'LEONIS', 'VICEMAP', 'ATLAS VI'], answer: 0, tip: 'Base YANIS du projet gtadb.org, sous licence CC BY 4.0. <code>MAP-17</code>' },
  { level: 'difficile', q: 'Que publie Rockstar le 19 novembre côté carte ?', options: ['Une carte interactive', 'Une carte imprimable gratuite', 'Un atlas payant', 'Rien du tout'], answer: 1, tip: 'Carte et poster à imprimer, puis version physique à 0,99 $. <code>MAP-16</code>' },
  { level: 'difficile', q: 'Combien de temps Digital Foundry a-t-il analysé sur la démo ?', options: ['6 minutes', '16 minutes', '26 minutes', '46 minutes'], answer: 2, tip: '26 minutes de démo passées au crible. <code>FAQ-08</code>', },
  { level: 'difficile', q: 'À combien descendent les pires chutes mesurées sur PS5 ?', options: ['18 fps', '23 fps', '27 fps', '29 fps'], answer: 1, tip: '23 fps en action lourde soutenue, cas extrême. <code>FAQ-08</code>' },
  { level: 'difficile', q: 'Quel est le seul point réellement manquable de la complétion ?', options: ['La méditation du chapitre 1', 'Un braquage de banque', 'Une course de rue', 'Un collectible sous-marin'], answer: 0, tip: 'La méditation du chapitre 1. <code>TRO-23</code>' },
  { level: 'difficile', q: 'Quand la checklist 100 % devient-elle visible dans le jeu ?', options: ['Dès le début', 'Au chapitre 3', 'Après la fin de l’histoire', 'Après le platine'], answer: 2, tip: 'Elle apparaît après l’histoire, mais la progression déjà faite compte. <code>TRO-32</code>' },
  { level: 'difficile', q: 'Combien d’entrées compte environ la base de progression interne ?', options: ['300', '800', '1 500', '3 000'], answer: 3, tip: 'Environ 3 000 entrées : véhicules, animaux, armes, braquages. <code>TRO-30</code>' },
  { level: 'difficile', q: 'Quel est le prix du coffret « The Goodtime State » ?', options: ['199,99 $', '299,99 $', '399,99 $', '499,99 $'], answer: 2, tip: '399,99 $ — et il ne contient pas le jeu. <code>FAQ-06</code>' },
  { level: 'difficile', q: 'Quel élément rend un mode 60 fps irréalisable sur cette génération ?', options: ['Le streaming des textures', 'Les cheveux simulés sur tous les PNJ', 'La taille de la carte', 'Le nombre de véhicules'], answer: 1, tip: 'Mèches simulées physiquement, PNJ compris. <code>DIV-08</code>' }
];

const LEVEL_ORDER = { facile: 'Facile', moyen: 'Moyen', difficile: 'Difficile' };

function shuffle(list) {
  const copy = list.slice();
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

export function initS5Quiz() {
  const root = document.querySelector('[data-s5-quiz]');
  if (!root) return;

  const qEl = root.querySelector('[data-quiz-q]');
  const optEl = root.querySelector('[data-quiz-opts]');
  const fbEl = root.querySelector('[data-quiz-fb]');
  const countEl = root.querySelector('[data-quiz-count]');
  const scoreEl = root.querySelector('[data-quiz-score]');
  const timerEl = root.querySelector('[data-quiz-timer]');
  const levelEl = root.querySelector('[data-quiz-level]');
  const nextBtn = root.querySelector('[data-quiz-next]');
  const startBtn = root.querySelector('[data-quiz-start]');
  const restartBtn = root.querySelector('[data-quiz-restart]');
  const resultEl = root.querySelector('[data-quiz-result]');
  const resultScore = root.querySelector('[data-quiz-result-score]');
  const resultText = root.querySelector('[data-quiz-result-text]');
  const levelChips = Array.from(root.querySelectorAll('[data-quiz-mode]'));

  let pool = QUESTIONS.slice();
  let index = 0;
  let score = 0;
  let locked = false;
  let timer = null;
  let remaining = 20;

  const stopTimer = () => { if (timer) { clearInterval(timer); timer = null; } };

  const startTimer = () => {
    stopTimer();
    remaining = 20;
    const paint = () => {
      if (!timerEl) return;
      timerEl.textContent = `${remaining} s`;
      timerEl.dataset.low = remaining <= 5 ? '1' : '0';
    };
    paint();
    timer = setInterval(() => {
      remaining -= 1;
      paint();
      if (remaining <= 0) {
        stopTimer();
        if (!locked) answer(-1);
      }
    }, 1000);
  };

  const paint = () => {
    const item = pool[index];
    if (!item) return finish();
    locked = false;
    if (fbEl) fbEl.innerHTML = '';
    if (countEl) countEl.textContent = `Question ${index + 1} / ${pool.length}`;
    if (scoreEl) scoreEl.textContent = `Score ${score}`;
    if (levelEl) { levelEl.textContent = LEVEL_ORDER[item.level]; levelEl.dataset.level = item.level; }
    if (qEl) qEl.textContent = item.q;
    if (optEl) {
      optEl.innerHTML = '';
      item.options.forEach((opt, n) => {
        const li = document.createElement('li');
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 's5-quiz__opt';
        b.textContent = opt;
        b.addEventListener('click', () => answer(n));
        li.appendChild(b);
        optEl.appendChild(li);
      });
    }
    if (nextBtn) nextBtn.disabled = true;
    startTimer();
  };

  const answer = (choice) => {
    if (locked) return;
    locked = true;
    stopTimer();
    const item = pool[index];
    const buttons = optEl ? Array.from(optEl.querySelectorAll('.s5-quiz__opt')) : [];
    buttons.forEach((b, n) => {
      b.disabled = true;
      if (n === item.answer) b.classList.add('is-correct');
      else if (n === choice) b.classList.add('is-wrong');
    });
    const correct = choice === item.answer;
    if (correct) score += 1;
    if (scoreEl) scoreEl.textContent = `Score ${score}`;
    if (fbEl) {
      const prefix = choice === -1 ? '⏱ Temps écoulé — ' : (correct ? '✓ Correct — ' : '✕ Raté — ');
      fbEl.innerHTML = prefix + item.tip;
    }
    if (nextBtn) {
      nextBtn.disabled = false;
      nextBtn.textContent = index + 1 === pool.length ? 'Voir le résultat' : 'Question suivante';
    }
  };

  const finish = () => {
    stopTimer();
    const total = pool.length;
    const pct = Math.round((score / total) * 100);
    let verdict;
    if (pct >= 90) verdict = 'Niveau Leonida Legend : vous connaissez le dossier mieux que la plupart des rédactions.';
    else if (pct >= 70) verdict = 'Solide : vous suivez l’actualité de près, quelques détails vous échappent encore.';
    else if (pct >= 50) verdict = 'Correct : les bases sont là, la partie technique et la complétion restent à revoir.';
    else verdict = 'À retravailler : commencez par la FAQ et la page Trophées, puis revenez.';
    if (qEl) qEl.textContent = 'Quiz terminé';
    if (optEl) optEl.innerHTML = '';
    if (fbEl) fbEl.innerHTML = '';
    if (timerEl) timerEl.textContent = '—';
    if (resultEl) resultEl.hidden = false;
    if (resultScore) resultScore.textContent = `${score} / ${total} — ${pct} %`;
    if (resultText) resultText.textContent = verdict;
    if (nextBtn) nextBtn.hidden = true;
  };

  const start = () => {
    const mode = root.dataset.mode || 'all';
    pool = mode === 'all' ? shuffle(QUESTIONS) : shuffle(QUESTIONS.filter(q => q.level === mode)).slice(0, 10);
    index = 0;
    score = 0;
    if (resultEl) resultEl.hidden = true;
    if (nextBtn) { nextBtn.hidden = false; nextBtn.textContent = 'Question suivante'; }
    paint();
  };

  levelChips.forEach(chip => chip.addEventListener('click', () => {
    root.dataset.mode = chip.dataset.quizMode;
    levelChips.forEach(c => c.setAttribute('aria-pressed', String(c === chip)));
    start();
  }));

  if (startBtn) startBtn.addEventListener('click', start);
  if (restartBtn) restartBtn.addEventListener('click', start);
  if (nextBtn) nextBtn.addEventListener('click', () => { index += 1; paint(); });

  start();
}
