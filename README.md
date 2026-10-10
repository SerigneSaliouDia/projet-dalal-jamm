# Projet Dalal Jamm — IA appliquée à la mammographie

Projet de Master 2 *Ingénierie des Données et Intelligence Artificielle*, réalisé avec le **CHN Dalal Jamm** (Sénégal).
Équipe : **Saliou**, **Manou**, **Babel**.

> ⚠️ **Aide à la décision.** Ce système assiste le radiologue ; il ne le remplace pas et ne pose aucun diagnostic.
> ⚠️ **Aucune donnée patiente dans ce dépôt.** Lire `CONFIDENTIALITE.md` avant toute chose.

## Objectif

Il ne s'agit pas d'une simple classification « cancer / pas cancer ». Le but final est de produire,
à partir des mammographies, un compte rendu radiologique structuré :

```
IMAGES DE MAMMOGRAPHIE
   -> analyse IA
   -> détection / caractéristiques (masse, calcifications, asymétrie, distorsion, adénopathie...)
   -> interprétation
   -> BI-RADS
   -> conclusion
   -> recommandation
   -> COMPTE RENDU STRUCTURÉ
```

## Données (non versionnées)

| Source | Format | Contenu |
|---|---|---|
| Images | DICOM / `.IMA` | Vues CC et MLO, sein droit et gauche (≈ 1965 fichiers, ≈ 231 examens) |
| Comptes rendus | `.docx` | ≈ 283 rapports : densité, signes, écho, BI-RADS, conclusion, recommandation |

Ces chiffres viennent d'explorations préliminaires et **doivent être revalidés** dans les sprints 1 et 2.
Le lien rapport ↔ examen n'est **pas** supposé : il est étudié au sprint 3.

## Principes de qualité des données

1. **Correctitude des données > organisation du code > rapidité.**
2. Une **absence reste une absence** : « absence de masse » ne devient jamais `masse = 1`.
3. Trois états par signe : `1` présent, `0` absence écrite dans le rapport, vide = non mentionné.
4. Chaque variable extraite garde sa **phrase source** (colonnes `evidence_*`).
5. Le texte original du radiologue est **conservé** (conclusion, observations).
6. Les BI-RADS gardent leur **latéralité** (droite / gauche).
7. On ne devine jamais une correspondance rapport ↔ images qui n'est pas démontrée.
8. Aucun terme médical n'est converti automatiquement en label (opacité ≠ masse, anomalie écho ≠ kyste).

## Structure du dépôt

```
projet-dalal-jamm/
├── README.md              <- ce fichier
├── TICKETS.md             <- les 17 sprints et leurs tâches
├── CONTRIBUTING.md        <- règles de travail : branches, commits, PR
├── CONFIDENTIALITE.md     <- règles sur les données patientes
├── docs/                  <- guides, décisions (ADR), dictionnaire de données
├── src/dalal_jamm/        <- le code (dicom, reports, linking, dataset, imaging, models, evaluation, generation)
├── notebooks/             <- notebooks courts : exploration et contrôles (sans sortie)
├── tests/                 <- tests automatiques (pytest)
├── scripts/               <- outils en ligne de commande
├── app/                   <- démo (sprint 15)
├── data/                  <- LOCAL SEULEMENT, ignoré par Git
├── .github/               <- CI, modèles de PR et d'issues
└── .vscode/               <- réglages VS Code recommandés
```

## Installation (VS Code, Windows / macOS / Linux)

Prérequis : [Git](https://git-scm.com/downloads), [Python 3.11](https://www.python.org/downloads/), [VS Code](https://code.visualstudio.com/).

```bash
git clone https://github.com/<organisation-ou-compte>/projet-dalal-jamm.git
cd projet-dalal-jamm

python -m venv .venv
# Windows (PowerShell) :  .venv\Scripts\Activate.ps1
# macOS / Linux        :  source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
nbstripout --install        # efface les sorties des notebooks avant chaque commit

# Indiquer où sont VOS données (variables d'environnement, voir .env.example)
python scripts/check_env.py
pytest
```

Dans VS Code : *Ctrl+Shift+P* → « Python: Select Interpreter » → choisir `.venv`. Acceptez l'installation des
extensions recommandées (fenêtre en bas à droite).

## Méthode de travail

> **Nouveau dans l'équipe ?** Commence par `docs/onboarding.md` (installation, première PR, cycle de la semaine).

- **Un sprint = une semaine**, 2 à 4 tâches par personne (voir `TICKETS.md`).
- Chaque personne travaille sur une branche `sprint-NN/prenom` et ouvre **une PR par sprint**.
- Une PR est relue par un autre membre, puis **fusionnée dans `main` par Saliou**.
- La CI (tests + lint) doit être verte avant la fusion.
- Détails : `CONTRIBUTING.md` et `docs/guide_git_debutant.md`.

## Feuille de route

| Phase | Sprints | Contenu |
|---|---|---|
| Cadre | S0 | Dépôt, environnement, cadre éthique |
| Données images | S1 | Inventaire DICOM |
| Données rapports | S2 | Lecture DOCX, pseudonymisation |
| Association | S3 | Rapports ↔ examens (étude de faisabilité) |
| Extraction | S4 – S7 | Sections, BI-RADS, signes, écho, conclusion |
| Validation | S8 | Échantillon annoté, précision mesurée |
| Dataset | S9 – S10 | Dataset final, analyse, décision de faisabilité |
| IA | S11 – S14 | Prétraitement, baseline, multi-vues, évaluation |
| Rapport | S15 | Génération du compte rendu |
| Clôture | S16 | Mémoire, soutenance, `v1.0.0` |

Le choix du modèle n'est **pas fixé à l'avance** : il dépendra de ce que les données permettent (ADR-002, sprint 10).
