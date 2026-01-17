# 05 - Workflow Avancé en 3 Phases

Pour les projets complexes, le workflow "tout d'un coup" ne fonctionne pas. La technique avancée sépare le travail en trois phases distinctes.

---

## Vue d'Ensemble

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   PHASE 1: CLARIFY           PHASE 2: PLAN                   │
│   ┌─────────────────┐        ┌─────────────────┐             │
│   │  Questions      │───────▶│  Génération     │             │
│   │  Requirements   │        │  des fichiers   │             │
│   │  Contraintes    │        │  PROMPT/TODO    │             │
│   └─────────────────┘        └────────┬────────┘             │
│          │                            │                      │
│          │                            │                      │
│          ▼                            ▼                      │
│   ┌─────────────────┐        ┌─────────────────┐             │
│   │  Humain valide  │        │  Humain valide  │             │
│   │  les specs      │        │  le plan        │             │
│   └─────────────────┘        └────────┬────────┘             │
│                                       │                      │
│                                       ▼                      │
│                              PHASE 3: EXECUTE                │
│                              ┌─────────────────┐             │
│                              │  Boucle Ralph   │             │
│                              │  autonome       │             │
│                              └────────┬────────┘             │
│                                       │                      │
│                                       ▼                      │
│                              ┌─────────────────┐             │
│                              │  Projet         │             │
│                              │  terminé        │             │
│                              └─────────────────┘             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 1 : Clarify (Clarification)

### Objectif
Collecter toutes les informations nécessaires **avant** de coder.

### Processus

```bash
claude --print "Mode Clarify. Pose-moi des questions pour comprendre le projet. Ne code PAS encore."
```

### Questions Typiques à Explorer

| Catégorie       | Questions                                             |
|-----------------|-------------------------------------------------------|
| Fonctionnel     | Quelles sont les features principales ?               |
| Technique       | Quelles technos/contraintes ?                         |
| Scope           | Qu'est-ce qui est hors scope ?                        |
| Existant        | Y a-t-il du code existant à intégrer ?                |
| Qualité         | Quels standards de qualité (tests, lint) ?            |
| Livrable        | Quel est le format de livraison attendu ?             |

### Output de Phase 1

Un fichier `specs/requirements.md` validé par l'humain :

```markdown
# Requirements - Projet X

## Fonctionnalités
- Feature A : [description]
- Feature B : [description]

## Contraintes Techniques
- Langage : Python 3.10+
- Dépendances : requests, click
- Pas de base de données

## Hors Scope
- Interface graphique
- Authentification
- Déploiement

## Standards
- Tests : pytest, couverture > 80%
- Lint : ruff, score > 9
- Commits : conventional commits

## Validé par
- [x] Humain a relu et approuvé
```

### Quand Passer à Phase 2

Critères de sortie de Phase 1 :
- [ ] Toutes les questions clarifiées
- [ ] specs/requirements.md créé
- [ ] Humain a validé explicitement

---

## Phase 2 : Plan (Planification)

### Objectif
Générer le plan d'exécution et les fichiers de contrôle.

### Processus

```bash
claude --print "Mode Plan. Génère PROMPT.md et TODO.md basés sur specs/requirements.md. Ne code PAS encore."
```

### Fichiers à Générer

#### PROMPT.md

```markdown
# PROMPT.md - Projet X

## Contexte
[Généré depuis requirements]

## Objectif
[Synthèse en 1-2 phrases]

## Spécifications
[Extrait de requirements.md]

## Critères de Succès
[Liste vérifiable]

## Workflow
[Étapes détaillées]

## HARD STOP
[Conditions d'arrêt]

## Guardrails
[Interdictions]
```

#### TODO.md

```markdown
# TODO.md - Projet X

## Status: PRÊT À EXÉCUTER

## Critères de Succès
- [ ] Critère 1
- [ ] Critère 2
- [ ] ...

## Plan d'Exécution
- [ ] Étape 1 : Setup initial
- [ ] Étape 2 : Implémentation Feature A
- [ ] Étape 3 : Tests Feature A
- [ ] ...
- [ ] Étape N : Documentation

## Checkpoints
- [ ] CHECKPOINT 1 : Feature A complète (tour ~10)
- [ ] CHECKPOINT 2 : Feature B complète (tour ~25)
- [ ] CHECKPOINT 3 : Tests passent (tour ~40)

## HARD STOP TRIGGER
- [ ] DONE - Projet terminé
```

### Revue du Plan

L'humain doit vérifier :

| Élément          | Question                                     |
|------------------|----------------------------------------------|
| Critères         | Sont-ils tous vérifiables ?                  |
| Étapes           | L'ordre est-il logique ?                     |
| Checkpoints      | Permettent-ils de détecter un dérapage ?     |
| HARD STOP        | Les conditions sont-elles claires ?          |
| Estimation       | Le nombre de tours est-il réaliste ?         |

### Quand Passer à Phase 3

Critères de sortie de Phase 2 :
- [ ] PROMPT.md généré et relu
- [ ] TODO.md avec plan détaillé
- [ ] Checkpoints définis
- [ ] Humain a validé explicitement

---

## Phase 3 : Execute (Exécution)

### Objectif
Lancer Ralph en boucle autonome.

### Lancement

```bash
# Option simple
claude --print "Mode Execute. Lis PROMPT.md et TODO.md. Exécute le plan."

# Option avec script
./loop.sh
```

### Script de Boucle Avancé

```bash
#!/bin/bash
# loop-advanced.sh

MAX_ITERATIONS=100
CHECKPOINT_INTERVAL=10
COST_WARNING=25
COST_MAX=50

iteration=0
start_time=$(date +%s)

log() {
    echo "[$(date '+%H:%M:%S')] $1"
}

check_hard_stop() {
    grep -q "\[x\] DONE" TODO.md 2>/dev/null
}

check_checkpoint() {
    local current=$1
    if (( current % CHECKPOINT_INTERVAL == 0 )); then
        log "📍 CHECKPOINT à l'itération $current"
        log "Vérification du TODO.md..."
        grep -E "^\- \[[ x]\]" TODO.md | head -10
        echo ""
    fi
}

while [ $iteration -lt $MAX_ITERATIONS ]; do
    iteration=$((iteration + 1))
    log "=== Iteration $iteration / $MAX_ITERATIONS ==="

    # Vérifier HARD STOP
    if check_hard_stop; then
        log "✅ HARD STOP - Projet terminé!"
        break
    fi

    # Checkpoint périodique
    check_checkpoint $iteration

    # Lancer Claude
    claude --print "Continue l'exécution. Tour $iteration. Lis TODO.md pour ton état."

    # Commit automatique
    if git diff --quiet 2>/dev/null; then
        log "Pas de changement"
    else
        git add -A
        git commit -m "[Ralph] Tour $iteration" --quiet
        log "Commit effectué"
    fi

    sleep 3
done

# Résumé final
end_time=$(date +%s)
duration=$((end_time - start_time))
log "=== TERMINÉ ==="
log "Durée : $((duration / 60)) minutes"
log "Iterations : $iteration"
log "Commits : $(git rev-list --count HEAD)"
```

### Monitoring Pendant l'Exécution

#### Terminal 1 : Boucle Ralph
```bash
./loop-advanced.sh
```

#### Terminal 2 : Suivi TODO
```bash
watch -n 5 'cat TODO.md'
```

#### Terminal 3 : Suivi Git
```bash
watch -n 10 'git log --oneline -15'
```

#### Terminal 4 : Coûts (si disponible)
```bash
watch -n 30 'cat ~/.claude/usage.json | jq .total_cost'
```

---

## Quand Régénérer le Plan

Parfois, il faut revenir en Phase 2. Signaux :

| Signal                              | Action                               |
|-------------------------------------|--------------------------------------|
| Ralph tourne sans progrès (10+ tours)| STOP → Revoir PROMPT.md              |
| Critère impossible à atteindre      | STOP → Modifier les critères         |
| Nouvelle contrainte découverte      | STOP → Mettre à jour requirements    |
| Architecture inadaptée              | STOP → Repenser le plan              |

### Procédure de Reset

```bash
# 1. Arrêter Ralph
# (Ctrl+C ou attendre HARD STOP)

# 2. Sauvegarder l'état
git add -A
git commit -m "[Ralph] PAUSE pour révision"

# 3. Créer une branche de backup
git branch backup-$(date +%Y%m%d%H%M%S)

# 4. Modifier le plan
# ... éditer PROMPT.md et TODO.md ...

# 5. Relancer
./loop-advanced.sh
```

---

## Signes et Guardrails

### Signes que Ralph Déraille

| Signe                               | Gravité | Action                       |
|-------------------------------------|---------|------------------------------|
| Même erreur 3+ fois                 | 🟡      | Ajouter un hint dans TODO.md |
| Fichiers supprimés par erreur       | 🟠      | Restaurer via git, clarifier |
| Boucle infinie sur un test          | 🟠      | Skip le test, noter en TODO  |
| Code incohérent / cassé             | 🔴      | Reset à un commit propre     |
| Coût > budget                       | 🔴      | STOP immédiat                |

### Guardrails Avancés

```markdown
## Guardrails (à ajouter dans PROMPT.md)

### Limites par Tour
- Max 3 fichiers modifiés par tour
- Max 200 lignes de code par tour
- Commit obligatoire si >50 lignes modifiées

### Validation Continue
- Après chaque modification : `npm test` ou équivalent
- Si tests cassés : réparer AVANT de continuer
- Si 3 échecs consécutifs : HARD STOP

### Points de Non-Retour
- NE PAS supprimer de fichiers sans raison explicite
- NE PAS modifier les dépendances sans validation
- NE PAS changer l'architecture sans checkpoint
```

---

## Template Workflow Complet

### Structure de Projet

```
projet/
├── specs/
│   └── requirements.md     # Phase 1 output
├── PROMPT.md               # Phase 2 output
├── TODO.md                 # Phase 2 output, Phase 3 state
├── loop.sh                 # Script d'exécution
└── src/                    # Phase 3 output
```

### Commandes par Phase

```bash
# PHASE 1 - Clarify
claude --print "Mode Clarify. Aide-moi à définir les requirements."
# → Créer specs/requirements.md
# → Valider avec l'humain

# PHASE 2 - Plan
claude --print "Mode Plan. Génère PROMPT.md et TODO.md depuis specs/."
# → Générer PROMPT.md
# → Générer TODO.md
# → Valider avec l'humain

# PHASE 3 - Execute
./loop.sh
# → Ralph travaille en autonomie
# → Surveiller les checkpoints
# → Récupérer le résultat
```

---

## Prochaine Étape

Découvrez les différentes [Implémentations](./06-implementations.md) de Ralph Wiggum disponibles.

---

[← Prompts Efficaces](./04-prompts-efficaces.md) | [Sommaire](./README.md) | [Implémentations →](./06-implementations.md)
