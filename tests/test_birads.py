"""Cas BI-RADS issus de l'audit (latéralité, inversions, contradictions)."""

import pytest

from dalal_jamm.reports.birads import extract_birads

XF = pytest.mark.xfail(raises=NotImplementedError, reason="Sprint 5 (S5-SA-1)")

# (conclusion normalisée, droite, gauche)
LATERALISED = [
    ("examen mammographique classe acr 4 a droite et acr 2 a gauche.", "4", "2"),
    ("examen mammographique classe acr 5 gauche et acr 2 a droite.", "2", "5"),
    ("examen mammographique classe acr 3 droit ; acr1 gauche.", "3", "1"),
    ("examen classe acr 4a a gauche et acr 1 a droite.", "1", "4A"),
    ("masse du sein droit classee acr 4. examen classe acr 2 a gauche.", "4", "2"),
    # formulations rencontrées dans les vrais rapports : fautes de frappe, côté sans « à », ordre inversé
    ("examen mammographique class acr 1 gauche et acr 3 droit (probable adeno fibrome).", "3", "1"),
    ("examen mammographique classe acr 2 a droit et acr 1 a gauche.", "2", "1"),
]


@XF
@pytest.mark.parametrize("text,right,left", LATERALISED)
def test_lateralised(text, right, left):
    r = extract_birads(text)
    assert (r.right, r.left) == (right, left)
    assert r.contradiction is False


@XF
def test_bilateral():
    r = extract_birads("examen mammographique classe acr 2 bilateral.")
    assert (r.global_, r.right, r.left, r.laterality) == ("2", "2", "2", "bilateral")


@XF
def test_roman_numerals():
    assert extract_birads("en faveur d'un adenofibrome : bi-rads iii.").global_ == "3"


@XF
def test_same_side_two_values_is_contradiction():
    r = extract_birads("acr 2 a droite. par ailleurs acr 3 a droite.")
    assert r.contradiction is True
    assert r.right is None
