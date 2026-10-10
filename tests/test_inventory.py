import pandas as pd
import pytest

from dalal_jamm.dicom.inventory import scan_files


@pytest.fixture
def fake_tree(tmp_path):
    """Arborescence FICTIVE : racine/patiente/examen/série/fichier."""
    files = [
        "P_B/E1/S2/c.ima",
        "P_A/E1/S2/a.IMA",
        "P_A/E1/S2/b.IMA",
        "P_B/E1/S2/d.txt",
        "P_B/E2/S1/e.IMA",
        "stray.IMA",
    ]
    for rel in files:
        f = tmp_path / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(b"x" * 10)
    return tmp_path


def test_counts_all_files_of_all_types(fake_tree):
    df = scan_files(fake_tree)
    assert len(df) == 6
    assert df["ext"].value_counts().to_dict() == {".ima": 5, ".txt": 1}


def test_extension_is_lowercase_and_size_is_read(fake_tree):
    df = scan_files(fake_tree)
    assert set(df["ext"]) == {".ima", ".txt"}
    assert (df.loc[df["rel_path"] != "stray.IMA", "size_bytes"] == 10).all()


def test_patient_index_follows_alphabetical_order(fake_tree):
    df = scan_files(fake_tree).set_index("rel_path")
    assert df.loc["P_A/E1/S2/a.IMA", "patient_idx"] == 0
    assert df.loc["P_B/E1/S2/c.ima", "patient_idx"] == 1


def test_file_at_root_has_no_patient_and_depth_one(fake_tree):
    row = scan_files(fake_tree).set_index("rel_path").loc["stray.IMA"]
    assert row["depth"] == 1
    assert pd.isna(row["patient_idx"]) and pd.isna(row["exam_folder"])


def test_folders_and_depth(fake_tree):
    row = scan_files(fake_tree).set_index("rel_path").loc["P_B/E2/S1/e.IMA"]
    assert (row["exam_folder"], row["series_folder"], row["depth"]) == ("E2", "S1", 4)


def test_order_is_deterministic(fake_tree):
    assert list(scan_files(fake_tree)["rel_path"]) == list(scan_files(fake_tree)["rel_path"])


def test_missing_folder_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        scan_files(tmp_path / "n_existe_pas")


def test_empty_folder_gives_empty_table(tmp_path):
    df = scan_files(tmp_path)
    assert len(df) == 0 and "rel_path" in df.columns

