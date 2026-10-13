"""Banc de tests de la négation. Cas issus de l'audit du notebook initial.

Quand vous implémentez `extract_sign_state`, retirez le marqueur xfail.
États : 1 = présent, 0 = absence explicitement écrite, None = non mentionné.
"""

import pytest

from dalal_jamm.reports.negation import extract_sign_state

XF = pytest.mark.xfail(raises=NotImplementedError, reason="Sprint 6 (S6-SA-1)")

CASES = [
    ("absence d'asymetrie de densite", ["asymetrie"], 0),
    ("pas d'asymetrie de densite", ["asymetrie"], 0),
    ("sans asymetrie", ["asymetrie"], 0),
    ("asymetrie focale de densite", ["asymetrie"], 1),
    ("presence d'une asymetrie de densite", ["asymetrie"], 1),
    ("asymetrie de densite predominant en retro areolaire", ["asymetrie"], 1),
    ("mise en evidence d'une asymetrie focale de densite", ["asymetrie"], 1),
    # négation en liste (faux positif de l'ancien notebook)
    ("pas de masse, de distorsion architecturale ou d'asymetrie de densite", ["asymetrie"], 0),
    ("pas de masse, de distorsion architecturale ou d'asymetrie de densite", ["masse"], 0),
    # présence + négation dans la même phrase (faux négatifs de l'ancien notebook)
    ("presence d'une masse spiculee associee a des microcalcifications, "
     "sans distorsion architecturale", ["masse"], 1),
    ("presence d'une masse spiculee associee a des microcalcifications, "
     "sans distorsion architecturale", ["calcification"], 1),
    ("presence d'une masse spiculee associee a des microcalcifications, "
     "sans distorsion architecturale", ["distorsion"], 0),
    # négation QUALIFIÉE : « absence de masse suspecte » n'exclut pas toute masse (rapports réels, S2)
    ("absence de masse suspecte", ["masse"], None),
    ("absence de masse evidente", ["masse"], None),
    # « absence de calcifications vasculaires » n'exclut pas les autres calcifications
    ("absence de calcifications vasculaires", ["calcification"], None),
    # non mentionné
    ("aspect normal du revetement cutane et du mamelon", ["masse"], None),
]


@XF
@pytest.mark.parametrize("text,terms,expected", CASES)
def test_sign_state(text, terms, expected):
    assert extract_sign_state(text, terms) == expected
