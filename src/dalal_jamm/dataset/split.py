"""Découpage train/validation/test PAR PATIENTE (Sprint 11)."""

from __future__ import annotations

import pandas as pd


def split_by_patient(df: pd.DataFrame, seed: int) -> pd.DataFrame:
    """Aucune patiente ne doit apparaître dans deux jeux. Découpage fixé et sauvegardé.

    Ticket : S11-SA-1
    """
    raise NotImplementedError("S11-SA-1")
