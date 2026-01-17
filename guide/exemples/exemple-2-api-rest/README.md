# Exemple 2 : API REST avec Express.js

## Description

Ce projet exemple crée une API REST de gestion de notes avec Express.js, incluant validation, tests et documentation.

**Idéal pour :** Projet intermédiaire, comprendre la gestion de dépendances npm.

## Caractéristiques

| Aspect           | Valeur                        |
|------------------|-------------------------------|
| Langage          | Node.js 18+                   |
| Framework        | Express.js                    |
| Validation       | Zod                           |
| Stockage         | JSON fichier (lowdb)          |
| Tests            | Vitest + Supertest            |
| Coût estimé      | $15-25                        |
| Tours estimés    | 40-60                         |

## Fonctionnalités à Implémenter

### Endpoints

| Méthode | Route           | Description              |
|---------|-----------------|--------------------------|
| GET     | /api/notes      | Liste toutes les notes   |
| GET     | /api/notes/:id  | Récupère une note        |
| POST    | /api/notes      | Crée une note            |
| PUT     | /api/notes/:id  | Met à jour une note      |
| DELETE  | /api/notes/:id  | Supprime une note        |

### Structure d'une Note

```json
{
  "id": "uuid-v4",
  "title": "Ma note",
  "content": "Contenu de la note",
  "tags": ["important", "travail"],
  "createdAt": "2026-01-17T10:00:00Z",
  "updatedAt": "2026-01-17T10:00:00Z"
}
```

## Structure Attendue

```
notes-api/
├── src/
│   ├── index.js         # Point d'entrée
│   ├── routes/
│   │   └── notes.js     # Routes API
│   ├── middleware/
│   │   └── validate.js  # Middleware validation
│   └── db/
│       └── index.js     # Connexion lowdb
├── tests/
│   └── notes.test.js    # Tests API
├── data/
│   └── db.json          # Base de données
├── package.json
└── README.md
```

## Comment Lancer

```bash
# 1. Créer un nouveau dossier
mkdir notes-api && cd notes-api
git init

# 2. Copier les fichiers PROMPT.md et TODO.md de cet exemple

# 3. Lancer Ralph (assurez-vous que npm est disponible)
claude --ralph "Exécute PROMPT.md"
```

## Résultat Attendu

```bash
# Démarrer le serveur
npm start
# → Server running on port 3000

# Tester les endpoints
curl http://localhost:3000/api/notes
# → []

curl -X POST http://localhost:3000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "content": "Hello"}'
# → {"id": "...", "title": "Test", ...}

curl http://localhost:3000/api/notes
# → [{"id": "...", "title": "Test", ...}]
```

## Vérification

```bash
# Installer et lancer les tests
npm install
npm test

# Vérifier le lint (optionnel)
npm run lint
```

## Notes

- L'API utilise lowdb pour un stockage JSON simple
- Zod valide les entrées côté serveur
- Les tests utilisent une base de données en mémoire
- CORS est activé pour permettre les requêtes cross-origin
