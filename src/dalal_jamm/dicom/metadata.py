"""Lecture des en-têtes DICOM, sans charger les pixels (Sprint 1).

Principes :
- on lit SEULEMENT l'en-tête (`stop_before_pixels=True`) : rapide, et indépendant de la compression ;
- une valeur absente reste VIDE (None) : on n'invente rien ;
- les erreurs sont enregistrées par CLASSE d'exception uniquement, car le message d'erreur
  contient le chemin du fichier, donc le nom de la patiente ;
- les colonnes préfixées `ident_` sont des IDENTIFIANTS (nom, numéro patient, numéro d'accès) :
  utiles pour l'association rapports <-> examens (sprint 3), à ne jamais afficher ni committer.
"""

from __future__ import annotations

from pathlib import Path

from pydicom import dcmread
from pydicom.errors import InvalidDicomError

from dalal_jamm.utils.fs import extended_path

# (nom de colonne, mot-clé DICOM)
HEADER_FIELDS: list[tuple[str, str]] = [
    ("ident_patient_name", "PatientName"),
    ("ident_patient_id", "PatientID"),
    ("ident_accession", "AccessionNumber"),
    ("study_date", "StudyDate"),
    ("study_time", "StudyTime"),
    ("study_uid", "StudyInstanceUID"),
    ("series_uid", "SeriesInstanceUID"),
    ("sop_uid", "SOPInstanceUID"),
    ("modality", "Modality"),
    ("study_description", "StudyDescription"),
    ("series_description", "SeriesDescription"),
    ("series_number", "SeriesNumber"),
    ("instance_number", "InstanceNumber"),
    ("image_laterality", "ImageLaterality"),
    ("laterality", "Laterality"),
    ("view_position", "ViewPosition"),
    ("presentation_intent", "PresentationIntentType"),
    ("image_type", "ImageType"),
    ("rows", "Rows"),
    ("columns", "Columns"),
    ("bits_allocated", "BitsAllocated"),
    ("photometric", "PhotometricInterpretation"),
    ("number_of_frames", "NumberOfFrames"),
    ("pixel_spacing", "ImagerPixelSpacing"),
    ("manufacturer", "Manufacturer"),
    ("model", "ManufacturerModelName"),
    ("body_part", "BodyPartExamined"),
]

COLUMNS = ["status", "error", "transfer_syntax", "view_code_meaning"] + [c for c, _ in HEADER_FIELDS]


def _to_text(value) -> str | None:
    """Valeur DICOM -> texte ; vide ou absent -> None."""
    if value is None:
        return None
    if isinstance(value, (list, tuple)) or value.__class__.__name__ == "MultiValue":
        text = "\\".join(str(v) for v in value)
    else:
        text = str(value)
    text = text.strip()
    return text or None


def _view_code_meaning(ds) -> str | None:
    seq = ds.get("ViewCodeSequence")
    if seq:
        return _to_text(seq[0].get("CodeMeaning"))
    return None


def _empty(status: str, error: str | None) -> dict:
    row = {c: None for c in COLUMNS}
    row["status"] = status
    row["error"] = error
    return row


def read_header(path: Path) -> dict:
    """Lit l'en-tête d'un fichier DICOM. Ne lève JAMAIS d'exception.

    Retourne un dict avec les colonnes de `COLUMNS` :
      status  'ok' (DICOM conforme), 'forced' (lu malgré un en-tête de fichier non conforme)
              ou 'error' (illisible)
      error   nom de la classe d'exception (jamais le message : il contient le chemin)

    Ticket : S1-MA-1
    """
    target = extended_path(path)
    ds = None
    status = "ok"
    try:
        ds = dcmread(target, stop_before_pixels=True)
    except InvalidDicomError:
        try:
            ds = dcmread(target, stop_before_pixels=True, force=True)
            status = "forced"
        except Exception as exc:  # noqa: BLE001 - on veut tout capturer, sans le message
            return _empty("error", type(exc).__name__)
    except Exception as exc:  # noqa: BLE001
        return _empty("error", type(exc).__name__)

    if ds.get("Modality") is None and ds.get("SOPInstanceUID") is None:
        return _empty("error", "NoDicomContent")

    row = _empty(status, None)
    meta = getattr(ds, "file_meta", None)
    row["transfer_syntax"] = _to_text(meta.get("TransferSyntaxUID")) if meta else None
    row["view_code_meaning"] = _view_code_meaning(ds)
    for column, keyword in HEADER_FIELDS:
        row[column] = _to_text(ds.get(keyword))
    return row
