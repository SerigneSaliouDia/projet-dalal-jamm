# Règles d'extraction

Règles de fond, à respecter dans tout le code et à compléter au fil des sprints.

1. Ne jamais inventer une information absente du rapport.
2. Une absence reste une absence : « absence de masse » ne devient jamais `masse = 1`.
3. « Opacité » n'est pas automatiquement « masse » ; une anomalie échographique n'est pas automatiquement un « kyste ».
4. Conserver le texte original du radiologue dans des champs descriptifs : les variables structurées ne le remplacent pas.
5. BI-RADS : conserver la latéralité ; deux valeurs différentes pour le même côté = contradiction signalée.
6. Un côté n'est jamais déduit du mot « droit » ou « gauche » trouvé ailleurs dans le document.
7. Les recommandations peuvent être dans la conclusion : on les extrait sans modifier la conclusion.
8. Un fichier peut contenir plusieurs comptes rendus : à détecter avant toute extraction.
9. Rechercher sur le texte normalisé, **stocker** le texte original.

## Cas particuliers rencontrés (sprint 2, lecture des 283 fichiers)

Observations faites sur les vrais rapports (sans aucun nom de patiente).

| Observation | Conséquence pour le pipeline |
|---|---|
| **Un même .docx contient plusieurs comptes rendus de patientes différentes** (observé : 4 mammographies et 1 hystérographie dans un fichier de 6095 caractères). Le nom du fichier ne désigne que la première patiente. | L'unité de travail est le **compte rendu**, pas le fichier : `rapport_id` distinct de `fichier`. Découpage avant extraction (S4-MA-2). |
| Des comptes rendus **non mammographiques** figurent dans les fichiers. | Les repérer et les écarter (colonne type d'examen). Ils ne passent pas dans le dataset. |
| Les en-têtes de page sont un **papier à en-tête** (ministère, hôpital, liste des radiologues) : 12 textes distincts pour 279 rapports, dont 3 modèles principaux. Aucune donnée de patiente observée dans les modèles répétés. | Les en-têtes et pieds de page sont **exclus** du texte analysé. |
| L'identité est dans le corps : `Prénom & Nom : … DATE : jj.mm.aa`, puis `Age : N ans`, `Indication clinique : …`, sur des lignes à tabulations. | Extraire nom, date et âge par compte rendu (utile pour l'association avec les images, sprint 3). |
| La densité est parfois **bilatérale** (« Densité : seins de type B ») et parfois par sein. | Le même type pour les deux seins n'est valide que si la formulation est bilatérale. |
| `Aires ganglionnaires : libres.` | Absence **explicite** d'adénopathie sans mot de négation : règle dédiée. |
| **Négation qualifiée** : « Absence de masse suspecte / évidente », « Absence de calcifications vasculaires ». | N'équivaut PAS à « pas de masse » ni « pas de calcification » : la valeur reste vide (non mentionné), la phrase source est conservée. À valider par un radiologue. |
| « Macrocalcification séquellaire » (bénigne) et « calcifications vasculaires » sont des catégories à part. | Ne pas les confondre avec une calcification suspecte. |
| L'**indication clinique** peut citer un ACR antérieur (« sein classé ACR 3 »). | Le BI-RADS du compte rendu est lu **uniquement dans la conclusion**. L'ACR de l'indication est un champ distinct. |
| Formulations de conclusion : `class` (faute), `à droit`, `ACR 1 gauche et ACR 3 droit`, `ACR 2 bilatéral`, `adéno fibrome` (avec espace). | Tests BI-RADS ajoutés ; dictionnaire de termes tolérant aux variantes. |
| Écho : la latéralité est dans la phrase (« … quadrant inféro-externe droit »), pas dans un titre ; dimensions `6 x 4.5 mm`, `4 mm de grand axe`. | Côté déterminé phrase par phrase ; décimales à point acceptées. |

## Questions à poser à un radiologue

1. « Aspect normal du revêtement cutané et du mamelon » vaut-il « pas de rétraction mamelonnaire » ?
2. « Absence de masse suspecte » : le radiologue exclut-il toute masse ou seulement les masses suspectes ?
3. Un « ganglion intra-mammaire » compte-t-il comme adénopathie ?
4. « Formation kystique » à l'écho équivaut-elle à un kyste ?
