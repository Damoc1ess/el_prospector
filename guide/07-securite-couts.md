# 07 - Sécurité et Gestion des Coûts

Ralph Wiggum exécute du code de manière autonome. La sécurité et le contrôle des coûts sont critiques.

---

## Pourquoi le Sandboxing est Obligatoire

### Risques Sans Sandboxing

| Risque                        | Exemple concret                                |
|-------------------------------|------------------------------------------------|
| Suppression de fichiers       | `rm -rf /` par erreur                          |
| Exfiltration de données       | Envoi de fichiers sensibles via curl           |
| Installation de malware       | `curl ... | bash` malveillant                  |
| Modification système          | Changement de configuration                    |
| Déni de service               | Boucle infinie consommant CPU/disque           |
| Fuites de secrets             | Lecture de .env, clés SSH                      |

### Règle d'Or

> **JAMAIS de Ralph en mode non-sandboxé sur une machine avec des données importantes.**

---

## Configuration Docker (Recommandé)

### Dockerfile Sécurisé

```dockerfile
# Dockerfile.ralph-secure
FROM node:20-slim

# Dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    jq \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Claude Code
RUN npm install -g @anthropic-ai/claude-code

# Utilisateur non-root avec UID fixe
RUN groupadd -g 1000 ralph \
    && useradd -u 1000 -g ralph -m -s /bin/bash ralph

# Permissions restrictives
RUN mkdir -p /project && chown ralph:ralph /project

# Pas d'accès réseau par défaut (override au runtime si besoin)
USER ralph
WORKDIR /project

# Limites de ressources (seront appliquées au runtime)
# --memory, --cpus via docker run

ENTRYPOINT ["claude"]
```

### Script de Lancement Sécurisé

```bash
#!/bin/bash
# run-ralph-secure.sh

PROJECT_DIR=$(pwd)
CONTAINER_NAME="ralph-$(date +%s)"

# Vérifications préalables
if [ ! -f "$PROJECT_DIR/PROMPT.md" ]; then
    echo "❌ PROMPT.md non trouvé"
    exit 1
fi

# Lancement avec restrictions
docker run \
    --name "$CONTAINER_NAME" \
    --rm \
    -it \
    \
    `# Montage du projet uniquement` \
    -v "$PROJECT_DIR:/project" \
    \
    `# Variables d'environnement` \
    -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
    \
    `# Limites de ressources` \
    --memory=4g \
    --cpus=2 \
    --pids-limit=100 \
    \
    `# Restrictions de sécurité` \
    --security-opt=no-new-privileges \
    --cap-drop=ALL \
    --read-only \
    --tmpfs /tmp:rw,noexec,nosuid,size=512m \
    \
    `# Pas de réseau par défaut` \
    --network=none \
    \
    ralph-secure:latest \
    --ralph "Exécute le projet PROMPT.md"

echo "Container $CONTAINER_NAME terminé"
```

### Options de Sécurité Expliquées

| Option                    | Effet                                       |
|---------------------------|---------------------------------------------|
| `--memory=4g`             | Limite RAM à 4GB                            |
| `--cpus=2`                | Limite à 2 CPU                              |
| `--pids-limit=100`        | Max 100 processus                           |
| `--no-new-privileges`     | Pas d'escalade de privilèges                |
| `--cap-drop=ALL`          | Supprime toutes les capabilities Linux      |
| `--read-only`             | Système de fichiers en lecture seule        |
| `--network=none`          | Pas d'accès réseau                          |

### Accès Réseau Contrôlé

Si le projet nécessite un accès réseau (npm install, etc.) :

```bash
# Créer un réseau isolé
docker network create ralph-net --internal

# Lancer avec réseau limité
docker run \
    --network=ralph-net \
    --dns=8.8.8.8 \
    ... rest of options ...
```

---

## Alternatives au Docker Local

### E2B (Code Interpreter)

Service cloud de sandboxing pour agents IA.

```bash
# Installation
pip install e2b-code-interpreter

# Configuration
export E2B_API_KEY="your_key"
```

```python
from e2b_code_interpreter import Sandbox

with Sandbox() as sandbox:
    # Upload du projet
    sandbox.filesystem.write("/project/PROMPT.md", open("PROMPT.md").read())

    # Exécution isolée
    result = sandbox.run_code("""
        import subprocess
        subprocess.run(["claude", "--ralph", "/project/PROMPT.md"])
    """)
```

**Avantages :** Isolation cloud, pas de config locale
**Inconvénients :** Coût additionnel, latence réseau

### Modal

Infrastructure serverless pour exécution isolée.

```python
import modal

app = modal.App("ralph-runner")
image = modal.Image.debian_slim().pip_install("anthropic")

@app.function(
    image=image,
    timeout=3600,  # 1 heure max
    memory=4096,   # 4GB RAM
    secrets=[modal.Secret.from_name("anthropic-key")]
)
def run_ralph(prompt_content: str):
    import subprocess
    with open("/tmp/PROMPT.md", "w") as f:
        f.write(prompt_content)
    return subprocess.run(
        ["claude", "--ralph", "/tmp/PROMPT.md"],
        capture_output=True,
        timeout=3500
    )
```

**Avantages :** Scalable, pay-per-use, isolation forte
**Inconvénients :** Courbe d'apprentissage, pas de persistance native

### Fly.io Machines

VMs légères isolées.

```bash
# fly.toml
app = "ralph-runner"

[build]
  dockerfile = "Dockerfile.ralph"

[env]
  MAX_ITERATIONS = "100"

[[vm]]
  cpu_kind = "shared"
  cpus = 2
  memory_mb = 4096

[processes]
  ralph = "claude --ralph PROMPT.md"
```

---

## Estimation des Coûts

### Tarification Claude (Janvier 2026)

| Modèle        | Input ($/1M tokens) | Output ($/1M tokens) |
|---------------|---------------------|----------------------|
| Claude Haiku  | $0.25               | $1.25                |
| Claude Sonnet | $3.00               | $15.00               |
| Claude Opus   | $15.00              | $75.00               |

### Coût par Type de Projet

| Type de projet              | Tours typ. | Tokens In | Tokens Out | Coût estimé   |
|-----------------------------|------------|-----------|------------|---------------|
| CLI simple (Python)         | 15-20      | ~50K      | ~20K       | $3-8          |
| API REST basique            | 30-50      | ~150K     | ~60K       | $15-30        |
| Application complète        | 80-120     | ~400K     | ~150K      | $50-100       |
| Migration/Refactoring batch | 50-100     | ~250K     | ~100K      | $30-60        |
| Projet complexe (multi-repo)| 150-300    | ~800K     | ~300K      | $150-300      |

### Formule d'Estimation

```
Coût ≈ (Tours × Tokens_par_tour_in × Prix_in) + (Tours × Tokens_par_tour_out × Prix_out)

Moyenne par tour (Sonnet):
- Input:  ~3,000 tokens  → $0.009
- Output: ~1,200 tokens  → $0.018
- Total:  ~$0.027/tour

Pour 100 tours: ~$2.70 (optimiste) à $5.00 (réaliste)
```

---

## Stratégies d'Optimisation des Coûts

### 1. Choix du Modèle Stratégique

```yaml
# Utiliser Haiku pour les tâches simples
phases:
  clarify:
    model: claude-haiku-3-5-sonnet  # Économique
  plan:
    model: claude-sonnet-4-20250514  # Équilibré
  execute:
    model: claude-sonnet-4-20250514  # Équilibré
```

### 2. Réduire le Contexte

```markdown
## PROMPT.md Optimisé

<!-- COMPACT: Éviter les répétitions -->

## Objectif
[1 phrase max]

## Specs
[Essentiel uniquement, pas de prose]

## Critères
1. [x] Critère 1
2. [ ] Critère 2

<!-- Pas de blabla -->
```

### 3. Checkpoints avec Résumé

```bash
# À chaque checkpoint, résumer l'état
checkpoint() {
    local iteration=$1
    claude --print "Résume l'état actuel en 50 mots max et écris-le dans TODO.md"
    # Cela "reset" partiellement le contexte
}
```

### 4. Limites de Coût Strictes

```json
{
  "ralph": {
    "maxCost": 25.00,
    "warningCost": 15.00,
    "pauseOnWarning": true
  }
}
```

### 5. Cache de Prompts (Anthropic)

Si disponible, utiliser le cache de prompts :

```python
# Le prompt système est caché
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    system=[{
        "type": "text",
        "text": open("PROMPT.md").read(),
        "cache_control": {"type": "ephemeral"}  # Cache pour 5 min
    }],
    messages=[...]
)
```

---

## Circuit Breakers

### Implémentation

```bash
#!/bin/bash
# circuit-breaker.sh

MAX_COST=50
COST_FILE=".ralph/cost.txt"
ERROR_THRESHOLD=5

check_cost() {
    local current_cost=$(cat "$COST_FILE" 2>/dev/null || echo "0")
    if (( $(echo "$current_cost > $MAX_COST" | bc -l) )); then
        echo "🛑 CIRCUIT BREAKER: Coût max atteint ($current_cost > $MAX_COST)"
        exit 1
    fi
}

check_errors() {
    local consecutive_errors=$(cat ".ralph/errors.txt" 2>/dev/null || echo "0")
    if [ "$consecutive_errors" -ge "$ERROR_THRESHOLD" ]; then
        echo "🛑 CIRCUIT BREAKER: Trop d'erreurs consécutives"
        exit 1
    fi
}

check_time() {
    local start_time=$(cat ".ralph/start_time.txt")
    local max_duration=3600  # 1 heure
    local current_time=$(date +%s)
    local elapsed=$((current_time - start_time))

    if [ "$elapsed" -ge "$max_duration" ]; then
        echo "🛑 CIRCUIT BREAKER: Temps max atteint"
        exit 1
    fi
}

# Appeler avant chaque itération
check_cost
check_errors
check_time
```

### Configuration des Limites

| Limite              | Valeur recommandée | Projet simple | Projet complexe |
|---------------------|--------------------|--------------:|----------------:|
| `maxCost`           | Variable           | $10-25        | $50-100         |
| `maxIterations`     | 100                | 30-50         | 100-200         |
| `maxTime`           | 1h                 | 30min         | 2-4h            |
| `errorThreshold`    | 5                  | 3             | 5-10            |
| `noProgressTimeout` | 10 tours           | 5             | 10-15           |

---

## Monitoring des Coûts en Temps Réel

### Script de Suivi

```bash
#!/bin/bash
# cost-monitor.sh

API_KEY="$ANTHROPIC_API_KEY"
POLL_INTERVAL=30

while true; do
    clear
    echo "=== Ralph Cost Monitor ==="
    echo ""

    # Lecture du fichier de coût local
    if [ -f ".ralph/cost.txt" ]; then
        current_cost=$(cat .ralph/cost.txt)
        echo "💰 Coût actuel: \$$current_cost"
    fi

    # Tokens utilisés
    if [ -f ".ralph/tokens.json" ]; then
        input=$(jq .input .ralph/tokens.json)
        output=$(jq .output .ralph/tokens.json)
        echo "📊 Tokens: ${input}K in / ${output}K out"
    fi

    # Progression
    if [ -f "TODO.md" ]; then
        total=$(grep -c "^\- \[" TODO.md)
        done=$(grep -c "^\- \[x\]" TODO.md)
        echo "📋 Progression: $done / $total tâches"
    fi

    echo ""
    echo "Mise à jour dans ${POLL_INTERVAL}s..."
    sleep $POLL_INTERVAL
done
```

---

## Checklist Sécurité

Avant chaque session Ralph :

- [ ] Docker ou sandbox configuré
- [ ] Pas de secrets dans le projet (.env, clés)
- [ ] Limite de coût définie
- [ ] Circuit breakers actifs
- [ ] Backup des fichiers importants
- [ ] Réseau désactivé ou restreint
- [ ] Monitoring des ressources actif

---

## Prochaine Étape

Apprenez à résoudre les problèmes courants dans [Troubleshooting](./08-troubleshooting.md).

---

[← Implémentations](./06-implementations.md) | [Sommaire](./README.md) | [Troubleshooting →](./08-troubleshooting.md)
