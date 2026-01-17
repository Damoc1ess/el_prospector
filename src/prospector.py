#!/usr/bin/env python3
"""
CLI principale pour la prospection d'hotels et restaurants.
"""

import argparse
import sys
import time
from typing import List, Dict, Optional

from google_places import GooglePlacesClient
from contact_scraper import ContactScraper
from exporter import Exporter


def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(
        description="Outil de prospection hotels/restaurants avec extraction contact"
    )

    parser.add_argument(
        "--city",
        required=True,
        help="Ville à prospecter (ex: Paris, Lyon)"
    )

    parser.add_argument(
        "--type",
        choices=["hotel", "restaurant", "all"],
        default="all",
        help="Type d'établissement (défaut: all)"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Nombre maximum de résultats (défaut: 20)"
    )

    parser.add_argument(
        "--no-scrape",
        action="store_true",
        help="Désactiver le scraping des sites web (plus rapide)"
    )

    parser.add_argument(
        "--output",
        default="prospection",
        help="Nom de fichier de sortie sans extension (défaut: prospection)"
    )

    parser.add_argument(
        "--format",
        choices=["csv", "json", "both"],
        default="csv",
        help="Format d'export (défaut: csv)"
    )

    args = parser.parse_args()

    # Initialisation des clients
    print(f"🔍 Recherche d'établissements à {args.city}...")

    try:
        google_client = GooglePlacesClient()
        scraper = ContactScraper() if not args.no_scrape else None
        exporter = Exporter()

    except Exception as e:
        print(f"❌ Erreur d'initialisation: {e}")
        sys.exit(1)

    # Recherche Google Places
    try:
        establishments = search_establishments(
            google_client,
            args.city,
            args.type,
            args.limit
        )

        if not establishments:
            print(f"❌ Aucun établissement trouvé pour {args.city}")
            sys.exit(1)

        print(f"✅ {len(establishments)} établissements trouvés")

    except Exception as e:
        print(f"❌ Erreur de recherche: {e}")
        sys.exit(1)

    # Enrichissement avec détails Google
    print("📋 Récupération des détails...")
    enriched_data = []

    for i, place in enumerate(establishments, 1):
        print(f"  {i}/{len(establishments)} - {place.get('name', 'N/A')}")

        try:
            details = google_client.get_place_details(place['place_id'])

            # Données de base
            contact_data = {
                'name': place.get('name', ''),
                'address': place.get('formatted_address', ''),
                'place_id': place['place_id'],
                'google_phone': details.get('international_phone_number', ''),
                'website': details.get('website', ''),
                'rating': place.get('rating', ''),
                'reviews': place.get('user_ratings_total', ''),
                'type': determine_type(place),
                'reservation_phone': '',
                'email': ''
            }

            enriched_data.append(contact_data)
            time.sleep(1)  # Respect API rate limits

        except Exception as e:
            print(f"    ⚠️  Erreur détails: {e}")
            continue

    # Scraping des sites web si demandé
    if scraper and not args.no_scrape:
        print("\n🌐 Scraping des sites web pour contacts...")

        for i, data in enumerate(enriched_data, 1):
            if not data['website']:
                print(f"  {i}/{len(enriched_data)} - {data['name']} - Pas de site web")
                continue

            print(f"  {i}/{len(enriched_data)} - {data['name']} - ", end="")

            try:
                contact_info = scraper.scrape_contact_info(data['website'])

                if contact_info['phone']:
                    data['reservation_phone'] = contact_info['phone']
                    print("✅ Téléphone trouvé")
                else:
                    print("❌ Pas de téléphone")

                if contact_info['email']:
                    data['email'] = contact_info['email']

                time.sleep(2)  # Délai entre scraping

            except Exception as e:
                print(f"❌ Erreur: {str(e)[:50]}...")
                continue

    # Export des résultats
    print(f"\n📊 Export des résultats ({len(enriched_data)} entrées)...")

    try:
        if args.format in ["csv", "both"]:
            success = exporter.export_csv(enriched_data, f"{args.output}.csv")
            if not success:
                sys.exit(1)

        if args.format in ["json", "both"]:
            success = exporter.export_json(enriched_data, f"{args.output}.json")
            if not success:
                sys.exit(1)

    except Exception as e:
        print(f"❌ Erreur d'export: {e}")
        sys.exit(1)

    print(f"\n🎉 Prospection terminée avec succès!")


def search_establishments(client: GooglePlacesClient, city: str, establishment_type: str, limit: int) -> List[Dict]:
    """Recherche des établissements via Google Places."""
    results = []

    if establishment_type == "all":
        types_to_search = ["restaurant", "hotel"]
    else:
        types_to_search = [establishment_type]

    for search_type in types_to_search:
        query = f"{search_type} in {city}"

        try:
            places = client.search_places(city, search_type)

            # Limiter les résultats
            type_limit = limit // len(types_to_search) if establishment_type == "all" else limit
            results.extend(places[:type_limit])

            time.sleep(1)  # Rate limiting

        except Exception as e:
            print(f"⚠️  Erreur recherche {search_type}: {e}")
            continue

    return results[:limit]


def determine_type(place: Dict) -> str:
    """Détermine le type d'établissement à partir du contexte de recherche."""
    # Pour l'instant, on utilise le type de recherche plutôt que les types Google
    # car les données Google Places v1 ne retournent pas les types détaillés
    name = place.get('name', '').lower()
    address = place.get('formatted_address', '').lower()

    # Mots-clés pour hotels
    hotel_keywords = ['hotel', 'hôtel', 'auberge', 'gîte', 'chambre', 'suite', 'resort']
    if any(keyword in name for keyword in hotel_keywords):
        return 'hotel'

    # Mots-clés pour restaurants
    restaurant_keywords = ['restaurant', 'bistro', 'brasserie', 'café', 'pizzeria', 'bar', 'bouillon']
    if any(keyword in name for keyword in restaurant_keywords):
        return 'restaurant'

    # Par défaut, considérer comme restaurant si c'est ambigu
    return 'restaurant'


if __name__ == "__main__":
    main()