# 03 - Premiers Pas avec Ralph Wiggum

Ce chapitre vous guide pas à pas dans la création de votre premier projet autonome avec Ralph Wiggum.

---

## Projet Exemple : CLI Todo en Python

Nous allons créer une CLI simple de gestion de tâches en Python. C'est un projet idéal pour débuter car :
- Scope limité et bien défini
- Pas de dépendances externes complexes
- Résultat facilement vérifiable

---

## Étape 1 : Créer la Structure du Projet

```bash
# Créer le dossier et initialiser git
mkdir ralph-todo-cli && cd ralph-todo-cli
git init

# Créer la structure
mkdir -p specs tests
touch PROMPT.md TODO.md specs/requirements.md
```

---

## Étape 2 : Écrire le PROMPT.md

Le PROMPT.md est le "cerveau" de Ralph. Il contient toutes les instructions.

```markdown
# PROMPT.md

## Contexte

Tu es en mode Ralph Wiggum. Tu dois créer une CLI de gestion de tâches en Python.
Travaille de manière autonome jusqu'à ce que tous les critères soient remplis.

## Objectif

Créer `todo.py`, une CLI Python qui permet de :
- Ajouter des tâches
- Lister les tâches
- Marquer une tâche comme terminée
- Supprimer une tâche

## Spécifications Techniques

### Stack
- Python 3.10+
- Pas de dépendances externes (stdlib only)
- Stockage : fichier JSON local (`todos.json`)

### Interface CLI

```
python todo.py add "Acheter du lait"
python todo.py list
python todo.py done 1
python todo.py delete 1
```

### Structure des Données (todos.json)

```json
{
  "tasks": [
    {"id": 1, "text": "Acheter du lait", "done": false, "created": "2026-01-17"}
  ]
}
```

## Critères de Succès (OBLIGATOIRES)

1. [ ] `todo.py` existe et est exécutable
2. [ ] La commande `add` fonctionne
3. [ ] La commande `list` affiche les tâches
4. [ ] La commande `done` marque une tâche
5. [ ] La commande `delete` supprime une tâche
6. [ ] Les tests passent (`python -m pytest tests/`)
7. [ ] Un README.md docummente l'usage

## Workflow

1. Lis ce fichier et specs/requirements.md
2. Mets à jour TODO.md avec ton plan
3. Implémente chaque fonctionnalité
4. Écris les tests
5. Vérifie que tout fonctionne
6. Mets à jour TODO.md en cochant les tâches

## HARD STOP

**ARRÊTE-TOI** quand :
- Tous les critères de succès sont cochés [x] dans TODO.md
- OU tu as fait plus de 50 itérations sans progrès
- OU tu rencontres une erreur que tu ne peux pas résoudre

Ne continue PAS indéfiniment. Si bloqué, écris le problème dans TODO.md et arrête.

## Guardrails

- UN commit par fonctionnalité complète
- Message de commit format : "[Ralph] feat: description"
- Ne modifie PAS ce fichier PROMPT.md
- Ne supprime PAS les fichiers existants sauf erreur
```

---

## Étape 3 : Écrire le TODO.md Initial

Le TODO.md track l'avancement. Ralph le met à jour au fur et à mesure.

```markdown
# TODO.md

## Status: EN COURS

## Critères de Succès

- [ ] `todo.py` existe et est exécutable
- [ ] Commande `add` fonctionne
- [ ] Commande `list` fonctionne
- [ ] Commande `done` fonctionne
- [ ] Commande `delete` fonctionne
- [ ] Tests passent
- [ ] README.md existe

## Plan d'Exécution

- [ ] Créer la structure de base de todo.py
- [ ] Implémenter le stockage JSON
- [ ] Implémenter la commande `add`
- [ ] Implémenter la commande `list`
- [ ] Implémenter la commande `done`
- [ ] Implémenter la commande `delete`
- [ ] Écrire les tests
- [ ] Écrire le README
- [ ] Vérification finale

## Notes

(Ralph ajoutera ses notes ici)

## HARD STOP TRIGGER

Quand tous les critères sont cochés, marquer :
- [x] DONE - Projet terminé
```

---

## Étape 4 : Ajouter les Spécifications

```markdown
# specs/requirements.md

## Exigences Fonctionnelles

### RF1 - Ajout de tâche
- Entrée : texte de la tâche
- Sortie : confirmation avec ID attribué
- ID auto-incrémenté

### RF2 - Liste des tâches
- Affiche toutes les tâches
- Format : `[ID] [STATUS] Texte`
- STATUS : `[ ]` ou `[x]`

### RF3 - Marquer terminé
- Entrée : ID de la tâche
- Change le status à done=true
- Erreur si ID inexistant

### RF4 - Suppression
- Entrée : ID de la tâche
- Supprime la tâche du fichier
- Erreur si ID inexistant

## Exigences Non-Fonctionnelles

- Le fichier JSON doit être formatté (indent=2)
- Gestion d'erreurs explicite
- Messages utilisateur clairs
```

---

## Étape 5 : Lancer Ralph

### Option A : Lancement Simple

```bash
claude --print "Lis PROMPT.md et commence à travailler. Mets à jour TODO.md régulièrement."
```

### Option B : Avec Script de Boucle

Créez `loop.sh` :

```bash
#!/bin/bash
# loop.sh - Boucle Ralph Wiggum

MAX_ITERATIONS=50
SLEEP_BETWEEN=5
HARD_STOP_PATTERN="DONE - Projet terminé"

iteration=0

while [ $iteration -lt $MAX_ITERATIONS ]; do
    iteration=$((iteration + 1))
    echo "=== Iteration $iteration / $MAX_ITERATIONS ==="

    # Vérifier le HARD STOP
    if grep -q "$HARD_STOP_PATTERN" TODO.md 2>/dev/null; then
        echo "✅ HARD STOP détecté - Projet terminé!"
        exit 0
    fi

    # Lancer Claude
    claude --print "Continue ton travail sur le projet. Lis TODO.md pour savoir où tu en es. Mets à jour TODO.md après chaque étape."

    # Commit automatique
    git add -A
    git commit -m "[Ralph] Iteration $iteration" --allow-empty 2>/dev/null

    # Pause entre itérations
    sleep $SLEEP_BETWEEN
done

echo "⚠️ Max iterations atteint"
```

Lancez :

```bash
chmod +x loop.sh
./loop.sh
```

---

## Étape 6 : Observer le Comportement

Pendant que Ralph travaille, vous pouvez :

### Suivre les Commits

```bash
# Dans un autre terminal
watch -n 5 'git log --oneline -10'
```

### Voir le TODO.md

```bash
watch -n 5 'cat TODO.md'
```

### Logs en Temps Réel

```bash
tail -f ~/.claude/logs/latest.log
```

---

## Ce à Quoi S'attendre

### Itérations Typiques

| Iteration | Action de Ralph                                   |
|-----------|---------------------------------------------------|
| 1-2       | Lit les fichiers, crée la structure de base       |
| 3-5       | Implémente `add` et `list`                        |
| 6-8       | Implémente `done` et `delete`                     |
| 9-12      | Écrit les tests, corrige les bugs                 |
| 13-15     | Écrit le README, vérifications finales            |
| 16        | Marque DONE dans TODO.md, s'arrête                |

### Coût Estimé

Pour ce projet simple :
- Tokens d'entrée : ~50,000
- Tokens de sortie : ~20,000
- **Coût total : ~$3-5**

---

## Vérification du Résultat

Une fois Ralph terminé :

```bash
# Vérifier la structure
ls -la

# Tester manuellement
python todo.py add "Test tâche"
python todo.py list
python todo.py done 1
python todo.py list
python todo.py delete 1

# Lancer les tests
python -m pytest tests/ -v

# Voir l'historique git
git log --oneline
```

---

## Exercices Pratiques

### Exercice 1 : Ajouter une Fonctionnalité

Modifiez le PROMPT.md pour ajouter :
- Une commande `priority` pour définir la priorité (haute/moyenne/basse)
- Relancez Ralph

### Exercice 2 : Améliorer les Tests

Modifiez TODO.md pour demander :
- Tests de cas limites (tâche inexistante, JSON corrompu)
- Couverture > 80%

### Exercice 3 : Mode Docker

Relancez le même projet dans un conteneur Docker pour pratiquer le sandboxing.

---

## Troubleshooting Premiers Pas

### "Claude ne trouve pas le fichier"

```bash
# Vérifier que vous êtes dans le bon dossier
pwd
ls -la PROMPT.md
```

### "Ralph tourne en boucle sans progresser"

Vérifiez que le PROMPT.md contient :
- Des critères de succès clairs et vérifiables
- Un HARD STOP explicite

### "Les commits ne se font pas"

```bash
# Vérifier que git est initialisé
git status

# Initialiser si nécessaire
git init
git add .
git commit -m "Initial commit"
```

---

## Prochaine Étape

Maintenant que vous avez réussi votre premier projet, apprenez à écrire des [Prompts Efficaces](./04-prompts-efficaces.md) pour des tâches plus complexes.

---

[← Installation](./02-installation.md) | [Sommaire](./README.md) | [Prompts Efficaces →](./04-prompts-efficaces.md)
