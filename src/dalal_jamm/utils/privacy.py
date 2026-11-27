"""Pseudonymisation : exam_id et table de correspondance privée (Sprint 2).

Principe : chaque examen reçoit un identifiant STABLE (même entrée = même sortie)
et NON RÉVERSIBLE (impossible de retrouver le patient à partir de l'ID).

Méthode : on concatène la clé d'entrée avec un SEL SECRET, puis on applique SHA-256.
Le sel est un fichier texte stocké dans data/private/ — jamais commité (gitignore).
Sans le sel, le hash ne peut pas être recalculé → protection supplémentaire.
"""

from __future__ import annotations

import hashlib
import secrets
from pathlib import Path

import pandas as pd

SALT_FILE = "salt.txt"
MAPPING_FILE = "mapping.csv"
EXAM_ID_PREFIX = "EX-"
HASH_LENGTH = 12


def _salt_path(private_dir: Path) -> Path:
    """Chemin du fichier sel dans le dossier privé."""
    return private_dir / SALT_FILE


def load_or_create_salt(private_dir: Path) -> str:
    """Charge le sel secret. S'il n'existe pas, en crée un nouveau.

    Le sel est une chaîne aléatoire de 32 caractères hexadécimaux.
    Il est stocké dans data/private/salt.txt (jamais commité).
    """
    path = _salt_path(private_dir)
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    private_dir.mkdir(parents=True, exist_ok=True)
    salt = secrets.token_hex(16)
    path.write_text(salt, encoding="utf-8")
    return salt


def make_exam_id(key: str, salt: str) -> str:
    """Génère un identifiant d'examen stable et non réversible.

    Fonctionnement :
    1. On colle la clé et le sel : "clé" + "sel"
    2. On calcule le SHA-256 de cette chaîne → empreinte de 64 caractères hex
    3. On garde les 12 premiers caractères et on ajoute le préfixe "EX-"

    Résultat : "EX-a1b2c3d4e5f6" — stable (même clé+sel = même résultat),
    non réversible (SHA-256 est un hash à sens unique).

    Ticket : S2-MA-1
    """
    combined = key + salt
    digest = hashlib.sha256(combined.encode("utf-8")).hexdigest()
    return EXAM_ID_PREFIX + digest[:HASH_LENGTH]


def build_mapping_table(
    records: pd.DataFrame,
    salt: str,
    key_column: str = "study_uid",
) -> pd.DataFrame:
    """Construit la table de correspondance exam_id <-> identité.

    Entrée : un DataFrame contenant au minimum la colonne clé (study_uid par défaut)
    et les colonnes d'identité (ident_patient_name, ident_patient_id, etc.).

    Sortie : un DataFrame avec exam_id + les colonnes d'identité, dédupliqué par exam_id.
    À stocker UNIQUEMENT dans data/private/.

    Ticket : S2-MA-1
    """
    ident_cols = [c for c in records.columns if c.startswith("ident_")]
    keep_cols = [key_column] + ident_cols

    df = records[keep_cols].drop_duplicates(subset=[key_column]).copy()
    df.insert(0, "exam_id", df[key_column].apply(lambda k: make_exam_id(str(k), salt)))
    return df.reset_index(drop=True)


def save_mapping(table: pd.DataFrame, private_dir: Path) -> Path:
    """Sauvegarde la table de correspondance en CSV dans data/private/.

    Ticket : S2-MA-3
    """
    private_dir.mkdir(parents=True, exist_ok=True)
    path = private_dir / MAPPING_FILE
    table.to_csv(path, index=False, encoding="utf-8")
    return path
