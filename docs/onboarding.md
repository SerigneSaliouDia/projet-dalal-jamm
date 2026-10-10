# Bienvenue dans le projet — guide de démarrage (Manou, Babel)

Ce guide suppose que vous n'avez **jamais** utilisé GitHub ni VS Code pour travailler à plusieurs.
Comptez environ **2 heures** pour tout faire une fois. Ensuite, le cycle de travail prend quelques minutes.
Suivez les étapes **dans l'ordre**, et copiez-collez les commandes sans les modifier (sauf ce qui est entre `< >`).

---

## 0. Les 6 mots à connaître

| Mot | Ce que c'est |
|---|---|
| **Dépôt** (repository) | Le dossier du projet, sauvegardé en ligne sur GitHub avec tout son historique |
| **Clone** | Copier le dépôt de GitHub sur votre ordinateur (une seule fois) |
| **Branche** | Votre copie de travail personnelle : vous y modifiez ce que vous voulez sans toucher au projet principal (`main`) |
| **Commit** | Une sauvegarde nommée de vos modifications, sur votre ordinateur |
| **Push** | Envoyer vos commits vers GitHub |
| **Pull Request (PR)** | Une demande : « voici mon travail, relisez-le puis ajoutez-le à `main` ». Quelqu'un d'autre le relit, Saliou le fusionne |

Le schéma de chaque semaine :

```
main (GitHub) --pull--> votre ordinateur --> branche --> commits --> push --> PR --> relecture --> Saliou fusionne
```

## 1. Les 3 règles d'or

1. **Jamais de donnée patiente sur GitHub** : pas d'images DICOM, pas de comptes rendus Word, pas de noms, pas de captures d'écran avec des noms. Lisez `CONFIDENTIALITE.md`.
2. **Ne travaillez jamais directement sur `main`.** Toujours sur votre branche `sprint-NN/prenom`.
3. **Une chose à la fois, et demandez de l'aide tôt** : si vous êtes bloqué depuis plus de 30 minutes, écrivez dans le groupe.

---

## 2. Installation (une seule fois)

### 2.1 Accepter l'invitation GitHub
1. Ouvrez l'e-mail d'invitation de GitHub (ou allez sur <https://github.com/notifications>) et cliquez sur **Accept invitation**.
2. Si vous n'avez pas de compte GitHub, créez-en un sur <https://github.com> **avec l'adresse e-mail où vous avez reçu l'invitation**.
3. Vérifiez que vous voyez le dépôt : <https://github.com/SerigneSaliouDia/projet-dalal-jamm>.

> L'invitation expire au bout de 7 jours. Si le lien ne marche plus, demandez à Saliou de la renvoyer avec votre **nom d'utilisateur GitHub**.

### 2.2 Installer les trois outils
| Outil | Lien | Attention |
|---|---|---|
| **Git** | <https://git-scm.com/download/win> | Installez avec les options par défaut |
| **Python** (3.11 ou plus récent) | <https://www.python.org/downloads/> | **Cochez « Add python.exe to PATH »** sur le premier écran |
| **Visual Studio Code** | <https://code.visualstudio.com/> | Options par défaut |

Redémarrez l'ordinateur après l'installation.

### 2.3 Dire à Git qui vous êtes
Ouvrez **PowerShell** (touche Windows, tapez `PowerShell`) :
```powershell
git config --global user.name "Prénom Nom"
git config --global user.email "votre-email-github@exemple.com"
```
Utilisez l'e-mail de votre compte GitHub.

### 2.4 Récupérer le projet
Choisissez un dossier **court, hors OneDrive**. Les chemins de ce projet sont très longs : un dossier profond fait échouer l'ouverture de certains fichiers.
```powershell
mkdir C:\Projets
cd C:\Projets
git clone https://github.com/SerigneSaliouDia/projet-dalal-jamm.git
cd projet-dalal-jamm
code .
```
Une fenêtre du navigateur s'ouvre pour connecter GitHub : acceptez. VS Code s'ouvre sur le projet. Si VS Code propose d'installer des extensions recommandées, **acceptez**.

### 2.5 Préparer Python dans VS Code
Dans VS Code : menu **Terminal → Nouveau terminal**. Tapez :
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
nbstripout --install
git config core.hooksPath .githooks
```
- Après `Activate`, vous devez voir **`(.venv)`** au début de la ligne. C'est le signe que tout est bien branché. **À chaque nouveau terminal, refaites uniquement la ligne `.venv\Scripts\Activate.ps1`.**
- Si PowerShell refuse l'activation (message sur « l'exécution de scripts »), tapez une fois `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, répondez `O`, puis recommencez.
- Dans VS Code : `Ctrl+Shift+P`, tapez `Python: Select Interpreter`, choisissez celui qui contient `.venv`.
- La dernière commande installe un garde-fou : elle **interdit** de pousser directement sur `main`.

### 2.6 Les données (ne les cherchez pas sur GitHub)
Les images et les comptes rendus ne passent **jamais** par GitHub. Saliou vous dira comment les récupérer, par le canal convenu avec l'hôpital. En attendant, tout le reste fonctionne.
Quand vous les aurez, rangez-les dans un dossier **court**, par exemple `C:\MAMMO`, puis :
```powershell
setx DALAL_DICOM_DIR "C:\MAMMO\Img"
setx DALAL_REPORTS_DIR "C:\MAMMO\rapport"
```
**Fermez complètement VS Code et rouvrez-le**, puis `python scripts/check_env.py` doit afficher **2254** fichiers DICOM et **283** rapports.
Si vous obtenez 2216 DICOM, la copie a perdu des fichiers aux chemins longs : refaites-la avec `robocopy`.

### 2.7 Vérifier que tout marche
```powershell
pytest -q
```
Résultat normal : des `passed`, des `xfailed` (tests « à venir », voulus) et peut-être un `skipped`.
**Un seul résultat est un problème : `failed`.** Dans ce cas, envoyez le message d'erreur à Saliou.

---

## 3. Votre première Pull Request (exercice)

But : faire tout le parcours une fois sur quelque chose d'inoffensif. Vous ajoutez **votre fiche personnelle** dans le projet.

**3.1 Partir d'un `main` à jour**
```powershell
git checkout main
git pull
```
**3.2 Créer votre branche** (remplacez `prenom` par votre prénom en minuscules, sans accent)
```powershell
git checkout -b sprint-00/prenom
```
**3.3 Créer votre fiche.** Dans VS Code, dans le dossier `docs/equipe`, créez le fichier `prenom.md` (clic droit sur le dossier → *New File*) avec ce contenu, complété :
```markdown
# Prénom

- Nom d'utilisateur GitHub :
- Ce pour quoi je suis à l'aise :
- Ce que je veux apprendre sur ce projet :
- Mes créneaux de travail habituels :
- Comment me joindre :
```
Enregistrez (`Ctrl+S`).

**3.4 Enregistrer (commit)**
```powershell
git status
git add docs/equipe/prenom.md
git commit -m "S0 : fiche d'équipe de Prénom"
```
`git status` vous montre ce qui a changé : vérifiez qu'il n'y a que votre fiche.

**3.5 Envoyer (push)**
```powershell
git push -u origin sprint-00/prenom
```
**3.6 Ouvrir la Pull Request.** Sur GitHub, un bandeau jaune propose **Compare & pull request** : cliquez. Mettez comme titre `[S0] Prénom — fiche d'équipe`, remplissez le modèle qui s'affiche, puis **Create pull request**.

**3.7 La relecture.** Une autre personne que vous relit : onglet **Files changed**, bouton **Review changes**, cochez **Approve**, **Submit review**. (Manou relit Babel, Babel relit Manou, Saliou relit les deux.)

**3.8 La fusion.** Quand la pastille **CI** est verte et la PR approuvée, **Saliou** clique sur **Squash and merge**. Ensuite, **tout le monde** fait :
```powershell
git checkout main
git pull
```

---

## 4. Le cycle de chaque semaine

1. **Lundi** (30 min, en visio) : on lit ensemble les tickets du sprint dans `TICKETS.md`. Chacun repère les siens.
2. **Partir à jour** : `git checkout main` puis `git pull`.
3. **Créer sa branche** : `git checkout -b sprint-NN/prenom` (NN = numéro du sprint sur deux chiffres, ex. `sprint-02/manou`).
4. **Travailler** dans VS Code. Après chaque petite avancée qui marche :
   ```powershell
   git status
   git add <les fichiers concernés>
   git commit -m "S2-MA-1 : ce que j'ai fait, en une phrase"
   ```
   Le code du ticket va dans le message de commit (ex. `S2-MA-1`).
5. **Tester** : `pytest -q` et `ruff check src tests scripts`. Il ne doit y avoir aucun `failed` ni aucune erreur `ruff`.
6. **Envoyer** : `git push -u origin sprint-NN/prenom` (la première fois), puis `git push`.
7. **Vendredi** : ouvrir la PR, la faire relire, répondre aux commentaires, Saliou fusionne.
8. **Cocher** les cases de vos tickets dans `TICKETS.md` (dans la PR).

> Si `main` a changé pendant votre semaine : `git fetch origin` puis `git merge origin/main`. Si Git annonce un **conflit**, ne paniquez pas et n'improvisez pas : écrivez à Saliou avant de continuer.

## 5. Relire la PR de quelqu'un d'autre (30 min maximum)

- Le code fait-il ce que le ticket demande ?
- Y a-t-il des tests, y compris pour les cas limites ?
- **Aucune donnée patiente** dans les fichiers (onglet *Files changed*) : noms, DICOM, Word, CSV d'identités.
- Écrivez des remarques **gentilles et précises**, puis **Approve** ou **Request changes**.

## 6. Quand ça ne marche pas

| Le message | Ce qu'il faut faire |
|---|---|
| `git n'est pas reconnu` / `python n'est pas reconnu` | Fermez et rouvrez VS Code. Sinon réinstallez en cochant « Add to PATH » |
| `pytest n'est pas reconnu` | Vous avez oublié d'activer l'environnement : `.venv\Scripts\Activate.ps1` (le `(.venv)` doit apparaître) |
| `Permission denied` / `403` / `repository not found` en poussant ou clonant | Vous n'avez pas accepté l'invitation, ou vous n'êtes pas connecté au bon compte GitHub |
| `Please tell me who you are` | Refaites l'étape 2.3 |
| `Push direct vers main REFUSE` | C'est **normal et voulu** : créez une branche (`git checkout -b sprint-NN/prenom`) et poussez celle-ci |
| `Your branch is behind 'origin/main'` | `git pull` |
| `CRLF will be replaced by LF` | Sans importance, ignorez |
| `failed` dans pytest | Envoyez le message d'erreur complet à Saliou |
| **J'ai commité un fichier de données par erreur** | **Prévenez Saliou tout de suite**, avant tout `push`. Non poussé : `git reset --soft HEAD~1`. Déjà poussé : ne touchez à rien |

## 7. Demander de l'aide

Écrivez dans le groupe, avec : **ce que vous vouliez faire**, **la commande exacte**, **le message d'erreur copié en texte** (pas une photo, et jamais avec des noms de patientes). On vous répond en moins d'une journée. Passé 30 minutes de blocage, demandez : c'est plus rapide pour tout le monde.

## 8. Aide-mémoire

| Je veux… | Commande |
|---|---|
| Voir ce qui a changé | `git status` |
| Voir les différences ligne par ligne | `git diff` |
| Voir l'historique | `git log --oneline -10` |
| Récupérer la dernière version de `main` | `git checkout main` puis `git pull` |
| Créer ma branche | `git checkout -b sprint-NN/prenom` |
| Changer de branche | `git checkout <nom-de-la-branche>` |
| Enregistrer | `git add <fichier>` puis `git commit -m "..."` |
| Envoyer | `git push` |
| Annuler un fichier non enregistré | `git restore <fichier>` |
| Tester | `pytest -q` |
| Vérifier le style du code | `ruff check src tests scripts` |
| Vérifier l'installation et les données | `python scripts/check_env.py` |

Pour aller plus loin : `CONTRIBUTING.md` (règles d'équipe) et `docs/guide_git_debutant.md`.
