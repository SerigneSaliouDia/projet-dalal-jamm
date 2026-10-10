"""Chemins du projet. Les données ne sont JAMAIS dans le dépôt Git.

Chaque membre définit, selon sa machine, des variables d'environnement (voir .env.example) :
    DALAL_DATA_DIR      dossier racine des données (défaut : ./data)
    DALAL_DICOM_DIR     dossier des images DICOM / IMA (défaut : <DATA>/raw/dicom)
    DALAL_REPORTS_DIR   dossier des comptes rendus DOCX (défaut : <DATA>/raw/reports)
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Paths:
    data: Path
    dicom: Path
    reports: Path
    interim: Path
    processed: Path
    private: Path
    outputs: Path


def get_paths() -> Paths:
    """Lit les variables d'environnement à chaque appel."""
    data = Path(os.environ.get("DALAL_DATA_DIR", REPO_ROOT / "data"))
    return Paths(
        data=data,
        dicom=Path(os.environ.get("DALAL_DICOM_DIR", data / "raw" / "dicom")),
        reports=Path(os.environ.get("DALAL_REPORTS_DIR", data / "raw" / "reports")),
        interim=data / "interim",
        processed=data / "processed",
        private=data / "private",
        outputs=data / "outputs",
    )


def ensure_dirs() -> Paths:
    """Crée les dossiers dérivés (interim, processed, private, outputs) s'ils n'existent pas."""
    p = get_paths()
    for d in (p.interim, p.processed, p.private, p.outputs):
        d.mkdir(parents=True, exist_ok=True)
    return p
