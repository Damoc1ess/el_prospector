# TODO.md - Migration Jest → Vitest

## Status: EN COURS

## Critères de Succès

- [ ] `jest` retiré des dépendances
- [ ] `vitest` ajouté aux dépendances
- [ ] `jest.config.js` supprimé
- [ ] `vitest.config.js` créé
- [ ] Script "test" mis à jour
- [ ] Fichiers .test.js en syntaxe ESM
- [ ] `jest.*` remplacés par `vi.*`
- [ ] `npm test` sans erreur
- [ ] TOUS les tests passent

## Plan d'Exécution

### Phase 1 : Analyse (Tours 1-5)
- [ ] Lister tous les fichiers de test
- [ ] Identifier les patterns Jest utilisés
- [ ] Compter le nombre total de tests
- [ ] Noter les éventuels mocks/spies

### Phase 2 : Dépendances (Tours 6-10)
- [ ] Retirer `jest` de package.json
- [ ] Ajouter `vitest` à package.json
- [ ] Mettre à jour le script "test"
- [ ] Ajouter `"type": "module"` si nécessaire
- [ ] `npm install`
- [ ] Commit : deps updated

### Phase 3 : Configuration (Tours 11-15)
- [ ] Créer `vitest.config.js`
- [ ] Supprimer `jest.config.js`
- [ ] Commit : config migrated

### Phase 4 : Migration des Tests (Tours 16-40)
- [ ] Migrer tests/calculator.test.js
- [ ] Vérifier : `npm test -- tests/calculator.test.js`
- [ ] Commit : migrate calculator tests
- [ ] Migrer tests/stringUtils.test.js
- [ ] Vérifier : `npm test -- tests/stringUtils.test.js`
- [ ] Commit : migrate stringUtils tests
- [ ] Migrer tests/arrayUtils.test.js
- [ ] Vérifier : `npm test -- tests/arrayUtils.test.js`
- [ ] Commit : migrate arrayUtils tests
- [ ] (Ajouter d'autres fichiers si trouvés)

### Phase 5 : Validation (Tours 41-50)
- [ ] Lancer tous les tests : `npm test`
- [ ] Vérifier que le nombre de tests est identique
- [ ] Vérifier qu'aucun test n'est skip
- [ ] Commit final

## Checkpoints

- [ ] CHECKPOINT 1 (Tour 10) : Dépendances migrées
- [ ] CHECKPOINT 2 (Tour 15) : Config migrée
- [ ] CHECKPOINT 3 (Tour 30) : 50% des fichiers migrés
- [ ] CHECKPOINT 4 (Tour 45) : Tous tests passent

## État Actuel

**Tour actuel :** 0
**Dernière action :** En attente
**Prochaine action :** Analyser les tests existants

## Inventaire Initial

### Fichiers de Test Trouvés
(À remplir par Ralph)

| Fichier              | Tests | Mocks | Status      |
|----------------------|-------|-------|-------------|
| calculator.test.js   | ?     | ?     | À migrer    |
| stringUtils.test.js  | ?     | ?     | À migrer    |
| arrayUtils.test.js   | ?     | ?     | À migrer    |

### Patterns Jest Détectés
(À remplir par Ralph)
- [ ] jest.fn()
- [ ] jest.mock()
- [ ] jest.spyOn()
- [ ] jest.useFakeTimers()
- [ ] beforeAll/beforeEach
- [ ] afterAll/afterEach

## Notes

(Ralph ajoute ses observations ici)

## Problèmes Rencontrés

(Ralph documente les problèmes)

## HARD STOP TRIGGER

<!-- - [x] DONE - Migration terminée -->
