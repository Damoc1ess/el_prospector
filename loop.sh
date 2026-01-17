#!/bin/bash

# =============================================================================
# RALPH WIGGUM LOOP SCRIPT - Avec Circuit Breakers
# =============================================================================

# Configuration
MAX_ITERATIONS=50
SLEEP_BETWEEN=5
HARD_STOP_FILE="TODO.md"
HARD_STOP_PATTERN="\[x\] DONE"
COMMIT_PREFIX="[Ralph]"
AUTO_COMMIT=true

# Circuit Breakers (recommandes par le guide)
MAX_TIME=3600          # 1 heure max
ERROR_THRESHOLD=5      # Arret apres 5 erreurs consecutives
NO_PROGRESS_LIMIT=10   # Arret si pas de commit pendant 10 tours

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Compteurs
consecutive_errors=0
tours_without_commit=0
last_commit_count=0

log() {
    echo -e "[$(date '+%H:%M:%S')] $1"
}

check_hard_stop() {
    grep -q "$HARD_STOP_PATTERN" "$HARD_STOP_FILE" 2>/dev/null
}

check_time_limit() {
    local current_time=$(date +%s)
    local elapsed=$((current_time - start_time))
    if [ "$elapsed" -ge "$MAX_TIME" ]; then
        log "${RED}CIRCUIT BREAKER: Temps max atteint (${MAX_TIME}s)${NC}"
        return 0
    fi
    return 1
}

check_progress() {
    local current_commits=$(git rev-list --count HEAD 2>/dev/null || echo "0")
    if [ "$current_commits" -eq "$last_commit_count" ]; then
        ((tours_without_commit++))
        if [ "$tours_without_commit" -ge "$NO_PROGRESS_LIMIT" ]; then
            log "${RED}CIRCUIT BREAKER: Pas de progres depuis $NO_PROGRESS_LIMIT tours${NC}"
            return 0
        fi
    else
        tours_without_commit=0
        last_commit_count=$current_commits
    fi
    return 1
}

auto_commit() {
    if [ "$AUTO_COMMIT" = true ]; then
        if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
            git add -A
            git commit -m "$COMMIT_PREFIX Tour $1" --quiet 2>/dev/null
            log "${GREEN}Commit effectue${NC}"
            consecutive_errors=0
            return 0
        fi
    fi
    return 1
}

# Verification des prerequis
if ! command -v claude &> /dev/null; then
    log "${RED}Claude Code non installe${NC}"
    exit 1
fi

if [ ! -f "PROMPT.md" ]; then
    log "${RED}PROMPT.md non trouve${NC}"
    exit 1
fi

if [ ! -f ".env" ]; then
    log "${YELLOW}ATTENTION: .env non trouve - verifiez la cle API${NC}"
fi

# Initialisation
start_time=$(date +%s)
last_commit_count=$(git rev-list --count HEAD 2>/dev/null || echo "0")

echo ""
log "${BLUE}========================================${NC}"
log "${BLUE}RALPH WIGGUM - Demarrage${NC}"
log "${BLUE}========================================${NC}"
log "Max iterations: $MAX_ITERATIONS"
log "Max temps: $((MAX_TIME / 60)) minutes"
log "Seuil erreurs: $ERROR_THRESHOLD"
echo ""

iteration=0

while [ $iteration -lt $MAX_ITERATIONS ]; do
    iteration=$((iteration + 1))

    echo "=================================================="
    log "${BLUE}Tour $iteration / $MAX_ITERATIONS${NC}"
    echo "=================================================="

    # Verifier HARD STOP
    if check_hard_stop; then
        log "${GREEN}HARD STOP detecte - Projet termine!${NC}"
        break
    fi

    # Circuit breakers
    if check_time_limit; then
        break
    fi

    if check_progress; then
        break
    fi

    # Executer Claude
    if ! claude --print "Tu es en mode Ralph Wiggum, tour $iteration.

INSTRUCTIONS:
1. Lis TODO.md pour l etat actuel
2. Lis PROMPT.md pour les instructions
3. Execute la prochaine tache non cochee
4. Mets a jour TODO.md apres chaque action
5. Si tout est fait, ecris '- [x] DONE - Projet termine' dans TODO.md

Tour: $iteration / $MAX_ITERATIONS"; then
        ((consecutive_errors++))
        log "${YELLOW}Erreur Claude ($consecutive_errors/$ERROR_THRESHOLD)${NC}"
        if [ "$consecutive_errors" -ge "$ERROR_THRESHOLD" ]; then
            log "${RED}CIRCUIT BREAKER: Trop d erreurs consecutives${NC}"
            break
        fi
    else
        consecutive_errors=0
    fi

    auto_commit $iteration

    sleep $SLEEP_BETWEEN
done

# Resume final
end_time=$(date +%s)
duration=$((end_time - start_time))

echo ""
echo "=================================================="
log "${BLUE}RESUME FINAL${NC}"
echo "=================================================="
echo "  Tours effectues : $iteration"
echo "  Duree           : $((duration / 60))m $((duration % 60))s"
echo "  Commits         : $(git rev-list --count HEAD 2>/dev/null || echo 'N/A')"

if check_hard_stop; then
    log "${GREEN}Projet termine avec succes!${NC}"
else
    log "${YELLOW}Arret sans completion - verifiez TODO.md${NC}"
fi
echo "=================================================="
