import math

import pytest

from dalal_jamm.dicom.views import classify_view, is_standard_view


def test_known_view_with_dicom_keywords():
    meta = {"ImageLaterality": "R", "ViewPosition": "CC", "SeriesDescription": "MAMMOGRAM, Diagnosis"}
    assert classify_view(meta) == ("R", "CC")


def test_known_view_with_inventory_column_names():
    assert classify_view({"image_laterality": "L", "view_position": "MLO"}) == ("L", "MLO")


def test_unknown_view_is_not_guessed():
    assert classify_view({}) == (None, None)


def test_series_description_is_never_used_to_guess():
    assert classify_view({"SeriesDescription": "MAMMOGRAM RIGHT CC"}) == (None, None)


@pytest.mark.parametrize("value", ["", "  ", None, math.nan])
def test_empty_or_nan_is_missing(value):
    assert classify_view({"image_laterality": value, "view_position": value}) == (None, None)


def test_case_and_spaces_are_normalised():
    assert classify_view({"ImageLaterality": " r ", "ViewPosition": "mlo"}) == ("R", "MLO")


def test_unknown_side_gives_none_but_view_is_kept():
    assert classify_view({"ImageLaterality": "B", "ViewPosition": "CC"}) == (None, "CC")


@pytest.mark.parametrize("view", ["LMO", "ML", "XCC"])
def test_non_standard_views_are_kept_not_mapped(view):
    side, v = classify_view({"ImageLaterality": "L", "ViewPosition": view})
    assert (side, v) == ("L", view) and not is_standard_view(v)


def test_standard_views():
    assert is_standard_view("CC") and is_standard_view("MLO") and not is_standard_view(None)
