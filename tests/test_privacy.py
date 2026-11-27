"""Tests de privacy.py : stabilité, non-réversibilité, isolation dans private/."""

import pandas as pd

from dalal_jamm.utils.privacy import (
    build_mapping_table,
    load_or_create_salt,
    make_exam_id,
    save_mapping,
)


def test_same_key_gives_same_id():
    """Stabilité : même clé + même sel = même exam_id à chaque appel."""
    salt = "test_salt_abc"
    assert make_exam_id("STUDY_123", salt) == make_exam_id("STUDY_123", salt)


def test_different_keys_give_different_ids():
    """Deux clés différentes ne produisent pas le même ID."""
    salt = "test_salt_abc"
    assert make_exam_id("STUDY_A", salt) != make_exam_id("STUDY_B", salt)


def test_different_salts_give_different_ids():
    """Le sel change le résultat : sans le bon sel, impossible de recalculer."""
    assert make_exam_id("STUDY_123", "sel_1") != make_exam_id("STUDY_123", "sel_2")


def test_exam_id_format():
    """L'ID commence par EX- et fait 15 caractères (3 + 12)."""
    eid = make_exam_id("STUDY_123", "sel")
    assert eid.startswith("EX-")
    assert len(eid) == 15


def test_key_not_visible_in_exam_id():
    """Non-réversibilité : la clé d'origine n'apparaît pas dans l'exam_id."""
    key = "NOM_PATIENT_SECRET"
    eid = make_exam_id(key, "sel")
    assert key not in eid
    assert key.lower() not in eid.lower()


def test_salt_not_visible_in_exam_id():
    """Le sel n'apparaît pas non plus dans l'ID."""
    salt = "mon_sel_secret"
    eid = make_exam_id("KEY", salt)
    assert salt not in eid


def test_load_or_create_salt_creates_file(tmp_path):
    """Le sel est créé automatiquement s'il n'existe pas."""
    private = tmp_path / "private"
    salt = load_or_create_salt(private)
    assert len(salt) == 32
    assert (private / "salt.txt").exists()


def test_load_or_create_salt_is_stable(tmp_path):
    """Deux appels renvoient le même sel (il est lu depuis le fichier)."""
    private = tmp_path / "private"
    salt1 = load_or_create_salt(private)
    salt2 = load_or_create_salt(private)
    assert salt1 == salt2


def test_build_mapping_table():
    """La table contient exam_id et les colonnes d'identité, dédupliquée."""
    records = pd.DataFrame({
        "study_uid": ["S1", "S1", "S2"],
        "ident_patient_name": ["Alice", "Alice", "Bob"],
        "ident_patient_id": ["P1", "P1", "P2"],
        "image_laterality": ["R", "L", "R"],
    })
    table = build_mapping_table(records, salt="sel")
    assert len(table) == 2
    assert "exam_id" in table.columns
    assert "ident_patient_name" in table.columns
    assert "ident_patient_id" in table.columns
    assert "image_laterality" not in table.columns


def test_save_mapping_writes_only_in_private(tmp_path):
    """Le fichier est écrit uniquement dans le dossier private/."""
    private = tmp_path / "private"
    table = pd.DataFrame({"exam_id": ["EX-aaa"], "ident_patient_name": ["Test"]})
    path = save_mapping(table, private)
    assert path.parent == private
    assert path.name == "mapping.csv"
    assert path.exists()
    parent_files = list(tmp_path.glob("*.csv"))
    assert len(parent_files) == 0
