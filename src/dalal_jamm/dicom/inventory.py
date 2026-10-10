"""Inventaire des fichiers DICOM / IMA (Sprint 1)."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

from dalal_jamm.utils.fs import extended_path

COLUMNS = ["rel_path", "patient_idx", "exam_folder", "series_folder",
           "depth", "ext", "size_bytes", "path_len"]


def scan_files(root: Path) -> pd.DataFrame:
    """Parcourt `root` récursivement et retourne 1 ligne par FICHIER (tous types).

    Structure attendue : <root>/<patiente>/<examen>/<série>/<fichier>. Rien n'est supposé :
    la colonne `depth` permet de vérifier que tous les fichiers ont bien cette profondeur.

    Le parcours utilise le préfixe Windows `\\\\?\\` : les fichiers dont le chemin dépasse 259
    caractères sont donc listés ET lisibles (sans lui, ils sont silencieusement ignorés par
    `Path.is_file()` ou provoquent une erreur).

    Colonnes :
      rel_path      chemin relatif à `root` (IDENTIFIANT : contient le nom de la patiente)
      patient_idx   numéro du dossier de 1er niveau (ordre alphabétique), None si fichier à la racine
      exam_folder   nom du dossier de 2e niveau (None si absent)
      series_folder nom du dossier de 3e niveau (None si absent)
      depth         nombre de niveaux de rel_path (fichier compris)
      ext           extension en minuscules ('(aucune)' si absente)
      size_bytes    taille du fichier (vide si illisible)
      path_len      longueur du chemin complet sans préfixe (limite Windows : 259)

    Les erreurs (accès refusé, taille illisible...) sont comptées dans `df.attrs["walk_errors"]`.

    Ticket : S1-SA-1
    """
    root = Path(root)
    if not root.is_dir():
        raise FileNotFoundError(f"Dossier introuvable : {root}")

    walk_root = extended_path(root)
    shown_root = os.path.abspath(root)
    errors: list[str] = []

    top_levels = sorted(e.name for e in os.scandir(walk_root) if e.is_dir())
    patient_index = {name: i for i, name in enumerate(top_levels)}

    rows = []
    for dirpath, dirnames, filenames in os.walk(walk_root, onerror=lambda e: errors.append(type(e).__name__)):
        dirnames.sort()
        rel_dir = dirpath[len(walk_root):].lstrip("\\/")
        dir_parts = rel_dir.replace("\\", "/").split("/") if rel_dir else []
        for name in sorted(filenames):
            parts = [*dir_parts, name]
            try:
                size = os.stat(os.path.join(dirpath, name)).st_size
            except OSError:
                size = None
                errors.append("stat")
            rows.append(
                {
                    "rel_path": "/".join(parts),
                    "patient_idx": patient_index.get(parts[0]) if len(parts) > 1 else None,
                    "exam_folder": parts[1] if len(parts) > 2 else None,
                    "series_folder": parts[2] if len(parts) > 3 else None,
                    "depth": len(parts),
                    "ext": os.path.splitext(name)[1].lower() or "(aucune)",
                    "size_bytes": size,
                    "path_len": len(os.path.join(shown_root, *parts)),
                }
            )

    df = pd.DataFrame(rows, columns=COLUMNS)
    df.attrs["walk_errors"] = len(errors)
    return df


def build_inventory(root: Path) -> pd.DataFrame:
    """Pour chaque fichier : lisible oui/non, motif d'échec, métadonnées d'en-tête.

    Ticket : S1-MA-1 (lecture des en-têtes) puis assemblage ici.
    """
    raise NotImplementedError("S1-MA-1")
