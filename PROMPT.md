# PROMPT.md - Outil de Prospection Hotels & Restaurants

## Contexte

Tu es en mode **Ralph Wiggum** - agent autonome qui travaille sans supervision.

**Mission :** Creer un outil CLI Python pour prospecter des hotels et restaurants via l API Google Maps, avec extraction des numeros de reservation depuis les sites web.

**Stack :** Python 3.10+ avec requests et BeautifulSoup

Tu persistes ton etat via :
- `TODO.md` pour l avancement (LIS CE FICHIER A CHAQUE TOUR)
- Git commits pour l historique

---

## Objectif

Creer un outil CLI qui :
1. Recherche des hotels/restaurants dans une ville via Google Maps
2. Visite chaque site web pour extraire le numero de RESERVATION
3. Exporte les contacts enrichis en CSV/JSON

---

## Specifications Techniques

### Stack

| Element | Choix |
|---------|-------|
| Langage | Python 3.10+ |
| HTTP | requests |
| Scraping | BeautifulSoup4 |
| CLI | argparse |
| Export | csv, json (stdlib) |
| Config | python-dotenv |

### Dependances a installer
```bash
pip install requests beautifulsoup4 python-dotenv
```

### API Google Maps

- **Text Search** : Trouver les etablissements par ville
- **Place Details** : Obtenir website, phone Google

Base URL : `https://maps.googleapis.com/maps/api/place`

### Extraction Numero Reservation (IMPORTANT)

Le scraper doit visiter le site web et chercher :

**Patterns de texte a detecter :**
- "Reservation", "Reservations", "Reserver"
- "Booking", "Book now", "Book a table"
- "Contact", "Nous contacter"
- "Tel", "Telephone", "Phone"
- "Appelez", "Call us"

**Formats de telephone francais a matcher :**
```
+33 X XX XX XX XX
0X XX XX XX XX
0X.XX.XX.XX.XX
0X-XX-XX-XX-XX
01 23 45 67 89
0123456789
```

**Logique d extraction :**
1. Telecharger la page HTML du site
2. Chercher les liens tel: (href="tel:...")
3. Chercher les numeros pres des mots "reservation", "booking"
4. Si pas trouve, prendre le premier numero de la page
5. Nettoyer et formater le numero

### Interface CLI

```bash
# Recherche basique
python src/prospector.py --city "Paris" --type restaurant

# Avec options
python src/prospector.py --city "Lyon" --type hotel --limit 20

# Sans scraping (plus rapide)
python src/prospector.py --city "Nice" --type all --no-scrape
```

### Donnees a recuperer

| Champ | Source | Priorite |
|-------|--------|----------|
| name | Google Places | Obligatoire |
| address | Google Places | Obligatoire |
| google_phone | Google Place Details | Obligatoire |
| website | Google Place Details | Important |
| **reservation_phone** | **Scraping site web** | **IMPORTANT** |
| email | Scraping site web | Optionnel |
| rating | Google Places | Optionnel |
| reviews_count | Google Places | Optionnel |
| place_id | Google Places | Obligatoire |

### Format de sortie CSV

```csv
name,address,google_phone,reservation_phone,email,website,rating,reviews,type
Le Petit Bistro,12 rue...,+33 1 23 45 67 89,+33 1 98 76 54 32,contact@...,https://...,4.5,120,restaurant
Hotel Royal,5 avenue...,+33 4 56 78 90 12,+33 4 00 00 00 00,,https://...,4.2,89,hotel
```

### Architecture

```
src/
├── prospector.py       # CLI principale
├── google_places.py    # Client API Google
├── contact_scraper.py  # Scraping site web (phone + email)
├── phone_extractor.py  # Detection et formatage numeros
└── exporter.py         # Export CSV/JSON
```

---

## Criteres de Succes

### Fonctionnels
1. [ ] Recherche par ville retourne des resultats
2. [ ] Filtre --type (hotel/restaurant/all) fonctionne
3. [ ] Numero Google recupere via Place Details
4. [ ] **Site web scrape pour trouver numero reservation**
5. [ ] **Numero reservation extrait correctement (test sur 5 sites)**
6. [ ] Email extrait si present sur le site
7. [ ] Export CSV avec toutes les colonnes
8. [ ] Export JSON valide
9. [ ] Option --no-scrape fonctionne
10. [ ] Option --limit fonctionne

### Qualite
11. [ ] Gestion erreurs (site inaccessible, timeout)
12. [ ] Timeout de 10s par site web
13. [ ] Messages de progression clairs
14. [ ] README.md avec exemples

---

## Workflow

**IMPORTANT : Suis cet ordre STRICTEMENT.**

### Phase 1 : Setup (Tours 1-3)
1. **Study** ce fichier PROMPT.md en entier
2. **Study** TODO.md pour l etat actuel
3. Creer `src/google_places.py` - client API basique
4. **Verify by running** : tester connexion API
5. Commit : `[Ralph] feat: google places client`

### Phase 2 : Google API (Tours 4-7)
6. Implementer Text Search (recherche par ville)
7. Implementer Place Details (phone, website)
8. **Verify by running** : tester sur "Paris restaurant"
9. Commit : `[Ralph] feat: google search and details`

### Phase 3 : Scraping (Tours 8-14)
10. Creer `src/phone_extractor.py` - regex pour numeros FR
11. **Verify by running** : tester extraction sur numeros exemples
12. Creer `src/contact_scraper.py` - visiter sites web
13. Implementer detection numero reservation
14. Implementer extraction email
15. **Verify by running** : tester sur 3 sites reels
16. Commit : `[Ralph] feat: contact scraper`

### Phase 4 : CLI & Export (Tours 15-20)
17. Creer `src/exporter.py` (CSV + JSON)
18. Creer `src/prospector.py` avec argparse
19. Integrer tous les modules
20. **Verify by running** : test complet Paris 10 restaurants
21. Commit : `[Ralph] feat: complete CLI`

### Phase 5 : Finalisation (Tours 21-25)
22. Gestion erreurs robuste (try/except)
23. Ajouter timeouts (10s par site)
24. Creer README.md avec exemples
25. **Verify by running** : tous les criteres
26. Commit final : `[Ralph] docs: project complete`

---

## HARD STOP

**ARRETE-TOI IMMEDIATEMENT** si :

| Condition | Action |
|-----------|--------|
| Tous criteres coches [x] dans TODO.md | Ecrire `[x] DONE` et STOP |
| 30 tours sans progres mesurable | Noter blocage et STOP |
| Meme erreur 5+ fois | Noter bug et STOP |
| API Google ne fonctionne pas | Noter erreur et STOP |

---

## Guardrails

### OBLIGATOIRE
- **DO NOT skip** la lecture de TODO.md a chaque tour
- Un commit par fonctionnalite complete
- Format : `[Ralph] type: description`
- Met a jour TODO.md apres chaque action
- **Sleep 1 seconde** entre requetes API Google
- **Sleep 2 secondes** entre chaque scraping de site
- **Timeout 10 secondes** par site web
- User-Agent realiste pour le scraping

### INTERDIT
- Modifier PROMPT.md
- Commiter la cle API (.env ignore)
- Scraper plus de 60 sites par minute
- **NEVER** continuer apres HARD STOP

### CONSEILS
- Utilise `requests.get(url, timeout=10)` pour les sites
- Gere les exceptions : ConnectionError, Timeout, etc.
- Si un site echoue, passe au suivant (ne bloque pas)
- Affiche : "Scraping site 1/20... OK" ou "ERREUR: timeout"

---

## Notes Techniques

### User-Agent pour scraping
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}
response = requests.get(url, headers=headers, timeout=10)
```

### Regex numeros francais
```python
import re

# Pattern pour numeros francais
phone_pattern = r'(?:\+33|0)\s*[1-9](?:[\s.-]*\d{2}){4}'

# Trouver tous les numeros
phones = re.findall(phone_pattern, text)
```

### Extraction liens tel:
```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')
tel_links = soup.find_all('a', href=re.compile(r'^tel:'))
for link in tel_links:
    phone = link['href'].replace('tel:', '')
```

### Detection numero reservation
```python
# Chercher le numero le plus proche de mots cles
keywords = ['reservation', 'reserver', 'booking', 'book']
# Analyser le contexte autour de chaque numero trouve
```
