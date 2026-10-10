"""Vérifie l'environnement local (S0). N'affiche jamais de noms de fichiers patients.

Usage :  python scripts/check_env.py
"""

from __future__ import annotations

import importlib
import os
import sys

from dalal_jamm.config import get_paths
from dalal_jamm.utils.fs import extended_path

PACKAGES = ["pandas", "numpy", "docx", "pydicom", "yaml", "matplotlib", "sklearn", "pytest"]


def count_files(folder, suffix: str) -> int:
    """Compte les fichiers finissant par `suffix`, y compris ceux aux chemins très longs."""
    if not folder.exists():
        return -1
    total = 0
    for _, _, names in os.walk(extended_path(folder)):
        total += sum(1 for n in names if n.lower().endswith(suffix))
    return total


def main() -> int:
    print(f"Python : {sys.version.split()[0]}")
    ok = True
    for name in PACKAGES:
        try:
            mod = importlib.import_module(name)
            print(f"  OK  {name} {getattr(mod, '__version__', '')}")
        except ImportError:
            print(f"  MANQUANT  {name}")
            ok = False

    p = get_paths()
    print("\nDonnées (comptages uniquement) :")
    targets = [("DICOM/IMA", p.dicom, ".ima"), ("Rapports DOCX", p.reports, ".docx")]
    for label, folder, suffix in targets:
        n = count_files(folder, suffix)
        print(f"  {label:<14}: {'dossier introuvable -> ' + str(folder) if n < 0 else n}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
