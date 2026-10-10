"""Identification de la vue (CC/MLO...) et du côté (D/G) d'une image (Sprint 1).

Règle : on ne devine jamais. Une valeur absente, vide ou inconnue donne None.
Les vues non standard (LMO, ML, XCC...) sont CONSERVÉES telles quelles : on ne les assimile
pas à CC ou MLO (décision clinique à valider avec un radiologue).
"""

from __future__ import annotations

import math

SIDES = ("R", "L")
STANDARD_VIEWS = ("CC", "MLO")


def _clean(value) -> str | None:
    """Texte en majuscules sans espaces ; None si absent, vide ou NaN (valeur lue dans un CSV)."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    text = str(value).strip().upper()
    return text or None


def classify_view(meta: dict) -> tuple[str | None, str | None]:
    """Retourne (côté, vue) à partir de ImageLaterality et ViewPosition.

    `meta` accepte les mots-clés DICOM (`ImageLaterality`, `ViewPosition`) ou les noms de colonnes
    de l'inventaire (`image_laterality`, `view_position`).
    côté : 'R' ou 'L', sinon None. vue : valeur lue (ex. 'CC', 'MLO', 'XCC'), sinon None.
    Aucune valeur n'est déduite d'un autre champ (nom de série, dossier...).

    Ticket : S1-MA-3
    """
    side = _clean(meta.get("ImageLaterality", meta.get("image_laterality")))
    view = _clean(meta.get("ViewPosition", meta.get("view_position")))
    return (side if side in SIDES else None), view


def is_standard_view(view: str | None) -> bool:
    """Vrai pour CC et MLO uniquement."""
    return view in STANDARD_VIEWS
