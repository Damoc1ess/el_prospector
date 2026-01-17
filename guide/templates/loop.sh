#!/bin/bash

# =============================================================================
# RALPH WIGGUM LOOP SCRIPT
# =============================================================================
#
# Script orchestrateur pour faire tourner Claude Code en boucle autonome.
#
# Usage:
#   chmod +x loop.sh
#   ./loop.sh
#
# Configuration:
#   Modifier les variables ci-dessous selon vos besoins.
#
# Prérequis:
#   - Claude Code installé (claude --version)
#   - jq installé (jq --version)
#   - Git initialisé dans le projet
#   - ANTHROPIC_API_KEY configurée
#
# =============================================================================

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------

# Nombre maximum d'itérations avant arrêt forcé
MAX_ITERATIONS=50

# Pause entre chaque itération (secondes)
SLEEP_BETWEEN=5

# Fichier à surveiller pour le HARD STOP
HARD_STOP_FILE="TODO.md"

# Pattern qui déclenche l'arrêt (regex grep)
HARD_STOP_PATTERN="\[x\] DONE"

# Intervalle entre les checkpoints (tours)
CHECKPOINT_INTERVAL=10

# Préfixe pour les messages de commit
COMMIT_PREFIX="[Ralph]"

# Activer les commits automatiques (true/false)
AUTO_COMMIT=true

# Mode verbose (true/false)
VERBOSE=true

# -----------------------------------------------------------------------------
# FONCTIONS UTILITAIRES
# -----------------------------------------------------------------------------

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log avec timestamp
log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log_info() {
    log "${BLUE}INFO${NC} $1"
}

log_success() {
    log "${GREEN}SUCCESS${NC} $1"
}

log_warning() {
    log "${YELLOW}WARNING${NC} $1"
}

log_error() {
    log "${RED}ERROR${NC} $1"
}

# Vérifier les prérequis
check_prerequisites() {
    log_info "Vérification des prérequis..."

    # Claude Code
    if ! command -v claude &> /dev/null; then
        log_error "Claude Code non installé. Installez avec: npm install -g @anthropic-ai/claude-code"
        exit 1
    fi

    # jq (optionnel mais recommandé)
    if ! command -v jq &> /dev/null; then
        log_warning "jq non installé. Installez avec: brew install jq"
    fi

    # Git
    if ! git rev-parse --is-inside-work-tree &> /dev/null; then
        log_warning "Pas de repo git. Initialisation..."
        git init
        git add .
        git commit -m "$COMMIT_PREFIX Initial commit" --allow-empty
    fi

    # PROMPT.md
    if [ ! -f "PROMPT.md" ]; then
        log_error "PROMPT.md non trouvé. Créez ce fichier avec vos instructions."
        exit 1
    fi

    # TODO.md
    if [ ! -f "$HARD_STOP_FILE" ]; then
        log_warning "$HARD_STOP_FILE non trouvé. Création d'un fichier minimal..."
        echo "# TODO.md" > "$HARD_STOP_FILE"
        echo "" >> "$HARD_STOP_FILE"
        echo "## Status: EN COURS" >> "$HARD_STOP_FILE"
    fi

    # ANTHROPIC_API_KEY
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        log_error "ANTHROPIC_API_KEY non définie. Exportez la variable d'environnement."
        exit 1
    fi

    log_success "Prérequis OK"
}

# Vérifier si le HARD STOP est déclenché
check_hard_stop() {
    if grep -q "$HARD_STOP_PATTERN" "$HARD_STOP_FILE" 2>/dev/null; then
        return 0  # HARD STOP détecté
    fi
    return 1  # Continuer
}

# Faire un checkpoint
do_checkpoint() {
    local iteration=$1
    log_info "📍 CHECKPOINT à l'itération $iteration"

    # Afficher le statut TODO
    echo ""
    echo "=== État TODO.md ==="
    grep -E "^\- \[[ x]\]" "$HARD_STOP_FILE" 2>/dev/null | head -15
    echo "===================="
    echo ""

    # Afficher les derniers commits
    echo "=== Derniers commits ==="
    git log --oneline -5 2>/dev/null
    echo "========================"
    echo ""
}

# Commit automatique
auto_commit() {
    local iteration=$1

    if [ "$AUTO_COMMIT" = true ]; then
        if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
            git add -A
            git commit -m "$COMMIT_PREFIX Tour $iteration" --quiet 2>/dev/null
            if [ $? -eq 0 ]; then
                log_info "Commit effectué"
            fi
        else
            [ "$VERBOSE" = true ] && log_info "Pas de changement à commit"
        fi
    fi
}

# -----------------------------------------------------------------------------
# BOUCLE PRINCIPALE
# -----------------------------------------------------------------------------

main() {
    log_info "🚀 Démarrage Ralph Wiggum Loop"
    log_info "Max iterations: $MAX_ITERATIONS"
    log_info "HARD STOP pattern: $HARD_STOP_PATTERN"

    check_prerequisites

    local iteration=0
    local start_time=$(date +%s)

    # Créer le dossier de logs
    mkdir -p .ralph

    # Sauvegarder l'heure de début
    echo "$start_time" > .ralph/start_time.txt

    echo ""
    log_info "=== DÉBUT DE LA BOUCLE ==="
    echo ""

    while [ $iteration -lt $MAX_ITERATIONS ]; do
        iteration=$((iteration + 1))

        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        log_info "🔄 Iteration $iteration / $MAX_ITERATIONS"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

        # Vérifier le HARD STOP
        if check_hard_stop; then
            log_success "✅ HARD STOP détecté - Projet terminé!"
            break
        fi

        # Checkpoint périodique
        if (( iteration % CHECKPOINT_INTERVAL == 0 )); then
            do_checkpoint $iteration
        fi

        # Lancer Claude
        log_info "Exécution de Claude..."

        claude --print "Tu es en mode Ralph Wiggum, tour $iteration.

INSTRUCTIONS:
1. Lis TODO.md pour connaître l'état actuel
2. Lis PROMPT.md pour les instructions
3. Exécute la prochaine tâche non cochée
4. Mets à jour TODO.md après chaque action
5. Si tous les critères sont cochés, écris '- [x] DONE - Projet terminé' dans TODO.md

Tour actuel: $iteration / $MAX_ITERATIONS

Commence maintenant."

        # Commit automatique
        auto_commit $iteration

        # Sauvegarder l'itération actuelle
        echo "$iteration" > .ralph/current_iteration.txt

        # Pause entre itérations
        if [ $iteration -lt $MAX_ITERATIONS ]; then
            [ "$VERBOSE" = true ] && log_info "Pause de ${SLEEP_BETWEEN}s..."
            sleep $SLEEP_BETWEEN
        fi
    done

    # Résumé final
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    local minutes=$((duration / 60))
    local seconds=$((duration % 60))

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_info "📊 RÉSUMÉ FINAL"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  Iterations effectuées : $iteration"
    echo "  Durée totale          : ${minutes}m ${seconds}s"
    echo "  Commits totaux        : $(git rev-list --count HEAD 2>/dev/null || echo 'N/A')"
    echo ""

    # État final
    if check_hard_stop; then
        log_success "🎉 Projet terminé avec succès!"
    elif [ $iteration -ge $MAX_ITERATIONS ]; then
        log_warning "⚠️ Limite d'itérations atteinte"
    fi

    echo ""
    echo "=== État final TODO.md ==="
    cat "$HARD_STOP_FILE"
    echo "=========================="
}

# -----------------------------------------------------------------------------
# GESTION DES SIGNAUX
# -----------------------------------------------------------------------------

cleanup() {
    echo ""
    log_warning "Interruption détectée (Ctrl+C)"
    log_info "Sauvegarde de l'état..."

    # Commit final
    git add -A
    git commit -m "$COMMIT_PREFIX INTERRUPTED - Sauvegarde manuelle" --quiet 2>/dev/null

    log_info "État sauvegardé. Vous pouvez relancer ./loop.sh pour continuer."
    exit 130
}

trap cleanup SIGINT SIGTERM

# -----------------------------------------------------------------------------
# POINT D'ENTRÉE
# -----------------------------------------------------------------------------

main "$@"
