# TODO.md - Prospection Hotels & Restaurants

## Status: EN COURS

---

## Criteres de Succes

### Google API
- [ ] Recherche par ville retourne des resultats
- [ ] Filtre --type (hotel/restaurant/all) fonctionne
- [ ] Numero Google recupere via Place Details

### Scraping (IMPORTANT)
- [ ] Site web scrape pour trouver numero reservation
- [ ] Numero reservation extrait correctement (test 5 sites)
- [ ] Email extrait si present

### Export
- [ ] Export CSV avec toutes colonnes
- [ ] Export JSON valide
- [ ] Option --no-scrape fonctionne
- [ ] Option --limit fonctionne

### Qualite
- [ ] Gestion erreurs (timeout, site down)
- [ ] Timeout 10s par site
- [ ] Messages progression clairs
- [ ] README.md complet

---

## Plan d Execution

### Phase 1 : Setup (Tours 1-3) ✓
- [x] Creer src/google_places.py
- [x] Tester connexion API Google
- [x] Commit setup

### Phase 2 : Google API (Tours 4-7) ✓
- [x] Implementer Text Search
- [x] Implementer Place Details
- [x] Tester sur Paris restaurant
- [x] Commit google API

### Phase 3 : Scraping (Tours 8-14)
- [x] Creer src/phone_extractor.py (regex FR)
- [x] Tester extraction numeros
- [x] Creer src/contact_scraper.py
- [x] Implementer detection reservation
- [x] Implementer extraction email
- [x] Tester sur 3 sites reels
- [x] Commit scraper

### Phase 4 : CLI & Export (Tours 15-20)
- [x] Creer src/exporter.py
- [x] Creer src/prospector.py
- [x] Integrer tous modules
- [x] Test complet 10 restaurants
- [x] Commit CLI

### Phase 5 : Finalisation (Tours 21-25)
- [x] Gestion erreurs robuste
- [ ] Ajouter timeouts
- [ ] Creer README.md
- [ ] Verification finale
- [ ] Commit final

---

## Etat Actuel

**Tour :** 9
**Derniere action :** Gestion erreurs robuste implémentée - codes d'erreur détaillés, retry automatique, validation des données
**Prochaine action :** Ajouter timeouts (configurations timeout par défaut 10s)

---

## Architecture

```
src/
├── prospector.py       # CLI principale
├── google_places.py    # Client API Google
├── contact_scraper.py  # Scraping site web
├── phone_extractor.py  # Detection numeros FR
└── exporter.py         # Export CSV/JSON
```

---

## Notes Techniques

### Dependances
```bash
pip install requests beautifulsoup4 python-dotenv
```

### Cle API
GOOGLE_MAPS_API_KEY dans .env

### Regex telephone FR
```
(?:\+33|0)\s*[1-9](?:[\s.-]*\d{2}){4}
```

---

## HARD STOP TRIGGER

- [ ] DONE - Projet termine
