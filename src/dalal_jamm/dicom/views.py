"""Identification de la vue (CC/MLO) et du côté (D/G) (Sprint 1)."""

from __future__ import annotations


def classify_view(meta: dict) -> tuple[str | None, str | None]:
    """Retourne (côté, vue) à partir de ImageLaterality, ViewPosition, SeriesDescription. Retourne
    (None, None) si non identifiable : ne jamais deviner.

    Ticket : S1-MA-3
    """
    raise NotImplementedError("S1-MA-3")
