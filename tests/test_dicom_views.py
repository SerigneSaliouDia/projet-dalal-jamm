import pytest

from dalal_jamm.dicom.views import classify_view

XF = pytest.mark.xfail(raises=NotImplementedError, reason="Sprint 1 (S1-MA-3)")


@XF
def test_known_view():
    meta = {"ImageLaterality": "R", "ViewPosition": "CC", "SeriesDescription": "MAMMOGRAM, Diagnosis"}
    assert classify_view(meta) == ("R", "CC")


@XF
def test_unknown_view_is_not_guessed():
    assert classify_view({}) == (None, None)
