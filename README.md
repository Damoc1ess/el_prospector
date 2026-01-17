# 🏨 Outil de Prospection Hotels & Restaurants

Outil CLI Python pour prospecter des hotels et restaurants via l'API Google Maps, avec extraction automatique des numéros de réservation depuis les sites web.

## ✨ Fonctionnalités

- 🔍 **Recherche Google Maps** : Trouve des établissements par ville via l'API Google Places
- 🌐 **Scraping intelligent** : Visite les sites web pour extraire numéros de réservation et emails
- 📊 **Export multi-format** : CSV et JSON avec données enrichies
- ⚡ **Performance** : Gestion des timeouts, rate limiting et retry automatique
- 🛡️ **Robuste** : Gestion d'erreurs complète et validation des données

## 🚀 Installation

### Prérequis
- Python 3.10 ou supérieur
- Clé API Google Maps avec accès aux Places API

### Installation des dépendances
```bash
pip install requests beautifulsoup4 python-dotenv
```

### Configuration API Google
1. Créer un fichier `.env` dans le dossier du projet
2. Ajouter votre clé API Google Maps :
```
GOOGLE_MAPS_API_KEY=votre_cle_api_ici
```

**Obtenir une clé API Google Maps :**
1. Aller sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créer ou sélectionner un projet
3. Activer les APIs "Places API (New)"
4. Créer une clé API et la copier dans le fichier `.env`

## 📋 Utilisation

### Commande de base
```bash
python src/prospector.py --city "Paris" --type restaurant
```

### Options disponibles

| Option | Description | Défaut |
|--------|-------------|--------|
| `--city` | Ville à prospecter (requis) | - |
| `--type` | Type d'établissement (`hotel`, `restaurant`, `all`) | `all` |
| `--limit` | Nombre maximum de résultats | `20` |
| `--no-scrape` | Désactiver le scraping (plus rapide) | `False` |
| `--output` | Nom de fichier de sortie sans extension | `prospection` |
| `--format` | Format d'export (`csv`, `json`, `both`) | `csv` |

### Exemples d'utilisation

```bash
# Recherche basique - restaurants à Paris
python src/prospector.py --city "Paris" --type restaurant

# Hotels à Lyon avec limite
python src/prospector.py --city "Lyon" --type hotel --limit 10

# Tous types d'établissements à Nice, sans scraping
python src/prospector.py --city "Nice" --type all --no-scrape

# Export JSON uniquement
python src/prospector.py --city "Marseille" --format json

# Export complet avec scraping
python src/prospector.py --city "Bordeaux" --format both --limit 30
```

## 📊 Données extraites

### Sources de données

| Champ | Source | Description |
|-------|--------|-------------|
| `name` | Google Places | Nom de l'établissement |
| `address` | Google Places | Adresse complète |
| `google_phone` | Google Place Details | Numéro Google officiel |
| `website` | Google Place Details | Site web officiel |
| `**reservation_phone**` | **Scraping site web** | **Numéro de réservation** |
| `email` | Scraping site web | Adresse email de contact |
| `rating` | Google Places | Note (sur 5) |
| `reviews` | Google Places | Nombre d'avis |
| `type` | Détection automatique | hotel/restaurant |

### Exemple de sortie CSV
```csv
name,address,google_phone,reservation_phone,email,website,rating,reviews,type
Le Petit Bistro,"12 rue de la Paix, 75001 Paris",+33 1 23 45 67 89,+33 1 98 76 54 32,contact@petitbistro.fr,https://petitbistro.fr,4.5,120,restaurant
Hotel Royal,"5 avenue des Champs, 75008 Paris",+33 4 56 78 90 12,+33 4 11 22 33 44,,https://hotelroyal.fr,4.2,89,hotel
```

## 🕷️ Extraction de numéros de réservation

Le scraper visite automatiquement les sites web et utilise une logique intelligente :

### 1. Détection par liens téléphone
Recherche les liens `<a href="tel:+33123456789">` en priorité.

### 2. Analyse contextuelle
Cherche les numéros près des mots-clés :
- **Français** : "réservation", "réserver", "contact", "appelez"
- **Anglais** : "booking", "book now", "book a table", "call us"

### 3. Fallback intelligent
Si aucun contexte de réservation, prend le premier numéro français valide.

### Formats supportés
- `+33 X XX XX XX XX`
- `0X XX XX XX XX`
- `0X.XX.XX.XX.XX`
- `0X-XX-XX-XX-XX`
- `0123456789`

## ⚡ Performance et limites

### Rate limiting
- **Google API** : 1 seconde entre requêtes
- **Scraping** : 2 secondes entre sites web
- **Timeout** : 10 secondes par site web

### Gestion d'erreurs
- ✅ Retry automatique sur erreurs temporaires (503, timeout)
- ✅ Continuation en cas d'échec d'un site
- ✅ Validation SSL et filtrage de contenu
- ✅ Protection contre sites trop volumineux (>5MB)

### Limitations
- Maximum 20 résultats par requête Google Places
- Scraping respectueux (User-Agent réaliste)
- Pas de scraping de plus de 60 sites/minute

## 🏗️ Architecture

```
src/
├── prospector.py       # CLI principale avec argparse
├── google_places.py    # Client API Google Places v1
├── contact_scraper.py  # Scraping site web + extraction contacts
├── phone_extractor.py  # Détection et formatage numéros FR
└── exporter.py         # Export CSV/JSON
```

### Modules principaux

#### `GooglePlacesClient`
- Text Search API pour trouver établissements par ville
- Place Details API pour récupérer téléphone et site web
- Gestion d'erreurs API et rate limiting

#### `ContactScraper`
- Téléchargement pages web avec retry
- Extraction numéros de réservation par contexte
- Extraction emails avec filtrage anti-spam

#### `PhoneExtractor`
- Regex optimisée pour numéros français
- Nettoyage et formatage automatique
- Détection contextuelle des numéros de réservation

#### `Exporter`
- Export CSV avec en-têtes standardisés
- Export JSON avec métadonnées
- Validation des données avant export

## 🐛 Dépannage

### Erreurs courantes

**❌ "API key invalide ou manquante"**
```bash
# Vérifier le fichier .env
cat .env
# Doit contenir : GOOGLE_MAPS_API_KEY=votre_cle
```

**❌ "Aucun établissement trouvé"**
- Vérifier l'orthographe de la ville
- Essayer avec une ville plus connue (Paris, Lyon, Marseille...)
- Changer le type d'établissement

**❌ "Timeout lors du scraping"**
- Normal pour certains sites lents
- Utiliser `--no-scrape` pour un test rapide
- Le scraping continue avec les autres sites

**❌ "Quota API dépassé"**
- Vérifier les quotas dans Google Cloud Console
- Attendre la remise à zéro du quota (24h)
- Optimiser avec `--limit` plus faible

### Messages d'état

| Message | Signification |
|---------|---------------|
| `✅ OK` | Scraping réussi avec contacts trouvés |
| `⚠️ Aucun contact trouvé` | Site accessible mais pas de numéro |
| `❌ ERREUR: timeout` | Site trop lent (>10s) |
| `❌ ERREUR: 403` | Site bloque les robots |
| `❌ ERREUR: 404` | Page non trouvée |

## 🧪 Tests

### Test rapide
```bash
# Test de l'API Google
python src/google_places.py

# Test du scraper
python src/contact_scraper.py

# Test de l'extracteur de numéros
python src/phone_extractor.py

# Test de l'exporteur
python src/exporter.py
```

### Test complet
```bash
# Test avec 5 restaurants parisiens (rapide)
python src/prospector.py --city "Paris" --type restaurant --limit 5
```

## 📝 Exemples avancés

### Prospection hôtels de luxe
```bash
python src/prospector.py --city "Cannes" --type hotel --limit 15 --format both
```

### Audit restaurants sans scraping (rapide)
```bash
python src/prospector.py --city "Toulouse" --type restaurant --no-scrape --limit 50
```

### Export personnalisé
```bash
python src/prospector.py --city "Strasbourg" --output "hotels_strasbourg" --format json
```

## 🔒 Respect des bonnes pratiques

- ✅ Rate limiting respectueux
- ✅ User-Agent réaliste
- ✅ Gestion SSL appropriée
- ✅ Timeouts configurés (10s)
- ✅ Pas de surcharge des serveurs
- ✅ Données pseudonymisées dans les logs

## 📄 Licence

Ce projet est destiné à un usage professionnel de prospection commerciale.
Respecter les CGU des sites web scrapés et les réglementations RGPD.

---

**Développé par Ralph Wiggum** 🤖 - Outil de prospection automatisé pour professionnels.