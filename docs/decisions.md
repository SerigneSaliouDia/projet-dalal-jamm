# Journal des décisions (ADR)

Format : une entrée par décision, jamais supprimée (on ajoute une entrée qui la remplace).

---
## ADR-000 — Aucune donnée patiente dans Git
- **Statut** : acceptée
- **Contexte** : DICOM et comptes rendus identifiants.
- **Décision** : les données restent en local ; le dépôt ne contient que code, tests, docs et données fictives.
- **Conséquences** : variables d'environnement `DALAL_*`, `.gitignore` strict, test automatique.

---
## ADR-001 — Association rapports ↔ examens
- **Statut** : à décider (sprint 3)
- **Options** : validée / partielle / impossible
- **Éléments** : taux de couverture, identifiants disponibles, ambiguïtés.

---
## ADR-002 — Tâches de modélisation retenues
- **Statut** : à décider (sprint 10)
- **Options** : classification bénin/suspect par sein ; signes multi-label ; BI-RADS regroupé ; autres.
- **Éléments** : effectifs par classe, examens complets, qualité de l'annotation.
