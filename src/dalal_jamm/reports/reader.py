"""Lecture des comptes rendus DOCX (Sprint 2).

Principes :
- le texte est restitué dans l'ORDRE du document (paragraphes et tableaux mêlés) ;
- le texte est ORIGINAL : accents, casse, espaces insécables conservés (la normalisation est une étape
  distincte, `reports/normalize.py`) ;
- les cellules fusionnées ne sont lues qu'une fois ;
- ce que la lecture ne sait PAS restituer (zones de texte, révisions, en-têtes et pieds de page...)
  n'est pas deviné : `inspect_docx` le SIGNALE pour que chaque document concerné soit vérifié à la main.
"""

from __future__ import annotations

import os
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

from dalal_jamm.utils.fs import extended_path

CELL_SEPARATOR = " | "


def _block_elements(parent_elm):
    """Paragraphes et tableaux enfants directs, dans l'ordre (y compris dans les contrôles de contenu)."""
    for child in parent_elm.iterchildren():
        if child.tag in (qn("w:p"), qn("w:tbl")):
            yield child
        elif child.tag == qn("w:sdt"):
            content = child.find(qn("w:sdtContent"))
            if content is not None:
                yield from _block_elements(content)


def _cell_text(cell) -> str:
    parts: list[str] = []
    for el in _block_elements(cell._tc):
        if el.tag == qn("w:p"):
            parts.append(Paragraph(el, cell).text)
        else:
            parts.extend(_table_lines(el, cell))
    return "\n".join(parts)


def _table_lines(tbl_elm, parent) -> list[str]:
    """Une ligne de texte par ligne de tableau ; une cellule fusionnée n'apparaît qu'une fois."""
    table = Table(tbl_elm, parent)
    seen: set = set()
    lines: list[str] = []
    for row in table.rows:
        cells: list[str] = []
        for cell in row.cells:
            if cell._tc in seen:
                continue
            seen.add(cell._tc)
            cells.append(_cell_text(cell))
        lines.append(CELL_SEPARATOR.join(cells))
    return lines


def _open(path: Path):
    """Ouvre un DOCX. Le message d'erreur ne contient JAMAIS le chemin (il contient le nom de la patiente)."""
    target = extended_path(path)
    if not os.path.isfile(target):
        raise FileNotFoundError("fichier introuvable")
    return Document(target)


def read_docx_ordered(path: Path) -> str:
    """Retourne le texte brut du document, dans l'ordre, une ligne par paragraphe ou ligne de tableau.

    Lève l'exception d'origine si le fichier est illisible (l'appelant décide quoi faire).

    Ticket : S2-SA-1
    """
    doc = _open(path)
    body = doc._body
    lines: list[str] = []
    for el in _block_elements(doc.element.body):
        if el.tag == qn("w:p"):
            lines.append(Paragraph(el, body).text)
        else:
            lines.extend(_table_lines(el, body))
    return "\n".join(lines)


def _part_text(part) -> str:
    """Texte d'un en-tête ou d'un pied de page (paragraphes et tableaux)."""
    lines: list[str] = []
    for el in _block_elements(part._element):
        if el.tag == qn("w:p"):
            lines.append(Paragraph(el, part).text)
        else:
            lines.extend(_table_lines(el, part))
    return "\n".join(lines).strip()


def _extras(doc) -> dict[str, list[str]]:
    """En-têtes, pieds de page et zones de texte d'un document déjà ouvert."""
    headers: list[str] = []
    footers: list[str] = []
    for section in doc.sections:
        for part in (section.header, section.first_page_header, section.even_page_header):
            if not part.is_linked_to_previous and _part_text(part):
                headers.append(_part_text(part))
        for part in (section.footer, section.first_page_footer, section.even_page_footer):
            if not part.is_linked_to_previous and _part_text(part):
                footers.append(_part_text(part))
    textboxes: list[str] = []
    for box in doc.element.body.iter(qn("w:txbxContent")):
        paragraphs = ["".join(t.text or "" for t in p.iter(qn("w:t"))) for p in box.iter(qn("w:p"))]
        text = "\n".join(paragraphs).strip()
        if text and text not in textboxes:  # Word écrit souvent chaque zone en double (formats de secours)
            textboxes.append(text)
    return {"headers": headers, "footers": footers, "textboxes": textboxes}


def read_extras(path: Path) -> dict[str, list[str]]:
    """Texte que `read_docx_ordered` ne restitue PAS : en-têtes, pieds de page, zones de texte.

    Retourne {"headers": [...], "footers": [...], "textboxes": [...]} : listes de textes non vides, sans
    doublon d'une même zone. Sert à décider, document par document ou par modèle, si ce texte compte.

    Ticket : S2-SA-2
    """
    return _extras(_open(path))


def inspect_docx(path: Path) -> dict:
    """Structure d'un document : ce qui peut échapper à `read_docx_ordered`.

    Colonnes (comptages) : n_paragraphs, n_tables, n_nested_tables, n_merged_cells, n_sections, n_images,
    n_textboxes, n_tracked_changes, n_content_controls, has_header_footer_text.
    Un document avec n_textboxes, n_tracked_changes ou has_header_footer_text > 0 est à vérifier à la main :
    du texte peut ne pas figurer dans `read_docx_ordered`.

    Ticket : S2-SA-2
    """
    doc = _open(path)
    body = doc.element.body
    extras = _extras(doc)
    n_tables = sum(1 for _ in body.iterchildren(qn("w:tbl")))
    all_tables = sum(1 for _ in body.iter(qn("w:tbl")))
    merged = sum(1 for _ in body.iter(qn("w:gridSpan"))) + sum(1 for _ in body.iter(qn("w:vMerge")))
    return {
        "n_paragraphs": sum(1 for _ in body.iterchildren(qn("w:p"))),
        "n_tables": n_tables,
        "n_nested_tables": all_tables - n_tables,
        "n_merged_cells": merged,
        "n_sections": len(doc.sections),
        "n_images": sum(1 for _ in body.iter(qn("a:blip"))),
        "n_textboxes": sum(1 for _ in body.iter(qn("w:txbxContent"))),
        "n_tracked_changes": sum(1 for _ in body.iter(qn("w:ins"))) + sum(1 for _ in body.iter(qn("w:del"))),
        "n_content_controls": sum(1 for _ in body.iter(qn("w:sdt"))),
        "has_header_footer_text": int(bool(extras["headers"] or extras["footers"])),
    }
