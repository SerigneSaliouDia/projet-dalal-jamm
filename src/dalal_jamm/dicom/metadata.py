"""Lecture des en-têtes DICOM, sans charger les pixels (Sprint 1)."""

from __future__ import annotations

from pathlib import Path


def read_header(path: Path) -> dict:
    """Lit l'en-tête (stop_before_pixels). Retourne Laterality, ViewPosition, SeriesDescription,
    StudyInstanceUID, SeriesInstanceUID, StudyDate, Rows, Columns, TransferSyntax... Ne lève pas
    d'exception : retourne {'error': motif} si illisible.

    Ticket : S1-MA-1
    """
    raise NotImplementedError("S1-MA-1")
