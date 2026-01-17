# 02 - Installation et Configuration

Ce guide vous accompagne dans l'installation du plugin officiel Ralph Wiggum pour Claude Code.

---

## Prérequis Système

### Outils Requis

| Outil       | Version Min | Installation (macOS)         | Vérification         |
|-------------|-------------|------------------------------|----------------------|
| Claude Code | 1.0+        | `npm install -g @anthropic-ai/claude-code` | `claude --version`   |
| Node.js     | 18+         | `brew install node`          | `node --version`     |
| Git         | 2.30+       | Préinstallé sur macOS        | `git --version`      |
| jq          | 1.6+        | `brew install jq`            | `jq --version`       |

### Outils Recommandés

| Outil       | Usage                        | Installation               |
|-------------|------------------------------|----------------------------|
| Docker      | Sandboxing sécurisé          | `brew install --cask docker` |
| tmux        | Sessions persistantes        | `brew install tmux`        |
| gh          | Intégration GitHub           | `brew install gh`          |

---

## Installation Rapide (5 minutes)

### Étape 1 : Vérifier Claude Code

```bash
claude --version
# Attendu: claude-code v1.x.x

# Si non installé:
npm install -g @anthropic-ai/claude-code
```

### Étape 2 : Installer jq (si manquant)

```bash
# macOS
brew install jq

# Linux (Debian/Ubuntu)
sudo apt-get install jq

# Vérification
jq --version
```

### Étape 3 : Créer le Fichier de Configuration

Créez ou éditez `.claude/settings.json` dans votre home directory :

```bash
mkdir -p ~/.claude
cat > ~/.claude/settings.json << 'EOF'
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(npm *)",
      "Bash(node *)",
      "Read",
      "Write",
      "Edit"
    ],
    "deny": [
      "Bash(rm -rf /)",
      "Bash(sudo *)"
    ]
  },
  "preferences": {
    "autoCommit": true,
    "maxTurns": 100
  }
}
EOF
```

### Étape 4 : Vérifier l'Installation

```bash
# Créer un dossier de test
mkdir ralph-test && cd ralph-test
git init

# Créer un prompt minimal
cat > PROMPT.md << 'EOF'
# Test Ralph Wiggum

## Tâche
Créer un fichier `hello.py` qui affiche "Hello, Ralph!".

## Critère de Succès
- Le fichier existe
- Il s'exécute sans erreur

## HARD STOP
Une fois le fichier créé et testé, arrête-toi.
EOF

# Lancer Claude en mode prompt
claude --print "Lis PROMPT.md et exécute la tâche"
```

---

## Configuration Avancée

### Structure Recommandée pour un Projet Ralph

```
mon-projet/
├── .claude/
│   └── settings.json      # Config locale du projet
├── PROMPT.md              # Instructions principales
├── TODO.md                # État d'avancement
├── specs/                 # Spécifications détaillées
│   ├── architecture.md
│   └── api.md
└── src/                   # Code généré
```

### Configuration Projet (`.claude/settings.json`)

```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(npm *)",
      "Bash(npx *)",
      "Bash(node *)",
      "Bash(python *)",
      "Bash(pytest *)",
      "Read",
      "Write",
      "Edit"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Bash(curl * | bash)",
      "Bash(wget * | bash)"
    ]
  },
  "model": "claude-sonnet-4-20250514",
  "preferences": {
    "autoCommit": true,
    "commitPrefix": "[Ralph]",
    "maxTurns": 200,
    "checkpointInterval": 10
  },
  "ralph": {
    "enabled": true,
    "hardStopFile": "TODO.md",
    "hardStopPattern": "\\[x\\] DONE",
    "maxCost": 50.00,
    "warningCost": 25.00
  }
}
```

### Options de Configuration

| Option                   | Type    | Description                                    | Défaut    |
|--------------------------|---------|------------------------------------------------|-----------|
| `maxTurns`               | number  | Nombre max d'itérations par session            | 100       |
| `autoCommit`             | boolean | Commit automatique après chaque changement     | false     |
| `commitPrefix`           | string  | Préfixe des messages de commit                 | ""        |
| `checkpointInterval`     | number  | Intervalle entre checkpoints (en tours)        | 10        |
| `ralph.enabled`          | boolean | Active le mode Ralph                           | false     |
| `ralph.hardStopFile`     | string  | Fichier à surveiller pour HARD STOP            | "TODO.md" |
| `ralph.hardStopPattern`  | regex   | Pattern qui déclenche l'arrêt                  | -         |
| `ralph.maxCost`          | number  | Coût max en $ avant arrêt forcé                | 100       |
| `ralph.warningCost`      | number  | Coût déclenchant un avertissement              | 50        |

---

## Configuration Docker (Recommandé)

Le sandboxing Docker est **fortement recommandé** pour isoler l'agent.

### Dockerfile pour Ralph

```dockerfile
# Dockerfile.ralph
FROM node:20-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    git \
    jq \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Installer Claude Code
RUN npm install -g @anthropic-ai/claude-code

# Créer un utilisateur non-root
RUN useradd -m -s /bin/bash ralph
USER ralph
WORKDIR /home/ralph/project

# Variables d'environnement
ENV ANTHROPIC_API_KEY=""

# Point d'entrée
ENTRYPOINT ["claude"]
```

### Script de Lancement Docker

```bash
#!/bin/bash
# run-ralph-docker.sh

PROJECT_DIR=$(pwd)

docker run -it --rm \
    -v "$PROJECT_DIR:/home/ralph/project" \
    -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
    ralph-image \
    --print "Lis PROMPT.md et exécute les tâches dans TODO.md"
```

### Build et Utilisation

```bash
# Build l'image
docker build -f Dockerfile.ralph -t ralph-image .

# Lancer Ralph dans Docker
chmod +x run-ralph-docker.sh
./run-ralph-docker.sh
```

---

## Configuration avec tmux (Sessions Persistantes)

Pour des sessions qui survivent à la déconnexion :

```bash
# Créer une session tmux
tmux new-session -d -s ralph

# Lancer Ralph dans tmux
tmux send-keys -t ralph 'cd /path/to/project && ./loop.sh' Enter

# Détacher (la session continue en background)
# Ctrl+B, puis D

# Se rattacher plus tard
tmux attach -t ralph

# Voir les logs en temps réel (autre terminal)
tmux capture-pane -t ralph -p
```

---

## Vérification Complète

Exécutez ce script pour vérifier que tout est correctement installé :

```bash
#!/bin/bash
# check-ralph-setup.sh

echo "=== Vérification Installation Ralph Wiggum ==="

# Claude Code
if command -v claude &> /dev/null; then
    echo "✅ Claude Code: $(claude --version 2>/dev/null | head -1)"
else
    echo "❌ Claude Code: Non installé"
fi

# Node.js
if command -v node &> /dev/null; then
    echo "✅ Node.js: $(node --version)"
else
    echo "❌ Node.js: Non installé"
fi

# Git
if command -v git &> /dev/null; then
    echo "✅ Git: $(git --version | cut -d' ' -f3)"
else
    echo "❌ Git: Non installé"
fi

# jq
if command -v jq &> /dev/null; then
    echo "✅ jq: $(jq --version)"
else
    echo "❌ jq: Non installé (brew install jq)"
fi

# Docker (optionnel)
if command -v docker &> /dev/null; then
    echo "✅ Docker: $(docker --version | cut -d' ' -f3 | tr -d ',')"
else
    echo "⚠️  Docker: Non installé (recommandé pour sandboxing)"
fi

# API Key
if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "✅ ANTHROPIC_API_KEY: Configurée"
else
    echo "❌ ANTHROPIC_API_KEY: Non définie"
fi

echo ""
echo "=== Configuration ==="

# Settings globaux
if [ -f ~/.claude/settings.json ]; then
    echo "✅ ~/.claude/settings.json existe"
else
    echo "⚠️  ~/.claude/settings.json non trouvé"
fi

echo ""
echo "=== Test Rapide ==="
echo "Pour tester, exécutez:"
echo '  claude --print "Dis bonjour"'
```

---

## Problèmes Courants

### "claude: command not found"

```bash
# Vérifier que npm global est dans le PATH
echo $PATH | grep -q "$(npm config get prefix)/bin" || \
    echo 'export PATH="$PATH:$(npm config get prefix)/bin"' >> ~/.zshrc

# Recharger
source ~/.zshrc
```

### "ANTHROPIC_API_KEY not set"

```bash
# Ajouter à ~/.zshrc ou ~/.bashrc
export ANTHROPIC_API_KEY="sk-ant-..."

# Recharger
source ~/.zshrc
```

### Permissions Docker

```bash
# Ajouter l'utilisateur au groupe docker (Linux)
sudo usermod -aG docker $USER
# Puis se déconnecter/reconnecter
```

---

## Prochaine Étape

Votre environnement est prêt ! Passez aux [Premiers Pas](./03-premiers-pas.md) pour lancer votre premier projet Ralph.

---

[← Introduction](./01-introduction.md) | [Sommaire](./README.md) | [Premiers Pas →](./03-premiers-pas.md)
