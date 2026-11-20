"""Exporte le texte brut ORIGINAL des comptes rendus et diagnostique leur structure (S2-SA-2, S2-SA-3).

Écrit dans data/interim/ (hors Git, contient des NOMS) :
  reports_text.jsonl          1 ligne par rapport : {"file": ..., "text": ...}
  reports_structure.csv       1 ligne par rapport : erreur, structure, longueur, empreinte du texte
  reports_check_sample.csv    10 rapports variés à comparer À LA MAIN avec le fichier Word

N'affiche que des COMPTAGES. Usage :  python scripts/export_report_texts.py
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import pandas as pd

from dalal_jamm.config import ensure_dirs
from dalal_jamm.reports.reader import inspect_docx, read_docx_ordered
from dalal_jamm.utils.fs import extended_path

# critères de variété pour choisir les rapports à vérifier à la main (le nom de colonne, l'étiquette)
CRITERIA = [
    ("n_tables", "tableau"),
    ("n_merged_cells", "cellules fusionnées"),
    ("n_nested_tables", "tableau imbriqué"),
    ("n_textboxes", "zone de texte"),
    ("n_tracked_changes", "révisions"),
    ("has_header_footer_text", "en-tête/pied de page"),
    ("n_images", "image"),
    ("n_content_controls", "contrôle de contenu"),
]


def list_reports(folder: Path) -> list[str]:
    names = [e.name for e in os.scandir(extended_path(folder)) if e.is_file()]
    return sorted(n for n in names if n.lower().endswith(".docx") and not n.startswith("~$"))


def pick_check_sample(df: pd.DataFrame, n: int = 10, seed: int = 42) -> pd.DataFrame:
    """Choisit n rapports variés : un par critère rencontré, le plus long, le plus court, puis au hasard."""
    ok = df[df["error"].isna()]
    chosen: dict[int, list[str]] = {}

    def take(idx: int, reason: str) -> None:
        if idx not in chosen and len(chosen) < n:
            chosen[idx] = []
        if idx in chosen:
            chosen[idx].append(reason)

    for col, label in CRITERIA:
        hit = ok[ok[col] > 0]
        if len(hit):
            take(hit.index[0], label)
    if len(ok):
        take(ok["n_chars"].idxmax(), "le plus long")
        non_empty = ok[ok["n_chars"] > 0]
        take((non_empty if len(non_empty) else ok)["n_chars"].idxmin(), "le plus court")
    for idx in ok.sample(frac=1, random_state=seed).index:
        if idx not in chosen:
            take(idx, "au hasard")
    rows = [
        {"n": i + 1, "file": df.loc[idx, "file"], "raisons": " ; ".join(reasons)}
        for i, (idx, reasons) in enumerate(chosen.items())
    ]
    return pd.DataFrame(rows)


def main() -> None:
    p = ensure_dirs()
    names = list_reports(p.reports)
    print(f"Lecture de {len(names)} comptes rendus...")
    rows, records = [], []
    for name in names:
        path = p.reports / name
        row = {"file": name, "error": None, "n_chars": 0, "text_hash": None}
        try:
            text = read_docx_ordered(path)
            row.update(inspect_docx(path))
            row["n_chars"] = len(text)
            row["text_hash"] = hashlib.sha1(text.encode("utf-8")).hexdigest()
            records.append({"file": name, "text": text})
        except Exception as exc:  # noqa: BLE001 - on ne garde que la classe : le message contient le chemin
            row["error"] = type(exc).__name__
        rows.append(row)
    df = pd.DataFrame(rows)

    with open(p.interim / "reports_text.jsonl", "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    df.to_csv(p.interim / "reports_structure.csv", index=False, encoding="utf-8")
    sample = pick_check_sample(df)
    sample.to_csv(p.interim / "reports_check_sample.csv", index=False, encoding="utf-8")

    ok = df[df["error"].isna()]
    errors = df["error"].value_counts().to_dict()
    print(f"\nLus : {len(ok)} | en erreur : {len(df) - len(ok)} {errors}")
    if ok.empty:
        return
    chars = ok["n_chars"]
    print(f"Texte vide : {int((chars == 0).sum())} | moins de 200 caractères : {int((chars < 200).sum())}")
    lengths = f"{chars.min()} / {int(chars.median())} / {chars.max()}"
    print(f"Longueur (caractères) min / médiane / max : {lengths}")
    print("\n== Structure (nombre de rapports concernés) ==")
    for col, label in CRITERIA:
        print(f"  {label:<24}: {int((ok[col] > 0).sum())}")
    print(f"  plusieurs sections      : {int((ok['n_sections'] > 1).sum())}")
    risky = (ok["n_textboxes"] > 0) | (ok["n_tracked_changes"] > 0) | (ok["has_header_footer_text"] > 0)
    print(f"\nRapports dont du texte peut manquer à la lecture : {int(risky.sum())}")
    print("  (zone de texte, révisions ou texte en en-tête/pied de page : à vérifier à la main)")
    dup = ok["text_hash"].duplicated(keep=False)
    groups = ok.loc[dup, "text_hash"].nunique()
    print(f"Rapports au texte strictement identique à un autre : {int(dup.sum())} (dans {groups} groupes)")
    print(f"\nÉchantillon à vérifier à la main : {len(sample)} rapports (reports_check_sample.csv)")
    print("Fichiers écrits dans data/interim/ (contiennent des NOMS : ne JAMAIS les committer)")


if __name__ == "__main__":
    main()
