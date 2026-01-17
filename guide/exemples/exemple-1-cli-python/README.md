# Exemple 1 : CLI Todo en Python

## Description

Ce projet exemple crée une CLI de gestion de tâches en Python pur (sans dépendances externes).

**Idéal pour :** Premier projet Ralph, comprendre le workflow de base.

## Caractéristiques

| Aspect           | Valeur                        |
|------------------|-------------------------------|
| Langage          | Python 3.10+                  |
| Dépendances      | Aucune (stdlib uniquement)    |
| Stockage         | Fichier JSON local            |
| Tests            | pytest                        |
| Coût estimé      | $5-10                         |
| Tours estimés    | 15-25                         |

## Fonctionnalités à Implémenter

1. `todo add "texte"` - Ajouter une tâche
2. `todo list` - Lister toutes les tâches
3. `todo done <id>` - Marquer une tâche comme terminée
4. `todo delete <id>` - Supprimer une tâche

## Structure Attendue

```
todo-cli/
├── todo.py              # CLI principale
├── todos.json           # Stockage des données
├── tests/
│   └── test_todo.py     # Tests unitaires
└── README.md            # Documentation
```

## Comment Lancer

```bash
# 1. Créer un nouveau dossier
mkdir todo-cli && cd todo-cli
git init

# 2. Copier les fichiers PROMPT.md et TODO.md de cet exemple

# 3. Lancer Ralph
claude --ralph "Exécute PROMPT.md"

# Ou avec le script de boucle:
# cp ../../templates/loop.sh .
# chmod +x loop.sh
# ./loop.sh
```

## Résultat Attendu

Après complétion, vous devriez pouvoir :

```bash
# Ajouter des tâches
python todo.py add "Acheter du lait"
# → Tâche ajoutée avec ID 1

python todo.py add "Appeler le médecin"
# → Tâche ajoutée avec ID 2

# Lister
python todo.py list
# → [ ] 1: Acheter du lait
# → [ ] 2: Appeler le médecin

# Marquer terminé
python todo.py done 1
# → Tâche 1 marquée comme terminée

# Lister à nouveau
python todo.py list
# → [x] 1: Acheter du lait
# → [ ] 2: Appeler le médecin

# Supprimer
python todo.py delete 1
# → Tâche 1 supprimée
```

## Vérification

```bash
# Tests
python -m pytest tests/ -v

# Vérification manuelle
python todo.py add "Test"
python todo.py list
python todo.py done 1
python todo.py delete 1
```

## Notes

- Cet exemple utilise `argparse` pour le parsing CLI
- Le fichier `todos.json` est créé automatiquement
- Les IDs sont auto-incrémentés et ne sont pas réutilisés après suppression
