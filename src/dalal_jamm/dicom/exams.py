"""Regroupement par examen et complétude (Sprint 1)."""

from __future__ import annotations

import pandas as pd


def group_by_exam(inventory: pd.DataFrame) -> pd.DataFrame:
    """Regroupe les images par examen (StudyInstanceUID).

    Ticket : S1-BA-3
    """
    raise NotImplementedError("S1-BA-3")


def check_completeness(exams: pd.DataFrame) -> pd.DataFrame:
    """Marque chaque examen complet (D-CC, D-MLO, G-CC, G-MLO) ou incomplet, avec les vues manquantes.

    Ticket : S1-BA-3
    """
    raise NotImplementedError("S1-BA-3")
