# Requirements - Projet Ralph Wiggum

## Description du Projet

Ce projet est un template de base pour utiliser la méthodologie Ralph Wiggum avec Claude Code CLI. Il permet de faire tourner l'agent en boucle autonome sur des tâches de développement.

---

## Fonctionnalités

### F1 - Boucle Autonome
- L'agent peut travailler sans supervision humaine
- Il lit ses instructions depuis PROMPT.md
- Il persiste son état dans TODO.md
- Il s'arrête automatiquement via HARD STOP

### F2 - Persistance via Fichiers
- PROMPT.md : Instructions permanentes
- TODO.md : État d'avancement
- specs/ : Spécifications et architecture
- Git commits : Historique des changements

### F3 - Guardrails de Sécurité
- Permissions définies dans .claude/settings.json
- Conditions HARD STOP claires
- Checkpoints de validation
- Limites de tours

---

## Contraintes Techniques

| Élément | Contrainte |
|---------|------------|
| CLI | Claude Code v1.0+ |
| Shell | Bash |
| Versioning | Git |
| Format fichiers | Markdown |
| Dépendances | jq (optionnel) |

---

## Hors Scope

- Interface graphique
- Base de données
- Déploiement cloud
- Authentification

---

## Standards de Qualité

### Structure des Fichiers
- Markdown pour la documentation
- JSON pour la configuration
- Bash pour les scripts

### Conventions de Nommage
- kebab-case pour les fichiers
- Majuscules pour les fichiers principaux (PROMPT.md, TODO.md)

### Commits Git
- Format : `[Ralph] type: description`
- Types : feat, fix, docs, chore

---

## Critères d'Acceptation

1. [ ] Le projet peut être cloné et utilisé immédiatement
2. [ ] La documentation est claire et complète
3. [ ] Le script loop.sh fonctionne sans modification
4. [ ] Les permissions sont configurées de manière sécurisée

---

## Validé par
- [ ] Humain a relu et approuvé
