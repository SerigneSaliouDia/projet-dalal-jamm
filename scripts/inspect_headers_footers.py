"""Que contiennent les en-têtes, pieds de page et zones de texte des rapports ? (S2-SA-2)

N'affiche que : des comptages, et le texte des modèles qui reviennent au moins 5 fois (en-tête d'hôpital...).
Les textes plus rares, qui peuvent contenir un nom de patiente ou une date, ne sont PAS affichés.
Usage :  python scripts/inspect_headers_footers.py
"""

from __future__ import annotations

import os
from collections import Counter
from pathlib import Path

import pandas as pd

from dalal_jamm.config import get_paths
from dalal_jamm.reports.reader import read_extras
from dalal_jamm.utils.fs import extended_path

TEMPLATE_MIN = 5


def one_line(text: str, limit: int = 300) -> str:
    flat = " ⏎ ".join(line.strip() for line in text.splitlines() if line.strip())
    return flat if len(flat) <= limit else flat[:limit] + "…"


def report_templates(label: str, texts: list[str]) -> None:
    counter = Counter(t for t in texts if t)
    templates = {t: c for t, c in counter.items() if c >= TEMPLATE_MIN}
    rare = sum(c for t, c in counter.items() if c < TEMPLATE_MIN)
    print(f"\n== {label} ==")
    print(f"Rapports avec un texte : {sum(counter.values())} | textes distincts : {len(counter)}")
    print(f"Modèles qui reviennent au moins {TEMPLATE_MIN} fois : {len(templates)}")
    for text, count in sorted(templates.items(), key=lambda kv: -kv[1]):
        print(f"  [{count} rapports] {one_line(text)}")
    print(f"Rapports avec un texte plus rare (non affiché, peut être propre à la patiente) : {rare}")


def main() -> None:
    folder: Path = get_paths().reports
    names = sorted(
        e.name for e in os.scandir(extended_path(folder))
        if e.is_file() and e.name.lower().endswith(".docx") and not e.name.startswith("~$")
    )
    headers, footers, boxes = [], [], []
    for name in names:
        extras = read_extras(folder / name)
        headers.append("\n".join(extras["headers"]))
        footers.append("\n".join(extras["footers"]))
        boxes.append("\n".join(extras["textboxes"]))
    print(f"{len(names)} rapports examinés")
    report_templates("EN-TÊTES", headers)
    report_templates("PIEDS DE PAGE", footers)
    n_boxes = sum(1 for b in boxes if b)
    print(f"\n== ZONES DE TEXTE ==\nRapports avec une zone de texte : {n_boxes} (contenu non affiché)")

    structure = get_paths().interim / "reports_structure.csv"
    if structure.exists():
        chars = pd.read_csv(structure)["n_chars"]
        quantiles = " / ".join(str(int(chars.quantile(q))) for q in (0.5, 0.9, 0.95, 0.99))
        print("\n== Longueur des rapports (caractères) ==")
        print(f"Quantiles 50 / 90 / 95 / 99 : {quantiles} | max : {chars.max()}")
        print(f"Rapports de plus de 2000 caractères : {int((chars > 2000).sum())}")
        print(f"Rapports de plus de 3000 caractères : {int((chars > 3000).sum())}")


if __name__ == "__main__":
    main()
