import os
import shutil

import pytest

from dalal_jamm.dicom.inventory import scan_files
from dalal_jamm.utils.fs import add_extended_prefix, extended_path


def test_prefix_added_to_drive_path():
    assert add_extended_prefix("C:\\MAMMO\\Img") == "\\\\?\\C:\\MAMMO\\Img"


def test_prefix_is_idempotent():
    p = "\\\\?\\C:\\MAMMO\\Img"
    assert add_extended_prefix(p) == p


def test_prefix_for_network_path():
    assert add_extended_prefix("\\\\serveur\\partage\\x") == "\\\\?\\UNC\\serveur\\partage\\x"


@pytest.mark.skipif(os.name == "nt", reason="comportement Windows testé séparément")
def test_extended_path_is_plain_absolute_path_outside_windows():
    assert extended_path("a") == os.path.abspath("a")


@pytest.mark.skipif(os.name != "nt", reason="chemins longs : spécifique à Windows")
def test_scan_files_reads_file_with_path_over_260_chars(tmp_path):
    """Reproduit le bug des 38 fichiers : chemin > 259 caractères."""
    deep = tmp_path / "P" / ("e" * 80) / ("s" * 80) / ("x" * 80)
    target = deep / "image.IMA"
    assert len(str(target)) > 260
    os.makedirs(extended_path(deep), exist_ok=True)
    with open(extended_path(target), "wb") as f:
        f.write(b"0123456789")
    try:
        df = scan_files(tmp_path)
        assert len(df) == 1
        assert df.loc[0, "size_bytes"] == 10
        assert df.attrs["walk_errors"] == 0
        assert df.loc[0, "path_len"] > 260
    finally:
        shutil.rmtree(extended_path(tmp_path / "P"), ignore_errors=True)
