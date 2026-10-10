"""Lit l'en-tête de TOUS les fichiers DICOM et écrit data/interim/dicom_inventory.csv (hors Git).

N'affiche que des COMPTAGES : aucun nom, aucun identifiant, aucun chemin.
Usage :  python scripts/run_header_inventory.py
"""

from __future__ import annotations

import pandas as pd

from dalal_jamm.config import ensure_dirs
from dalal_jamm.dicom.inventory import build_inventory, scan_files


def counts(series: pd.Series, top: int | None = None) -> dict:
    vc = series.fillna("(vide)").value_counts()
    return (vc.head(top) if top else vc).to_dict()


def main() -> None:
    paths = ensure_dirs()
    files = scan_files(paths.dicom)
    print(f"Lecture de {len(files)} en-têtes...")
    df = build_inventory(paths.dicom, files)
    out = paths.interim / "dicom_inventory.csv"
    df.to_csv(out, index=False, encoding="utf-8")

    ok = df[df["status"] != "error"]
    print(f"\n== Lecture ==\nStatut : {counts(df['status'])}")
    print(f"Erreurs (classes d'exception) : {counts(df.loc[df['status'] == 'error', 'error'])}")
    print(f"Syntaxes de transfert : {counts(ok['transfer_syntax'])}")

    print("\n== Contenu ==")
    print(f"Modalité : {counts(ok['modality'])}")
    print(f"Fabricant / modèle : {counts(ok['manufacturer'])} / {counts(ok['model'])}")
    print(f"Description de série (top 10) : {counts(ok['series_description'], 10)}")
    print(f"Intention de présentation par dossier de série :\n"
          f"{pd.crosstab(ok['series_folder'], ok['presentation_intent'].fillna('(vide)')).to_string()}")
    print(f"Type d'image (top 6) : {counts(ok['image_type'], 6)}")
    size = (ok["rows"].astype(str) + " x " + ok["columns"].astype(str)).where(ok["rows"].notna())
    print(f"Dimensions lignes x colonnes (top 6) : {counts(size, 6)}")
    print(f"Nombre de frames : {counts(ok['number_of_frames'])}")

    print("\n== Côté et vue, par dossier de série ==")
    table = pd.crosstab(
        [ok["series_folder"].fillna("(vide)"), ok["image_laterality"].fillna("(vide)")],
        ok["view_position"].fillna("(vide)"),
    )
    print(table.to_string())
    both = ok.dropna(subset=["image_laterality", "laterality"])
    print(f"ImageLaterality et Laterality toutes deux présentes : {len(both)} "
          f"dont différentes : {int((both['image_laterality'] != both['laterality']).sum())}")
    print(f"Signification du code de vue (top 6) : {counts(ok['view_code_meaning'], 6)}")

    print("\n== Identifiants (comptages uniquement) ==")
    for col in ("ident_patient_name", "ident_patient_id", "ident_accession", "study_date", "study_uid"):
        print(f"Vides pour {col} : {int(ok[col].isna().sum())} / {len(ok)}")
    print(f"UID d'étude distincts : {ok['study_uid'].nunique()} | de série : {ok['series_uid'].nunique()}"
          f" | d'image : {ok['sop_uid'].nunique()}")
    print(f"Images en double (même SOPInstanceUID) : {int(ok['sop_uid'].dropna().duplicated().sum())}")
    exam = ok.groupby(["patient_idx", "exam_folder"])["study_uid"].nunique()
    print(f"Dossiers d'examen contenant plusieurs UID d'étude : {int((exam > 1).sum())} / {len(exam)}")
    spread = ok.dropna(subset=["study_uid"]).groupby("study_uid")[["patient_idx", "exam_folder"]].apply(
        lambda g: len(g.drop_duplicates()))
    n_spread = int((spread > 1).sum())
    print(f"UID d'étude répartis dans plusieurs dossiers d'examen : {n_spread} / {len(spread)}")
    pat = ok.groupby("patient_idx")["ident_patient_id"].nunique()
    print(f"Dossiers patientes contenant plusieurs numéros patient : {int((pat > 1).sum())} / {len(pat)}")
    dates = ok["study_date"].dropna()
    if len(dates):
        print(f"Date d'étude : de {dates.min()} à {dates.max()}")

    print(f"\nTable écrite dans : {out}  (contient des NOMS et des IDENTIFIANTS : ne JAMAIS la committer)")


if __name__ == "__main__":
    main()
