import pytest

from dalal_jamm.reports.density import extract_density

XF = pytest.mark.xfail(raises=NotImplementedError, reason="Sprint 5 (S5-MA-2)")


@XF
@pytest.mark.parametrize("section,expected", [
    ("densite mammaire de type c selon birads.", "C"),
    ("densite mammaire de type a selon birads.", "A"),
    ("aspect normal du revetement cutane.", None),
])
def test_density_per_side(section, expected):
    assert extract_density(section) == expected
