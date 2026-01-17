# 06 - Implémentations de Ralph Wiggum

Plusieurs outils implémentent le pattern Ralph Wiggum. Ce chapitre présente les options disponibles.

---

## Vue d'Ensemble

| Outil                    | Éditeur       | Modèles supportés | Sandboxing natif |
|--------------------------|---------------|-------------------|------------------|
| Plugin Officiel Anthropic| Anthropic     | Claude uniquement | Oui (Docker)     |
| Goose (Block)            | Block         | Multi-modèle      | Oui              |
| frankbria/ralph-claude   | Communauté    | Claude            | Non              |
| Vercel AI SDK            | Vercel        | Multi-modèle      | Non              |

---

## 1. Plugin Officiel Anthropic

Le plugin officiel intégré à Claude Code depuis décembre 2025.

### Installation

```bash
# Déjà inclus dans Claude Code v1.0+
claude --version
```

### Configuration

Dans `.claude/settings.json` :

```json
{
  "ralph": {
    "enabled": true,
    "maxTurns": 100,
    "hardStopFile": "TODO.md",
    "hardStopPattern": "\\[x\\] DONE",
    "autoCommit": true,
    "checkpointInterval": 10
  }
}
```

### Utilisation

```bash
# Lancement mode Ralph
claude --ralph "Exécute le projet défini dans PROMPT.md"

# Avec options
claude --ralph --max-turns 50 --sandbox docker
```

### Commandes Disponibles

| Commande                        | Description                           |
|---------------------------------|---------------------------------------|
| `claude --ralph`                | Lance en mode boucle autonome         |
| `claude --ralph --dry-run`      | Simule sans exécuter                  |
| `claude --ralph --resume`       | Reprend une session interrompue       |
| `claude --ralph --status`       | Affiche l'état actuel                 |
| `claude --ralph --stop`         | Arrête proprement la boucle           |

### Paramètres

| Paramètre            | Type    | Défaut   | Description                        |
|----------------------|---------|----------|------------------------------------|
| `--max-turns`        | number  | 100      | Limite d'itérations                |
| `--sandbox`          | string  | "none"   | Mode sandbox (none/docker/e2b)     |
| `--checkpoint`       | number  | 10       | Intervalle de checkpoint           |
| `--cost-limit`       | number  | 100      | Limite de coût en $                |
| `--model`            | string  | "sonnet" | Modèle à utiliser                  |

### Avantages

- ✅ Intégration native avec Claude Code
- ✅ Support officiel Anthropic
- ✅ Sandboxing Docker intégré
- ✅ Gestion des coûts automatique

### Inconvénients

- ❌ Claude uniquement (pas de multi-modèle)
- ❌ Moins de customisation que les alternatives
- ❌ Logs limités

---

## 2. Goose (Block)

Framework open-source de Block (anciennement Square) pour agents autonomes.

### Installation

```bash
# Via pip
pip install goose-ai

# Via brew (macOS)
brew install block/tap/goose
```

### Configuration

Fichier `~/.config/goose/config.yaml` :

```yaml
provider: anthropic
model: claude-sonnet-4-20250514

loop:
  max_iterations: 100
  checkpoint_interval: 10

sandbox:
  enabled: true
  type: docker
  image: goose-sandbox:latest

persistence:
  state_file: .goose/state.json
  git_auto_commit: true
```

### Utilisation

```bash
# Lancement
goose run --prompt PROMPT.md

# Avec configuration spécifique
goose run --config goose.yaml --prompt PROMPT.md

# Mode interactif (pour debugging)
goose run --interactive
```

### Architecture

```
┌─────────────────────────────────────────┐
│              GOOSE                       │
├─────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │ Planner │  │ Executor│  │ Monitor │  │
│  └────┬────┘  └────┬────┘  └────┬────┘  │
│       │            │            │        │
│       ▼            ▼            ▼        │
│  ┌─────────────────────────────────────┐│
│  │         Provider Abstraction        ││
│  │  (Claude / GPT / Gemini / Local)    ││
│  └─────────────────────────────────────┘│
│                    │                     │
│                    ▼                     │
│  ┌─────────────────────────────────────┐│
│  │          Tool Registry              ││
│  │  (bash, file, git, custom...)       ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
```

### Multi-Modèle

Goose peut utiliser différents modèles :

```yaml
# config.yaml - Multi-modèle
providers:
  planning:
    provider: anthropic
    model: claude-opus-4-20250514
  execution:
    provider: openai
    model: gpt-4-turbo
  review:
    provider: google
    model: gemini-pro
```

### Avantages

- ✅ Multi-modèle (Claude, GPT, Gemini, local)
- ✅ Architecture modulaire extensible
- ✅ Sandboxing robuste
- ✅ Tooling riche (plugins)
- ✅ Open-source actif

### Inconvénients

- ❌ Courbe d'apprentissage plus raide
- ❌ Configuration plus complexe
- ❌ Pas spécifiquement optimisé pour Claude

---

## 3. frankbria/ralph-claude-code

Implémentation communautaire avec monitoring avancé.

### Installation

```bash
git clone https://github.com/frankbria/ralph-claude-code.git
cd ralph-claude-code
npm install
```

### Configuration

Fichier `ralph.config.js` :

```javascript
module.exports = {
  claude: {
    model: 'claude-sonnet-4-20250514',
    maxTokens: 8192
  },

  loop: {
    maxIterations: 100,
    sleepBetween: 5000,  // ms
    checkpointEvery: 10
  },

  monitoring: {
    dashboard: true,
    port: 3000,
    metrics: ['tokens', 'cost', 'time', 'commits']
  },

  hardStop: {
    file: 'TODO.md',
    pattern: /\[x\] DONE/,
    maxCost: 50
  },

  git: {
    autoCommit: true,
    prefix: '[Ralph]'
  }
};
```

### Utilisation

```bash
# Lancement avec dashboard
npm run ralph -- --prompt PROMPT.md

# Mode headless
npm run ralph -- --prompt PROMPT.md --no-dashboard
```

### Dashboard de Monitoring

L'outil inclut un dashboard web temps réel :

```
┌──────────────────────────────────────────────┐
│  RALPH WIGGUM DASHBOARD         localhost:3000│
├──────────────────────────────────────────────┤
│                                              │
│  Iteration: 23/100      Status: RUNNING      │
│  ━━━━━━━━━━━░░░░░░░░░░░░░░░░  23%            │
│                                              │
│  METRICS                                     │
│  ┌────────────┬────────────┬────────────┐   │
│  │ Tokens In  │ Tokens Out │ Cost       │   │
│  │ 125,340    │ 48,230     │ $12.45     │   │
│  └────────────┴────────────┴────────────┘   │
│                                              │
│  TODO PROGRESS                               │
│  ☑ Setup initial          ☑ Feature A       │
│  ☑ Tests Feature A        ☐ Feature B       │
│  ☐ Tests Feature B        ☐ Documentation   │
│                                              │
│  RECENT COMMITS                              │
│  • [Ralph] feat: implement Feature A         │
│  • [Ralph] test: add tests for Feature A     │
│  • [Ralph] Tour 23 - working on Feature B    │
│                                              │
└──────────────────────────────────────────────┘
```

### Avantages

- ✅ Dashboard de monitoring excellent
- ✅ Métriques détaillées
- ✅ Visualisation du progrès
- ✅ Open-source, customisable

### Inconvénients

- ❌ Pas de sandboxing natif
- ❌ Dépendances Node.js
- ❌ Maintenance communautaire
- ❌ Claude uniquement

---

## 4. Vercel AI SDK

Framework pour développeurs JS/TS voulant construire leurs propres agents.

### Installation

```bash
npm install ai @ai-sdk/anthropic
```

### Implémentation Custom

```typescript
// ralph.ts
import { anthropic } from '@ai-sdk/anthropic';
import { generateText, tool } from 'ai';
import { z } from 'zod';
import * as fs from 'fs';
import { execSync } from 'child_process';

const readFileTool = tool({
  description: 'Read a file from the filesystem',
  parameters: z.object({
    path: z.string().describe('File path to read')
  }),
  execute: async ({ path }) => fs.readFileSync(path, 'utf-8')
});

const writeFileTool = tool({
  description: 'Write content to a file',
  parameters: z.object({
    path: z.string(),
    content: z.string()
  }),
  execute: async ({ path, content }) => {
    fs.writeFileSync(path, content);
    return `Written to ${path}`;
  }
});

const bashTool = tool({
  description: 'Execute a bash command',
  parameters: z.object({
    command: z.string()
  }),
  execute: async ({ command }) => {
    try {
      return execSync(command, { encoding: 'utf-8' });
    } catch (e: any) {
      return `Error: ${e.message}`;
    }
  }
});

async function ralphLoop(maxIterations: number = 100) {
  for (let i = 0; i < maxIterations; i++) {
    console.log(`\n=== Iteration ${i + 1} ===`);

    // Check HARD STOP
    const todo = fs.readFileSync('TODO.md', 'utf-8');
    if (todo.includes('[x] DONE')) {
      console.log('✅ HARD STOP - Project complete!');
      break;
    }

    const prompt = fs.readFileSync('PROMPT.md', 'utf-8');

    const { text, toolCalls } = await generateText({
      model: anthropic('claude-sonnet-4-20250514'),
      tools: { readFile: readFileTool, writeFile: writeFileTool, bash: bashTool },
      maxTokens: 4096,
      messages: [
        { role: 'system', content: prompt },
        { role: 'user', content: `Continue working. Iteration ${i + 1}. Read TODO.md for current state.` }
      ]
    });

    console.log('Response:', text?.slice(0, 200) + '...');
    console.log('Tool calls:', toolCalls?.length || 0);

    // Auto-commit
    try {
      execSync('git add -A && git commit -m "[Ralph] Iteration ' + (i + 1) + '"', {
        encoding: 'utf-8'
      });
    } catch (e) {
      // No changes to commit
    }

    await new Promise(r => setTimeout(r, 3000));
  }
}

ralphLoop(100);
```

### Avantages

- ✅ Contrôle total sur l'implémentation
- ✅ Multi-modèle (toute la galerie AI SDK)
- ✅ Intégration facile dans projets existants
- ✅ TypeScript natif

### Inconvénients

- ❌ Pas d'outil prêt à l'emploi
- ❌ Développement requis
- ❌ Pas de sandboxing intégré
- ❌ Pas de monitoring inclus

---

## Résumé Comparatif

| Critère             | Plugin Officiel | Goose      | frankbria  | Vercel SDK |
|---------------------|-----------------|------------|------------|------------|
| Facilité d'usage    | ⭐⭐⭐⭐⭐            | ⭐⭐⭐        | ⭐⭐⭐⭐       | ⭐⭐         |
| Sandboxing          | ⭐⭐⭐⭐⭐            | ⭐⭐⭐⭐⭐      | ⭐           | ⭐           |
| Multi-modèle        | ⭐               | ⭐⭐⭐⭐⭐      | ⭐           | ⭐⭐⭐⭐⭐      |
| Monitoring          | ⭐⭐⭐             | ⭐⭐⭐        | ⭐⭐⭐⭐⭐      | ⭐           |
| Customisation       | ⭐⭐              | ⭐⭐⭐⭐       | ⭐⭐⭐⭐       | ⭐⭐⭐⭐⭐      |
| Documentation       | ⭐⭐⭐⭐⭐            | ⭐⭐⭐⭐       | ⭐⭐⭐        | ⭐⭐⭐⭐       |

### Recommandations

| Cas d'usage                          | Outil recommandé        |
|--------------------------------------|-------------------------|
| Débutant / Usage simple              | Plugin Officiel         |
| Multi-modèle / Comparaison           | Goose                   |
| Monitoring avancé                    | frankbria               |
| Intégration custom / TypeScript      | Vercel AI SDK           |
| Production / Sécurité critique       | Plugin Officiel + Docker|

---

## Prochaine Étape

Apprenez à sécuriser vos agents et optimiser les coûts dans [Sécurité & Coûts](./07-securite-couts.md).

---

[← Workflow Avancé](./05-workflow-avance.md) | [Sommaire](./README.md) | [Sécurité & Coûts →](./07-securite-couts.md)
