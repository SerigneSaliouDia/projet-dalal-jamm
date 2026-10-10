"""Découpage d'un compte rendu en sections (Sprint 4).

Clés attendues : 'entete', 'densite', 'sein_droit', 'sein_gauche', 'echo', 'conclusion'.
Le découpage repose sur la POSITION des en-têtes, pas sur leur ordre : un rapport où
« Sein gauche » précède « Sein droit » doit donner les mêmes sections.
"""

from __future__ import annotations

SECTION_KEYS = ("entete", "densite", "sein_droit", "sein_gauche", "echo", "conclusion")


def split_sections(text_norm: str) -> dict[str, str]:
    """Retourne un dict {clé: texte}. Section absente -> chaîne vide.

    Ticket : S4-MA-1
    """
    raise NotImplementedError("S4-MA-1")


def split_multiple_reports(text_norm: str) -> list[str]:
    """Si un fichier contient plusieurs comptes rendus, retourne un texte par compte rendu.

    Ticket : S4-MA-2
    """
    raise NotImplementedError("S4-MA-2")
