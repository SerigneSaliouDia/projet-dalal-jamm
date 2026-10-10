import pytest

from dalal_jamm.reports.sections import split_sections

XF = pytest.mark.xfail(raises=NotImplementedError, reason="Sprint 4 (S4-MA-1)")

NORMAL = (
    "sein droit : presence d'une masse spiculee. "
    "sein gauche : pas de masse. "
    "complement echographique : formation hypoechogene. "
    "conclusion : acr 4 a droite et acr 1 a gauche."
)
INVERSE = (
    "sein gauche : pas de masse. "
    "sein droit : presence d'une masse spiculee. "
    "conclusion : acr 4 a droite et acr 1 a gauche."
)


@XF
def test_normal_order():
    s = split_sections(NORMAL)
    assert "masse spiculee" in s["sein_droit"] and "masse spiculee" not in s["sein_gauche"]
    assert s["conclusion"].startswith("acr 4") or "acr 4" in s["conclusion"]


@XF
def test_inverse_order_gives_same_sections():
    s = split_sections(INVERSE)
    assert "masse spiculee" in s["sein_droit"]
    assert "masse spiculee" not in s["sein_gauche"]
