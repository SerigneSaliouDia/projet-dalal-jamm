import pandas as pd

from dalal_jamm.dicom.exams import check_completeness, group_by_exam, summarize_exams

PRES, PROC = "FOR PRESENTATION", "FOR PROCESSING"


def rows(study, series, intent, views, status="ok"):
    return [
        {"status": status, "study_uid": study, "series_uid": series, "patient_idx": 0,
         "series_folder": f"folder_{series}", "presentation_intent": intent,
         "image_laterality": lat, "view_position": view}
        for lat, view in views
    ]


FOUR = [("R", "CC"), ("R", "MLO"), ("L", "CC"), ("L", "MLO")]


def build(*groups):
    return pd.DataFrame([r for g in groups for r in g])


def get(df, series):
    return df[df["series_uid"] == series].iloc[0]


def test_complete_exact_series():
    s = check_completeness(group_by_exam(build(rows("E1", "S1", PRES, FOUR))))
    r = get(s, "S1")
    assert r["complete"] and r["exact"] and not r["has_repeats"] and r["missing"] == ""
    assert r["n_images"] == 4


def test_repeat_keeps_series_complete_but_not_exact():
    r = get(check_completeness(group_by_exam(build(rows("E1", "S1", PRES, FOUR + [("R", "CC")])))), "S1")
    assert r["complete"] and r["has_repeats"] and not r["exact"] and r["n_R_CC"] == 2


def test_missing_view_is_listed():
    r = get(check_completeness(group_by_exam(build(rows("E1", "S1", PRES, FOUR[:3])))), "S1")
    assert not r["complete"] and r["missing"] == "L-MLO"


def test_unilateral_exam_misses_two_views():
    r = get(check_completeness(group_by_exam(build(rows("E1", "S1", PRES, FOUR[:2])))), "S1")
    assert not r["complete"] and r["missing"] == "L-CC;L-MLO"


def test_non_standard_view_does_not_replace_a_standard_one():
    r = get(check_completeness(group_by_exam(build(rows("E1", "S1", PRES, FOUR[:3] + [("L", "XCC")])))), "S1")
    assert not r["complete"] and r["n_other"] == 1 and r["missing"] == "L-MLO"


def test_missing_laterality_is_unclassified_not_guessed():
    r = get(group_by_exam(build(rows("E1", "S1", PRES, FOUR + [(None, "CC")]))), "S1")
    assert r["n_unclassified"] == 1 and r["n_R_CC"] == 1


def test_unreadable_files_are_dropped_and_counted():
    inv = build(rows("E1", "S1", PRES, FOUR), rows(None, None, None, [(None, None)], status="error"))
    out = group_by_exam(inv)
    assert len(out) == 1 and out.attrs["dropped_rows"] == 1


def test_exam_summary_distinguishes_missing_series_from_incomplete():
    inv = build(
        rows("E1", "S1", PRES, FOUR), rows("E1", "S2", PROC, FOUR[:3]),
        rows("E2", "S3", PRES, FOUR),  # examen sans série brute
    )
    ex = summarize_exams(check_completeness(group_by_exam(inv))).set_index("study_uid")
    assert bool(ex.loc["E1", "complete_presentation"]) is True
    assert bool(ex.loc["E1", "complete_processing"]) is False
    assert pd.isna(ex.loc["E2", "complete_processing"])
