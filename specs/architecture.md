# Architecture - Projet Ralph Wiggum

## Vue d'Ensemble

Ce projet utilise la méthodologie **Ralph Wiggum** pour faire tourner Claude Code CLI en boucle autonome. L'agent travaille sans supervision humaine, utilisant des fichiers et des commits git pour maintenir sa mémoire à travers les sessions.

---

## Les Trois Piliers de Ralph

### 1. La Boucle Autonome

```
┌─────────────────────────────────────────────────┐
│                                                 │
│   ┌─────────────┐     ┌─────────────┐          │
│   │  PROMPT.md  │────▶│   Claude    │          │
│   │ (Instructions)    │    Code     │          │
│   └─────────────┘     └──────┬──────┘          │
│                              │                  │
│                              ▼                  │
│                    ┌──────────────────┐        │
│                    │    Exécution     │        │
│                    │  (code, tests,   │        │
│                    │   git commits)   │        │
│                    └────────┬─────────┘        │
│                             │                  │
│                             ▼                  │
│                    ┌──────────────────┐        │
│                    │    TODO.md       │◀──┐    │
│                    │   (progrès)      │   │    │
│                    └────────┬─────────┘   │    │
│                             │             │    │
│                             ▼             │    │
│                    ┌──────────────────┐   │    │
│                    │   Terminé ?      │───┘    │
│                    │   (HARD STOP)    │ Non    │
│                    └────────┬─────────┘        │
│                             │ Oui              │
│                             ▼                  │
│                    ┌──────────────────┐        │
│                    │      STOP        │        │
│                    └──────────────────┘        │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 2. La Persistance via Fichiers

L'agent n'a pas de mémoire entre les sessions. Pour contourner cette limite :

| Fichier | Rôle |
|---------|------|
| `PROMPT.md` | Instructions persistantes (ne change pas) |
| `TODO.md` | État d'avancement (mis à jour en continu) |
| `specs/` | Spécifications et décisions architecturales |
| Git commits | Historique complet des changements |

### 3. Les Guardrails

Règles strictes pour éviter que l'agent ne déraille :

- **HARD STOP** : Conditions d'arrêt obligatoires
- **Checkpoints** : Points de validation intermédiaires
- **Limites de tours** : Nombre max d'itérations par session

---

## Workflow en 3 Phases

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│   PHASE 1: CLARIFY            PHASE 2: PLAN                      │
│   ┌──────────────────┐        ┌──────────────────┐              │
│   │  - Questions     │───────▶│  - Génération    │              │
│   │  - Requirements  │        │    PROMPT.md     │              │
│   │  - Contraintes   │        │  - Génération    │              │
│   └──────────────────┘        │    TODO.md       │              │
│           │                   └────────┬─────────┘              │
│           ▼                            │                         │
│   ┌──────────────────┐                 ▼                         │
│   │  Humain valide   │        ┌──────────────────┐              │
│   │  les specs       │        │  Humain valide   │              │
│   └──────────────────┘        │  le plan         │              │
│                               └────────┬─────────┘              │
│                                        │                         │
│                                        ▼                         │
│                               PHASE 3: EXECUTE                   │
│                               ┌──────────────────┐              │
│                               │  Boucle Ralph    │              │
│                               │  (loop.sh)       │              │
│                               │  autonome        │              │
│                               └────────┬─────────┘              │
│                                        │                         │
│                                        ▼                         │
│                               ┌──────────────────┐              │
│                               │  Projet terminé  │              │
│                               └──────────────────┘              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Phase 1 : Clarify (Clarification)

**Objectif :** Collecter toutes les informations avant de coder.

```bash
claude --print "Mode Clarify. Pose-moi des questions pour comprendre le projet."
```

**Output :** `specs/requirements.md` validé par l'humain

### Phase 2 : Plan (Planification)

**Objectif :** Générer le plan d'exécution et les fichiers de contrôle.

```bash
claude --print "Mode Plan. Génère PROMPT.md et TODO.md basés sur specs/"
```

**Output :** `PROMPT.md` et `TODO.md` validés par l'humain

### Phase 3 : Execute (Exécution)

**Objectif :** Lancer Ralph en boucle autonome.

```bash
./loop.sh
```

**Output :** Projet terminé avec commits git

---

## Structure des Fichiers

```
ralph-test/
├── .claude/
│   └── settings.json       # Configuration Claude Code (permissions, préférences)
│
├── PROMPT.md               # Instructions principales pour l'agent
│                           # - Contexte et objectif
│                           # - Spécifications techniques
│                           # - Critères de succès
│                           # - HARD STOP conditions
│                           # - Guardrails
│
├── TODO.md                 # État d'avancement (mémoire de Ralph)
│                           # - Critères à cocher
│                           # - Plan d'exécution
│                           # - Checkpoints
│                           # - Notes et journal
│                           # - HARD STOP trigger
│
├── specs/
│   ├── requirements.md     # Exigences fonctionnelles et non-fonctionnelles
│   ├── architecture.md     # Ce fichier (architecture du projet)
│   └── api.md              # Spécifications API (si applicable)
│
├── loop.sh                 # Script orchestrateur de la boucle Ralph
│
├── src/                    # Code source généré par Ralph
│   └── ...
│
├── tests/                  # Tests générés par Ralph
│   └── ...
│
└── guide/                  # Documentation de référence Ralph Wiggum
    └── ...
```

---

## Composants Clés

### PROMPT.md

Le "cerveau" de Ralph. Contient toutes les instructions permanentes.

**Sections obligatoires :**
- Contexte
- Objectif
- Spécifications techniques
- Critères de succès (vérifiables)
- Workflow
- HARD STOP
- Guardrails

### TODO.md

La "mémoire" de Ralph entre les sessions.

**Comportement :**
- Ralph le LIT au début de chaque tour
- Ralph le MET À JOUR après chaque action
- Contient le trigger HARD STOP : `- [x] DONE`

### loop.sh

Script bash qui orchestre la boucle.

**Fonctionnalités :**
- Vérifie les prérequis
- Lance Claude en boucle
- Détecte le HARD STOP
- Commits automatiques
- Checkpoints périodiques
- Gestion des interruptions (Ctrl+C)

### .claude/settings.json

Configuration des permissions et préférences.

**Permissions recommandées :**
```json
{
  "allow": ["Bash(git *)", "Bash(npm *)", "Read", "Write", "Edit"],
  "deny": ["Bash(rm -rf *)", "Bash(sudo *)"]
}
```

---

## Conditions HARD STOP

L'agent s'arrête immédiatement si :

| Condition | Action |
|-----------|--------|
| Tous les critères cochés `[x]` | Commit final et STOP |
| N tours sans progrès | Note le blocage et STOP |
| Même erreur 5+ fois | Note le bug et STOP |
| Erreur système | Note l'erreur et STOP |
| Coût max dépassé | STOP forcé |

---

## Flux de Données

```
┌─────────────────┐
│     Humain      │
│  (supervision)  │
└────────┬────────┘
         │
         │ Définit
         ▼
┌─────────────────┐     ┌─────────────────┐
│   PROMPT.md     │────▶│    Claude       │
│   (statique)    │     │     Code        │
└─────────────────┘     └────────┬────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    TODO.md      │     │    src/         │     │    Git          │
│   (dynamique)   │     │   (code)        │     │  (historique)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │
         │ Trigger
         ▼
┌─────────────────┐
│   HARD STOP     │
│   (arrêt)       │
└─────────────────┘
```

---

## Décisions Techniques

| Décision | Justification |
|----------|---------------|
| Fichiers MD pour la persistance | Format lisible, versionnable, éditable |
| Git pour l'historique | Rollback possible, traçabilité complète |
| Script bash pour l'orchestration | Simple, portable, pas de dépendances |
| Checkpoints réguliers | Détection précoce des dérapages |
| Pattern HARD STOP explicite | Arrêt automatique fiable |

---

## Coûts Estimés

| Type de projet | Tokens estimés | Coût approximatif |
|----------------|----------------|-------------------|
| Simple (CLI basique) | ~50-70k | $3-5 |
| Moyen (API REST) | ~100-150k | $15-25 |
| Complexe (Refactoring) | ~150-200k | $20-40 |

---

## Prochaines Étapes

1. Compléter `specs/requirements.md` avec les exigences du projet
2. Générer `PROMPT.md` avec les instructions détaillées
3. Configurer `TODO.md` avec le plan d'exécution
4. Copier `loop.sh` depuis les templates
5. Lancer la boucle Ralph
