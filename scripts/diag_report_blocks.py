"""Combien de comptes rendus dans chaque fichier .docx, et de quel type ? (S2-SA-2 / S2-BA-1)

À lancer APRÈS scripts/export_report_texts.py. N'affiche que des COMPTAGES et des titres d'examen.
Un « bloc » = un compte rendu = une ligne « Prénom & Nom : ... ».
Si un titre affiché contient un nom, remplacez-le par XXX avant de l'envoyer.
Usage :  python scripts/diag_report_blocks.py
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter

from dalal_jamm.config import get_paths

NAME_FIELD = re.compile(r"prenom\s*&\s*nom\s*:")


def norm(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")


def previous_lines(lines: list[str], index: int, how_many: int = 3) -> list[str]:
    """Les `how_many` dernières lignes non vides avant `lines[index]`."""
    out: list[str] = []
    for line in reversed(lines[:index]):
        if line.strip():
            out.append(line.strip())
            if len(out) == how_many:
                break
    return out


def main() -> None:
    path = get_paths().interim / "reports_text.jsonl"
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    per_file: list[int] = []
    n_mammo = n_other = 0
    files_without_mammo = files_with_other = 0
    titles: Counter = Counter()
    for rec in records:
        lines = norm(rec["text"]).splitlines()
        idx = [i for i, line in enumerate(lines) if NAME_FIELD.search(line)]
        per_file.append(len(idx))
        mammo_here = other_here = 0
        for i in idx:
            before = previous_lines(lines, i)
            if any(b.startswith("mammographie") for b in before):
                mammo_here += 1
            else:
                other_here += 1
            titles[before[0] if before else "(rien avant)"] += 1
        n_mammo += mammo_here
        n_other += other_here
        files_without_mammo += mammo_here == 0
        files_with_other += other_here > 0

    dist = dict(sorted(Counter(per_file).items()))
    print(f"Fichiers : {len(records)}")
    print(f"Nombre de comptes rendus par fichier (nb de blocs -> nb de fichiers) : {dist}")
    print(f"Comptes rendus au total : {sum(per_file)}")
    print(f"  introduits par un titre « mammographie » : {n_mammo}")
    print(f"  sans titre « mammographie » (autre examen ou format différent) : {n_other}")
    print(f"Fichiers sans aucun compte rendu de mammographie : {files_without_mammo}")
    print(f"Fichiers contenant au moins un compte rendu non mammographique : {files_with_other}")
    print("\nLigne qui précède « Prénom & Nom » (top 12) :")
    for title, count in titles.most_common(12):
        print(f"  [{count}] {title[:80]}")


if __name__ == "__main__":
    main()
