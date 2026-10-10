# Guide Git / GitHub pas à pas (premier dépôt)

Ce guide suppose que vous partez de zéro. Les commandes se tapent dans le terminal de VS Code
(*Terminal → Nouveau terminal*). Sous Windows, installez **Git for Windows** (inclut Git Bash).

## Partie A — Saliou : créer le dépôt (une seule fois)

### A1. Se présenter à Git
```bash
git config --global user.name "Saliou Votre-Nom"
git config --global user.email "votre-email@exemple.com"
```
(Utilisez l'e-mail de votre compte GitHub.)

### A2. Créer le dépôt vide sur GitHub
1. Sur github.com : **New repository**.
2. Nom : `projet-dalal-jamm` (GitHub n'accepte pas les espaces ; « Dalal Jamm » s'écrit avec un seul « l » final).
3. **Private**.
4. **Ne cochez pas** « Add a README », « .gitignore » ni « license » (le projet les contient déjà).
5. **Create repository**, puis copiez l'adresse HTTPS affichée.

### A3. Envoyer le squelette
Décompressez l'archive du projet, ouvrez le dossier dans VS Code, puis :
```bash
git init -b main
git add .
git status                 # LISEZ la liste : aucun .docx, .IMA, .dcm ne doit apparaître
git commit -m "S0 : squelette initial du projet"
git remote add origin https://github.com/<votre-compte>/projet-dalal-jamm.git
git push -u origin main
```
Si `git status` montre un fichier de données : **ne commitez pas**, retirez-le (`git rm --cached <fichier>`) et vérifiez `.gitignore`.

### A4. Inviter l'équipe
GitHub → **Settings → Collaborators → Add people** : Manou et Babel, rôle **Write**.

### A5. Protéger `main`
> **Dépôt privé sur GitHub Free :** les rulesets et la protection de branche ne sont **pas** disponibles
> (ils exigent GitHub Pro/Team, ou un dépôt public). Deux solutions : demander **GitHub Pro gratuit pour étudiants**
> (<https://education.github.com/pack>), puis appliquer les réglages ci-dessous ; en attendant, utiliser le
> garde-fou local décrit dans `CONTRIBUTING.md` (`git config core.hooksPath .githooks`).

GitHub → **Settings → Rules → Rulesets → New branch ruleset** :
- Nom : `protect-main`, Enforcement : *Active*, cible : branche par défaut (`main`).
- Cocher : **Restrict deletions**, **Require a pull request before merging** (1 approbation),
  **Require status checks to pass** (ajouter le job `tests`), **Block force pushes**.

Dans **Settings → General → Pull Requests** : n'autorisez que **Squash merging** et activez
« Automatically delete head branches ».

Pour que vous puissiez fusionner vos propres PR, ajoutez-vous (administrateur) à la liste de contournement
(*Bypass list*), mais faites quand même relire vos PR par un autre membre.

## Partie B — Manou et Babel : première installation

```bash
git clone https://github.com/<compte-de-saliou>/projet-dalal-jamm.git
cd projet-dalal-jamm
```
Puis suivez la section « Installation » du `README.md`.

## Partie C — Le cycle de chaque sprint (tout le monde)

### C1. Partir d'un `main` à jour
```bash
git checkout main
git pull
```

### C2. Créer sa branche de sprint
```bash
git checkout -b sprint-01/manou        # adaptez le numéro et votre prénom
```

### C3. Travailler, puis enregistrer
Après chaque petite avancée :
```bash
git status                              # que s'est-il passé ?
git add src/dalal_jamm/dicom/metadata.py tests/test_dicom_views.py   # ajoutez des fichiers précis
git commit -m "S1-MA-1 : lit les en-têtes DICOM sans les pixels"
```
Évitez `git add .` tant que vous n'êtes pas sûr de ce qu'il ajoute.

### C4. Envoyer sa branche
```bash
git push -u origin sprint-01/manou      # la première fois ; ensuite : git push
```

### C5. Ouvrir la Pull Request
GitHub affiche un bandeau « Compare & pull request ». Cliquez, remplissez le modèle, demandez la relecture d'un
autre membre (colonne *Reviewers*), puis **Create pull request**.

### C6. Après les remarques
Corrigez dans votre branche, `git add`, `git commit`, `git push` : la PR se met à jour toute seule.

## Partie D — Saliou : fusionner

1. Ouvrir la PR : l'onglet **Checks** doit être vert, la relecture **Approved**.
2. Parcourir **Files changed** : aucun fichier de données, aucun nom de patiente.
3. **Squash and merge → Confirm**. La branche est supprimée automatiquement.
4. Dans le terminal :
```bash
git checkout main
git pull
```
5. Annoncer dans le groupe que `main` est à jour.

## Partie E — Mettre sa branche à jour pendant un sprint

Si `main` a avancé (PR d'un autre fusionnée) :
```bash
git fetch origin
git merge origin/main
```
En cas de **conflit**, Git marque les fichiers concernés avec `<<<<<<<`, `=======`, `>>>>>>>`.
VS Code propose « Accept Current / Incoming / Both » : choisissez, vérifiez que le code fonctionne,
puis `git add <fichier>` et `git commit`. En cas de doute, demandez avant de pousser.

## Partie F — Accident : une donnée patiente a été commitée

- **Pas encore poussée** : `git reset --soft HEAD~1`, retirez le fichier de l'index (`git restore --staged <fichier>`), recommitez.
- **Déjà poussée** : prévenez immédiatement l'équipe. Supprimer le fichier dans un nouveau commit **ne suffit pas**.
  Il faut réécrire l'historique (outil `git filter-repo`) puis forcer la mise à jour, ou recréer le dépôt
  à partir d'un état propre, et informer le CHN selon ce qui a été convenu. Ne tentez pas de le faire seul : on le fait à plusieurs.

## Aide-mémoire

| Je veux… | Commande |
|---|---|
| Voir l'état | `git status` |
| Voir mes changements | `git diff` |
| Voir l'historique | `git log --oneline -10` |
| Changer de branche | `git checkout <branche>` |
| Annuler un fichier non commité | `git restore <fichier>` |
| Mettre de côté mon travail | `git stash` / `git stash pop` |
| Récupérer ce qui est sur GitHub | `git pull` |
