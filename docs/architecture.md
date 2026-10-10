# Architecture du projet

## Flux de données

```
DOCX (rapports) --reader--> texte original --normalize--> texte normalisé
                                   |                           |
                                   |                       sections
                                   |                           |
                                   |        signes / densité / BI-RADS / écho / conclusion
                                   v                           v
                         champs descriptifs (texte original)   champs structurés (1 / 0 / vide)
                                                   \         /
                                                    reports_structured_vN.csv
DICOM (images) --inventory--> en-têtes --views / exams--> examens (D-CC, D-MLO, G-CC, G-MLO)
                                                                |
                         linking (association DÉMONTRÉE) <------+
                                   |
                              dataset final (1 ligne = 1 exam_id)
                                   |
                       préparation IA -> modèle -> évaluation -> génération du compte rendu
```

## Modélisation (à décider au sprint 10, ADR-002)

```
image -> détection / caractéristiques
      -> caractéristiques -> interprétation / BI-RADS
      -> interprétation -> génération du compte rendu (par gabarit)
```

## Modules

| Package | Rôle |
|---|---|
| `dicom` | Inventaire, en-têtes, vues, examens |
| `reports` | Lecture DOCX, normalisation, sections, extraction |
| `linking` | Association rapports ↔ examens |
| `dataset` | Dataset final, qualité, découpage par patiente |
| `imaging` | Prétraitement, augmentation, datasets |
| `models` | Baseline, multi-vues, entraînement |
| `evaluation` | Métriques, évaluation du compte rendu |
| `generation` | Gabarit, génération |
| `utils` | Pseudonymisation |
