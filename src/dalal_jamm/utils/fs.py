"""Outils système de fichiers : chemins longs sous Windows.

Windows refuse d'ouvrir un fichier dont le chemin dépasse 259 caractères, sauf si le chemin est
écrit avec le préfixe « \\\\?\\ ». Les noms de dossiers de ce projet contiennent le nom de la patiente
et dépassent parfois cette limite : TOUT accès aux données doit passer par `extended_path`.
"""

from __future__ import annotations

import os

_PREFIX = "\\\\?\\"
_UNC_PREFIX = "\\\\?\\UNC\\"


def add_extended_prefix(abs_path: str) -> str:
    """Ajoute le préfixe Windows à un chemin ABSOLU de style Windows (idempotent)."""
    if abs_path.startswith(_PREFIX):
        return abs_path
    if abs_path.startswith("\\\\"):
        return _UNC_PREFIX + abs_path[2:]
    return _PREFIX + abs_path


def extended_path(path) -> str:
    """Chemin absolu utilisable au-delà de 260 caractères sous Windows ; simple chemin absolu ailleurs."""
    p = os.path.abspath(os.fspath(path))
    return add_extended_prefix(p) if os.name == "nt" else p
