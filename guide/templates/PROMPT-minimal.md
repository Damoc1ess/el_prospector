# PROMPT.md - Template Minimal

<!--
  TEMPLATE MINIMAL RALPH WIGGUM

  Utilisation:
  1. Copier ce fichier dans votre projet
  2. Remplacer les [PLACEHOLDERS] par vos valeurs
  3. Supprimer les commentaires <!-- -->
  4. Lancer: claude --ralph "Exécute PROMPT.md"
-->

## Contexte

Tu es en mode Ralph Wiggum - agent autonome.
Tu dois créer [NOM_DU_PROJET] en [TECHNOLOGIE].

## Objectif

[Décrire l'objectif en 1-2 phrases maximum]

## Spécifications

### Stack
- Langage : [Python 3.10+ / Node.js 20+ / ...]
- Dépendances : [liste ou "aucune"]
- Stockage : [fichier JSON / SQLite / ...]

### Fonctionnalités
1. [Fonctionnalité A]
2. [Fonctionnalité B]
3. [Fonctionnalité C]

## Critères de Succès

<!-- Chaque critère DOIT être vérifiable par une commande -->

1. [ ] [Critère vérifiable 1]
2. [ ] [Critère vérifiable 2]
3. [ ] [Critère vérifiable 3]
4. [ ] Tests passent : `[commande de test]`
5. [ ] README.md existe

## HARD STOP

**ARRÊTE-TOI** quand :
- Tous les critères ci-dessus sont cochés [x]
- OU tu as fait [50] tours sans progrès

## Guardrails

- Un commit par fonctionnalité : `[Ralph] feat: description`
- Ne pas modifier ce fichier PROMPT.md
- Mettre à jour TODO.md après chaque étape
