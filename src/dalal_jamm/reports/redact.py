"""Masquage des noms de patientes avant tout partage de texte de rapport (aide, relecture, mémoire).

Le nom est lu sur la ligne « Prénom & Nom : … » de chaque compte rendu, puis chacun de ses mots (3 lettres ou
plus) est remplacé par XXX PARTOUT dans le texte, sans tenir compte des accents ni de la casse.
Ce masquage réduit le risque, il ne le supprime pas : l'âge, la date et le contenu clinique restent, et un
nom écrit autrement que sur la ligne « Prénom & Nom » peut échapper. Relisez avant de partager.
"""

from __future__ import annotations

import re
import unicodedata

MASK = "XXX"
MIN_TOKEN_LENGTH = 3

# « Prénom & Nom : <nom> » ; le nom s'arrête à une tabulation, à 2 espaces ou plus, ou au mot DATE.
_NAME_LINE = re.compile(
    r"pr[eéÉ]nom\s*&\s*nom\s*:\s*(?P<name>.+?)(?=\t|\s{2,}|date\s*:|$)", re.IGNORECASE | re.MULTILINE
)


def _fold(text: str) -> str:
    """Minuscules sans accents ; la longueur est conservée pour un texte en forme NFC."""
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")


def patient_name_tokens(text: str) -> set[str]:
    """Mots (en minuscules sans accents) des noms lus sur les lignes « Prénom & Nom : … »."""
    tokens: set[str] = set()
    for match in _NAME_LINE.finditer(text):
        for token in re.split(r"[\s\-'’_]+", _fold(match.group("name"))):
            if len(token) >= MIN_TOKEN_LENGTH and token.isalpha():
                tokens.add(token)
    return tokens


def mask_patient_names(text: str) -> str:
    """Remplace par XXX chaque mot des noms de patientes de `text`. Sans ligne de nom : texte inchangé."""
    text = unicodedata.normalize("NFC", text)
    tokens = patient_name_tokens(text)
    if not tokens:
        return text
    folded = _fold(text)
    alternatives = "|".join(sorted(map(re.escape, tokens), key=len, reverse=True))
    pattern = re.compile(r"(?<![a-z0-9])(?:" + alternatives + r")(?![a-z0-9])")
    pieces, last = [], 0
    for m in pattern.finditer(folded):
        pieces.append(text[last:m.start()])
        pieces.append(MASK)
        last = m.end()
    pieces.append(text[last:])
    return "".join(pieces)
