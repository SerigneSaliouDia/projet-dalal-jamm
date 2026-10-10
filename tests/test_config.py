from pathlib import Path

from dalal_jamm.config import get_paths


def test_paths_default_are_inside_repo(monkeypatch):
    for var in ("DALAL_DATA_DIR", "DALAL_DICOM_DIR", "DALAL_REPORTS_DIR"):
        monkeypatch.delenv(var, raising=False)
    p = get_paths()
    assert isinstance(p.data, Path)
    assert p.dicom == p.data / "raw" / "dicom"
    assert p.reports == p.data / "raw" / "reports"


def test_env_override(monkeypatch, tmp_path):
    monkeypatch.setenv("DALAL_REPORTS_DIR", str(tmp_path))
    assert get_paths().reports == tmp_path
