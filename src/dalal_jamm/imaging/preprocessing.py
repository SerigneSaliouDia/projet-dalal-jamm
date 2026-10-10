"""Prétraitement des images (Sprint 11)."""

from __future__ import annotations

from pathlib import Path

import numpy as np


def load_pixels(path: Path) -> np.ndarray:
    """DICOM -> tableau (gère MONOCHROME1/2, rescale).

    Ticket : S11-MA-1
    """
    raise NotImplementedError("S11-MA-1")


def preprocess(image: np.ndarray) -> np.ndarray:
    """Normalisation, recadrage du sein, redimensionnement.

    Ticket : S11-MA-1
    """
    raise NotImplementedError("S11-MA-1")
