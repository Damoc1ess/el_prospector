#!/usr/bin/env python3
"""
CLI principale pour la prospection d'hotels et restaurants.
"""

import argparse
import sys
import time
import requests
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

        # Validation des arguments
        if args.limit <= 0:
            print(f"❌ Limite invalide: {args.limit} (doit être > 0)")
            sys.exit(1)
        elif args.limit > 500:
            print(f"⚠️  Limite très élevée: {args.limit}, cela pourrait prendre du temps")

    except ValueError as e:
        if "GOOGLE_MAPS_API_KEY" in str(e):
            print("❌ Clé API Google manquante")
            print("  Créez un fichier .env avec GOOGLE_MAPS_API_KEY=votre_cle")
            sys.exit(1)
        else:
            print(f"❌ Erreur de configuration: {e}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur d'initialisation inattendue: {e}")
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
            print(f"  Vérifiez l'orthographe de '{args.city}' ou essayez une ville plus connue")
            sys.exit(1)

        print(f"✅ {len(establishments)} établissements trouvés")

    except ValueError as e:
        print(f"❌ Erreur de paramètres de recherche: {e}")
        sys.exit(1)
    except requests.RequestException as e:
        print(f"❌ Erreur de connexion Google Places: {e}")
        print("  Vérifiez votre connexion internet et votre clé API")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur de recherche inattendue: {e}")
        sys.exit(1)

    # Enrichissement avec détails Google
    print("📋 Récupération des détails...")
    enriched_data = []
    failed_details = 0
    max_failures = len(establishments) // 2  # Allow up to 50% failures

    for i, place in enumerate(establishments, 1):
        place_name = place.get('name', 'N/A')
        print(f"  {i}/{len(establishments)} - {place_name}...", end=" ")

        try:
            details = google_client.get_place_details(place['place_id'])

            if details:
                # Données de base avec validation
                contact_data = {
                    'name': place.get('name', '').strip() or 'N/A',
                    'address': place.get('formatted_address', '').strip() or 'N/A',
                    'place_id': place['place_id'],
                    'google_phone': details.get('international_phone_number', '').strip() if details.get('international_phone_number') else '',
                    'website': details.get('website', '').strip() if details.get('website') else '',
                    'rating': place.get('rating', ''),
                    'reviews': place.get('user_ratings_total', ''),
                    'type': determine_type(place),
                    'reservation_phone': '',
                    'email': ''
                }

                enriched_data.append(contact_data)
                print("✅")
            else:
                # Place details failed, but keep basic info
                contact_data = {
                    'name': place.get('name', '').strip() or 'N/A',
                    'address': place.get('formatted_address', '').strip() or 'N/A',
                    'place_id': place['place_id'],
                    'google_phone': '',
                    'website': '',
                    'rating': place.get('rating', ''),
                    'reviews': place.get('user_ratings_total', ''),
                    'type': determine_type(place),
                    'reservation_phone': '',
                    'email': ''
                }
                enriched_data.append(contact_data)
                failed_details += 1
                print("⚠️  Pas de détails")

            time.sleep(1)  # Respect API rate limits

        except KeyboardInterrupt:
            print("\n❌ Interrompu par l'utilisateur")
            break
        except Exception as e:
            failed_details += 1
            print(f"❌ Erreur: {str(e)[:30]}")

            # Keep basic info even if details fail
            try:
                contact_data = {
                    'name': place.get('name', '').strip() or 'N/A',
                    'address': place.get('formatted_address', '').strip() or 'N/A',
                    'place_id': place['place_id'],
                    'google_phone': '',
                    'website': '',
                    'rating': place.get('rating', ''),
                    'reviews': place.get('user_ratings_total', ''),
                    'type': determine_type(place),
                    'reservation_phone': '',
                    'email': ''
                }
                enriched_data.append(contact_data)
            except Exception:
                continue

            # Stop if too many failures
            if failed_details > max_failures:
                print(f"\n❌ Trop d'échecs ({failed_details}/{len(establishments)}), arrêt")
                break

    if failed_details > 0:
        print(f"\n⚠️  {failed_details}/{len(establishments)} établissements sans détails complets")

    # Scraping des sites web si demandé
    if scraper and not args.no_scrape:
        print("\n🌐 Scraping des sites web pour contacts...")

        sites_to_scrape = [data for data in enriched_data if data.get('website')]
        sites_without_website = len(enriched_data) - len(sites_to_scrape)

        if sites_without_website > 0:
            print(f"  {sites_without_website}/{len(enriched_data)} établissements sans site web")

        if not sites_to_scrape:
            print("  ❌ Aucun site web à scraper")
        else:
            scraping_failures = 0
            successful_scrapes = 0
            max_scraping_failures = len(sites_to_scrape) // 3  # Allow up to 33% failures

            for i, data in enumerate(enriched_data, 1):
                if not data.get('website'):
                    continue

                print(f"  {i}/{len(enriched_data)} - {data['name'][:30]}... ", end="")

                try:
                    contact_info = scraper.scrape_contact_info(data['website'])

                    # Update data with extracted information
                    contact_found = False
                    if contact_info.get('reservation_phone'):
                        data['reservation_phone'] = contact_info['reservation_phone']
                        contact_found = True

                    if contact_info.get('email'):
                        data['email'] = contact_info['email']
                        contact_found = True

                    if contact_found:
                        successful_scrapes += 1

                except KeyboardInterrupt:
                    print("\n❌ Scraping interrompu par l'utilisateur")
                    break
                except Exception as e:
                    scraping_failures += 1
                    print(f"❌ Erreur: {str(e)[:30]}")

                    # Stop if too many scraping failures
                    if scraping_failures > max_scraping_failures:
                        print(f"\n⚠️  Trop d'échecs de scraping ({scraping_failures}/{len(sites_to_scrape)})")
                        print("  Continuant sans scraping des sites restants...")
                        break

            # Summary of scraping results
            if sites_to_scrape:
                print(f"\n📊 Scraping terminé: {successful_scrapes} succès, {scraping_failures} échecs")

    # Validation finale des données
    if not enriched_data:
        print("❌ Aucune donnée à exporter")
        sys.exit(1)

    # Export des résultats
    print(f"\n📊 Export des résultats ({len(enriched_data)} entrées)...")

    try:
        # Validation des données avant export
        validation_errors = exporter.validate_data(enriched_data)
        if validation_errors:
            print("⚠️  Avertissements de validation:")
            for error in validation_errors[:5]:  # Show only first 5 errors
                print(f"  - {error}")
            if len(validation_errors) > 5:
                print(f"  ... et {len(validation_errors) - 5} autres erreurs")

        export_success = True

        if args.format in ["csv", "both"]:
            print("  Exportation CSV...", end=" ")
            csv_success = exporter.export_csv(enriched_data, f"{args.output}.csv")
            if not csv_success:
                export_success = False
                print("❌")
            else:
                print("✅")

        if args.format in ["json", "both"]:
            print("  Exportation JSON...", end=" ")
            json_success = exporter.export_json(enriched_data, f"{args.output}.json")
            if not json_success:
                export_success = False
                print("❌")
            else:
                print("✅")

        if not export_success:
            print("❌ Échec de l'export")
            sys.exit(1)

    except PermissionError:
        print("❌ Erreur de permissions - impossible d'écrire les fichiers")
        print("  Vérifiez les droits d'écriture dans le dossier courant")
        sys.exit(1)
    except OSError as e:
        print(f"❌ Erreur système d'export: {e}")
        print("  Vérifiez l'espace disque disponible")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur d'export inattendue: {e}")
        sys.exit(1)

    print(f"\n🎉 Prospection terminée avec succès!")
    print(f"📁 Fichiers générés: {args.output}.{args.format}")

    # Statistics summary
    stats_summary = []
    successful_places = sum(1 for d in enriched_data if d.get('google_phone') or d.get('website'))
    with_reservation_phone = sum(1 for d in enriched_data if d.get('reservation_phone'))
    with_email = sum(1 for d in enriched_data if d.get('email'))

    print(f"📊 Résumé:")
    print(f"  - {len(enriched_data)} établissements exportés")
    print(f"  - {successful_places} avec données Google complètes")
    if not args.no_scrape:
        print(f"  - {with_reservation_phone} avec téléphone réservation")
        print(f"  - {with_email} avec adresse email")


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