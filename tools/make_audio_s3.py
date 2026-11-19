#!/usr/bin/env python3
"""
Génère les 2 MP3 originaux du lot S3 (AUD011–AUD012).

Ce script réutilise les synthèses de `tools/make_audio.py` (NumPy + lameenc) :
aucun sample sous licence, aucune musique officielle Rockstar, aucun WAV.
Les deux pistes sont des ambiances / jingles de fan guide non officiel.

Usage : python3 tools/make_audio_s3.py
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_audio as base  # noqa: E402 — import local volontaire

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sunset_cruise() -> np.ndarray:
    """Nappe plus chaude que la nuit S2 : croisière au coucher de soleil."""
    tt = base.t(12.0)
    pad = np.zeros_like(tt)
    for freq, amp in ((65.41, .24), (98.0, .22), (130.81, .18), (196.0, .12), (261.63, .07)):
        pad += amp * np.sin(2 * np.pi * freq * tt + 0.35 * np.sin(2 * np.pi * .09 * tt))
    lfo = .78 + .22 * np.sin(2 * np.pi * .075 * tt)
    sea = .09 * base.noise(12.0, 31, lowpass=380)
    gull = .025 * np.sin(2 * np.pi * 1450 * tt) * (np.sin(2 * np.pi * .31 * tt) > .94)
    return pad * lfo + sea + gull


def guide_intro() -> np.ndarray:
    """Court jingle d'ouverture : motif héroïque + arpège de validation."""
    motif = base.character_theme(82.41, 4.2, 41)
    arp = np.concatenate([
        base.tone(523.25, .16) * np.exp(-np.linspace(0, 3.2, int(base.SR * .16), dtype=np.float32)),
        base.tone(659.25, .16) * np.exp(-np.linspace(0, 3.2, int(base.SR * .16), dtype=np.float32)),
        base.tone(783.99, .16) * np.exp(-np.linspace(0, 3.2, int(base.SR * .16), dtype=np.float32)),
        base.tone(1046.5, .44) * np.exp(-np.linspace(0, 3.0, int(base.SR * .44), dtype=np.float32)),
        np.zeros(int(base.SR * .05), dtype=np.float32),
    ])
    return np.concatenate([motif[:int(base.SR * 3.4)], arp])


PRESETS = {
    'ambiances/homepage_ambiance_sunset_cruise_01.mp3': sunset_cruise,
    'jingles/homepage_jingle_guide_intro_01.mp3': guide_intro,
}


def main() -> None:
    print('Génération des 2 MP3 originaux S3 (AUD011–AUD012)…')
    for rel, factory in PRESETS.items():
        dest = os.path.join(ROOT, 'assets', 'audio', rel)
        base.save_mp3(np.asarray(factory(), dtype=np.float32), dest)
    print('Terminé. 2 MP3 — 0 sample sous licence, 0 fichier WAV.')


if __name__ == '__main__':
    main()
