# Règles de travail

## Branches

- `main` : toujours propre et fonctionnelle. **Personne ne pousse directement dessus.**

> **Protection de `main` sur GitHub Free + dépôt privé :** les règles de protection de branche ne sont pas
> disponibles dans cette configuration (elles exigent GitHub Pro/Team, ou un dépôt public). En attendant,
> la règle « personne ne pousse sur `main` » repose sur **notre discipline** et sur un garde-fou local.
> **Chacun l'active une fois sur sa machine, dans le dossier du projet :**
>
> ```
> git config core.hooksPath .githooks
> ```
>
> Ensuite, `git push` vers `main` est refusé avec un message explicatif. C'est un filet de sécurité contre
> les accidents, pas une vraie protection : on peut le contourner (`--no-verify`), donc ne le faites pas.
> Seul Saliou modifie `main`, en fusionnant des Pull Requests sur GitHub.
- Une branche **par personne et par sprint** : `sprint-NN/prenom` (ex. `sprint-03/babel`).
- Besoin d'isoler une tâche : `sprint-NN/prenom-sujet-court` (ex. `sprint-05/saliou-birads-cotes`).

## Commits

Petits, fréquents, avec un message clair à l'impératif et le ticket :

```
S5-SA-1 : segmente la conclusion autour de chaque ACR
S6-MA-1 : ajoute evidence_* pour les signes
fix : corrige le côté inversé pour « ACR 5 gauche et ACR 2 à droite »
docs : précise la règle birads_global
```

## Pull Requests (une par sprint et par personne)

1. Mettre à jour sa branche avec `main` (`git fetch` puis `git merge origin/main`).
2. Lancer `pytest` et `ruff check src tests scripts`.
3. Pousser la branche et ouvrir la PR sur GitHub (le modèle de PR s'affiche : le remplir).
4. Demander la relecture d'**un autre membre** (jamais l'auteur lui-même).
5. Répondre aux commentaires, corriger, repousser.
6. Quand la CI est verte et la PR approuvée, **Saliou** clique sur *Squash and merge*, puis supprime la branche.
7. Chacun fait ensuite `git checkout main && git pull` avant de créer sa branche du sprint suivant.

## Relire une PR (30 min maximum)

- Le code fait-il ce que le ticket demande ?
- Les tests couvrent-ils les cas limites (négations, côtés, valeurs manquantes) ?
- Une absence est-elle bien traitée comme une absence ?
- **Aucune donnée patiente** : noms, DICOM, DOCX, CSV d'identités, sorties de notebook.

## Code

- Les fonctions vivent dans `src/dalal_jamm/`, les notebooks les appellent. Pas de fonction de 500 lignes.
- Une fonction = une responsabilité. Tout test écrit **avant** le code (voir les `xfail` existants :
  quand le code passe le test, **retirez le marqueur** `xfail`).
- Pas de chemin absolu en dur (`C:\...`) : utiliser `dalal_jamm.config`.
- Pas de nom de médecin ou de patiente dans le code.
- Python 3.11, formatage et lint avec `ruff`.

## Notebooks

- Courts, numérotés, avec objectif et tickets en première cellule.
- **Sorties effacées avant commit** : `nbstripout --install` (une seule fois par machine).
- Aucun nom de patiente affiché, même pendant le développement.

## Décisions importantes

Toute décision structurante (association validée ou non, choix de la tâche de modélisation, règle de
calcul d'un champ) est consignée dans `docs/decisions.md`.
