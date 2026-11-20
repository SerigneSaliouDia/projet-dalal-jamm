"""Découpage des fichiers en comptes rendus, puis d'un compte rendu en sections.

Un fichier .docx peut contenir PLUSIEURS comptes rendus de patientes différentes (observé : jusqu'à 5).
L'unité de travail est le compte rendu, pas le fichier.

Clés attendues pour un compte rendu : 'entete', 'densite', 'sein_droit', 'sein_gauche', 'echo', 'conclusion'.
Le découpage en sections repose sur la POSITION des en-têtes, pas sur leur ordre : un rapport où
« Sein gauche » précède « Sein droit » doit donner les mêmes sections.
"""

from __future__ import annotations

import re
import unicodedata

SECTION_KEYS = ("entete", "densite", "sein_droit", "sein_gauche", "echo", "conclusion")

_NAME_FIELD = re.compile(r"prenom\s*&\s*nom\s*:")
_SIGNATURE = re.compile(r"^(dr|pr|docteur|professeur|radiologue)\b")
MAX_TITLE_LENGTH = 120


def fold(text: str) -> str:
    """Minuscules sans accents, retours à la ligne conservés (sert à CHERCHER, jamais à stocker)."""
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")


def _looks_like_title(folded_line: str) -> bool:
    """Une ligne de titre est courte, sans « : » et n'est pas une signature de radiologue."""
    line = folded_line.strip()
    return bool(line) and ":" not in line and len(line) <= MAX_TITLE_LENGTH and not _SIGNATURE.match(line)


def split_multiple_reports(text: str) -> list[str]:
    """Découpe le texte ORIGINAL d'un fichier en comptes rendus (texte original, lignes conservées).

    Un compte rendu commence à la ligne « Prénom & Nom : … » ; la ligne non vide qui la précède est son
    titre (ex. « MAMMOGRAPHIE BILATERALE ») sauf si c'est une signature (« Dr … », « Radiologue »).
    Ce qui précède le premier compte rendu lui est rattaché. Sans ligne « Prénom & Nom », le fichier
    entier est retourné comme un seul compte rendu (à examiner). Aucune ligne n'est perdue ni modifiée.

    Ticket : S4-MA-2 (avancé au sprint 2 : indispensable avant l'association rapports <-> examens)
    """
    lines = text.splitlines()
    if not any(line.strip() for line in lines):
        return []
    folded = [fold(line) for line in lines]
    name_lines = [i for i, line in enumerate(folded) if _NAME_FIELD.search(line)]
    if not name_lines:
        return [text.strip("\n")]

    starts: list[int] = []
    for k, i in enumerate(name_lines):
        previous_name_line = name_lines[k - 1] if k > 0 else -1
        j = i - 1
        while j > previous_name_line and not folded[j].strip():
            j -= 1
        is_title = j > previous_name_line and _looks_like_title(folded[j])
        starts.append(j if is_title else i)
    starts[0] = 0

    blocks = []
    for k, start in enumerate(starts):
        end = starts[k + 1] if k + 1 < len(starts) else len(lines)
        blocks.append("\n".join(lines[start:end]).strip("\n"))
    return blocks


def report_title(block: str) -> str | None:
    """Ligne de titre du compte rendu (texte original), si elle précède la ligne « Prénom & Nom »."""
    lines = block.splitlines()
    for i, line in enumerate(lines):
        if _NAME_FIELD.search(fold(line)):
            before = [candidate.strip() for candidate in lines[:i] if candidate.strip()]
            return before[-1] if before and _looks_like_title(fold(before[-1])) else None
    return None


def is_mammography(block: str) -> bool:
    """Vrai si le titre contient « mammographie » (tolère les fautes de frappe : « amammographie »).

    Sans titre, vrai si le compte rendu comporte une section « Sein droit » ou « Sein gauche ».
    Un compte rendu d'un autre examen (échographie abdominale, hystérographie...) donne Faux.
    """
    title = report_title(block)
    if title is not None:
        return "mammographie" in fold(title)
    body = fold(block)
    return "sein droit" in body or "sein gauche" in body


def split_sections(text_norm: str) -> dict[str, str]:
    """Retourne un dict {clé: texte} pour UN compte rendu. Section absente -> chaîne vide.

    Ticket : S4-MA-1
    """
    raise NotImplementedError("S4-MA-1")
