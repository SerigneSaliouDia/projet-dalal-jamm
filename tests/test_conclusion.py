import pytest

from dalal_jamm.reports.conclusion import extract_conclusion

XF = pytest.mark.xfail(raises=NotImplementedError, reason="Sprint 7 (S7-MA-1)")

TEXT = (
    "CONCLUSION :\nFormation isoéchogène hétérogène avec des calcifications mesurant 15 x 11 mm "
    "en faveur d'un adénofibrome : BI-RADS III.\nSurveillance dans 06 mois."
)


@XF
def test_conclusion_keeps_original_text():
    conclusion, _ = extract_conclusion(TEXT)
    assert "adénofibrome" in conclusion      # accents conservés
    assert "BI-RADS III" in conclusion       # casse conservée


@XF
def test_recommendation_extracted_without_destroying_conclusion():
    conclusion, reco = extract_conclusion(TEXT)
    assert reco == "Surveillance dans 06 mois"
    assert "Surveillance dans 06 mois" in conclusion


@XF
def test_multiple_recommendations_are_kept():
    text = "CONCLUSION : Nodule ACR 3. Surveillance dans 06 mois. Intérêt d'une biopsie si augmentation."
    _, reco = extract_conclusion(text)
    assert "Surveillance dans 06 mois" in reco and "biopsie" in reco
