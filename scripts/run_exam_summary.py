"""Complétude des séries et des examens, à partir de data/interim/dicom_inventory.csv.

À lancer APRÈS scripts/run_header_inventory.py. N'affiche que des COMPTAGES.
Écrit dans data/interim/ (hors Git) : dicom_series.csv (1 ligne par série), dicom_exams.csv (1 par examen).
Usage :  python scripts/run_exam_summary.py
"""

from __future__ import annotations

import pandas as pd

from dalal_jamm.config import get_paths
from dalal_jamm.dicom.exams import (
    INTENT_PRESENTATION,
    INTENT_PROCESSING,
    check_completeness,
    group_by_exam,
    summarize_exams,
)


def n_true(s: pd.Series) -> int:
    """Nombre de valeurs vraies (les valeurs vides comptent comme faux)."""
    return int(s.fillna(False).astype(bool).sum())


def report_series(series: pd.DataFrame, intent: str, label: str) -> None:
    s = series[series["presentation_intent"] == intent]
    inc = s[~s["complete"]]
    counts = inc["missing"].astype(str).str.count(";").add(1) if len(inc) else pd.Series(dtype=int)
    n_missing = counts.value_counts().sort_index().to_dict()
    print(f"\n== Séries {label} : {len(s)} ==")
    print(f"Complètes (>= 1 image pour D-CC, D-MLO, G-CC, G-MLO) : {n_true(s['complete'])}")
    print(f"  dont exactement 4 images, rien d'autre : {n_true(s['exact'])}")
    print(f"  dont avec répétition d'une vue         : {n_true(s['complete'] & s['has_repeats'])}")
    print(f"Incomplètes : {len(inc)}")
    print(f"  nombre de vues manquantes -> séries : {n_missing}")
    print(f"  vues manquantes (top 8) : {inc['missing'].value_counts().head(8).to_dict()}")
    print(f"Séries avec une vue non standard (LMO, ML, XCC...) : {int((s['n_other'] > 0).sum())}")
    print(f"Images sans côté ou sans vue : {int(s['n_unclassified'].sum())}")
    sizes = s["n_images"].value_counts().sort_index().to_dict()
    print(f"Images par série (nb images -> nb séries) : {sizes}")


def main() -> None:
    p = get_paths()
    inv = pd.read_csv(p.interim / "dicom_inventory.csv", dtype=str)
    series = check_completeness(group_by_exam(inv))
    exams = summarize_exams(series)
    series.to_csv(p.interim / "dicom_series.csv", index=False)
    exams.to_csv(p.interim / "dicom_exams.csv", index=False)

    print(f"Fichiers écartés (illisibles ou sans UID) : {series.attrs['dropped_rows']}")
    print(f"Séries : {len(series)} | examens : {len(exams)}")
    if series.empty:
        raise SystemExit("Aucune série exploitable : vérifiez dicom_inventory.csv (study_uid, series_uid).")
    report_series(series, INTENT_PRESENTATION, "TRAITÉES (FOR PRESENTATION)")
    report_series(series, INTENT_PROCESSING, "BRUTES (FOR PROCESSING)")

    pres, proc = exams["complete_presentation"], exams["complete_processing"]
    both = exams.dropna(subset=["n_presentation", "n_processing"])
    diff = both[both["n_presentation"] != both["n_processing"]]
    print("\n== Examens ==")
    print(f"Série traitée complète : {n_true(pres)}")
    print(f"Série brute complète   : {n_true(proc)}")
    print(f"Les deux complètes     : {n_true(pres & proc)}")
    print(f"Sans série traitée : {int(pres.isna().sum())} | sans série brute : {int(proc.isna().sum())}")
    print(f"Examens avec les deux séries et un nombre d'images différent : {len(diff)} / {len(both)}")
    print(f"Examens avec au moins une vue non standard : {int((exams['n_other_views'] > 0).sum())}")
    print("\nTables écrites dans data/interim/ (contiennent des UID : ne JAMAIS les committer)")


if __name__ == "__main__":
    main()
