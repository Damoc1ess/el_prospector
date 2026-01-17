# Exemple 3 : Migration Jest → Vitest

## Description

Ce projet exemple migre une suite de tests Jest existante vers Vitest, en conservant tous les tests fonctionnels.

**Idéal pour :** Comprendre les tâches de refactoring/migration avec Ralph.

## Caractéristiques

| Aspect           | Valeur                        |
|------------------|-------------------------------|
| Type             | Migration/Refactoring         |
| Source           | Jest                          |
| Cible            | Vitest                        |
| Tests existants  | 15+ tests                     |
| Coût estimé      | $10-20                        |
| Tours estimés    | 30-50                         |

## Scénario

Vous avez un projet Node.js avec Jest pour les tests. Vous souhaitez migrer vers Vitest pour :
- Performance améliorée (ESM natif)
- Meilleure compatibilité avec Vite
- API similaire à Jest

## Ce que Ralph Doit Faire

1. Analyser les tests Jest existants
2. Remplacer les dépendances (jest → vitest)
3. Migrer la configuration (jest.config.js → vitest.config.js)
4. Adapter la syntaxe si nécessaire
5. Vérifier que tous les tests passent

## Structure du Projet Source

```
project/
├── src/
│   ├── calculator.js    # Module exemple
│   ├── stringUtils.js   # Module exemple
│   └── arrayUtils.js    # Module exemple
├── tests/
│   ├── calculator.test.js
│   ├── stringUtils.test.js
│   └── arrayUtils.test.js
├── jest.config.js
├── package.json
└── README.md
```

## Différences Jest vs Vitest

| Aspect              | Jest                    | Vitest                   |
|---------------------|-------------------------|--------------------------|
| Import              | Automatique (globals)   | `import { test } from 'vitest'` |
| Config              | jest.config.js          | vitest.config.js         |
| Commande            | `jest`                  | `vitest`                 |
| Mocking             | `jest.fn()`             | `vi.fn()`                |
| Timers              | `jest.useFakeTimers()`  | `vi.useFakeTimers()`     |

## Comment Lancer

```bash
# 1. Créer le projet source
mkdir migration-test && cd migration-test
git init

# 2. Copier les fichiers PROMPT.md et TODO.md

# 3. Créer les fichiers source Jest (voir ci-dessous)

# 4. Lancer Ralph
claude --ralph "Exécute PROMPT.md"
```

## Fichiers Source à Créer

Avant de lancer Ralph, créez ces fichiers pour avoir une base Jest à migrer :

### src/calculator.js
```javascript
export function add(a, b) { return a + b; }
export function subtract(a, b) { return a - b; }
export function multiply(a, b) { return a * b; }
export function divide(a, b) {
  if (b === 0) throw new Error('Division by zero');
  return a / b;
}
```

### tests/calculator.test.js (Jest)
```javascript
const { add, subtract, multiply, divide } = require('../src/calculator');

describe('Calculator', () => {
  test('adds two numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  test('subtracts two numbers', () => {
    expect(subtract(5, 3)).toBe(2);
  });

  test('multiplies two numbers', () => {
    expect(multiply(3, 4)).toBe(12);
  });

  test('divides two numbers', () => {
    expect(divide(10, 2)).toBe(5);
  });

  test('throws on division by zero', () => {
    expect(() => divide(10, 0)).toThrow('Division by zero');
  });
});
```

### jest.config.js
```javascript
module.exports = {
  testEnvironment: 'node',
  testMatch: ['**/tests/**/*.test.js']
};
```

## Résultat Attendu

Après migration :
- `vitest.config.js` remplace `jest.config.js`
- Tests utilisent `import` au lieu de `require`
- `npm test` lance Vitest au lieu de Jest
- Tous les 15+ tests passent

## Vérification

```bash
# Vérifier que Vitest est installé
npm list vitest

# Lancer les tests
npm test

# Vérifier la sortie
# ✓ src/calculator.js (5 tests)
# ✓ src/stringUtils.js (5 tests)
# ✓ src/arrayUtils.js (5 tests)
```

## Notes

- Ralph ne doit PAS modifier le code source (src/), seulement les tests
- La logique métier reste inchangée
- Seule la couche de test est migrée
