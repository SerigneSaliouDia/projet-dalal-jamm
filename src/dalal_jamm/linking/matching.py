"""Association rapports <-> examens (Sprint 3)."""

from __future__ import annotations

import pandas as pd


def normalize_name(name: str) -> str:
    """Normalise un nom (accents, casse, ordre prénom/nom).

    Ticket : S3-MA-1
    """
    raise NotImplementedError("S3-MA-1")


def match_reports_to_exams(reports: pd.DataFrame, exams: pd.DataFrame) -> pd.DataFrame:
    """Correspondance exacte puis approchée. Une association non démontrée reste NON associée.

    Ticket : S3-MA-1
    """
    raise NotImplementedError("S3-MA-1")
