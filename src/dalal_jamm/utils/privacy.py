"""Pseudonymisation : exam_id et table de correspondance privée (Sprint 2)."""

from __future__ import annotations

import pandas as pd


def make_exam_id(key: str) -> str:
    """Génère un identifiant d'examen stable et non réversible à partir d'une clé (avec sel secret).

    Ticket : S2-MA-1
    """
    raise NotImplementedError("S2-MA-1")


def build_mapping_table(records: pd.DataFrame) -> pd.DataFrame:
    """Construit la table exam_id <-> identité. À stocker UNIQUEMENT dans data/private/.

    Ticket : S2-MA-1
    """
    raise NotImplementedError("S2-MA-1")
