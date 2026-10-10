"""Pipeline complet rapports -> tableau structuré (Sprint 9)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def run_pipeline(reports_dir: Path, out_csv: Path) -> pd.DataFrame:
    """Lit, normalise, découpe, extrait, valide, écrit un CSV versionné.

    Ticket : S9-SA-1
    """
    raise NotImplementedError("S9-SA-1")
