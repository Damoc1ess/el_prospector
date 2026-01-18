#!/usr/bin/env python3
"""
Exporter - Export prospecting data to CSV and JSON
"""

import csv
import json
from typing import List, Dict, Any
from pathlib import Path


class Exporter:
    """Class to export prospecting data to CSV and JSON"""

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
        Export data to CSV format

        Args:
            data: List of establishments with their info
            filename: Output filename (with .csv)

        Returns:
            bool: True if export succeeded
        """
        try:
            filepath = Path(filename)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.csv_headers)
                writer.writeheader()

                for item in data:
                    # Prepare data with default values
                    row = {}
                    for header in self.csv_headers:
                        value = item.get(header, '')

                        # Convert special values
                        if header == 'rating' and value:
                            row[header] = f"{value:.1f}"
                        elif header == 'reviews' and value:
                            row[header] = str(value)
                        else:
                            row[header] = str(value) if value else ''

                    writer.writerow(row)

            print(f"OK: CSV export successful: {filename} ({len(data)} entries)")
            return True

        except Exception as e:
            print(f"ERROR: CSV export failed: {e}")
            return False

    def export_json(self, data: List[Dict[str, Any]], filename: str) -> bool:
        """
        Export data to JSON format

        Args:
            data: List of establishments with their info
            filename: Output filename (with .json)

        Returns:
            bool: True if export succeeded
        """
        try:
            filepath = Path(filename)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # Prepare JSON data with metadata
            json_data = {
                "metadata": {
                    "total_count": len(data),
                    "export_timestamp": None,  # Will be added by CLI
                    "export_type": "prospection_hotels_restaurants"
                },
                "establishments": data
            }

            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(json_data, jsonfile, ensure_ascii=False, indent=2)

            print(f"OK: JSON export successful: {filename} ({len(data)} entries)")
            return True

        except Exception as e:
            print(f"ERROR: JSON export failed: {e}")
            return False

    def export_both(self, data: List[Dict[str, Any]], base_filename: str) -> Dict[str, bool]:
        """
        Export data to both CSV and JSON

        Args:
            data: List of establishments with their info
            base_filename: Base filename without extension

        Returns:
            dict: Export status {"csv": bool, "json": bool}
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
        Validate data before export

        Args:
            data: List of establishments

        Returns:
            list: List of validation errors (empty if OK)
        """
        errors = []

        if not data:
            errors.append("No data to export")
            return errors

        required_fields = ['name', 'place_id']

        for i, item in enumerate(data):
            for field in required_fields:
                if not item.get(field):
                    errors.append(f"Entry {i+1}: missing field '{field}'")

        return errors


def demo_export():
    """Test function for the exporter"""

    # Test data
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

    print("Testing exporter...")

    # Validate data
    errors = exporter.validate_data(test_data)
    if errors:
        print("ERROR: Validation errors:")
        for error in errors:
            print(f"  - {error}")
        return False

    # Test CSV export
    csv_success = exporter.export_csv(test_data, "test_export.csv")

    # Test JSON export
    json_success = exporter.export_json(test_data, "test_export.json")

    # Test both export
    both_results = exporter.export_both(test_data, "test_combined")

    print(f"Results:")
    print(f"  CSV: {'OK' if csv_success else 'FAILED'}")
    print(f"  JSON: {'OK' if json_success else 'FAILED'}")
    print(f"  Both: CSV={'OK' if both_results['csv'] else 'FAILED'}, JSON={'OK' if both_results['json'] else 'FAILED'}")

    return csv_success and json_success and all(both_results.values())


if __name__ == "__main__":
    demo_export()
