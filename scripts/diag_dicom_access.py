"""Diagnostic d'accès aux DICOM : fichiers illisibles, chemins longs, dossiers vides.

À lancer APRÈS scripts/run_inventory.py. N'affiche que des comptages.
Usage :  python scripts/diag_dicom_access.py
"""

from __future__ import annotations

import os

import pandas as pd

from dalal_jamm.config import get_paths
from dalal_jamm.utils.fs import extended_path


def count_files_below(folder: str) -> int:
    return sum(len(files) for _, _, files in os.walk(folder))


def main() -> None:
    p = get_paths()
    df = pd.read_csv(p.interim / "dicom_files.csv")
    unreadable = df["size_bytes"].isna()
    long_path = df["path_len"] >= 260

    print(f"Fichiers listés                         : {len(df)}")
    print(f"  taille illisible                      : {int(unreadable.sum())}")
    print(f"  chemin de 260 caractères ou plus      : {int(long_path.sum())}")
    print(f"  illisibles ET chemin >= 260           : {int((unreadable & long_path).sum())}")
    if unreadable.any():
        sub = df.loc[unreadable, "path_len"]
        print(f"  longueur des chemins illisibles       : min {sub.min()} / max {sub.max()}")
    lengths = df["path_len"]
    print(f"  longueur max / médiane de tous        : {lengths.max()} / {int(lengths.median())}")

    root = extended_path(p.dicom)
    n1 = n2 = empty1 = empty2 = access_errors = 0
    for d1 in os.scandir(root):
        if not d1.is_dir():
            continue
        n1 += 1
        total1 = 0
        try:
            level2 = [d for d in os.scandir(d1.path) if d.is_dir()]
        except OSError:
            access_errors += 1
            continue
        for d2 in level2:
            n2 += 1
            c = count_files_below(d2.path)
            total1 += c
            empty2 += c == 0
        empty1 += total1 == 0
    print(f"\nDossiers de 1er niveau : {n1} dont sans aucun fichier : {empty1}")
    print(f"Dossiers de 2e niveau  : {n2} dont sans aucun fichier : {empty2}")
    print(f"Dossiers inaccessibles : {access_errors}")


if __name__ == "__main__":
    main()
