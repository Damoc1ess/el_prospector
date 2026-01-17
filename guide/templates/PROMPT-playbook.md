# PROMPT.md - Template Playbook Avancé

<!--
  TEMPLATE AVANCÉ RALPH WIGGUM (PLAYBOOK)

  Ce template inclut:
  - Workflow en 3 phases
  - Guardrails complets
  - Checkpoints
  - Patterns de langage optimisés

  Utilisation:
  1. Copier ce fichier et TODO-template.md
  2. Remplir les sections
  3. Lancer: claude --ralph "Exécute PROMPT.md"
-->

## Contexte

Tu es en mode **Ralph Wiggum** - un agent autonome qui travaille sans supervision.

**Mission :** Créer [NOM_DU_PROJET]
**Stack :** [TECHNOLOGIE]
**Durée estimée :** [X] tours

Tu as accès à :
- Lecture/écriture de fichiers
- Exécution de commandes bash (limitées)
- Git pour versionner

Tu persistes ton état via :
- `TODO.md` pour l'avancement (LIS CE FICHIER À CHAQUE TOUR)
- Commits git pour l'historique

---

## Objectif

[Décrire l'objectif final en 1-2 phrases claires et précises]

---

## Spécifications Techniques

### Stack

| Élément         | Choix                           |
|-----------------|--------------------------------|
| Langage         | [Python 3.10+ / Node.js 20+]   |
| Framework       | [aucun / Express / FastAPI]    |
| Dépendances     | [liste ou "stdlib only"]       |
| Stockage        | [JSON local / SQLite]          |
| Tests           | [pytest / jest / vitest]       |

### Architecture

```
[NOM_PROJET]/
├── src/
│   ├── main.[ext]
│   └── [modules]/
├── tests/
│   └── test_[modules].[ext]
├── README.md
└── [config files]
```

### Interface / API

<!-- Définir précisément les interfaces -->

```
[Exemples de commandes CLI ou endpoints API]
```

### Structure des Données

```json
{
  "exemple": "de structure attendue"
}
```

---

## Critères de Succès

<!-- CHAQUE critère DOIT être vérifiable par une commande ou un test -->

### Fonctionnels
1. [ ] [Commande] retourne [résultat attendu]
2. [ ] [Fonctionnalité] fonctionne correctement
3. [ ] [Cas limite] est géré

### Qualité
4. [ ] Tests passent : `[commande de test]`
5. [ ] Lint propre : `[commande lint]` (optionnel)
6. [ ] README.md avec sections : Install, Usage, API

### Livrables
7. [ ] Code fonctionnel et testé
8. [ ] Documentation complète
9. [ ] Git historique propre

---

## Workflow

**IMPORTANT :** Suis cet ordre STRICTEMENT.

### Phase 1 : Setup (Tours 1-3)
1. **Study** ce fichier PROMPT.md en entier
2. **Study** TODO.md pour comprendre l'état actuel
3. Créer la structure de dossiers
4. Initialiser les fichiers de base
5. Commit : `[Ralph] chore: initial setup`

### Phase 2 : Implémentation (Tours 4-N)
6. Pour CHAQUE fonctionnalité :
   a. Implémenter le code
   b. **Verify by running** les tests
   c. Commit : `[Ralph] feat: [description]`
   d. Mettre à jour TODO.md

### Phase 3 : Finalisation (Tours N-Fin)
7. Écrire les tests manquants
8. Écrire le README.md
9. Vérifier TOUS les critères de succès
10. Commit final : `[Ralph] docs: complete project`

---

## Checkpoints

<!-- Ces checkpoints permettent de détecter un dérapage -->

| Tour  | Checkpoint                          | Action si non atteint      |
|-------|-------------------------------------|----------------------------|
| 5     | Setup terminé, 1 feature ok         | Revoir l'architecture      |
| 15    | 50% des features                    | Simplifier le scope        |
| 25    | Toutes features + tests             | Focus sur complétion       |
| 30    | Critères tous cochés                | HARD STOP                  |

---

## HARD STOP

**ARRÊTE-TOI IMMÉDIATEMENT** si :

| Condition                               | Action                         |
|-----------------------------------------|--------------------------------|
| ✅ Tous critères cochés [x] dans TODO.md | Commit final et STOP           |
| ❌ [50] tours sans progrès mesurable     | Note le blocage et STOP        |
| ❌ Même erreur 5+ fois consécutives      | Note le bug et STOP            |
| ❌ Erreur système (permissions, réseau)  | Note l'erreur et STOP          |

**Quand tu t'arrêtes :**
1. Écris le statut final dans TODO.md
2. Commit : `[Ralph] STOP: [raison]`

---

## Guardrails

### OBLIGATOIRE
- Lis TODO.md à CHAQUE début de tour
- UN commit par fonctionnalité complète
- Format commit : `[Ralph] type: description`
  - Types : feat, fix, test, docs, chore
- Mets à jour TODO.md après chaque commit

### INTERDIT
- ❌ Modifier ce fichier PROMPT.md
- ❌ Supprimer des fichiers sans raison explicite
- ❌ Installer des dépendances non listées
- ❌ Accéder au réseau (sauf si spécifié)
- ❌ Modifier des fichiers hors du projet

### LIMITES PAR TOUR
- Max 3 fichiers modifiés
- Max 200 lignes de code
- Commit obligatoire si >100 lignes modifiées

---

## Notes Techniques

<!-- Ajouter ici des précisions techniques si nécessaire -->

### Conventions de Code
- [Style guide à suivre]
- [Naming conventions]

### Erreurs Connues à Éviter
- [Piège 1]
- [Piège 2]

---

## Ressources

<!-- Liens vers documentation utile -->

- [Lien 1]
- [Lien 2]
