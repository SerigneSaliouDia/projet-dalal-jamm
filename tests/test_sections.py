from pathlib import Path

import pytest

from dalal_jamm.reports.sections import (
    is_mammography,
    report_title,
    split_multiple_reports,
    split_sections,
)

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



# ---- Découpage des fichiers à plusieurs comptes rendus (implémenté) ----

FIXTURE = Path(__file__).parent / "fixtures" / "fichier_multi_rapports_fictif.txt"


def non_empty(text):
    return [line for line in text.splitlines() if line.strip()]


def test_one_file_can_contain_several_reports_of_several_patients():
    """Structure observée dans un vrai fichier : 3 mammographies + 1 autre examen, patientes différentes."""
    blocks = split_multiple_reports(FIXTURE.read_text(encoding="utf-8"))
    assert len(blocks) == 4
    assert all("Prénom & Nom" in b for b in blocks)
    assert [is_mammography(b) for b in blocks] == [True, True, True, False]


def test_split_loses_no_line_and_changes_none():
    text = FIXTURE.read_text(encoding="utf-8")
    assert non_empty("\n".join(split_multiple_reports(text))) == non_empty(text)


def test_each_block_starts_with_its_own_title_not_the_previous_signature():
    blocks = split_multiple_reports(FIXTURE.read_text(encoding="utf-8"))
    assert [b.splitlines()[0] for b in blocks[:3]] == ["MAMMOGRAPHIE BILATERALE"] * 3
    assert not blocks[3].lstrip().lower().startswith(("dr", "radiologue"))
    assert blocks[3].lstrip().startswith("Prénom & Nom")  # pas de titre pour ce compte rendu
    assert report_title(blocks[0]) == "MAMMOGRAPHIE BILATERALE" and report_title(blocks[3]) is None


def test_original_text_is_kept_in_blocks():
    blocks = split_multiple_reports(FIXTURE.read_text(encoding="utf-8"))
    assert "Présence d’une opacité ovalaire" in blocks[0]  # accents et apostrophe typographique conservés


def test_single_report_gives_one_block():
    text = "MAMMOGRAPHIE\nPrénom & Nom \t: Test UN\tDATE : 01.01.26\nCONCLUSION :\nACR 1.\n"
    assert len(split_multiple_reports(text)) == 1


def test_file_without_name_field_is_returned_whole_for_review():
    assert split_multiple_reports("texte sans identité\nCONCLUSION : ACR 2") == ["texte sans identité\nCONCLUSION : ACR 2"]


def test_empty_text_gives_no_block():
    assert split_multiple_reports("") == [] and split_multiple_reports("\n  \n") == []


def test_typo_in_title_is_still_a_mammography():
    block = "AMAMMOGRAPHIE BILATERALE\nPrénom & Nom : Test UN DATE : 01.01.26\nSein droit :\nRAS"
    assert is_mammography(block)


def test_other_exam_title_is_not_a_mammography():
    block = "Compte rendu échographie abdominale\nPrénom & Nom : Test UN DATE : 01.01.26\nFoie normal."
    assert report_title(block) == "Compte rendu échographie abdominale" and not is_mammography(block)


def test_conclusion_line_is_not_mistaken_for_a_title():
    text = (
        "MAMMOGRAPHIE\nPrénom & Nom : A UN\nCONCLUSION :\nACR 1.\n"
        "Résultat : normal\n"
        "Prénom & Nom : B DEUX\nCONCLUSION :\nACR 2.\n"
    )
    blocks = split_multiple_reports(text)
    assert len(blocks) == 2
    assert "Résultat : normal" in blocks[0]  # contient un « : » : ce n'est pas un titre
    assert blocks[1].startswith("Prénom & Nom : B DEUX")
