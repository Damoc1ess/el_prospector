#!/bin/bash

# =============================================================================
# RALPH-INIT : Lanceur simplifié pour projets Ralph Wiggum
# =============================================================================
#
# Usage:
#   ./ralph-init.sh
#
# Ce script génère automatiquement PROMPT.md et TODO.md
# pour démarrer un nouveau projet avec Ralph.
#
# =============================================================================

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

clear
echo -e "${CYAN}${BOLD}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║   🤖 RALPH WIGGUM - Générateur de Projet                  ║"
echo "║                                                           ║"
echo "║   \"Me fail English? That's unpossible!\"                   ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# -----------------------------------------------------------------------------
# ÉTAPE 1 : Type de projet
# -----------------------------------------------------------------------------

echo -e "${BOLD}📋 ÉTAPE 1 : Quel type de projet ?${NC}"
echo ""
echo "  1) 🐍 CLI Python      - Application en ligne de commande"
echo "  2) 🟢 API Node.js     - Backend REST avec Express"
echo "  3) 🐍 API Python      - Backend REST avec FastAPI"
echo "  4) 📜 Script Bash     - Automatisation shell"
echo "  5) 🔧 Utilitaire      - Outil standalone"
echo "  6) ✏️  Personnalisé    - Définir moi-même"
echo ""
read -p "Votre choix (1-6) : " PROJECT_TYPE

# -----------------------------------------------------------------------------
# ÉTAPE 2 : Nom du projet
# -----------------------------------------------------------------------------

echo ""
echo -e "${BOLD}📝 ÉTAPE 2 : Nom du projet${NC}"
echo ""
read -p "Nom (ex: mon-outil) : " PROJECT_NAME

if [ -z "$PROJECT_NAME" ]; then
    PROJECT_NAME="ralph-project"
fi

# -----------------------------------------------------------------------------
# ÉTAPE 3 : Description
# -----------------------------------------------------------------------------

echo ""
echo -e "${BOLD}📄 ÉTAPE 3 : Description courte${NC}"
echo ""
read -p "Description : " PROJECT_DESC

if [ -z "$PROJECT_DESC" ]; then
    PROJECT_DESC="Projet généré par Ralph Wiggum"
fi

# -----------------------------------------------------------------------------
# GÉNÉRATION DES FICHIERS
# -----------------------------------------------------------------------------

echo ""
echo -e "${YELLOW}⚙️  Génération des fichiers...${NC}"

# Déterminer le template selon le type
case $PROJECT_TYPE in
    1) # CLI Python
        STACK="Python 3.10+"
        FRAMEWORK="argparse ou click"
        TEST_CMD="python -m pytest tests/ -v"
        LINT_CMD="ruff check ."
        EXTENSION="py"
        TEMPLATE="cli-python"
        ;;
    2) # API Node.js
        STACK="Node.js 20+"
        FRAMEWORK="Express.js"
        TEST_CMD="npm test"
        LINT_CMD="npm run lint"
        EXTENSION="js"
        TEMPLATE="api-node"
        ;;
    3) # API Python
        STACK="Python 3.10+"
        FRAMEWORK="FastAPI"
        TEST_CMD="python -m pytest tests/ -v"
        LINT_CMD="ruff check ."
        EXTENSION="py"
        TEMPLATE="api-python"
        ;;
    4) # Script Bash
        STACK="Bash"
        FRAMEWORK="Shell script"
        TEST_CMD="shellcheck *.sh"
        LINT_CMD="shellcheck *.sh"
        EXTENSION="sh"
        TEMPLATE="script-bash"
        ;;
    5) # Utilitaire
        STACK="Python 3.10+"
        FRAMEWORK="stdlib only"
        TEST_CMD="python -m pytest tests/ -v"
        LINT_CMD="ruff check ."
        EXTENSION="py"
        TEMPLATE="utilitaire"
        ;;
    *) # Personnalisé
        STACK="À définir"
        FRAMEWORK="À définir"
        TEST_CMD="À définir"
        LINT_CMD="À définir"
        EXTENSION="py"
        TEMPLATE="custom"
        ;;
esac

# -----------------------------------------------------------------------------
# GÉNÉRER PROMPT.md
# -----------------------------------------------------------------------------

cat > PROMPT.md << EOF
# PROMPT.md - $PROJECT_NAME

## Contexte

Tu es en mode **Ralph Wiggum** - un agent autonome qui travaille sans supervision.

**Mission :** $PROJECT_DESC
**Stack :** $STACK
**Framework :** $FRAMEWORK

Tu persistes ton état via :
- \`TODO.md\` pour l'avancement (LIS CE FICHIER À CHAQUE TOUR)
- Commits git pour l'historique

---

## Objectif

$PROJECT_DESC

---

## Spécifications Techniques

### Stack

| Élément | Choix |
|---------|-------|
| Langage | $STACK |
| Framework | $FRAMEWORK |
| Tests | $TEST_CMD |

### Architecture

\`\`\`
$PROJECT_NAME/
├── src/
│   └── main.$EXTENSION
├── tests/
│   └── test_main.$EXTENSION
├── README.md
└── TODO.md
\`\`\`

---

## Critères de Succès

### Fonctionnels
1. [ ] Le code principal fonctionne
2. [ ] Les fonctionnalités demandées sont implémentées
3. [ ] Gestion des erreurs basique

### Qualité
4. [ ] Tests passent : \`$TEST_CMD\`
5. [ ] README.md avec instructions d'installation et usage

### Livrables
6. [ ] Code fonctionnel dans src/
7. [ ] Tests dans tests/
8. [ ] Documentation complète

---

## Workflow

### Phase 1 : Setup (Tours 1-3)
1. Lire ce fichier et TODO.md
2. Créer la structure de dossiers
3. Initialiser les fichiers de base

### Phase 2 : Implémentation (Tours 4-15)
4. Implémenter les fonctionnalités une par une
5. Écrire les tests correspondants
6. Commit après chaque fonctionnalité

### Phase 3 : Finalisation (Tours 16-20)
7. Vérifier tous les critères
8. Écrire le README.md
9. Commit final

---

## HARD STOP

**ARRÊTE-TOI** quand :
- Tous les critères sont cochés [x] dans TODO.md
- OU 30 tours sans progrès
- OU erreur répétée 5+ fois

Quand tu t'arrêtes :
1. Met à jour TODO.md avec le statut final
2. Ajoute \`- [x] DONE - Projet terminé\`

---

## Guardrails

### OBLIGATOIRE
- Lis TODO.md à chaque tour
- Un commit par fonctionnalité
- Format : \`[Ralph] type: description\`

### INTERDIT
- Modifier PROMPT.md
- Supprimer des fichiers sans raison
- Continuer après HARD STOP
EOF

# -----------------------------------------------------------------------------
# GÉNÉRER TODO.md
# -----------------------------------------------------------------------------

cat > TODO.md << EOF
# TODO.md - $PROJECT_NAME

## Status: EN COURS

---

## Critères de Succès

- [ ] Code principal fonctionne
- [ ] Fonctionnalités implémentées
- [ ] Gestion des erreurs
- [ ] Tests passent
- [ ] README.md complet

---

## Plan d'Exécution

### Phase 1 : Setup
- [ ] Créer structure de dossiers (src/, tests/)
- [ ] Créer fichiers de base
- [ ] Commit initial

### Phase 2 : Implémentation
- [ ] Implémenter la fonctionnalité principale
- [ ] Ajouter les fonctionnalités secondaires
- [ ] Écrire les tests

### Phase 3 : Finalisation
- [ ] Écrire README.md
- [ ] Vérification finale
- [ ] Commit final

---

## État Actuel

**Tour :** 0
**Dernière action :** Initialisation
**Prochaine action :** Lire PROMPT.md

---

## Notes

(Ralph ajoutera ses observations ici)

---

## HARD STOP TRIGGER

<!-- Quand tous les critères sont cochés, écrire : -->
<!-- - [x] DONE - Projet terminé -->
EOF

# -----------------------------------------------------------------------------
# CRÉER LA STRUCTURE
# -----------------------------------------------------------------------------

mkdir -p src tests

# -----------------------------------------------------------------------------
# RÉSUMÉ
# -----------------------------------------------------------------------------

echo ""
echo -e "${GREEN}${BOLD}✅ Projet initialisé !${NC}"
echo ""
echo -e "${BOLD}Fichiers créés :${NC}"
echo "  📄 PROMPT.md  - Instructions pour Ralph"
echo "  📋 TODO.md    - Plan d'exécution"
echo "  📁 src/       - Code source"
echo "  📁 tests/     - Tests"
echo ""
echo -e "${BOLD}Configuration :${NC}"
echo "  Nom    : $PROJECT_NAME"
echo "  Stack  : $STACK"
echo "  Type   : $TEMPLATE"
echo ""
echo -e "${CYAN}${BOLD}🚀 Pour lancer Ralph :${NC}"
echo ""
echo "  ./loop.sh"
echo ""
echo -e "${YELLOW}Conseil : Éditez PROMPT.md pour préciser les fonctionnalités souhaitées${NC}"
echo ""
