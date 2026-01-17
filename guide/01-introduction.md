# 01 - Introduction à Ralph Wiggum

## Qu'est-ce que Ralph Wiggum ?

Ralph Wiggum est une technique de développement assisté par IA qui consiste à faire tourner Claude Code CLI en **boucle autonome** sur des tâches de développement complexes. L'agent travaille sans supervision humaine pendant des heures, utilisant des fichiers et des commits git pour maintenir sa mémoire à travers les sessions.

### L'Idée Fondamentale

Au lieu de :
```
Humain: "Ajoute cette fonction"
Claude: [écrit la fonction]
Humain: "Maintenant ajoute les tests"
Claude: [écrit les tests]
Humain: "Corrige cette erreur"
...
```

Avec Ralph Wiggum :
```
Humain: "Construis une CLI complète avec tests, docs et CI/CD"
[Lance Ralph et part dormir]
[Au réveil: projet terminé avec 47 commits]
```

---

## Origine et Créateur

La technique a été créée par **Geoffrey Huntley** (@GeoffreyHuntley), un développeur australien connu pour ses contributions open-source. Il a documenté et popularisé la méthode à partir de mai 2025.

### Pourquoi ce nom ?

Le nom vient de **Ralph Wiggum**, le fils du chef de police Wiggum dans Les Simpsons. Ralph est connu pour ses déclarations absurdes mais attachantes comme "Me fail English? That's unpossible!"

L'analogie est délibérée :

> "Claude is deterministically bad in an undeterministic world. It will keep trying until it accidentally succeeds."
> — Geoffrey Huntley

Comme Ralph, l'agent peut sembler faire des erreurs "stupides" sur des tâches individuelles. Mais avec :
- **Suffisamment d'itérations**
- **Persistance via fichiers/git**
- **Des guardrails bien définis**

...il finit par accomplir des projets entiers que peu de développeurs humains pourraient faire seuls.

---

## Comment Ça Fonctionne

Le principe repose sur trois piliers :

### 1. La Boucle Autonome

```
┌─────────────────────────────────────────┐
│                                         │
│  ┌─────────┐    ┌─────────┐            │
│  │ PROMPT  │───▶│ Claude  │            │
│  │  .md    │    │  Code   │            │
│  └─────────┘    └────┬────┘            │
│                      │                  │
│                      ▼                  │
│              ┌──────────────┐          │
│              │  Exécution   │          │
│              │  (code, git) │          │
│              └──────┬───────┘          │
│                     │                  │
│                     ▼                  │
│              ┌──────────────┐          │
│              │   TODO.md    │◀─────┐   │
│              │  (progrès)   │      │   │
│              └──────┬───────┘      │   │
│                     │              │   │
│                     ▼              │   │
│              ┌──────────────┐      │   │
│              │   Terminé?   │──Non─┘   │
│              └──────┬───────┘          │
│                     │Oui               │
│                     ▼                  │
│              ┌──────────────┐          │
│              │    STOP      │          │
│              └──────────────┘          │
│                                         │
└─────────────────────────────────────────┘
```

### 2. La Persistance via Fichiers

L'agent n'a pas de mémoire entre les sessions. Pour contourner cette limite :
- **PROMPT.md** : Les instructions persistantes
- **TODO.md** : L'état d'avancement (checklist)
- **Git commits** : L'historique complet des changements
- **Fichiers specs/** : Les décisions architecturales

### 3. Les Guardrails

Des règles strictes pour éviter que l'agent ne déraille :
- **HARD STOP** : Conditions d'arrêt obligatoires
- **Checkpoints** : Points de validation intermédiaires
- **Limites de tours** : Nombre max d'itérations par session

---

## Chronologie de l'Adoption

| Date           | Événement                                               |
|----------------|---------------------------------------------------------|
| **Mai 2025**   | Geoffrey Huntley documente la technique                 |
| **Juin 2025**  | Premier projet majeur : Cursed Lang (langage complet)   |
| **Août 2025**  | La communauté adopte massivement la technique           |
| **Sept 2025**  | Goose (Block) intègre le pattern officiellement         |
| **Oct 2025**   | Hackathon YC : 6 repos créés pour $297 avec Ralph       |
| **Déc 2025**   | Anthropic sort le plugin officiel pour Claude Code      |
| **Jan 2026**   | Documentation officielle et best practices stabilisées  |

---

## Cas d'Usage Typiques

### Idéal Pour

| Tâche                          | Pourquoi Ralph excelle                           |
|--------------------------------|--------------------------------------------------|
| Création de projet from scratch | Pas de code existant à comprendre               |
| Migration/Refactoring batch    | Tâches répétitives avec patterns clairs          |
| Génération de tests            | Processus mécanique bien défini                  |
| Documentation technique        | Extraction d'info depuis le code                 |
| Prototypage rapide             | Itération rapide sans perfection requise         |

### Moins Adapté Pour

| Tâche                          | Problème                                         |
|--------------------------------|--------------------------------------------------|
| Debug de bugs subtils          | Nécessite compréhension profonde du contexte     |
| Code critique (sécurité)       | Risque d'erreurs non détectées                   |
| Intégration systèmes complexes | Trop de dépendances externes                     |
| Code avec beaucoup de legacy   | Context window insuffisant                       |

---

## Les Trois Lois de Ralph Wiggum

Geoffrey Huntley a codifié trois principes fondamentaux :

### 1. "Les fichiers sont la mémoire"

> L'agent oublie tout entre les sessions. Tout ce qui compte doit être écrit dans des fichiers.

- TODO.md pour l'état
- Commits git pour l'historique
- Specs/ pour les décisions

### 2. "Les guardrails définissent le succès"

> Un prompt sans limites claires mène à l'échec. Définissez précisément :
> - Critères de succès vérifiables
> - Conditions d'arrêt (HARD STOP)
> - Ce qui est hors scope

### 3. "L'itération bat la perfection"

> Un agent qui fait 100 tentatives trouvera une solution. Un humain qui cherche la solution parfaite du premier coup... prendra plus de temps.

---

## Avertissements Importants

### Coûts

Ralph peut **consommer beaucoup de tokens**. Un projet moyen coûte $10-50, mais des projets complexes peuvent dépasser $100-200.

### Sécurité

**Jamais** de Ralph sans sandboxing. L'agent a accès au système de fichiers et peut exécuter des commandes bash. Utilisez Docker ou un environnement isolé.

### Supervision

Même en mode "autonome", vérifiez périodiquement :
- Les commits git (qualité du code)
- Les coûts API
- Les boucles infinies potentielles

---

## Prochaine Étape

Maintenant que vous comprenez le concept, passez à l'[Installation](./02-installation.md) pour configurer votre environnement.

---

[← Retour au sommaire](./README.md) | [Installation →](./02-installation.md)
