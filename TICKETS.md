# TICKETS — plan de travail par sprint

Équipe : **Saliou** (SA), **Manou** (MA), **Babel** (BA). Un sprint = une semaine.

> Les dates sont **proposées** (démarrage le lundi 12 octobre 2026) : ajustez-les à votre calendrier. Si une tâche glisse, elle passe au sprint suivant : **ne jamais dépasser ~10 h par personne et par semaine** (2 h/jour × 5 jours).

## Comment lire ce fichier

- Identifiant : `S<sprint>-<SA|MA|BA>-<n>` (ex. `S5-SA-1`). Les tâches communes sont `S<sprint>-ALL-<n>`.
- Une case se coche **dans la PR** qui livre la tâche.
- Chaque personne travaille sur sa branche de sprint : `sprint-NN/prenom` (ex. `sprint-05/manou`) et ouvre **une PR par sprint**. Saliou fusionne dans `main` après relecture d'un autre membre.
- Les rôles sont une **répartition de départ** : n'importe qui peut échanger une tâche si c'est noté dans la PR.

## Rituels hebdomadaires

| Moment | Durée | Contenu |
|---|---|---|
| Lundi | 30 min | Planification : lecture des tickets, questions, blocages |
| Mercredi | 15 min | Point d'étape (ou message écrit dans le groupe) |
| Vendredi | 30 min | Revue : démo de ce qui est fait, relecture croisée des PR, merge par Saliou |

## Définition de « terminé » (valable pour chaque sprint)

- [ ] Tests passent en local et en CI (`pytest`, `ruff check src tests scripts`)
- [ ] Tests `xfail` satisfaits : marqueur retiré
- [ ] Aucune donnée patiente dans la PR (voir checklist du modèle de PR)
- [ ] Notebooks sans sortie (`nbstripout`)
- [ ] Documentation et `TICKETS.md` à jour
- [ ] PR relue par un autre membre que son auteur, puis fusionnée par Saliou

## Vue d'ensemble

| Sprint | Semaine du | Thème |
|---|---|---|
| S0 | 12/10/2026 | Mise en place |
| S1 | 19/10/2026 | Inventaire DICOM |
| S2 | 26/10/2026 | Inventaire des rapports et pseudonymisation |
| S3 | 02/11/2026 | Association rapports ↔ examens (étude) |
| S4 | 09/11/2026 | Banc de tests et découpage en sections |
| S5 | 16/11/2026 | BI-RADS et densité |
| S6 | 23/11/2026 | Signes radiologiques à 3 états |
| S7 | 30/11/2026 | Échographie, conclusion et recommandations |
| S8 | 07/12/2026 | Validation par échantillon annoté |
| S9 | 14/12/2026 | Pipeline complet et dataset final |
| S10 | 21/12/2026 | Analyse des données et décision de faisabilité |
| S11 | 28/12/2026 | Prétraitement des images et découpage |
| S12 | 04/01/2027 | Modèle de référence (baseline) |
| S13 | 11/01/2027 | Modélisation améliorée |
| S14 | 18/01/2027 | Évaluation complète |
| S15 | 25/01/2027 | Génération du compte rendu |
| S16 | 01/02/2027 | Finalisation |

Durée prévue : **17 semaines** (jusqu'au 05/02/2027), soit environ 4 mois. Les sprints 12 à 15 pourront être modifiés après la décision de faisabilité du sprint 10.

---

## Sprint 0 — Mise en place

**Semaine du 12/10/2026**

**Objectif :** Tout le monde peut cloner, installer, lancer les tests et ouvrir une PR. Le cadre éthique est clarifié.

**Livrables :**
- Dépôt GitHub privé avec `main` protégée
- CI verte
- Environnement VS Code fonctionnel sur 3 machines
- Réponse écrite sur l'usage des données (hors Git)

### Tâches communes

- [ ] **S0-ALL-1** — Installer l'environnement : Git, Python 3.11, VS Code + extensions, venv, `pip install -r requirements.txt`, `pip install -e .`, `pytest` (chacun) · ~2 h
- [ ] **S0-ALL-2** — Placer les données en local hors Git et définir `DALAL_*` ; `python scripts/check_env.py` doit compter les fichiers (chacun) · ~1 h

### Saliou — branche `sprint-00/saliou` (~8 h)

- [ ] **S0-SA-1** — Créer le dépôt privé `projet-dalal-jamm`, pousser le squelette, protéger `main` (guide `docs/guide_git_debutant.md`) · ~2 h
- [ ] **S0-SA-2** — Inviter Manou et Babel, créer le tableau GitHub Projects (À faire / En cours / En revue / Fait) et les labels · ~1 h
- [ ] **S0-SA-3** — Vérifier l'autorisation d'usage des données auprès du CHN (qui, quoi, où) et consigner la réponse HORS Git · ~2 h

### Manou — branche `sprint-00/manou` (~9 h)

- [ ] **S0-MA-1** — Vérifier que la CI GitHub Actions passe au vert sur la première PR, corriger si besoin · ~2 h
- [ ] **S0-MA-2** — Installer `nbstripout` sur les 3 machines (procédure dans `CONTRIBUTING.md`) et la tester · ~2 h
- [ ] **S0-MA-3** — Fiabiliser `scripts/check_env.py` (versions, dossiers, comptages sans noms de patientes) · ~2 h

### Babel — branche `sprint-00/babel` (~10 h)

- [ ] **S0-BA-1** — Faire une PR d'essai en suivant `docs/guide_git_debutant.md` à la lettre et corriger les étapes peu claires · ~2 h
- [ ] **S0-BA-2** — Compléter `docs/data_dictionary.md` à partir de la liste des variables du notebook archivé · ~3 h
- [ ] **S0-BA-3** — Compléter `docs/glossaire.md` (BI-RADS, ACR, CC/MLO, densité A-D...) · ~2 h

---

## Sprint 1 — Inventaire DICOM

**Semaine du 19/10/2026**

**Objectif :** Savoir exactement ce que contiennent les 1965 fichiers : lisibles, illisibles (et pourquoi), examens complets ou non.

**Livrables :**
- `data/interim/dicom_inventory.csv` (hors Git)
- Synthèse chiffrée dans `docs/dicom_notes.md`
- Liste des échecs de lecture classés par cause

### Saliou — branche `sprint-01/saliou` (~8 h)

- [ ] **S1-SA-1** — `dicom/inventory.py` : parcours récursif (.IMA, .dcm, sans extension), 1 ligne par fichier · ~3 h
- [ ] **S1-SA-2** — Exécuter `notebooks/01_inventaire_dicom.ipynb` sur toutes les données et résumer · ~3 h
- [ ] **S1-SA-3** — Tableau de synthèse (trouvés / lus / échecs / examens) dans `docs/dicom_notes.md` · ~2 h

### Manou — branche `sprint-01/manou` (~10 h)

- [ ] **S1-MA-1** — `dicom/metadata.py` : lecture des en-têtes sans pixels (UID, date, latéralité, vue, série, dimensions, syntaxe de transfert) · ~4 h
- [ ] **S1-MA-2** — Tests unitaires avec un DICOM synthétique créé par pydicom · ~3 h
- [ ] **S1-MA-3** — `dicom/views.py` : identification CC/MLO et D/G, cas non identifiables listés (ne jamais deviner) · ~3 h

### Babel — branche `sprint-01/babel` (~9 h)

- [ ] **S1-BA-1** — Classer les échecs de lecture (écart 1965 vs 970) : cause et solution · ~4 h
- [ ] **S1-BA-2** — Documenter les cas particuliers dans `docs/dicom_notes.md` · ~2 h
- [ ] **S1-BA-3** — `dicom/exams.py` : regroupement par examen et détection des examens complets/incomplets · ~3 h

---

## Sprint 2 — Inventaire des rapports et pseudonymisation

**Semaine du 26/10/2026**

**Objectif :** Lire les 283 DOCX proprement, repérer doublons et rapports multiples, et séparer l'identité du reste (exam_id).

**Livrables :**
- `reports/reader.py` testé
- `data/interim/reports_inventory.csv`
- Table de correspondance privée (`data/private/`)

### Saliou — branche `sprint-02/saliou` (~8 h)

- [ ] **S2-SA-1** — `reports/reader.py` : texte dans l'ordre du document (paragraphes + tableaux), cellules fusionnées dédupliquées · ~4 h
- [ ] **S2-SA-2** — Tester sur 10 DOCX variés et noter les cas problématiques · ~2 h
- [ ] **S2-SA-3** — Export du texte brut original des 283 rapports vers `data/interim/` (hors Git) · ~2 h

### Manou — branche `sprint-02/manou` (~7 h)

- [ ] **S2-MA-1** — `utils/privacy.py` : `make_exam_id` stable avec sel secret et table de correspondance dans `data/private/` · ~4 h
- [ ] **S2-MA-2** — Tests de `privacy.py` (stabilité, non-réversibilité, aucune écriture hors `private/`) · ~2 h
- [ ] **S2-MA-3** — Définir le format et la sauvegarde de la table de correspondance privée · ~1 h

### Babel — branche `sprint-02/babel` (~8 h)

- [ ] **S2-BA-1** — Inventaire des DOCX : nombre, doublons de nom, vides/illisibles, rapports multiples · ~4 h
- [ ] **S2-BA-2** — Documenter les cas particuliers (`docs/extraction_rules.md`) · ~2 h
- [ ] **S2-BA-3** — Vérifier à la main 15 rapports multiples ou en doublon · ~2 h

---

## Sprint 3 — Association rapports ↔ examens (étude)

**Semaine du 02/11/2026**

**Objectif :** Démontrer (ou non) comment relier un rapport à un examen. Rien n'est supposé : tout est mesuré.

**Livrables :**
- `docs/linking_study.md`
- Rapport de couverture chiffré
- ADR-001 : association validée, partielle ou impossible

### Tâches communes

- [ ] **S3-ALL-1** — Réunion de décision et rédaction de l'ADR-001 dans `docs/decisions.md` (tous) · ~1 h

### Saliou — branche `sprint-03/saliou` (~8 h)

- [ ] **S3-SA-1** — Extraction fiable du nom et de la date d'examen des rapports (écart nom du fichier / nom dans le document, date du fichier / date du texte) · ~4 h
- [ ] **S3-SA-2** — Lister les identifiants DICOM disponibles (PatientName, PatientID, StudyDate, AccessionNumber...) et leur taux de remplissage · ~3 h

### Manou — branche `sprint-03/manou` (~10 h)

- [ ] **S3-MA-1** — `linking/matching.py` : normalisation des noms (accents, casse, ordre prénom/nom), clé nom + date, correspondance exacte · ~4 h
- [ ] **S3-MA-2** — Tests du matching (accents, inversions, espaces, homonymes) · ~2 h
- [ ] **S3-MA-3** — Correspondance approchée avec seuil ; sous le seuil = NON associé, jamais automatique · ~3 h

### Babel — branche `sprint-03/babel` (~9 h)

- [ ] **S3-BA-1** — `linking/coverage.py` : rapports sans examen, examens sans rapport, correspondances multiples ou ambiguës · ~4 h
- [ ] **S3-BA-2** — Relire à la main 30 correspondances · ~2 h
- [ ] **S3-BA-3** — Rédiger `docs/linking_study.md` · ~2 h

---

## Sprint 4 — Banc de tests et découpage en sections

**Semaine du 09/11/2026**

**Objectif :** Écrire les tests AVANT les extracteurs et découper les rapports en sections, indépendamment de l'ordre.

**Livrables :**
- Tests négation et BI-RADS enrichis
- `reports/normalize.py`
- `reports/sections.py` (ordre inversé, rapports multiples)

### Saliou — branche `sprint-04/saliou` (~8 h)

- [ ] **S4-SA-1** — Enrichir `tests/test_negation.py` avec les cas de l'audit et de vrais exemples anonymisés · ~3 h
- [ ] **S4-SA-2** — `reports/normalize.py` : recherche sur le normalisé, stockage sur l'original · ~3 h
- [ ] **S4-SA-3** — Tests de sections (ordre inversé, rapports multiples) · ~2 h

### Manou — branche `sprint-04/manou` (~8 h)

- [ ] **S4-MA-1** — `reports/sections.py` : découpage par position des en-têtes (densité, sein D/G, écho, conclusion) · ~5 h
- [ ] **S4-MA-2** — Découpage des rapports multiples dans un même fichier · ~3 h

### Babel — branche `sprint-04/babel` (~7 h)

- [ ] **S4-BA-1** — Enrichir `tests/test_birads.py` (latéralisés, romains, 4A-4C, contradictions) · ~3 h
- [ ] **S4-BA-2** — Créer 30 rapports FICTIFS de référence dans `tests/fixtures/` · ~3 h
- [ ] **S4-BA-3** — Enrichir `tests/test_density.py` (D différent de G) · ~1 h

---

## Sprint 5 — BI-RADS et densité

**Semaine du 16/11/2026**

**Objectif :** Extraire BI-RADS (global, droit, gauche) et densité par sein, sans jamais recopier une valeur sur l'autre côté.

**Livrables :**
- `reports/birads.py` (tests verts)
- `reports/density.py`
- Audit des 283 rapports : cas ambigus listés

### Saliou — branche `sprint-05/saliou` (~8 h)

- [ ] **S5-SA-1** — `reports/birads.py` : segmentation autour de chaque ACR, côté le plus proche dans le même segment · ~6 h
- [ ] **S5-SA-2** — Cas particuliers : droit/droite/sein droit, chiffres romains, 4A-4C, caractères parasites · ~2 h

### Manou — branche `sprint-05/manou` (~8 h)

- [ ] **S5-MA-1** — Contradictions et cohérence (même côté, valeurs divergentes) ; champ `note` · ~3 h
- [ ] **S5-MA-2** — `reports/density.py` : densité par sein, sans recopie · ~3 h
- [ ] **S5-MA-3** — Règles de calcul de `birads_global` documentées dans `docs/extraction_rules.md` · ~2 h

### Babel — branche `sprint-05/babel` (~8 h)

- [ ] **S5-BA-1** — Audit BI-RADS sur les 283 rapports : export des cas ambigus ou contradictoires · ~3 h
- [ ] **S5-BA-2** — Relecture manuelle des cas exportés et ajout des cas aux tests · ~3 h
- [ ] **S5-BA-3** — Tableau des contradictions à faire valider par un radiologue · ~2 h

---

## Sprint 6 — Signes radiologiques à 3 états

**Semaine du 23/11/2026**

**Objectif :** Masse, calcification, distorsion, asymétrie, adénopathie, rétraction : 1 / 0 / non mentionné, avec la phrase source.

**Livrables :**
- `reports/negation.py` et `reports/signs.py` (tests verts)
- Colonnes `evidence_*`
- Règles écrites dans `docs/extraction_rules.md`

### Saliou — branche `sprint-06/saliou` (~7 h)

- [ ] **S6-SA-1** — `reports/negation.py` : portée de la négation (listes coordonnées, « mais », « sans », « avec ») · ~5 h
- [ ] **S6-SA-2** — Cas limites : « sans… mais présence de… », négation sur plusieurs propositions · ~2 h

### Manou — branche `sprint-06/manou` (~8 h)

- [ ] **S6-MA-1** — `reports/signs.py` : signes par côté avec 3 états · ~6 h
- [ ] **S6-MA-2** — Colonnes `evidence_<signe>_<côté>` (phrase originale déclenchante) · ~2 h

### Babel — branche `sprint-06/babel` (~8 h)

- [ ] **S6-BA-1** — Test de non-régression : comparer ancienne et nouvelle extraction sur les 283 et lister les différences · ~3 h
- [ ] **S6-BA-2** — Règles écrites (opacité ≠ masse, etc.) dans `docs/extraction_rules.md` · ~3 h
- [ ] **S6-BA-3** — Liste des termes ambigus à faire valider par un radiologue (opacité, ganglion, plage...) · ~2 h

---

## Sprint 7 — Échographie, conclusion et recommandations

**Semaine du 30/11/2026**

**Objectif :** Structurer le complément échographique, conserver la conclusion originale et extraire les recommandations.

**Livrables :**
- `reports/echo.py`
- `reports/conclusion.py`
- `reports/measurements.py`

### Saliou — branche `sprint-07/saliou` (~8 h)

- [ ] **S7-SA-1** — `reports/echo.py` : lésions par côté, descriptions, caractéristiques (sans tout transformer en kyste) · ~6 h
- [ ] **S7-SA-2** — Tests de l'écho (kyste, galactocèle, ectasie, formation, adénopathie) · ~2 h

### Manou — branche `sprint-07/manou` (~8 h)

- [ ] **S7-MA-1** — `reports/conclusion.py` : conclusion en texte original, recommandation sans détruire la conclusion · ~5 h
- [ ] **S7-MA-2** — Retirer les noms de médecins codés en dur du code (passer par un fichier de config) · ~1 h
- [ ] **S7-MA-3** — Tests de conclusion (recommandations multiples) · ~2 h

### Babel — branche `sprint-07/babel` (~8 h)

- [ ] **S7-BA-1** — `reports/measurements.py` : dimensions, quadrant, heure, distance au mamelon · ~4 h
- [ ] **S7-BA-2** — Tests des mesures · ~2 h
- [ ] **S7-BA-3** — Documenter les formulations rares rencontrées · ~2 h

---

## Sprint 8 — Validation par échantillon annoté

**Semaine du 07/12/2026**

**Objectif :** Mesurer la précision réelle de l'extraction face à une annotation manuelle.

**Livrables :**
- Échantillon stratifié de 50 rapports
- `docs/annotation_guide.md`
- Rapport de précision par champ

### Tâches communes

- [ ] **S8-ALL-1** — Corriger les 5 erreurs les plus fréquentes (chacun une) · ~2 h

### Saliou — branche `sprint-08/saliou` (~8 h)

- [ ] **S8-SA-1** — Constituer un échantillon stratifié de 50 rapports (BI-RADS, négations, écho, bilatéral...) · ~2 h
- [ ] **S8-SA-2** — Rédiger `docs/annotation_guide.md` (définitions, 3 états, cas limites) · ~2 h
- [ ] **S8-SA-3** — Obtenir un créneau avec un radiologue pour relire 20 rapports · ~2 h

### Manou — branche `sprint-08/manou` (~9 h)

- [ ] **S8-MA-1** — Script de comparaison extraction vs annotation : précision, rappel par champ · ~4 h
- [ ] **S8-MA-2** — Rapport d'erreurs par champ (CSV ou markdown) · ~3 h

### Babel — branche `sprint-08/babel` (~9 h)

- [ ] **S8-BA-1** — Annoter l'échantillon manuellement · ~5 h
- [ ] **S8-BA-2** — Double annotation de 15 rapports avec Saliou, mesure de l'accord · ~2 h

---

## Sprint 9 — Pipeline complet et dataset final

**Semaine du 14/12/2026**

**Objectif :** Produire un tableau structuré versionné, puis le dataset par examen avec ses contrôles qualité.

**Livrables :**
- `reports_structured_v1.csv`
- `dataset/build.py`
- Rapport qualité automatique
- `docs/data_dictionary.md` final

### Saliou — branche `sprint-09/saliou` (~7 h)

- [ ] **S9-SA-1** — `reports/pipeline.py` : lecture → extraction → validation → CSV versionné · ~5 h
- [ ] **S9-SA-2** — CLI `python -m dalal_jamm.reports.pipeline` et règle de versionnage des CSV · ~2 h

### Manou — branche `sprint-09/manou` (~7 h)

- [ ] **S9-MA-1** — `dataset/build.py` : jointure exam_id ↔ chemins images (D-CC, D-MLO, G-CC, G-MLO) + labels · ~5 h
- [ ] **S9-MA-2** — Tests de `build.py` sur données fictives · ~2 h

### Babel — branche `sprint-09/babel` (~8 h)

- [ ] **S9-BA-1** — `dataset/quality.py` : manquants, incohérences signes/conclusion, doublons, examens incomplets · ~4 h
- [ ] **S9-BA-2** — Rapport qualité automatique (markdown) · ~2 h
- [ ] **S9-BA-3** — Finaliser `docs/data_dictionary.md` · ~2 h

---

## Sprint 10 — Analyse des données et décision de faisabilité

**Semaine du 21/12/2026**

**Objectif :** Savoir ce que les données permettent vraiment de modéliser avant de choisir une architecture.

**Livrables :**
- Graphiques de distribution
- Effectifs utilisables par tâche
- ADR-002 : tâches de modélisation retenues

### Tâches communes

- [ ] **S10-ALL-1** — Décision go / no-go sur les tâches de modélisation et rédaction de l'ADR-002 (tous) · ~1 h

### Saliou — branche `sprint-10/saliou` (~7 h)

- [ ] **S10-SA-1** — Distributions BI-RADS, signes, par sein · ~4 h
- [ ] **S10-SA-2** — Graphiques et tableaux dans `notebooks/05_dataset_analyse.ipynb` · ~2 h

### Manou — branche `sprint-10/manou` (~8 h)

- [ ] **S10-MA-1** — Examens complets / incomplets, effectifs utilisables · ~4 h
- [ ] **S10-MA-2** — Effectifs par tâche (binaire bénin/suspect, signes multi-label, BI-RADS regroupé) · ~3 h

### Babel — branche `sprint-10/babel` (~8 h)

- [ ] **S10-BA-1** — Note de faisabilité : quelles tâches sont réalistes avec ces effectifs · ~4 h
- [ ] **S10-BA-2** — Préparer la présentation à l'encadrant · ~2 h
- [ ] **S10-BA-3** — Mettre à jour `README.md` et `TICKETS.md` selon ADR-002 · ~1 h

---

## Sprint 11 — Prétraitement des images et découpage

**Semaine du 28/12/2026**

**Objectif :** Images exploitables et jeux train/validation/test séparés par patiente.

**Livrables :**
- `imaging/preprocessing.py`
- `dataset/split.py`
- Contrôle visuel documenté

### Saliou — branche `sprint-11/saliou` (~6 h)

- [ ] **S11-SA-1** — `dataset/split.py` : split train/val/test PAR PATIENTE, stratifié, fixé et sauvegardé · ~4 h
- [ ] **S11-SA-2** — Test : aucune patiente dans deux jeux · ~2 h

### Manou — branche `sprint-11/manou` (~8 h)

- [ ] **S11-MA-1** — `imaging/preprocessing.py` : DICOM → tableau, MONOCHROME1/2, normalisation, recadrage, redimensionnement · ~6 h
- [ ] **S11-MA-2** — Tests sur DICOM synthétique · ~2 h

### Babel — branche `sprint-11/babel` (~8 h)

- [ ] **S11-BA-1** — Contrôle visuel de 50 exemples par vue (orientation, miroir, D/G, CC/MLO) · ~4 h
- [ ] **S11-BA-2** — `imaging/augmentation.py` : augmentations cliniquement plausibles · ~2 h
- [ ] **S11-BA-3** — Documenter les artefacts rencontrés (marqueurs, annotations incrustées) · ~2 h

---

## Sprint 12 — Modèle de référence (baseline)

**Semaine du 04/01/2027**

**Objectif :** Un premier modèle simple, mesuré correctement, pour savoir d'où l'on part.

**Livrables :**
- Baseline entraînée
- `evaluation/metrics.py`
- Journal d'expériences

### Saliou — branche `sprint-12/saliou` (~7 h)

- [ ] **S12-SA-1** — `models/baseline.py` : baseline simple sur la tâche fixée par l'ADR-002 · ~5 h
- [ ] **S12-SA-2** — Journal d'expériences (tableau avec seed, config, métriques) · ~2 h

### Manou — branche `sprint-12/manou` (~7 h)

- [ ] **S12-MA-1** — `imaging/datasets.py` : Dataset/DataLoader multi-vues (CC + MLO par sein) · ~5 h
- [ ] **S12-MA-2** — Tests du Dataset · ~2 h

### Babel — branche `sprint-12/babel` (~7 h)

- [ ] **S12-BA-1** — `evaluation/metrics.py` : AUC, sensibilité, spécificité, F1 par classe, matrice de confusion, IC bootstrap · ~4 h
- [ ] **S12-BA-2** — Tests des métriques sur cas jouets · ~2 h
- [ ] **S12-BA-3** — Politique de calcul : Colab/Kaggle interdits pour des données patientes sans autorisation écrite · ~1 h

---

## Sprint 13 — Modélisation améliorée

**Semaine du 11/01/2027**

**Objectif :** Améliorer la baseline : transfert, fusion de vues, gestion du déséquilibre.

**Livrables :**
- Modèle pré-entraîné
- Modèle multi-vues
- Validation croisée par patiente

### Saliou — branche `sprint-13/saliou` (~8 h)

- [ ] **S13-SA-1** — Transfert learning (CNN pré-entraîné) sur une vue · ~6 h
- [ ] **S13-SA-2** — `models/train.py` reproductible (seed, config sauvegardée) · ~2 h

### Manou — branche `sprint-13/manou` (~8 h)

- [ ] **S13-MA-1** — `models/multiview.py` : fusion CC + MLO · ~6 h
- [ ] **S13-MA-2** — Ablation : 1 vue contre 2 vues · ~2 h

### Babel — branche `sprint-13/babel` (~8 h)

- [ ] **S13-BA-1** — Gestion du déséquilibre (poids de classe, rééchantillonnage) · ~5 h
- [ ] **S13-BA-2** — Validation croisée par patiente · ~3 h

---

## Sprint 14 — Évaluation complète

**Semaine du 18/01/2027**

**Objectif :** Évaluer séparément la détection des signes, le BI-RADS et le côté ; ne pas se limiter à l'accuracy.

**Livrables :**
- Tableaux de résultats
- Analyse d'erreurs
- Revue clinique d'un échantillon d'erreurs

### Saliou — branche `sprint-14/saliou` (~6 h)

- [ ] **S14-SA-1** — Évaluation de la détection des signes par signe et par côté · ~4 h
- [ ] **S14-SA-2** — Tableaux de résultats reproductibles · ~2 h

### Manou — branche `sprint-14/manou` (~6 h)

- [ ] **S14-MA-1** — Évaluation du BI-RADS : par classe, kappa pondéré, erreurs à ±1 · ~4 h
- [ ] **S14-MA-2** — Matrices de confusion et analyse des confusions · ~2 h

### Babel — branche `sprint-14/babel` (~9 h)

- [ ] **S14-BA-1** — Analyse d'erreurs : cas manqués, faux positifs · ~4 h
- [ ] **S14-BA-2** — Cartes d'attention (Grad-CAM) sur des cas types · ~3 h
- [ ] **S14-BA-3** — Revue de 30 erreurs avec un radiologue · ~2 h

---

## Sprint 15 — Génération du compte rendu

**Semaine du 25/01/2027**

**Objectif :** Produire un compte rendu structuré à partir des prédictions, avec règles explicites et mention d'aide au radiologue.

**Livrables :**
- `generation/template.py`
- `generation/report_generator.py`
- Démo minimale
- Évaluation des comptes rendus générés

### Saliou — branche `sprint-15/saliou` (~8 h)

- [ ] **S15-SA-1** — `generation/template.py` : gabarit de compte rendu à partir des champs structurés · ~5 h
- [ ] **S15-SA-2** — Règles de recommandation par BI-RADS, explicites et validées par un radiologue · ~3 h

### Manou — branche `sprint-15/manou` (~8 h)

- [ ] **S15-MA-1** — `generation/report_generator.py` : prédictions → BI-RADS → conclusion → recommandation → compte rendu · ~4 h
- [ ] **S15-MA-2** — Démo minimale dans `app/` (image → compte rendu) · ~4 h

### Babel — branche `sprint-15/babel` (~8 h)

- [ ] **S15-BA-1** — `evaluation/report_eval.py` : concordance champ par champ et cohérence interne · ~4 h
- [ ] **S15-BA-2** — Mention « aide à la décision, ne remplace pas le radiologue » dans toutes les sorties · ~1 h
- [ ] **S15-BA-3** — Relecture critique de 20 comptes rendus générés · ~3 h

---

## Sprint 16 — Finalisation

**Semaine du 01/02/2027**

**Objectif :** Dépôt propre, reproductible, documenté ; mémoire et soutenance prêts.

**Livrables :**
- Tag `v1.0.0`
- Mémoire
- Soutenance et démo

### Saliou — branche `sprint-16/saliou` (~8 h)

- [ ] **S16-SA-1** — Rédiger la méthodologie du mémoire · ~5 h
- [ ] **S16-SA-2** — Rédiger les limites et l'éthique (données, biais, usage clinique) · ~3 h

### Manou — branche `sprint-16/manou` (~7 h)

- [ ] **S16-MA-1** — Nettoyage du dépôt, README final, reproductibilité (`scripts/run_all`) · ~6 h
- [ ] **S16-MA-2** — Tag `v1.0.0` et release notes · ~1 h

### Babel — branche `sprint-16/babel` (~8 h)

- [ ] **S16-BA-1** — Préparer la soutenance (plan, supports) · ~5 h
- [ ] **S16-BA-2** — Préparer la démo et ses captures (sans donnée réelle) · ~3 h

---

## Bilan de charge

| Personne | Total estimé |
|---|---|
| Saliou | ~128 h sur 17 semaines |
| Manou | ~136 h sur 17 semaines |
| Babel | ~140 h sur 17 semaines |

Ces estimations servent à équilibrer la charge ; elles seront recalibrées à la fin du sprint 3.
