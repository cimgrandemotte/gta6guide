#!/usr/bin/env python3
"""
Générateur d'ambiances & effets sonores ORIGINAUX au format MP3.

IMPORTANT — honnêteté des assets :
  Ce script ne reproduit AUCUN extrait musical, aucune bande-son Rockstar,
  aucun sample de moteur réel. Il synthétise des signaux (bruit filtré,
  nappes, sweeps, clics) avec NumPy puis les encode en MP3 via lameenc.
  Les fichiers produits sont des "ambiances synthétiques originales".

Prérequis (non persistés dans le snapshot du workspace, à réinstaller si besoin) :
    python3 -m pip install numpy lameenc

Usage :
    python3 tools/make_audio.py
    python3 tools/make_audio.py --outdir assets/audio/ambiances

Règle du projet : TOUS les audios sont des .mp3, ≤ 10 par réponse de l'agent.
"""
from __future__ import annotations

import argparse
import math
import os
import struct
import sys

import numpy as np

try:
    import lameenc
except ImportError:
    sys.exit("Module 'lameenc' manquant → python3 -m pip install numpy lameenc")

SR = 44100          # Hz
BITRATE = 192       # kbps


def normalize(x: np.ndarray, peak: float = 0.85) -> np.ndarray:
    m = float(np.max(np.abs(x))) or 1.0
    return x / m * peak


def fade(x: np.ndarray, ms: int = 30) -> np.ndarray:
    n = max(1, int(SR * ms / 1000))
    if len(x) < 2 * n:
        n = len(x) // 2
    env = np.ones(len(x), dtype=np.float32)
    env[:n] = np.linspace(0, 1, n, dtype=np.float32)
    env[-n:] = np.linspace(1, 0, n, dtype=np.float32)
    return x * env


def to_pcm16(x: np.ndarray) -> bytes:
    y = np.clip(x, -1.0, 1.0)
    return struct.pack('<%dh' % len(y), *(np.int16(y * 32767)).tolist())


def save_mp3(x: np.ndarray, path: str) -> None:
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    enc = lameenc.Encoder()
    enc.set_bit_rate(BITRATE)
    enc.set_in_sample_rate(SR)
    enc.set_channels(1)
    enc.set_quality(2)
    pcm = to_pcm16(fade(normalize(x)))
    data = enc.encode(pcm) + enc.flush()
    with open(path, 'wb') as f:
        f.write(data)
    print(f'  ✓ {path}  ({len(data) // 1024} Ko)')


def t(seconds: float) -> np.ndarray:
    return np.arange(int(SR * seconds), dtype=np.float32) / SR


def tone(freq: float, seconds: float, kind: str = 'sine') -> np.ndarray:
    tt = t(seconds)
    if kind == 'sine':
        return np.sin(2 * np.pi * freq * tt, dtype=np.float32)
    if kind == 'tri':
        return (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * freq * tt)).astype(np.float32)
    return np.sign(np.sin(2 * np.pi * freq * tt)).astype(np.float32)


def sweep(f0: float, f1: float, seconds: float) -> np.ndarray:
    tt = t(seconds)
    phase = 2 * np.pi * (f0 * tt + (f1 - f0) * tt ** 2 / (2 * seconds))
    return np.sin(phase, dtype=np.float32)


def noise(seconds: float, seed: int = 0, lowpass: float | None = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(int(SR * seconds)).astype(np.float32)
    if lowpass:
        # Filtre passe-bas à un pôle, suffisant pour une nappe/ambiance.
        a = math.exp(-2 * math.pi * lowpass / SR)
        y = np.empty_like(x)
        acc = np.float32(0)
        for i, v in enumerate(x):
            acc = a * acc + (1 - a) * v
            y[i] = acc
        x = y
    return x


def vibe_pad(seconds: float = 14.0, seed: int = 1) -> np.ndarray:
    """Nappe synthwave lente + grain urbain filtré : 'Vice City by night'."""
    tt = t(seconds)
    pad = np.zeros_like(tt)
    for f, amp in ((55, .30), (82.4, .24), (110, .20), (164.8, .12), (220, .08)):
        pad += amp * np.sin(2 * np.pi * f * tt + 0.4 * np.sin(2 * np.pi * 0.07 * tt))
    lfo = 0.75 + 0.25 * np.sin(2 * np.pi * 0.11 * tt)
    city = 0.10 * noise(seconds, seed, lowpass=420)
    shimmer = 0.05 * np.sin(2 * np.pi * 880 * tt) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.23 * tt))
    return pad * lfo + city + shimmer


def nature_pad(seconds: float = 14.0, seed: int = 2) -> np.ndarray:
    """Nappe organique + souffle/insectes : 'Leonida wetlands'."""
    tt = t(seconds)
    wind = 0.28 * noise(seconds, seed, lowpass=260)
    crickets = 0.06 * np.sin(2 * np.pi * 4200 * tt) * (
        np.sin(2 * np.pi * 7.5 * tt) > 0.85).astype(np.float32)
    drone = 0.14 * np.sin(2 * np.pi * 73.4 * tt) + 0.09 * np.sin(2 * np.pi * 146.8 * tt)
    swell = 0.7 + 0.3 * np.sin(2 * np.pi * 0.05 * tt)
    return (wind + drone) * swell + crickets


def ui_blip(f0: float = 900, f1: float = 1500, seconds: float = 0.09) -> np.ndarray:
    return sweep(f0, f1, seconds) * np.exp(-np.linspace(0, 6, int(SR * seconds), dtype=np.float32))


def ui_click() -> np.ndarray:
    n = int(SR * 0.11)
    x = 0.5 * noise(0.11, 7) * np.exp(-np.linspace(0, 22, n, dtype=np.float32))
    x += 0.45 * np.sin(2 * np.pi * 210 * np.arange(n, dtype=np.float32) / SR) * \
         np.exp(-np.linspace(0, 18, n, dtype=np.float32))
    return x


def whoosh(seconds: float = 0.7) -> np.ndarray:
    x = noise(seconds, 11, lowpass=1400)
    env = np.sin(np.pi * np.linspace(0, 1, len(x), dtype=np.float32)) ** 2
    return x * env + 0.25 * sweep(120, 60, seconds) * env


def character_theme(root: float, seconds: float = 10.0, seed: int = 3) -> np.ndarray:
    tt = t(seconds)
    x = np.zeros_like(tt)
    for i, f in enumerate((root, root * 1.5, root * 2, root * 2.5)):
        x += (0.26 / (i + 1)) * np.sin(2 * np.pi * f * tt + i * 0.6)
    pulse = np.sin(2 * np.pi * 0.5 * tt) ** 8
    x += 0.16 * pulse * np.sin(2 * np.pi * root * 4 * tt)
    x *= 0.65 + 0.35 * np.sin(2 * np.pi * 0.08 * tt)
    return x + 0.04 * noise(seconds, seed, lowpass=600)


def metallic_click() -> np.ndarray:
    n = int(SR * 0.24)
    tt = np.arange(n, dtype=np.float32) / SR
    env = np.exp(-np.linspace(0, 16, n, dtype=np.float32))
    return (0.4 * np.sin(2 * np.pi * 1750 * tt) + 0.3 * np.sin(2 * np.pi * 2630 * tt) +
            0.3 * noise(0.24, 13)) * env


def engine_sim(seconds: float = 4.0) -> np.ndarray:
    """Rugissement synthétique : harmoniques d'un V8 stylisé, PAS un enregistrement."""
    tt = t(seconds)
    rpm = 55 + 45 * (1 - np.exp(-tt * 1.4)) + 6 * np.sin(2 * np.pi * 3.2 * tt)
    phase = 2 * np.pi * np.cumsum(rpm) / SR
    x = np.zeros_like(tt)
    for h, a in ((1, .42), (2, .28), (3, .18), (4, .12), (6, .07)):
        x += a * np.sin(h * phase)
    x += 0.16 * noise(seconds, 17, lowpass=900)
    return x * (0.55 + 0.45 * np.minimum(1, tt * 2))


def victory() -> np.ndarray:
    parts = []
    for f, d in ((523.25, .13), (659.25, .13), (783.99, .13), (1046.5, .38)):
        parts.append(tone(f, d) * np.exp(-np.linspace(0, 3.5, int(SR * d), dtype=np.float32)))
    parts.append(np.zeros(int(SR * .02), dtype=np.float32))
    return np.concatenate(parts)


PRESETS = {
    'homepage_ambiance_vicecity_night_01.mp3': lambda: vibe_pad(14, 1),
    'homepage_ui_hover_01.mp3': lambda: ui_blip(900, 1500, .09),
    'homepage_ui_click_01.mp3': ui_click,
    'homepage_ui_transition_01.mp3': lambda: whoosh(.7),
    'characters_jason_theme_01.mp3': lambda: character_theme(65.4, 10, 3),
    'characters_lucia_theme_01.mp3': lambda: character_theme(73.4, 10, 4),
    'map_leonida_ambiance_01.mp3': lambda: nature_pad(14, 2),
    'weapons_equip_sound_01.mp3': metallic_click,
    'vehicles_engine_v8_01.mp3': lambda: engine_sim(4),
    'quiz_correct_answer_01.mp3': victory,
}

DEFAULT_LAYOUT = {
    'homepage_ambiance_vicecity_night_01.mp3': 'ambiances',
    'characters_jason_theme_01.mp3': 'jingles',
    'characters_lucia_theme_01.mp3': 'jingles',
    'map_leonida_ambiance_01.mp3': 'ambiances',
    'vehicles_engine_v8_01.mp3': 'ambiances',
    'quiz_correct_answer_01.mp3': 'ui',
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--outdir', default=None,
                    help='Dossier de sortie unique (sinon répartition assets/audio/{ambiances,ui,jingles})')
    args = ap.parse_args()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print('Génération des 10 MP3 originaux (lot AUD001–AUD010)…')
    for name, factory in PRESETS.items():
        if args.outdir:
            dest = os.path.join(args.outdir, name)
        else:
            sub = DEFAULT_LAYOUT.get(name, 'ui')
            dest = os.path.join(root, 'assets', 'audio', sub, name)
        save_mp3(np.asarray(factory(), dtype=np.float32), dest)
    print('Terminé. 10 fichiers MP3 — 0 sample sous licence.')


if __name__ == '__main__':
    main()
