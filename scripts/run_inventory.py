"""Inventaire des fichiers du dossier DICOM : écrit data/interim/dicom_files.csv (hors Git).

N'affiche que des comptages. Usage :  python scripts/run_inventory.py
"""

from __future__ import annotations

from collections import Counter

from dalal_jamm.config import ensure_dirs
from dalal_jamm.dicom.inventory import scan_files


def main() -> None:
    paths = ensure_dirs()
    df = scan_files(paths.dicom)
    out = paths.interim / "dicom_files.csv"
    df.to_csv(out, index=False, encoding="utf-8")

    exams = df.dropna(subset=["exam_folder"]).groupby(["patient_idx", "exam_folder"]).size()
    keys = ["patient_idx", "exam_folder", "series_folder"]
    series = df.dropna(subset=["series_folder"]).groupby(keys).size()

    print(f"Fichiers : {len(df)} | erreurs de parcours : {df.attrs['walk_errors']}")
    print(f"Fichiers à taille illisible : {int(df['size_bytes'].isna().sum())}")
    print("Extensions :", df["ext"].value_counts().to_dict())
    print("Profondeur :", df["depth"].value_counts().to_dict())
    print(f"Patientes (dossiers 1er niveau) : {df['patient_idx'].nunique()}")
    print(f"Examens (dossiers 2e niveau)    : {len(exams)}")
    print(f"Séries (dossiers 3e niveau)     : {len(series)}")
    print("Fichiers par examen  (nb fichiers -> nb examens) :", dict(sorted(Counter(exams).items())))
    print("Fichiers par série   (nb fichiers -> nb séries)  :", dict(sorted(Counter(series).items())))
    print("Noms de séries (top 10) :", df["series_folder"].value_counts().head(10).to_dict())
    print("Longueur max d'un chemin :", int(df["path_len"].max()))
    print(f"\nTable écrite dans : {out}  (contient des noms : ne JAMAIS la committer)")


if __name__ == "__main__":
    main()
