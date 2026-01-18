#!/usr/bin/env python3
"""
Main CLI for hotel and restaurant prospecting.
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
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Hotel/restaurant prospecting tool with contact extraction"
    )

    parser.add_argument(
        "--city",
        required=True,
        help="City to prospect (e.g., Paris, Lyon)"
    )

    parser.add_argument(
        "--type",
        choices=["hotel", "restaurant", "all"],
        default="all",
        help="Establishment type (default: all)"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of results (default: 20)"
    )

    parser.add_argument(
        "--no-scrape",
        action="store_true",
        help="Disable website scraping (faster)"
    )

    parser.add_argument(
        "--output",
        default="prospection",
        help="Output filename without extension (default: prospection)"
    )

    parser.add_argument(
        "--format",
        choices=["csv", "json", "both"],
        default="csv",
        help="Export format (default: csv)"
    )

    args = parser.parse_args()

    # Initialize clients
    print(f"Searching for establishments in {args.city}...")

    try:
        google_client = GooglePlacesClient()
        scraper = ContactScraper() if not args.no_scrape else None
        exporter = Exporter()

        # Validate arguments
        if args.limit <= 0:
            print(f"ERROR: Invalid limit: {args.limit} (must be > 0)")
            sys.exit(1)
        elif args.limit > 500:
            print(f"WARNING: Very high limit: {args.limit}, this may take a while")

    except ValueError as e:
        if "GOOGLE_MAPS_API_KEY" in str(e):
            print("ERROR: Missing Google API key")
            print("  Create a .env file with GOOGLE_MAPS_API_KEY=your_key")
            sys.exit(1)
        else:
            print(f"ERROR: Configuration error: {e}")
            sys.exit(1)
    except Exception as e:
        print(f"ERROR: Unexpected initialization error: {e}")
        sys.exit(1)

    # Google Places search
    try:
        establishments = search_establishments(
            google_client,
            args.city,
            args.type,
            args.limit
        )

        if not establishments:
            print(f"ERROR: No establishments found for {args.city}")
            print(f"  Check the spelling of '{args.city}' or try a more well-known city")
            sys.exit(1)

        print(f"OK: {len(establishments)} establishments found")

    except ValueError as e:
        print(f"ERROR: Search parameter error: {e}")
        sys.exit(1)
    except requests.RequestException as e:
        print(f"ERROR: Google Places connection error: {e}")
        print("  Check your internet connection and API key")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Unexpected search error: {e}")
        sys.exit(1)

    # Enrich with Google details
    print("Fetching details...")
    enriched_data = []
    failed_details = 0
    max_failures = len(establishments) // 2  # Allow up to 50% failures

    for i, place in enumerate(establishments, 1):
        place_name = place.get('name', 'N/A')
        print(f"  {i}/{len(establishments)} - {place_name}...", end=" ")

        try:
            details = google_client.get_place_details(place['place_id'])

            if details:
                # Base data with validation
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
                print("OK")
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
                print("WARNING: No details")

            time.sleep(1)  # Respect API rate limits

        except KeyboardInterrupt:
            print("\nERROR: Interrupted by user")
            break
        except Exception as e:
            failed_details += 1
            print(f"ERROR: {str(e)[:30]}")

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
                print(f"\nERROR: Too many failures ({failed_details}/{len(establishments)}), stopping")
                break

    if failed_details > 0:
        print(f"\nWARNING: {failed_details}/{len(establishments)} establishments without complete details")

    # Scrape websites if requested
    if scraper and not args.no_scrape:
        print("\nScraping websites for contacts...")

        sites_to_scrape = [data for data in enriched_data if data.get('website')]
        sites_without_website = len(enriched_data) - len(sites_to_scrape)

        if sites_without_website > 0:
            print(f"  {sites_without_website}/{len(enriched_data)} establishments without website")

        if not sites_to_scrape:
            print("  ERROR: No websites to scrape")
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
                    print("\nERROR: Scraping interrupted by user")
                    break
                except Exception as e:
                    scraping_failures += 1
                    print(f"ERROR: {str(e)[:30]}")

                    # Stop if too many scraping failures
                    if scraping_failures > max_scraping_failures:
                        print(f"\nWARNING: Too many scraping failures ({scraping_failures}/{len(sites_to_scrape)})")
                        print("  Continuing without scraping remaining sites...")
                        break

            # Summary of scraping results
            if sites_to_scrape:
                print(f"\nScraping complete: {successful_scrapes} successful, {scraping_failures} failed")

    # Final data validation
    if not enriched_data:
        print("ERROR: No data to export")
        sys.exit(1)

    # Export results
    print(f"\nExporting results ({len(enriched_data)} entries)...")

    try:
        # Validate data before export
        validation_errors = exporter.validate_data(enriched_data)
        if validation_errors:
            print("WARNING: Validation warnings:")
            for error in validation_errors[:5]:  # Show only first 5 errors
                print(f"  - {error}")
            if len(validation_errors) > 5:
                print(f"  ... and {len(validation_errors) - 5} more errors")

        export_success = True

        if args.format in ["csv", "both"]:
            print("  Exporting CSV...", end=" ")
            csv_success = exporter.export_csv(enriched_data, f"{args.output}.csv")
            if not csv_success:
                export_success = False
                print("FAILED")
            else:
                print("OK")

        if args.format in ["json", "both"]:
            print("  Exporting JSON...", end=" ")
            json_success = exporter.export_json(enriched_data, f"{args.output}.json")
            if not json_success:
                export_success = False
                print("FAILED")
            else:
                print("OK")

        if not export_success:
            print("ERROR: Export failed")
            sys.exit(1)

    except PermissionError:
        print("ERROR: Permission error - cannot write files")
        print("  Check write permissions in the current folder")
        sys.exit(1)
    except OSError as e:
        print(f"ERROR: System export error: {e}")
        print("  Check available disk space")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Unexpected export error: {e}")
        sys.exit(1)

    print(f"\nProspecting completed successfully!")
    print(f"Generated files: {args.output}.{args.format}")

    # Statistics summary
    stats_summary = []
    successful_places = sum(1 for d in enriched_data if d.get('google_phone') or d.get('website'))
    with_reservation_phone = sum(1 for d in enriched_data if d.get('reservation_phone'))
    with_email = sum(1 for d in enriched_data if d.get('email'))

    print(f"Summary:")
    print(f"  - {len(enriched_data)} establishments exported")
    print(f"  - {successful_places} with complete Google data")
    if not args.no_scrape:
        print(f"  - {with_reservation_phone} with reservation phone")
        print(f"  - {with_email} with email address")


def search_establishments(client: GooglePlacesClient, city: str, establishment_type: str, limit: int) -> List[Dict]:
    """Search for establishments via Google Places."""
    results = []

    if establishment_type == "all":
        types_to_search = ["restaurant", "hotel"]
    else:
        types_to_search = [establishment_type]

    for search_type in types_to_search:
        query = f"{search_type} in {city}"

        try:
            places = client.search_places(city, search_type)

            # Limit results
            type_limit = limit // len(types_to_search) if establishment_type == "all" else limit
            results.extend(places[:type_limit])

            time.sleep(1)  # Rate limiting

        except Exception as e:
            print(f"WARNING: Search error for {search_type}: {e}")
            continue

    return results[:limit]


def determine_type(place: Dict) -> str:
    """Determine establishment type from search context."""
    # For now, we use the search type rather than Google types
    # because Google Places v1 data doesn't return detailed types
    name = place.get('name', '').lower()
    address = place.get('formatted_address', '').lower()

    # Hotel keywords
    hotel_keywords = ['hotel', 'auberge', 'gite', 'chambre', 'suite', 'resort']
    if any(keyword in name for keyword in hotel_keywords):
        return 'hotel'

    # Restaurant keywords
    restaurant_keywords = ['restaurant', 'bistro', 'brasserie', 'cafe', 'pizzeria', 'bar', 'bouillon']
    if any(keyword in name for keyword in restaurant_keywords):
        return 'restaurant'

    # Default to restaurant if ambiguous
    return 'restaurant'


if __name__ == "__main__":
    main()
