# Guide Ralph Wiggum - Claude Code en Mode Autonome

> "Me fail English? That's unpossible!" - Ralph Wiggum

## Qu'est-ce que Ralph Wiggum ?

**Ralph Wiggum** est une technique qui permet de faire tourner Claude Code CLI en boucle autonome pendant des heures, voire des jours. Au lieu de superviser chaque étape, vous définissez une tâche complexe et laissez l'agent travailler seul jusqu'à complétion.

Le nom vient du personnage des Simpsons : comme Ralph, l'agent peut sembler "déterministiquement mauvais" sur certaines tâches individuelles, mais avec suffisamment d'itérations et de persistance (via fichiers et git), il finit par accomplir des projets entiers.

---

## Table des Matières

| #  | Chapitre                                                     | Description                           |
|----|--------------------------------------------------------------|---------------------------------------|
| 01 | [Introduction](./01-introduction.md)                         | Philosophie et fonctionnement         |
| 02 | [Installation](./02-installation.md)                         | Setup du plugin officiel              |
| 03 | [Premiers Pas](./03-premiers-pas.md)                         | Votre premier projet Ralph            |
| 04 | [Prompts Efficaces](./04-prompts-efficaces.md)               | Templates et bonnes pratiques         |
| 05 | [Workflow Avancé](./05-workflow-avance.md)                   | Les 3 phases : Clarify, Plan, Execute |
| 06 | [Implémentations](./06-implementations.md)                   | Plugin officiel et alternatives       |
| 07 | [Sécurité & Coûts](./07-securite-couts.md)                   | Sandboxing et optimisation            |
| 08 | [Troubleshooting](./08-troubleshooting.md)                   | Erreurs courantes et solutions        |
| 09 | [Cas d'Étude](./09-cas-etude.md)                             | Success stories et échecs             |
| 10 | [Comparatif](./10-comparatif.md)                             | Comparaison détaillée des outils      |

---

## Ressources Prêtes à l'Emploi

### Templates
- [`PROMPT-minimal.md`](./templates/PROMPT-minimal.md) - Template basique pour démarrer
- [`PROMPT-playbook.md`](./templates/PROMPT-playbook.md) - Template avancé avec guardrails
- [`TODO-template.md`](./templates/TODO-template.md) - Format TODO avec HARD STOP
- [`loop.sh`](./templates/loop.sh) - Script bash orchestrateur

### Exemples Complets
- [`exemple-1-cli-python/`](./exemples/exemple-1-cli-python/) - CLI de gestion de tâches (~$5-10)
- [`exemple-2-api-rest/`](./exemples/exemple-2-api-rest/) - API REST Express.js (~$15-25)
- [`exemple-3-refactoring/`](./exemples/exemple-3-refactoring/) - Migration Jest → Vitest (~$10-20)

---

## Prérequis

Avant de commencer, assurez-vous d'avoir :

| Outil          | Version minimale | Vérification                |
|----------------|------------------|-----------------------------|
| Claude Code    | v1.0+            | `claude --version`          |
| Node.js        | v18+             | `node --version`            |
| Git            | v2.30+           | `git --version`             |
| Docker         | v24+ (optionnel) | `docker --version`          |
| jq             | v1.6+            | `jq --version`              |

Installation rapide des dépendances (macOS) :
```bash
brew install jq
```

---

## Par Où Commencer ?

### Niveau Débutant
1. Lisez l'[Introduction](./01-introduction.md) pour comprendre le concept
2. Suivez le guide d'[Installation](./02-installation.md)
3. Lancez votre premier projet avec [Premiers Pas](./03-premiers-pas.md)

### Niveau Intermédiaire
1. Étudiez les [Prompts Efficaces](./04-prompts-efficaces.md)
2. Maîtrisez le [Workflow en 3 Phases](./05-workflow-avance.md)
3. Essayez les [Exemples](./exemples/) fournis

### Niveau Avancé
1. Comparez les [Implémentations](./06-implementations.md)
2. Optimisez avec [Sécurité & Coûts](./07-securite-couts.md)
3. Apprenez des [Cas d'Étude](./09-cas-etude.md)

---

## Avertissement

Ralph Wiggum est une technique puissante mais qui nécessite :
- Un **sandboxing strict** (Docker recommandé)
- Une **surveillance des coûts** (peut dépasser $100 sur gros projets)
- Des **backups réguliers** (commits git automatiques)

Ne lancez **jamais** Ralph en mode non-sandboxé sur du code de production.

---

## Contribuer

Ce guide est open-source. Pour suggérer des améliorations :
1. Ouvrez une issue
2. Proposez une PR avec vos ajouts
3. Partagez vos propres cas d'étude

---

*Dernière mise à jour : Janvier 2026*
