# PROMPT.md - Migration Jest → Vitest

## Contexte

Tu es en mode **Ralph Wiggum** - agent autonome.
Tu dois migrer une suite de tests Jest vers Vitest.

## Objectif

Migrer tous les tests Jest existants vers Vitest en conservant la même couverture de tests et en s'assurant que tous les tests passent.

## Spécifications

### Stack Initiale (Jest)

```json
{
  "devDependencies": {
    "jest": "^29.0.0"
  },
  "scripts": {
    "test": "jest"
  }
}
```

### Stack Cible (Vitest)

```json
{
  "devDependencies": {
    "vitest": "^1.0.0"
  },
  "scripts": {
    "test": "vitest run"
  }
}
```

### Mapping des Changements

| Jest                     | Vitest                           |
|--------------------------|----------------------------------|
| `jest.config.js`         | `vitest.config.js`               |
| `require('...')`         | `import ... from '...'`          |
| `jest.fn()`              | `vi.fn()`                        |
| `jest.mock()`            | `vi.mock()`                      |
| `jest.spyOn()`           | `vi.spyOn()`                     |
| `jest.useFakeTimers()`   | `vi.useFakeTimers()`             |
| `jest.runAllTimers()`    | `vi.runAllTimers()`              |
| `beforeAll/beforeEach`   | Identique (importer de vitest)   |
| `describe/test/expect`   | Identique (importer de vitest)   |

### vitest.config.js Cible

```javascript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,  // Optionnel: permet de ne pas importer describe/test/expect
    environment: 'node',
    include: ['tests/**/*.test.js']
  }
});
```

## Critères de Succès

1. [ ] `jest` retiré des dépendances
2. [ ] `vitest` ajouté aux dépendances
3. [ ] `jest.config.js` supprimé
4. [ ] `vitest.config.js` créé
5. [ ] package.json script "test" mis à jour
6. [ ] Tous les fichiers .test.js utilisent la syntaxe ESM
7. [ ] Tous les `jest.*` remplacés par `vi.*`
8. [ ] `npm test` s'exécute sans erreur
9. [ ] TOUS les tests passent (même nombre qu'avant)
10. [ ] Pas de régression fonctionnelle

## Workflow

1. Lis ce fichier et TODO.md
2. **Analyse** : Liste tous les fichiers de test existants
3. **Inventaire** : Note les patterns Jest utilisés (mocks, spies, timers)
4. **Dépendances** : Remplace jest par vitest dans package.json
5. **Config** : Crée vitest.config.js, supprime jest.config.js
6. **Migration** : Pour CHAQUE fichier de test :
   a. Convertir les imports
   b. Remplacer jest.* par vi.*
   c. Vérifier que le fichier est valide
7. **Validation** : Lance `npm test`, vérifie que tous les tests passent
8. Commit et marque DONE

## HARD STOP

**ARRÊTE-TOI** quand :
- Tous les critères sont cochés [x] dans TODO.md
- OU tu as fait 50 tours sans progrès

## Guardrails

### OBLIGATOIRE
- Lire TODO.md à chaque tour
- Commit après chaque fichier migré
- Format : `[Ralph] refactor: migrate X.test.js to vitest`

### INTERDIT ⚠️
- **NE JAMAIS modifier les fichiers dans src/** (code source)
- Ne modifier QUE les fichiers de test et de config
- Ne pas changer la logique des tests
- Ne pas supprimer de tests

### VALIDATION
Après chaque fichier migré :
```bash
npm test -- tests/[fichier].test.js
```

Si un test échoue :
1. Vérifie la syntaxe
2. Vérifie les imports
3. Vérifie les mocks
4. Si toujours en échec après 3 tentatives : note dans TODO.md et passe au suivant

## Notes Techniques

### Pattern de Migration Fichier

```javascript
// AVANT (Jest)
const { myFunc } = require('../src/module');

describe('myFunc', () => {
  test('does something', () => {
    expect(myFunc()).toBe(true);
  });
});

// APRÈS (Vitest)
import { describe, test, expect } from 'vitest';
import { myFunc } from '../src/module.js';

describe('myFunc', () => {
  test('does something', () => {
    expect(myFunc()).toBe(true);
  });
});
```

### Si globals: true dans config

```javascript
// Pas besoin d'importer describe/test/expect
import { myFunc } from '../src/module.js';

describe('myFunc', () => {
  test('does something', () => {
    expect(myFunc()).toBe(true);
  });
});
```

### Migration des Mocks

```javascript
// AVANT (Jest)
jest.mock('../src/api');
const mockFn = jest.fn();
jest.spyOn(obj, 'method');

// APRÈS (Vitest)
import { vi } from 'vitest';
vi.mock('../src/api');
const mockFn = vi.fn();
vi.spyOn(obj, 'method');
```
