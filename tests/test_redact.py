from dalal_jamm.reports.redact import MASK, mask_patient_names, patient_name_tokens

LINE = "Prénom & Nom \t: Aminata Mbacké EXEMPLE\t\t\t   \t\tDATE : 01.01.26\nAge : 40 ans\n"


def test_name_on_the_name_line_is_masked_and_date_kept():
    out = mask_patient_names(LINE)
    assert "Aminata" not in out and "EXEMPLE" not in out and "Mbacké" not in out
    assert f"Prénom & Nom \t: {MASK} {MASK} {MASK}" in out
    assert "DATE : 01.01.26" in out and "Age : 40 ans" in out


def test_name_is_masked_everywhere_ignoring_case_and_accents():
    text = LINE + "Nom du dossier : MBACKE_AMINATA_EXEMPLE\nMme exemple revient.\n"
    out = mask_patient_names(text)
    assert "MBACKE" not in out and "AMINATA" not in out and "exemple" not in out.lower()


def test_medical_text_is_untouched():
    text = LINE + "Sein droit :\nAbsence de masse suspecte.\nCONCLUSION : ACR 2 bilatéral.\n"
    out = mask_patient_names(text)
    assert "Absence de masse suspecte." in out and "ACR 2 bilatéral" in out


def test_a_name_inside_a_longer_word_is_not_masked():
    text = "Prénom & Nom : Awa DIA\t\tDATE : 01.01.26\nDiagnostic : normal. Diaphragme libre.\n"
    out = mask_patient_names(text)
    assert "Diagnostic" in out and "Diaphragme" in out and "DIA\t" not in out


def test_several_reports_in_one_text_are_all_masked():
    text = (
        "Prénom & Nom : Fatou MODELE\t\tDATE : 01.01.26\nRAS\n"
        "Prénom & Nom : Mariama TEST\t\tDATE : 01.01.26\nRAS\n"
    )
    out = mask_patient_names(text)
    assert all(word not in out for word in ("Fatou", "MODELE", "Mariama", "TEST"))


def test_text_without_a_name_line_is_unchanged():
    text = "Compte rendu sans identité : Sein droit RAS.\n"
    assert mask_patient_names(text) == text


def test_short_words_of_a_name_are_not_used_as_tokens():
    assert patient_name_tokens("Prénom & Nom : Awa DE LA TOUR\t\tDATE : 01.01.26") == {"awa", "tour"}
