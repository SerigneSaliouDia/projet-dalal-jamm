"""Garde-fou : aucune donnée patiente ne doit être suivie par Git."""

import shutil
import subprocess
from pathlib import Path

import pytest

FORBIDDEN = {".dcm", ".ima", ".docx", ".doc"}
REPO = Path(__file__).resolve().parents[1]


@pytest.mark.skipif(shutil.which("git") is None, reason="git indisponible")
def test_no_forbidden_extensions_tracked():
    out = subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True, text=True)
    if out.returncode != 0:
        pytest.skip("pas un dépôt git")
    bad = [f for f in out.stdout.splitlines() if Path(f).suffix.lower() in FORBIDDEN]
    assert not bad, f"Fichiers de données suivis par Git : {bad}"


@pytest.mark.skipif(shutil.which("git") is None, reason="git indisponible")
def test_nothing_tracked_under_data_except_readme():
    out = subprocess.run(["git", "ls-files", "data"], cwd=REPO, capture_output=True, text=True)
    if out.returncode != 0:
        pytest.skip("pas un dépôt git")
    tracked = [f for f in out.stdout.splitlines() if f != "data/README.md"]
    assert not tracked, f"Fichiers suivis dans data/ : {tracked}"
