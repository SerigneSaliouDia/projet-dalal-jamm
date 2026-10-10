# Dossier `data/` (non versionné)

**Rien de ce dossier, à part ce fichier, n'est suivi par Git.** Les DICOM et les comptes rendus sont
des données de santé identifiantes (voir `CONFIDENTIALITE.md`).

## Organisation locale conseillée

```
data/
├── raw/
│   ├── dicom/        <- fichiers .IMA / .dcm (lecture seule, jamais modifiés)
│   └── reports/      <- comptes rendus .docx (lecture seule)
├── interim/          <- résultats intermédiaires (inventaires, texte extrait)
├── processed/        <- tableaux structurés, dataset final (avec exam_id uniquement)
├── private/          <- table exam_id <-> identité, SEULEMENT ici, jamais partagée
└── outputs/          <- figures, résultats, modèles
```

Les dossiers `interim/`, `processed/`, `private/` et `outputs/` sont créés par
`dalal_jamm.config.ensure_dirs()`.

## Si vos données sont ailleurs (ex. `C:\MAMMO`)

Ne les déplacez pas : indiquez leur emplacement avec des variables d'environnement (voir `.env.example`),
par exemple `DALAL_REPORTS_DIR=C:\MAMMO\rapport`.

## Où récupérer les données

Auprès de Saliou, via le canal partagé convenu entre vous (à décrire ici sans mettre de lien public).
