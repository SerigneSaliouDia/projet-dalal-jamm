"""Regroupement par examen et complétude (Sprint 1).

Un examen est identifié par son StudyInstanceUID (vérifié : 1 dossier d'examen = 1 UID).
Un examen contient 2 séries : images brutes (FOR PROCESSING) et traitées (FOR PRESENTATION).
La complétude se juge PAR SÉRIE : au moins une image pour chacune des 4 vues D-CC, D-MLO, G-CC, G-MLO.
Les répétitions et les vues non standard ne rendent pas un examen incomplet : elles sont comptées à part.
"""

from __future__ import annotations

import pandas as pd

from dalal_jamm.dicom.views import classify_view, is_standard_view

FOUR_VIEWS = ["n_R_CC", "n_R_MLO", "n_L_CC", "n_L_MLO"]
SERIES_KEYS = ["study_uid", "series_uid"]
INTENT_PRESENTATION = "FOR PRESENTATION"
INTENT_PROCESSING = "FOR PROCESSING"


def _combo(side: str | None, view: str | None) -> str:
    if side is None or view is None:
        return "unclassified"
    return f"{side}-{view}" if is_standard_view(view) else "other"


def group_by_exam(inventory: pd.DataFrame) -> pd.DataFrame:
    """1 ligne par SÉRIE d'un examen, avec le nombre d'images par vue.

    Colonnes : study_uid, series_uid, patient_idx, series_folder, presentation_intent, n_images,
    n_R_CC, n_R_MLO, n_L_CC, n_L_MLO, n_other (vue non standard), n_unclassified (côté ou vue absent).
    Les fichiers illisibles ou sans study_uid sont écartés : leur nombre est dans `attrs["dropped_rows"]`.

    Ticket : S1-BA-3
    """
    usable = (
        inventory["status"].ne("error") & inventory["study_uid"].notna() & inventory["series_uid"].notna()
    )
    df = inventory[usable].copy()
    combos = []
    for lat, view in zip(df["image_laterality"], df["view_position"]):
        combos.append(_combo(*classify_view({"image_laterality": lat, "view_position": view})))
    df["combo"] = combos

    columns = ["R-CC", "R-MLO", "L-CC", "L-MLO", "other", "unclassified"]
    counts = df.groupby(SERIES_KEYS)["combo"].value_counts().unstack(fill_value=0)
    counts = counts.reindex(columns=columns, fill_value=0)
    counts.columns = ["n_" + c.replace("-", "_") for c in columns]
    info = df.groupby(SERIES_KEYS)[["patient_idx", "series_folder", "presentation_intent"]].first()
    out = info.join(counts)
    out.insert(len(info.columns), "n_images", counts.sum(axis=1))
    out = out.reset_index()
    out.attrs["dropped_rows"] = int((~usable).sum())
    return out


def check_completeness(series: pd.DataFrame) -> pd.DataFrame:
    """Ajoute à chaque série : complete, exact (4 images exactement, rien d'autre), has_repeats, missing.

    Ticket : S1-BA-3
    """
    out = series.copy()
    four = out[FOUR_VIEWS]
    out["complete"] = (four >= 1).all(axis=1)
    out["exact"] = (four == 1).all(axis=1) & (out["n_other"] == 0) & (out["n_unclassified"] == 0)
    out["has_repeats"] = (four > 1).any(axis=1)
    out["missing"] = four.apply(
        lambda r: ";".join(c[2:].replace("_", "-") for c in FOUR_VIEWS if r[c] == 0), axis=1
    )
    return out


def summarize_exams(series_checked: pd.DataFrame) -> pd.DataFrame:
    """1 ligne par examen : complétude de la série traitée et de la série brute.

    Une valeur vide (NA) signifie que l'examen n'a PAS de série de ce type.
    """
    def per_intent(intent: str, name: str) -> pd.DataFrame:
        sub = series_checked[series_checked["presentation_intent"] == intent]
        g = sub.groupby("study_uid")
        return pd.DataFrame({f"complete_{name}": g["complete"].all(), f"n_{name}": g["n_images"].sum()})

    exams = pd.DataFrame(index=pd.Index(series_checked["study_uid"].unique(), name="study_uid"))
    exams = exams.join(per_intent(INTENT_PRESENTATION, "presentation"))
    exams = exams.join(per_intent(INTENT_PROCESSING, "processing"))
    for col in ("complete_presentation", "complete_processing"):
        exams[col] = exams[col].astype("boolean")
    other = series_checked.groupby("study_uid")["n_other"].sum()
    exams["n_other_views"] = other
    return exams.reset_index()
