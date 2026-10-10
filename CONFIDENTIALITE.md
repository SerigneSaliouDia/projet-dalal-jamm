# Confidentialité des données

Les images DICOM et les comptes rendus du CHN Dalal Jamm sont des **données de santé identifiantes**
(noms, âges, dates, identifiants DICOM). Elles ne sont pas la propriété de l'équipe.

## Règles absolues

1. **Aucune donnée réelle dans Git** : ni DICOM/IMA, ni DOCX, ni CSV contenant des noms, ni captures d'écran avec noms.
   `.gitignore` et un test automatique (`tests/test_no_patient_data_tracked.py`) servent de garde-fous,
   mais ne remplacent pas votre vigilance.
2. **Les sorties de notebooks sont des données** : elles peuvent afficher des noms. Effacez-les (`nbstripout`).
3. **Pseudonymisation dès le début** : après le sprint 2, tout le travail utilise `exam_id`. La table
   `exam_id ↔ identité` reste dans `data/private/`, jamais partagée, jamais envoyée en ligne.
4. **Pas de service externe** (Colab, Kaggle, API en ligne, assistants IA) avec des données patientes sans
   autorisation écrite du CHN.
5. **Partage entre membres** : uniquement par le canal convenu avec le CHN, jamais par messagerie publique.
6. **Données fictives pour les tests** : `tests/fixtures/` ne contient que des textes inventés.

## En cas d'erreur

Si une donnée patiente a été ajoutée à un commit :
- **non poussé** : `git reset --soft HEAD~1`, retirer le fichier, refaire le commit ;
- **déjà poussé** : prévenir immédiatement Saliou. Supprimer le fichier ne suffit pas (l'historique le garde) ;
  le dépôt devra être nettoyé (voir `docs/guide_git_debutant.md`, section « Accident »).

## À clarifier au sprint 0

- Qui, au CHN, autorise l'usage des données et pour quel périmètre ?
- Où les données doivent-elles être stockées et qui peut y accéder ?
- Quelles sorties (figures, tableaux, extraits) peuvent figurer dans le mémoire ?
