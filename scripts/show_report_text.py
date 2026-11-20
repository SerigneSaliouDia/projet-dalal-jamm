"""Écrit le texte extrait d'un rapport de l'échantillon dans un fichier, pour le comparer au Word.

Le nom de la patiente n'est PAS affiché dans le terminal : il est dans la première ligne du fichier écrit.
Usage :  python scripts/show_report_text.py <n>      (n = numéro dans reports_check_sample.csv)
"""

from __future__ import annotations

import sys

import pandas as pd

from dalal_jamm.config import get_paths
from dalal_jamm.reports.reader import read_docx_ordered, read_extras
from dalal_jamm.reports.redact import mask_patient_names


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
    path = p.reports / name
    body = read_docx_ordered(path)
    extras = read_extras(path)
    parts = [body + "\n"]
    for key, title in (("headers", "EN-TÊTE"), ("footers", "PIED DE PAGE"), ("textboxes", "ZONE DE TEXTE")):
        for text in extras[key]:
            line = "-" * 20
            parts.append(f"\n{line} {title} (non inclus dans le texte principal) {line}\n{text}\n")
    content = "".join(parts)
    meta = f"CHOISI POUR : {reasons}\n{'=' * 60}\n"

    full = p.interim / f"check_{n}.txt"
    full.write_text(f"FICHIER : {name}\n{meta}{content}", encoding="utf-8")
    shareable = p.interim / f"check_{n}_partageable.txt"
    shareable.write_text(f"FICHIER : (masqué)\n{meta}{mask_patient_names(content)}", encoding="utf-8")
    out = full
    print(f"Texte complet (NOMS, ne pas partager) : {out}")
    print(f"Version aux noms masqués (relire avant de partager) : {shareable}")
    print(f"Raisons du choix : {reasons}")
    print("Compare le fichier complet au document Word (nom en 1re ligne).")
    print("Si tu partages un texte, utilise la version masquée.")


if __name__ == "__main__":
    main()
