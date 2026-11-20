"""Découpe les fichiers en comptes rendus (un fichier peut en contenir plusieurs).

Lit data/interim/reports_text.jsonl (scripts/export_report_texts.py) et écrit dans data/interim/
(hors Git, contient des NOMS) :
  reports_blocks.jsonl   1 ligne par compte rendu : report_id, file, block_index, n_blocks, title,
                         is_mammography, n_chars, text
  reports_blocks.csv     les mêmes colonnes sans le texte

N'affiche que des COMPTAGES. Usage :  python scripts/split_reports.py
"""

from __future__ import annotations

import json
import re
from collections import Counter

import pandas as pd

from dalal_jamm.config import get_paths
from dalal_jamm.reports.sections import fold, is_mammography, report_title, split_multiple_reports

NAME_FIELD = re.compile(r"prenom\s*&\s*nom\s*:")


def main() -> None:
    p = get_paths()
    raw = (p.interim / "reports_text.jsonl").read_text(encoding="utf-8")
    records = [json.loads(line) for line in raw.splitlines()]
    records.sort(key=lambda r: r["file"])

    rows, texts = [], []
    mismatches = 0
    for rec in records:
        blocks = split_multiple_reports(rec["text"])
        name_lines = [line for line in fold(rec["text"]).splitlines() if NAME_FIELD.search(line)]
        expected = len(name_lines) or 1
        mismatches += len(blocks) != expected
        for k, block in enumerate(blocks):
            rows.append({
                "report_id": f"R{len(rows) + 1:04d}",
                "file": rec["file"],
                "block_index": k + 1,
                "n_blocks": len(blocks),
                "title": report_title(block),
                "is_mammography": is_mammography(block),
                "n_chars": len(block),
            })
            texts.append(block)
    df = pd.DataFrame(rows)
    df.to_csv(p.interim / "reports_blocks.csv", index=False, encoding="utf-8")
    with open(p.interim / "reports_blocks.jsonl", "w", encoding="utf-8") as f:
        for row, text in zip(rows, texts):
            f.write(json.dumps({**row, "text": text}, ensure_ascii=False) + "\n")

    per_file = df.groupby("file")["report_id"].count()
    mammo = df[df["is_mammography"]]
    other = df[~df["is_mammography"]]
    print(f"Fichiers : {len(records)} | comptes rendus : {len(df)}")
    print(f"Comptes rendus par fichier (nb -> nb de fichiers) : {dict(sorted(Counter(per_file).items()))}")
    print(f"Fichiers dont le nombre de blocs diffère du nombre de lignes « Prénom & Nom » : {mismatches}")
    print(f"Mammographies : {len(mammo)} | autres examens : {len(other)}")
    mammo_per_file = df.groupby("file")["is_mammography"].sum()
    print(f"Fichiers sans aucune mammographie : {int((mammo_per_file == 0).sum())}")
    print(f"Comptes rendus sans titre : {int(df['title'].isna().sum())}")
    sizes = f"{df['n_chars'].min()} / {int(df['n_chars'].median())} / {df['n_chars'].max()}"
    print(f"Longueur d'un compte rendu (caractères) min / médiane / max : {sizes}")
    print("Titres des autres examens (hors mammographie) :")
    for title, count in Counter(other["title"].fillna("(sans titre)")).most_common(10):
        print(f"  [{count}] {title[:80]}")
    print("\nFichiers écrits dans data/interim/ (contiennent des NOMS : ne JAMAIS les committer)")


if __name__ == "__main__":
    main()
