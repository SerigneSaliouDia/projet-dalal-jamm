# Notes sur les DICOM

## Chiffres validés par l'inventaire du 10/10/2026

| Mesure | Valeur préliminaire | Valeur validée (inventaire du 10/10/2026) |
|---|---|---|
| Fichiers `.IMA` trouvés | ≈ 1965 | **2254** (dont 38 aux chemins ≥ 260 caractères, lisibles via le préfixe `\\?\`) |
| Dossiers patientes | – | 269 (3 sans fichier, donc 266 avec images) |
| Dossiers d'examen | ≈ 231 | 271 (3 sans fichier, donc 268 avec images) |
| Séries | – | 533 : `MAMMOGRAM_RAW_DIAGNOSIS_0001` (1131 fichiers), `MAMMOGRAM_DIAGNOSIS_0002` (1123 fichiers) |
| Fichiers lus correctement (en-tête) | ≈ 970 | à mesurer (S1-MA-1) |
| Examens complets (4 vues) | ≈ 200 | à mesurer (S1-MA-3, S1-BA-3) |
| Examens incomplets | ≈ 31 | à mesurer |

Remarques :
- Les « 231 examens » préliminaires ne sont pas forcément comparables aux 271 dossiers d'examen : la méthode de comptage n'était pas la même. À recomparer avec les identifiants d'étude lus dans les en-têtes.
- Le nombre de fichiers par examen n'indique pas qu'un examen est complet : seule la lecture de la latéralité et de la vue dans chaque en-tête le dira.
- Deux types de séries seulement. Les noms suggèrent des images brutes (« RAW ») et des images traitées : à confirmer avec les en-têtes.

## Causes d'échec de lecture

| N° | Cause | Fichiers | Solution |
|---|---|---|---|
| 1 | Chemin de 260 caractères ou plus (limite Windows) | 38 | Préfixe `\\?\` via `dalal_jamm.utils.fs.extended_path()` |

D'autres causes éventuelles seront ajoutées après la lecture des en-têtes (S1-MA-1).

## Champs d'en-tête utiles

`ImageLaterality`, `ViewPosition`, `SeriesDescription`, `StudyInstanceUID`, `SeriesInstanceUID`,
`StudyDate`, `Rows`, `Columns`, syntaxe de transfert.