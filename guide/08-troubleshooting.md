# 08 - Troubleshooting

Ce chapitre couvre les erreurs les plus fréquentes et leurs solutions.

---

## Erreurs Courantes

### 1. "Bash command permission check failed"

**Symptôme :**
```
Error: Bash command permission check failed
Command "npm install" is not in the allowed list
```

**Cause :** Les permissions bash ne sont pas configurées.

**Solution :**

```json
// .claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(npm *)",
      "Bash(node *)",
      "Bash(python *)",
      "Bash(git *)"
    ]
  }
}
```

Ou mode interactif :
```bash
claude --print "..." --allow-bash
```

---

### 2. "jq: command not found"

**Symptôme :**
```
./loop.sh: line 23: jq: command not found
```

**Cause :** jq n'est pas installé.

**Solution :**

```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq

# Alpine (Docker)
apk add jq
```

---

### 3. "ANTHROPIC_API_KEY not set"

**Symptôme :**
```
Error: ANTHROPIC_API_KEY environment variable is not set
```

**Cause :** Clé API non configurée.

**Solution :**

```bash
# Dans ~/.zshrc ou ~/.bashrc
export ANTHROPIC_API_KEY="sk-ant-..."

# Recharger
source ~/.zshrc

# Vérifier
echo $ANTHROPIC_API_KEY
```

Pour Docker :
```bash
docker run -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" ...
```

---

### 4. Context Window Overflow (Context Rot)

**Symptôme :**
- Ralph "oublie" ce qu'il faisait
- Répète les mêmes actions
- Ignore des instructions du PROMPT.md

**Cause :** Le contexte dépasse la limite du modèle.

**Solutions :**

1. **Réduire le PROMPT.md**
```markdown
<!-- AVANT: 2000 mots -->
<!-- APRÈS: 500 mots essentiels -->
```

2. **Checkpoints avec résumé**
```bash
# Tous les 10 tours
claude --print "Résume en 100 mots l'état actuel et écris dans TODO.md"
```

3. **Nouveaux fichiers de contexte**
```markdown
# TODO.md

## État Actuel (mise à jour tour 25)
- Feature A: COMPLÈTE
- Feature B: EN COURS (50%)
- Reste: Feature C, D

## Focus Immédiat
Terminer Feature B, tests inclus.
```

4. **Découper en sous-tâches**
```
Projet complet → Phase 1 (PROMPT-1.md) → Phase 2 (PROMPT-2.md) → ...
```

---

### 5. Spirale sur le Même Bug

**Symptôme :**
- Ralph essaie la même solution 5+ fois
- Le même test échoue en boucle
- Pas de progrès malgré les itérations

**Cause :** L'agent n'a pas assez d'informations ou le bug est complexe.

**Solutions :**

1. **Intervention manuelle**
```markdown
# TODO.md

## NOTE HUMAINE (tour 23)
Le bug est dans la fonction X ligne Y.
Le problème: [explication]
Approche suggérée: [hint]
```

2. **Skip temporaire**
```markdown
## Guardrails
- Si un test échoue 3 fois: le skip avec @skip
- Créer une issue TODO pour plus tard
```

3. **Reset partiel**
```bash
# Revenir à un état stable
git checkout <commit-stable> -- src/problematic-file.js

# Relancer avec instructions spécifiques
claude --print "Le fichier X a été reset. Réimplémente différemment."
```

---

### 6. Ralph Ne S'arrête Pas

**Symptôme :**
- Tous les critères semblent remplis
- Le pattern HARD STOP n'est pas déclenché
- L'agent continue indéfiniment

**Cause :** Pattern HARD STOP mal défini ou non reconnu.

**Solutions :**

1. **Vérifier le pattern**
```bash
# Le pattern TODO.md doit EXACTEMENT correspondre
grep "\[x\] DONE" TODO.md
```

2. **Simplifier le trigger**
```markdown
## HARD STOP TRIGGER
Écris exactement cette ligne quand terminé:
RALPH_COMPLETE=true
```

3. **Forcer l'arrêt manuel**
```bash
# Créer le trigger manuellement
echo "- [x] DONE - Projet terminé" >> TODO.md
```

4. **Limite de temps**
```bash
timeout 3600 ./loop.sh  # Max 1 heure
```

---

### 7. Commits Git Échouent

**Symptôme :**
```
nothing to commit, working tree clean
# ou
fatal: not a git repository
```

**Solutions :**

```bash
# Vérifier que git est initialisé
cd /path/to/project
git status

# Si non initialisé
git init
git add .
git commit -m "Initial commit"

# Si "nothing to commit" est OK
# Modifier loop.sh pour ignorer
git commit --allow-empty -m "[Ralph] Tour $i"
```

---

### 8. Docker : Permission Denied

**Symptôme :**
```
permission denied while trying to connect to Docker daemon
```

**Solutions :**

```bash
# Linux: ajouter au groupe docker
sudo usermod -aG docker $USER
# Puis logout/login

# macOS: démarrer Docker Desktop
open -a Docker

# Vérifier
docker ps
```

---

### 9. Rate Limiting API

**Symptôme :**
```
Error: 429 Too Many Requests
Rate limit exceeded
```

**Solutions :**

1. **Ajouter des délais**
```bash
# loop.sh
sleep 10  # Entre chaque itération
```

2. **Exponential backoff**
```bash
retry_with_backoff() {
    local max_attempts=5
    local delay=5

    for ((i=1; i<=max_attempts; i++)); do
        if "$@"; then
            return 0
        fi
        echo "Attempt $i failed, waiting ${delay}s..."
        sleep $delay
        delay=$((delay * 2))
    done
    return 1
}

retry_with_backoff claude --print "..."
```

3. **Réduire le parallélisme**
```json
{
  "ralph": {
    "concurrency": 1,
    "minDelayBetweenCalls": 5000
  }
}
```

---

### 10. Fichiers Corrompus ou Invalides

**Symptôme :**
- JSON invalide dans todos.json
- Code Python avec erreurs de syntaxe
- Fichiers à moitié écrits

**Solutions :**

1. **Restaurer via git**
```bash
# Voir les versions
git log --oneline -- fichier.json

# Restaurer
git checkout HEAD~3 -- fichier.json
```

2. **Validation automatique**
```markdown
## Guardrails
- Après chaque écriture JSON: `python -m json.tool fichier.json`
- Après chaque écriture Python: `python -m py_compile fichier.py`
```

3. **Backup avant modification**
```bash
# Dans loop.sh
cp fichier.json fichier.json.bak
```

---

## Debugging Avancé

### Activer les Logs Verbeux

```bash
# Logs détaillés
DEBUG=claude:* claude --print "..."

# Logs dans un fichier
claude --print "..." 2>&1 | tee ralph-debug.log
```

### Analyser l'Historique Git

```bash
# Voir tous les changements de Ralph
git log --oneline --all | grep "\[Ralph\]"

# Diff entre deux états
git diff <commit1> <commit2>

# Trouver quand un bug a été introduit
git bisect start
git bisect bad HEAD
git bisect good <commit-stable>
```

### Inspecter l'État de Claude

```bash
# Si disponible
cat ~/.claude/state.json | jq .

# Tokens utilisés
cat ~/.claude/usage.json | jq .
```

---

## Quand Arrêter et Intervenir

### Signaux d'Alarme

| Signal                              | Sévérité | Action                      |
|-------------------------------------|----------|-----------------------------|
| Même erreur 3+ fois                 | 🟡       | Ajouter un hint             |
| Coût > 50% du budget                | 🟡       | Évaluer le progrès          |
| Aucun commit depuis 10 tours        | 🟠       | Vérifier les logs           |
| Fichiers supprimés par erreur       | 🟠       | Restaurer, clarifier règles |
| Code manifestement faux             | 🟠       | Reset partiel               |
| Coût > budget                       | 🔴       | STOP immédiat               |
| Boucle infinie détectée             | 🔴       | STOP + analyse              |

### Procédure d'Intervention

```bash
# 1. Arrêter proprement
# Ctrl+C ou kill le process

# 2. Sauvegarder l'état
git add -A
git commit -m "[HUMAN] Intervention - Tour $X"

# 3. Analyser
cat TODO.md
git log --oneline -20

# 4. Corriger
# - Éditer PROMPT.md si instructions floues
# - Éditer TODO.md avec des hints
# - Fix manuel si bug simple

# 5. Relancer
./loop.sh
```

---

## FAQ

### Q: Ralph peut-il casser mon système ?

**R:** Oui, si pas sandboxé. Utilisez TOUJOURS Docker ou un environnement isolé.

### Q: Combien de temps laisser tourner ?

**R:** Dépend du projet. Règle : si pas de progrès visible en 20 tours, intervenir.

### Q: Puis-je reprendre après une interruption ?

**R:** Oui, c'est l'avantage du système fichier. Le TODO.md conserve l'état.

### Q: Comment éviter les coûts excessifs ?

**R:** Définir `maxCost` dans la config et surveiller avec les circuit breakers.

---

## Prochaine Étape

Découvrez des cas réels dans [Cas d'Étude](./09-cas-etude.md).

---

[← Sécurité & Coûts](./07-securite-couts.md) | [Sommaire](./README.md) | [Cas d'Étude →](./09-cas-etude.md)
