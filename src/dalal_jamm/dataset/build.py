"""Dataset final : une ligne par exam_id (Sprint 9)."""

from __future__ import annotations

import pandas as pd


def build_dataset(reports: pd.DataFrame, exams: pd.DataFrame) -> pd.DataFrame:
    """Colonnes : exam_id, image_right_cc/mlo, image_left_cc/mlo, signes D/G, BI-RADS D/G, conclusion,
    recommandation.

    Ticket : S9-MA-1
    """
    raise NotImplementedError("S9-MA-1")
