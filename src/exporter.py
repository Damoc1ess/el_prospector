#!/usr/bin/env python3
"""
Exporter - Export des données de prospection en CSV et JSON
"""

import csv
import json
from typing import List, Dict, Any
from pathlib import Path


class Exporter:
    """Classe pour exporter les données de prospection en CSV et JSON"""

    def __init__(self):
        self.csv_headers = [
            'name',
            'address',
            'google_phone',
            'reservation_phone',
            'email',
            'website',
            'rating',
            'reviews',
            'type'
        ]

    def export_csv(self, data: List[Dict[str, Any]], filename: str) -> bool:
        """
        Exporte les données au format CSV

        Args:
            data: Liste des établissements avec leurs infos
            filename: Nom du fichier de sortie (avec .csv)

        Returns:
            bool: True si l'export a réussi
        """
        try:
            filepath = Path(filename)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.csv_headers)
                writer.writeheader()

                for item in data:
                    # Préparation des données avec valeurs par défaut
                    row = {}
                    for header in self.csv_headers:
                        value = item.get(header, '')

                        # Conversion des valeurs spéciales
                        if header == 'rating' and value:
                            row[header] = f"{value:.1f}"
                        elif header == 'reviews' and value:
                            row[header] = str(value)
                        else:
                            row[header] = str(value) if value else ''

                    writer.writerow(row)

            print(f"✅ Export CSV réussi: {filename} ({len(data)} entrées)")
            return True

        except Exception as e:
            print(f"❌ Erreur export CSV: {e}")
            return False

    def export_json(self, data: List[Dict[str, Any]], filename: str) -> bool:
        """
        Exporte les données au format JSON

        Args:
            data: Liste des établissements avec leurs infos
            filename: Nom du fichier de sortie (avec .json)

        Returns:
            bool: True si l'export a réussi
        """
        try:
            filepath = Path(filename)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # Préparation des données JSON avec métadonnées
            json_data = {
                "metadata": {
                    "total_count": len(data),
                    "export_timestamp": None,  # Sera ajouté par le CLI
                    "export_type": "prospection_hotels_restaurants"
                },
                "establishments": data
            }

            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(json_data, jsonfile, ensure_ascii=False, indent=2)

            print(f"✅ Export JSON réussi: {filename} ({len(data)} entrées)")
            return True

        except Exception as e:
            print(f"❌ Erreur export JSON: {e}")
            return False

    def export_both(self, data: List[Dict[str, Any]], base_filename: str) -> Dict[str, bool]:
        """
        Exporte les données en CSV et JSON

        Args:
            data: Liste des établissements avec leurs infos
            base_filename: Nom de base sans extension

        Returns:
            dict: Status des exports {"csv": bool, "json": bool}
        """
        csv_file = f"{base_filename}.csv"
        json_file = f"{base_filename}.json"

        results = {
            "csv": self.export_csv(data, csv_file),
            "json": self.export_json(data, json_file)
        }

        return results

    def validate_data(self, data: List[Dict[str, Any]]) -> List[str]:
        """
        Valide les données avant export

        Args:
            data: Liste des établissements

        Returns:
            list: Liste des erreurs de validation (vide si OK)
        """
        errors = []

        if not data:
            errors.append("Aucune donnée à exporter")
            return errors

        required_fields = ['name', 'place_id']

        for i, item in enumerate(data):
            for field in required_fields:
                if not item.get(field):
                    errors.append(f"Entrée {i+1}: champ '{field}' manquant")

        return errors


def demo_export():
    """Fonction de test pour l'exporteur"""

    # Données de test
    test_data = [
        {
            'name': 'Le Petit Bistro',
            'address': '12 rue de la Paix, 75001 Paris',
            'google_phone': '+33 1 23 45 67 89',
            'reservation_phone': '+33 1 98 76 54 32',
            'email': 'contact@petitbistro.fr',
            'website': 'https://petitbistro.fr',
            'rating': 4.5,
            'reviews': 120,
            'type': 'restaurant',
            'place_id': 'ChIJAQAAAAAAAA'
        },
        {
            'name': 'Hotel Royal',
            'address': '5 avenue des Champs, 75008 Paris',
            'google_phone': '+33 4 56 78 90 12',
            'reservation_phone': '+33 4 00 00 00 00',
            'email': '',
            'website': 'https://hotelroyal.fr',
            'rating': 4.2,
            'reviews': 89,
            'type': 'hotel',
            'place_id': 'ChIJBBBBBBBBBB'
        }
    ]

    exporter = Exporter()

    print("🧪 Test de l'exporteur...")

    # Validation des données
    errors = exporter.validate_data(test_data)
    if errors:
        print("❌ Erreurs de validation:")
        for error in errors:
            print(f"  - {error}")
        return False

    # Test export CSV
    csv_success = exporter.export_csv(test_data, "test_export.csv")

    # Test export JSON
    json_success = exporter.export_json(test_data, "test_export.json")

    # Test export both
    both_results = exporter.export_both(test_data, "test_combined")

    print(f"📊 Résultats:")
    print(f"  CSV: {'✅' if csv_success else '❌'}")
    print(f"  JSON: {'✅' if json_success else '❌'}")
    print(f"  Both: CSV={'✅' if both_results['csv'] else '❌'}, JSON={'✅' if both_results['json'] else '❌'}")

    return csv_success and json_success and all(both_results.values())


if __name__ == "__main__":
    demo_export()