# Notes sur les DICOM

## Chiffres validés (inventaires du 10/10/2026)

| Mesure | Valeur préliminaire | Valeur validée |
|---|---|---|
| Fichiers `.IMA` | ≈ 1965 | **2254** (dont 38 aux chemins ≥ 260 caractères, lisibles via `\\?\`) |
| Dossiers patientes | – | 269 (3 sans fichier, donc 266 avec images) |
| Dossiers d'examen | ≈ 231 | 271 (3 sans fichier, donc **268 examens**, 1 UID d'étude chacun) |
| Séries | – | 533 : 268 brutes (`FOR PROCESSING`, 1131 images), 265 traitées (`FOR PRESENTATION`, 1123 images) |
| Fichiers lus (en-tête) | ≈ 970 | **2254 / 2254** (aucune erreur ; tous non compressés, Explicit VR Little Endian) |
| Examens complets | ≈ 200 | **232** (séries traitée et brute complètes) |
| Examens incomplets ou sans série traitée | ≈ 31 | 36 (dont 3 sans série traitée) |

## Constats

- Un seul appareil : Siemens Mammomat Inspiration, modalité `MG`.
- `MAMMOGRAM_RAW_DIAGNOSIS_0001` = images brutes (`FOR PROCESSING`, `ORIGINAL`) ; `MAMMOGRAM_DIAGNOSIS_0002` = images traitées (`FOR PRESENTATION`, `DERIVED`). Série retenue pour le modèle : à décider (ADR-002).
- Aucun numéro d'accès (vide dans les 2254 fichiers).
- 1 dossier d'examen = 1 `StudyInstanceUID` ; 1 dossier patiente = 1 numéro patient ; aucune image en double.
- Dates d'étude : de 20240510 à 20260508. À comparer avec la date du dossier et celle du rapport (sprint 3).
- Deux formats d'image : 3518 x 2800 (2224 images) et 2800 x 2082 (30 images).
- Vues non standard par série : LMO 7, ML 5, XCC 6 ; 14 examens concernés.
- 33 séries traitées incomplètes, dont 19 n'ont qu'un sein (D-CC+D-MLO manquent : 8 ; G-CC+G-MLO : 11). Hypothèse : examens unilatéraux, à vérifier avec les rapports.
- 3 examens sans série traitée. 1 examen sur 265 a un nombre d'images différent entre séries brute et traitée.

## Définition de la complétude

Une série est **complète** si elle contient au moins une image pour chacune des 4 vues D-CC, D-MLO, G-CC, G-MLO.
Les répétitions d'une vue et les vues non standard (LMO, ML, XCC) ne rendent pas une série incomplète,
mais une vue non standard ne remplace jamais une vue manquante. Un examen est complet si ses séries le sont.

## Causes d'échec de lecture

| N° | Cause | Fichiers | Solution |
|---|---|---|---|
| 1 | Chemin de 260 caractères ou plus (limite Windows) | 38 | Préfixe `\\?\` via `dalal_jamm.utils.fs.extended_path()` |

Aucune autre cause : tous les en-têtes sont lisibles.

## Questions ouvertes pour un radiologue

1. Une vue LMO, ML ou XCC peut-elle remplacer une MLO ou une CC manquante ? (Aujourd'hui : non.)
2. Les examens à un seul sein sont-ils des examens unilatéraux voulus ?
3. Quelle série (brute ou traitée) le radiologue lit-il pour rédiger son compte rendu ?
4. Les images répétées d'une même vue sont-elles des reprises après un défaut technique ?

## Champs d'en-tête utiles

`ImageLaterality`, `ViewPosition`, `SeriesDescription`, `StudyInstanceUID`, `SeriesInstanceUID`,
`StudyDate`, `PresentationIntentType`, `Rows`, `Columns`, syntaxe de transfert.