#!/usr/bin/env python3
"""
Test du scraper sur 3 sites réels de restaurants parisiens.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from contact_scraper import ContactScraper

def test_real_websites():
    """Test le scraper sur 3 sites réels de restaurants parisiens."""

    # Sites de test - restaurants parisiens connus
    test_sites = [
        {
            'name': 'L\'Ami Jean',
            'url': 'http://lamijean.fr',
            'type': 'restaurant'
        },
        {
            'name': 'Le Comptoir du Relais',
            'url': 'https://hotel-paris-relais-saint-germain.com/fr/restaurant/',
            'type': 'restaurant'
        },
        {
            'name': 'Breizh Café',
            'url': 'https://breizhcafe.com',
            'type': 'restaurant'
        }
    ]

    scraper = ContactScraper()
    results = []

    print("=== TEST DU SCRAPER SUR 3 SITES RÉELS ===\n")

    for i, site in enumerate(test_sites, 1):
        print(f"Test {i}/3 - {site['name']}")
        print(f"URL: {site['url']}")
        print("-" * 50)

        # Scraper le site
        result = scraper.scrape_contact_info(site['url'])

        # Afficher les résultats
        print(f"Numéro de réservation: {result['reservation_phone'] or 'Non trouvé'}")
        print(f"Email: {result['email'] or 'Non trouvé'}")

        # Stocker pour le résumé
        results.append({
            'name': site['name'],
            'url': site['url'],
            'reservation_phone': result['reservation_phone'],
            'email': result['email'],
            'success': result['reservation_phone'] is not None or result['email'] is not None
        })

        print("\n" + "="*60 + "\n")

    # Résumé des résultats
    print("=== RÉSUMÉ DES TESTS ===")
    successful_tests = sum(1 for r in results if r['success'])

    for result in results:
        status = "✓ SUCCESS" if result['success'] else "✗ ECHEC"
        print(f"{status} - {result['name']}")
        if result['reservation_phone']:
            print(f"  📞 Téléphone: {result['reservation_phone']}")
        if result['email']:
            print(f"  📧 Email: {result['email']}")
        print()

    print(f"Résultats: {successful_tests}/3 sites ont retourné des informations")

    # Critère de succès : au moins 2/3 sites doivent retourner des infos
    if successful_tests >= 2:
        print("✅ TEST GLOBAL RÉUSSI - Le scraper fonctionne correctement")
        return True
    else:
        print("❌ TEST GLOBAL ÉCHOUÉ - Le scraper nécessite des améliorations")
        return False

if __name__ == "__main__":
    success = test_real_websites()
    sys.exit(0 if success else 1)