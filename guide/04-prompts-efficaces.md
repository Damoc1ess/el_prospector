# 04 - Rédiger des Prompts Efficaces

La qualité du prompt détermine le succès de Ralph. Un bon prompt transforme une tâche vague en mission claire et vérifiable.

---

## Anatomie d'un Prompt Ralph

Un prompt efficace suit cette structure :

```
┌─────────────────────────────────────┐
│           1. CONTEXTE               │  Qui es-tu ? Que fais-tu ?
├─────────────────────────────────────┤
│           2. OBJECTIF               │  Quel est le but final ?
├─────────────────────────────────────┤
│      3. SPÉCIFICATIONS              │  Détails techniques
├─────────────────────────────────────┤
│    4. CRITÈRES DE SUCCÈS            │  Comment vérifier le succès ?
├─────────────────────────────────────┤
│         5. WORKFLOW                 │  Étapes à suivre
├─────────────────────────────────────┤
│         6. HARD STOP                │  Quand s'arrêter
├─────────────────────────────────────┤
│        7. GUARDRAILS                │  Ce qu'il ne faut PAS faire
└─────────────────────────────────────┘
```

---

## Section par Section

### 1. Contexte

Établit le rôle et le mode opératoire.

```markdown
## Contexte

Tu es en mode Ralph Wiggum - agent autonome qui travaille sans supervision.
Tu dois créer [PROJET] en [TECHNOLOGIE].

Tu as accès à :
- Lecture/écriture de fichiers
- Exécution de commandes bash
- Git pour versionner ton travail

Tu persistes ton état via :
- TODO.md pour l'avancement
- Git commits pour l'historique
```

### 2. Objectif

Court, précis, mesurable.

**Mauvais :**
> Crée une bonne application de gestion de tâches.

**Bon :**
> Créer `todo-cli`, une application Python qui permet d'ajouter, lister, compléter et supprimer des tâches via la ligne de commande.

### 3. Spécifications

Les détails techniques sans ambiguïté.

```markdown
## Spécifications Techniques

### Stack
- Langage : Python 3.10+
- Dépendances : aucune (stdlib only)
- Stockage : JSON local

### Interface
| Commande                    | Description           |
|-----------------------------|-----------------------|
| `todo add "texte"`          | Ajoute une tâche      |
| `todo list`                 | Liste les tâches      |
| `todo done <id>`            | Marque terminée       |
| `todo delete <id>`          | Supprime la tâche     |

### Structure des Données
```json
{"tasks": [{"id": 1, "text": "...", "done": false}]}
```
```

### 4. Critères de Succès

Des conditions **vérifiables** que Ralph peut cocher.

```markdown
## Critères de Succès

Chaque critère DOIT être vérifiable par une commande ou un test :

1. [ ] `python todo.py add "test"` retourne "Task added with ID 1"
2. [ ] `python todo.py list` affiche la tâche ajoutée
3. [ ] `python todo.py done 1` retourne "Task 1 marked as done"
4. [ ] `python todo.py delete 1` retourne "Task 1 deleted"
5. [ ] `python -m pytest tests/` retourne 0 erreurs
6. [ ] `cat README.md` contient les instructions d'usage
```

### 5. Workflow

L'ordre des opérations.

```markdown
## Workflow

1. **Lecture** : Lis ce fichier et specs/ entièrement
2. **Plan** : Écris ton plan dans TODO.md
3. **Setup** : Crée la structure de fichiers
4. **Implémentation** : Une fonctionnalité à la fois
5. **Tests** : Écris les tests après chaque fonctionnalité
6. **Validation** : Vérifie chaque critère de succès
7. **Documentation** : Écris le README à la fin
8. **Commit final** : "[Ralph] feat: complete todo-cli"
```

### 6. HARD STOP

Les conditions d'arrêt **absolues**.

```markdown
## HARD STOP

**ARRÊTE-TOI IMMÉDIATEMENT** si :

1. ✅ Tous les critères de succès sont cochés [x]
2. ❌ Tu as fait 50+ tours sans progrès mesurable
3. ❌ Tu rencontres une erreur système (permissions, réseau)
4. ❌ Le coût estimé dépasse $50

Quand tu t'arrêtes :
- Écris le statut final dans TODO.md
- Commit avec message "[Ralph] STOP: <raison>"
```

### 7. Guardrails

Ce qui est interdit.

```markdown
## Guardrails

### INTERDIT
- Modifier PROMPT.md
- Supprimer des fichiers sans raison
- Installer des dépendances non spécifiées
- Faire des requêtes réseau
- Accéder à des dossiers hors projet

### OBLIGATOIRE
- Un commit par fonctionnalité
- Tests avant validation
- Messages de commit préfixés [Ralph]
- Mise à jour de TODO.md à chaque étape
```

---

## Patterns de Langage Efficaces

Certains mots déclenchent des comportements utiles :

| Pattern               | Effet                                      |
|-----------------------|--------------------------------------------|
| `study X carefully`   | Force une lecture approfondie              |
| `ultrathink`          | Déclenche une réflexion plus longue        |
| `step by step`        | Force une décomposition                    |
| `verify by running`   | Exécute pour vérifier                      |
| `DO NOT skip`         | Emphase sur l'importance                   |
| `MUST/NEVER`          | Contraintes absolues                       |
| `before continuing`   | Crée un checkpoint                         |

### Exemples d'Utilisation

```markdown
## Workflow

1. **Study** the existing codebase carefully before making any changes
2. **Ultrathink** about the architecture before implementing
3. **Step by step**, implement each function
4. **Verify by running** the tests after each change
5. **DO NOT skip** the documentation step
6. **NEVER** modify files outside the src/ directory
7. **Before continuing** to the next feature, ensure all tests pass
```

---

## Mauvais vs Bon Prompt

### Exemple Mauvais

```markdown
# Projet

Fais une CLI en Python pour gérer des todos.
Elle doit marcher bien.
```

**Problèmes :**
- Pas de critères vérifiables
- Pas de HARD STOP
- "marcher bien" n'est pas mesurable
- Pas de structure de données définie

### Exemple Bon

```markdown
# PROMPT.md - CLI Todo Python

## Contexte
Tu es en mode Ralph Wiggum, agent autonome.

## Objectif
Créer `todo.py` : CLI de gestion de tâches.

## Spécifications
- Python 3.10+, stdlib only
- Stockage : todos.json
- Commandes : add, list, done, delete

## Critères de Succès
1. [ ] `python todo.py add "test"` fonctionne
2. [ ] `python todo.py list` affiche les tâches
3. [ ] Tests passent : `pytest tests/`
4. [ ] README.md existe

## HARD STOP
- Tous critères cochés → STOP
- 50 tours sans progrès → STOP

## Guardrails
- Un commit par feature
- Ne pas modifier PROMPT.md
```

---

## Templates de Critères

### Pour du Code

```markdown
## Critères de Succès - Code

1. [ ] Le fichier `main.py` existe
2. [ ] `python main.py --help` affiche l'aide
3. [ ] `python main.py [args]` retourne le résultat attendu
4. [ ] Pas d'erreur `pylint main.py` (score > 8)
5. [ ] `python -m pytest` : 0 échecs
```

### Pour des Tests

```markdown
## Critères de Succès - Tests

1. [ ] Dossier `tests/` existe
2. [ ] Au moins 5 fichiers de test
3. [ ] `pytest --cov=src` : couverture > 80%
4. [ ] Tests des cas limites inclus
5. [ ] Tests d'erreurs inclus
```

### Pour de la Documentation

```markdown
## Critères de Succès - Documentation

1. [ ] README.md avec sections : Install, Usage, API
2. [ ] Exemples de code fonctionnels
3. [ ] CHANGELOG.md à jour
4. [ ] Commentaires docstring sur fonctions publiques
```

### Pour du Refactoring

```markdown
## Critères de Succès - Refactoring

1. [ ] Tous les tests existants passent encore
2. [ ] Aucune régression fonctionnelle
3. [ ] Le nouveau code respecte [PATTERN]
4. [ ] Performance équivalente ou meilleure
5. [ ] Diff git montre la migration claire
```

---

## Anti-Patterns à Éviter

### 1. Critères Vagues

❌ "L'application doit être rapide"
✅ "Le temps de réponse de `list` < 100ms pour 1000 tâches"

### 2. Pas de HARD STOP

❌ Pas de section HARD STOP
✅ "ARRÊTE après 50 tours ou quand tous critères sont cochés"

### 3. Trop de Liberté

❌ "Choisis la meilleure architecture"
✅ "Utilise le pattern Repository avec ces interfaces..."

### 4. Pas de Fichier d'État

❌ Pas de TODO.md mentionné
✅ "Mets à jour TODO.md après chaque étape"

### 5. Dépendances Implicites

❌ "Utilise les bonnes bibliothèques"
✅ "Dépendances autorisées : requests, click, pytest"

---

## Checklist Avant Lancement

Avant de lancer Ralph, vérifiez que votre prompt contient :

- [ ] Section Contexte avec rôle et mode
- [ ] Objectif en 1-2 phrases maximum
- [ ] Spécifications techniques complètes
- [ ] Critères de succès vérifiables (pas vagues)
- [ ] HARD STOP avec conditions claires
- [ ] Guardrails explicites
- [ ] Référence à TODO.md pour l'état
- [ ] Format de commit défini

---

## Prochaine Étape

Maintenant que vous savez écrire des prompts efficaces, découvrez le [Workflow Avancé](./05-workflow-avance.md) en 3 phases.

---

[← Premiers Pas](./03-premiers-pas.md) | [Sommaire](./README.md) | [Workflow Avancé →](./05-workflow-avance.md)
