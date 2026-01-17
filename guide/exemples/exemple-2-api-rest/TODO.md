# TODO.md - API REST Notes

## Status: EN COURS

## Critères de Succès

- [ ] `npm install` s'exécute sans erreur
- [ ] `npm start` démarre sur port 3000
- [ ] GET /api/notes fonctionne
- [ ] POST /api/notes fonctionne
- [ ] GET /api/notes/:id fonctionne
- [ ] PUT /api/notes/:id fonctionne
- [ ] DELETE /api/notes/:id fonctionne
- [ ] Validation retourne 400 si invalide
- [ ] Tests passent : `npm test`
- [ ] README.md complet

## Plan d'Exécution

### Phase 1 : Setup (Tours 1-5)
- [ ] Créer package.json avec `npm init -y`
- [ ] Ajouter `"type": "module"`
- [ ] Installer les dépendances
- [ ] Créer la structure de dossiers
- [ ] Configurer Express de base avec health check
- [ ] Commit : setup initial

### Phase 2 : Storage (Tours 6-10)
- [ ] Configurer lowdb dans src/db/index.js
- [ ] Créer les fonctions CRUD de base
- [ ] Tester le stockage
- [ ] Commit : storage layer

### Phase 3 : Validation (Tours 11-15)
- [ ] Créer schémas Zod dans src/schemas/note.js
- [ ] Créer middleware validation
- [ ] Créer middleware error handler
- [ ] Commit : validation layer

### Phase 4 : Routes (Tours 16-35)
- [ ] Implémenter GET /api/notes
- [ ] Tester avec curl
- [ ] Implémenter POST /api/notes
- [ ] Tester avec curl
- [ ] Implémenter GET /api/notes/:id
- [ ] Tester avec curl
- [ ] Implémenter PUT /api/notes/:id
- [ ] Tester avec curl
- [ ] Implémenter DELETE /api/notes/:id
- [ ] Tester avec curl
- [ ] Commit : routes complètes

### Phase 5 : Tests (Tours 36-50)
- [ ] Configurer Vitest
- [ ] Tests GET /api/notes
- [ ] Tests POST /api/notes
- [ ] Tests GET /api/notes/:id
- [ ] Tests PUT /api/notes/:id
- [ ] Tests DELETE /api/notes/:id
- [ ] Tests validation errors
- [ ] Tests 404 errors
- [ ] Vérifier tous les tests passent
- [ ] Commit : tests complets

### Phase 6 : Documentation (Tours 51-60)
- [ ] Écrire README.md
- [ ] Documenter tous les endpoints
- [ ] Ajouter exemples curl
- [ ] Commit : documentation

### Phase 7 : Validation Finale
- [ ] Vérifier tous les critères
- [ ] Commit final

## Checkpoints

- [ ] CHECKPOINT 1 (Tour 10) : Setup + Storage OK
- [ ] CHECKPOINT 2 (Tour 20) : 3 routes fonctionnelles
- [ ] CHECKPOINT 3 (Tour 40) : Toutes routes + validation
- [ ] CHECKPOINT 4 (Tour 55) : Tests passent

## État Actuel

**Tour actuel :** 0
**Dernière action :** En attente
**Prochaine action :** npm init, installer deps

## Notes

(Ralph ajoute ses notes ici)

## Commandes de Test

```bash
# Health check
curl http://localhost:3000/health

# Liste notes
curl http://localhost:3000/api/notes

# Créer note
curl -X POST http://localhost:3000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "content": "Hello"}'

# Récupérer note
curl http://localhost:3000/api/notes/{id}

# Mettre à jour
curl -X PUT http://localhost:3000/api/notes/{id} \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated"}'

# Supprimer
curl -X DELETE http://localhost:3000/api/notes/{id}
```

## HARD STOP TRIGGER

<!-- - [x] DONE - Projet terminé -->
