"""Extraction BI-RADS / ACR avec latéralité (Sprint 5).

Règles du projet :
- conserver droite / gauche quand le rapport les précise ;
- plusieurs valeurs différentes pour le MÊME côté = contradiction (jamais de valeur choisie en silence) ;
- ne jamais recopier une valeur sur l'autre côté sans que le rapport le dise (« bilatéral »).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BiradsResult:
    global_: str | None = None   # valeur unique valable pour les deux seins
    right: str | None = None     # '1'..'6', '4A', '4B', '4C'
    left: str | None = None
    laterality: str | None = None  # 'bilateral', 'asymetrique', 'droite', 'gauche', None
    contradiction: bool = False
    note: str | None = None


def extract_birads(conclusion_norm: str) -> BiradsResult:
    """Entrée : conclusion normalisée (minuscules, sans accents).

    Ticket : S5-SA-1
    """
    raise NotImplementedError("S5-SA-1")
