"""Écrit le texte extrait d'un rapport de l'échantillon dans un fichier, pour le comparer au Word.

Le nom de la patiente n'est PAS affiché dans le terminal : il est dans la première ligne du fichier écrit.
Usage :  python scripts/show_report_text.py <n>      (n = numéro dans reports_check_sample.csv)
"""

from __future__ import annotations

import sys

import pandas as pd

from dalal_jamm.config import get_paths
from dalal_jamm.reports.reader import read_docx_ordered, read_extras


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        raise SystemExit("Usage : python scripts/show_report_text.py <n>")
    n = int(sys.argv[1])
    p = get_paths()
    sample = pd.read_csv(p.interim / "reports_check_sample.csv")
    row = sample[sample["n"] == n]
    if row.empty:
        raise SystemExit(f"Numéro {n} absent de l'échantillon (1 à {len(sample)}).")
    name, reasons = row.iloc[0]["file"], row.iloc[0]["raisons"]
    out = p.interim / f"check_{n}.txt"
    header = f"FICHIER : {name}\nCHOISI POUR : {reasons}\n{'=' * 60}\n"
    path = p.reports / name
    body = read_docx_ordered(path)
    extras = read_extras(path)
    parts = [header + body + "\n"]
    for key, title in (("headers", "EN-TÊTE"), ("footers", "PIED DE PAGE"), ("textboxes", "ZONE DE TEXTE")):
        for text in extras[key]:
            parts.append(f"\n{'-' * 20} {title} (non inclus dans le texte principal) {'-' * 20}\n{text}\n")
    out.write_text("".join(parts), encoding="utf-8")
    print(f"Texte extrait écrit dans : {out}")
    print(f"Raisons du choix : {reasons}")
    print("Ouvre ce fichier ET le document Word correspondant (nom en 1re ligne) et compare.")


if __name__ == "__main__":
    main()
