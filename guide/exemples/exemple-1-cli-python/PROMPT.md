# PROMPT.md - CLI Todo Python

## Contexte

Tu es en mode **Ralph Wiggum** - agent autonome.
Tu dois créer `todo.py`, une CLI de gestion de tâches en Python.

## Objectif

Créer une CLI Python qui permet d'ajouter, lister, compléter et supprimer des tâches via la ligne de commande, avec stockage persistant en JSON.

## Spécifications Techniques

### Stack
- Langage : Python 3.10+
- Dépendances : **aucune** (stdlib uniquement)
- Stockage : fichier JSON local (`todos.json`)
- Tests : pytest

### Interface CLI

| Commande                    | Description                    | Output attendu                |
|-----------------------------|--------------------------------|-------------------------------|
| `python todo.py add "txt"`  | Ajoute une tâche               | "Tâche ajoutée avec ID X"     |
| `python todo.py list`       | Liste toutes les tâches        | Format: "[x] ID: texte"       |
| `python todo.py done <id>`  | Marque terminée                | "Tâche X marquée comme terminée" |
| `python todo.py delete <id>`| Supprime la tâche              | "Tâche X supprimée"           |

### Structure des Données (todos.json)

```json
{
  "next_id": 3,
  "tasks": [
    {"id": 1, "text": "Acheter du lait", "done": false},
    {"id": 2, "text": "Appeler médecin", "done": true}
  ]
}
```

### Architecture

```
todo-cli/
├── todo.py          # Fichier principal avec argparse
├── todos.json       # Créé automatiquement
├── tests/
│   └── test_todo.py # Tests pytest
└── README.md
```

## Critères de Succès

1. [ ] `todo.py` existe et est exécutable
2. [ ] `python todo.py add "test"` fonctionne et retourne un message avec ID
3. [ ] `python todo.py list` affiche les tâches au format `[x] ID: texte`
4. [ ] `python todo.py done 1` marque la tâche 1 comme terminée
5. [ ] `python todo.py delete 1` supprime la tâche 1
6. [ ] Gestion d'erreur si ID inexistant
7. [ ] `python -m pytest tests/` : tous les tests passent
8. [ ] `README.md` avec sections Installation et Usage

## Workflow

1. Lis ce fichier et TODO.md
2. Crée la structure de base (`todo.py`, `tests/`)
3. Implémente les fonctions de stockage JSON
4. Implémente la commande `add`
5. Implémente la commande `list`
6. Implémente la commande `done`
7. Implémente la commande `delete`
8. Ajoute la gestion d'erreurs
9. Écris les tests
10. Écris le README
11. Vérifie tous les critères
12. Marque DONE dans TODO.md

## HARD STOP

**ARRÊTE-TOI** quand :
- Tous les critères de succès sont cochés [x] dans TODO.md
- OU tu as fait 30 tours sans progrès

Quand terminé, écris dans TODO.md :
```
- [x] DONE - Projet terminé
```

## Guardrails

### OBLIGATOIRE
- Un commit par fonctionnalité : `[Ralph] feat: description`
- Mettre à jour TODO.md après chaque commit
- Tester chaque commande après implémentation

### INTERDIT
- Modifier ce fichier PROMPT.md
- Utiliser des dépendances externes (requests, click, etc.)
- Supprimer des fichiers sans raison

## Notes Techniques

### Utilise argparse

```python
import argparse

parser = argparse.ArgumentParser(description='Gestionnaire de tâches')
subparsers = parser.add_subparsers(dest='command')

# Exemple pour add
add_parser = subparsers.add_parser('add')
add_parser.add_argument('text', help='Texte de la tâche')
```

### Format d'affichage list

```
[ ] 1: Acheter du lait
[x] 2: Appeler médecin
```

### Gestion du fichier JSON

- Créer le fichier s'il n'existe pas
- Utiliser `json.load()` et `json.dump()`
- Indentation de 2 espaces pour lisibilité
