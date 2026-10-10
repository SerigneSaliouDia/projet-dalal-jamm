# Dictionnaire de données

## Convention des trois états (signes)

| Valeur | Sens |
|---|---|
| `1` | Signe présent (écrit comme présent dans le rapport) |
| `0` | Absence **explicitement écrite** (« pas de masse ») |
| vide | Non mentionné : on ne sait pas |

Chaque signe a une colonne `evidence_<signe>_<d|g>` : la phrase originale qui a déclenché la valeur.

## Table des rapports structurés (sortie sprint 9)

À compléter au sprint 0 à partir de la liste du notebook archivé, puis à finaliser au sprint 9.

| Colonne | Type | Description | Source |
|---|---|---|---|
| `exam_id` | texte | Identifiant pseudonymisé de l'examen | privacy |
| `densite_d`, `densite_g` | A/B/C/D | Densité mammaire par sein | rapport |
| `masse_d`, `masse_g` | 1/0/vide | Masse | rapport |
| `calcif_d`, `calcif_g` | 1/0/vide | Calcifications | rapport |
| `asymetrie_d`, `asymetrie_g` | 1/0/vide | Asymétrie | rapport |
| `distorsion_d`, `distorsion_g` | 1/0/vide | Distorsion architecturale | rapport |
| `adenopathie_d`, `adenopathie_g` | 1/0/vide | Adénopathie | rapport |
| `retraction_mamelonnaire_d`, `_g` | 1/0/vide | Rétraction mamelonnaire | rapport |
| `birads_d`, `birads_g` | 1–6, 4A–4C | BI-RADS par sein | conclusion |
| `birads_global`, `birads_lateralite`, `birads_contradiction` | | Valeur globale, latéralité, alerte | conclusion |
| `observation_d`, `observation_g` | texte | Texte original du radiologue par sein | rapport |
| `lesions_d`, `lesions_g` | texte | Descriptions de lésions (texte original) | rapport |
| `echo_d`, `echo_g`, `echo_non_lateralise` | texte | Complément échographique | rapport |
| `conclusion` | texte | Conclusion **originale** | rapport |
| `recommandation` | texte | Recommandation (extraite de la conclusion) | rapport |

## Table du dataset final (sortie sprint 9)

`exam_id`, `image_right_cc`, `image_right_mlo`, `image_left_cc`, `image_left_mlo`, `split`
(train/val/test, par patiente), puis les colonnes ci-dessus.
