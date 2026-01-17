# PROMPT.md - API REST Notes Express.js

## Contexte

Tu es en mode **Ralph Wiggum** - agent autonome.
Tu dois créer une API REST de gestion de notes avec Express.js.

## Objectif

Créer une API REST complète avec CRUD, validation des entrées, tests automatisés et documentation.

## Spécifications Techniques

### Stack

| Élément         | Technologie                    |
|-----------------|--------------------------------|
| Runtime         | Node.js 18+                    |
| Framework       | Express.js 4.x                 |
| Validation      | Zod                            |
| Stockage        | lowdb (JSON file)              |
| Tests           | Vitest + Supertest             |
| IDs             | uuid v4                        |

### Dépendances Autorisées

```json
{
  "dependencies": {
    "express": "^4.18.0",
    "zod": "^3.22.0",
    "lowdb": "^7.0.0",
    "uuid": "^9.0.0",
    "cors": "^2.8.0"
  },
  "devDependencies": {
    "vitest": "^1.0.0",
    "supertest": "^6.3.0"
  }
}
```

### Architecture

```
notes-api/
├── src/
│   ├── index.js           # Point d'entrée, config Express
│   ├── routes/
│   │   └── notes.js       # Routes CRUD notes
│   ├── middleware/
│   │   ├── validate.js    # Middleware validation Zod
│   │   └── errorHandler.js # Gestion erreurs globale
│   ├── schemas/
│   │   └── note.js        # Schémas Zod
│   └── db/
│       └── index.js       # Config lowdb
├── tests/
│   └── notes.test.js      # Tests API
├── data/
│   └── db.json            # Fichier DB (gitignore)
├── package.json
├── .gitignore
└── README.md
```

### API Endpoints

| Méthode | Route              | Body              | Response                     |
|---------|--------------------|--------------------|------------------------------|
| GET     | /api/notes         | -                  | 200: Note[]                  |
| GET     | /api/notes/:id     | -                  | 200: Note \| 404: error      |
| POST    | /api/notes         | {title, content, tags?} | 201: Note \| 400: error |
| PUT     | /api/notes/:id     | {title?, content?, tags?} | 200: Note \| 404: error |
| DELETE  | /api/notes/:id     | -                  | 204 \| 404: error            |

### Schéma Note

```typescript
interface Note {
  id: string;          // UUID v4
  title: string;       // 1-100 chars, requis
  content: string;     // 1-10000 chars, requis
  tags: string[];      // Optionnel, max 10 tags
  createdAt: string;   // ISO 8601
  updatedAt: string;   // ISO 8601
}
```

### Format Erreur

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title is required",
    "details": [...]
  }
}
```

## Critères de Succès

1. [ ] `npm install` s'exécute sans erreur
2. [ ] `npm start` démarre le serveur sur port 3000
3. [ ] GET /api/notes retourne un tableau (vide ou non)
4. [ ] POST /api/notes crée une note et retourne 201
5. [ ] GET /api/notes/:id retourne la note ou 404
6. [ ] PUT /api/notes/:id met à jour et retourne 200
7. [ ] DELETE /api/notes/:id supprime et retourne 204
8. [ ] POST avec données invalides retourne 400
9. [ ] `npm test` : tous les tests passent (10+ tests)
10. [ ] README.md avec documentation API complète

## Workflow

1. Lis ce fichier et TODO.md
2. Initialise le projet npm (`npm init -y`)
3. Installe les dépendances
4. Configure Express de base avec health check
5. Implémente le stockage lowdb
6. Implémente les schémas Zod
7. Implémente les routes une par une
8. Ajoute la gestion d'erreurs
9. Écris les tests
10. Écris le README
11. Vérifie tous les critères
12. Marque DONE dans TODO.md

## HARD STOP

**ARRÊTE-TOI** quand :
- Tous les critères sont cochés [x] dans TODO.md
- OU tu as fait 60 tours sans progrès

## Guardrails

### OBLIGATOIRE
- `npm install` après modification de package.json
- Tester chaque endpoint après implémentation avec curl
- Un commit par fonctionnalité

### INTERDIT
- Modifier ce fichier PROMPT.md
- Installer des dépendances non listées
- Utiliser une vraie base de données (SQLite, MongoDB, etc.)

### NOTES
- lowdb v7 est ESM-only, utilise `"type": "module"` dans package.json
- Pour les tests, crée une instance lowdb en mémoire
