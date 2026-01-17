"""
Google Places API client for hotel and restaurant prospecting.
"""

import os
import time
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GooglePlacesClient:
    """Client for Google Places API Text Search and Place Details."""

    BASE_URL = "https://places.googleapis.com/v1"

    def __init__(self):
        """Initialize client with API key from environment."""
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY must be set in environment or .env file")

    def search_places(self, city: str, place_type: str = "restaurant", limit: int = 20) -> List[Dict]:
        """
        Search for places in a city using Text Search API.

        Args:
            city: City name to search in
            place_type: Type of place ('restaurant', 'hotel', or 'all')
            limit: Maximum number of results to return

        Returns:
            List of place dictionaries with basic info
        """
        if place_type == "all":
            text_query = f"hotels and restaurants in {city}"
        else:
            text_query = f"{place_type}s in {city}"

        url = f"{self.BASE_URL}/places:searchText"

        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': self.api_key,
            'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.id,places.rating,places.userRatingCount'
        }

        payload = {
            'textQuery': text_query,
            'languageCode': 'fr',
            'maxResultCount': min(limit, 20)  # Max 20 per request
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

            places = data.get('places', [])

            # Transform to compatible format
            transformed_places = []
            for place in places:
                transformed_place = {
                    'place_id': place.get('id'),
                    'name': place.get('displayName', {}).get('text', 'Unknown'),
                    'formatted_address': place.get('formattedAddress', 'Unknown'),
                    'rating': place.get('rating'),
                    'user_ratings_total': place.get('userRatingCount', 0)
                }
                transformed_places.append(transformed_place)

            # Sleep to respect API rate limits
            time.sleep(1)

            return transformed_places

        except requests.RequestException as e:
            print(f"Error searching places: {e}")
            return []

    def get_place_details(self, place_id: str) -> Optional[Dict]:
        """
        Get detailed information for a place using Place Details API.

        Args:
            place_id: Google Places ID

        Returns:
            Dictionary with detailed place information or None if error
        """
        url = f"{self.BASE_URL}/places/{place_id}"

        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': self.api_key,
            'X-Goog-FieldMask': 'displayName,formattedAddress,nationalPhoneNumber,websiteUri,rating,userRatingCount'
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Transform to compatible format
            result = {
                'name': data.get('displayName', {}).get('text', 'Unknown'),
                'formatted_address': data.get('formattedAddress', 'Unknown'),
                'formatted_phone_number': data.get('nationalPhoneNumber'),
                'website': data.get('websiteUri'),
                'rating': data.get('rating'),
                'user_ratings_total': data.get('userRatingCount', 0)
            }

            # Sleep to respect API rate limits
            time.sleep(1)
            return result

        except requests.RequestException as e:
            print(f"Error getting place details: {e}")
            return None

    def test_connection(self) -> bool:
        """
        Test the connection to Google Places API.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Test 1: Search places
            print("Testing Text Search API...")
            test_places = self.search_places("Paris", "restaurant", 2)
            if not test_places:
                print("✗ Google Places Text Search returned no results")
                return False

            print(f"✓ Text Search successful - Found {len(test_places)} places")
            print(f"  Example: {test_places[0]['name']} - {test_places[0]['formatted_address']}")

            # Test 2: Place Details
            print("\nTesting Place Details API...")
            place_id = test_places[0]['place_id']
            details = self.get_place_details(place_id)
            if not details:
                print("✗ Place Details API failed")
                return False

            print("✓ Place Details successful")
            print(f"  Name: {details.get('name')}")
            print(f"  Phone: {details.get('formatted_phone_number', 'N/A')}")
            print(f"  Website: {details.get('website', 'N/A')}")
            print(f"  Rating: {details.get('rating', 'N/A')}")

            return True

        except Exception as e:
            print(f"✗ Google Places API connection failed: {e}")
            return False


if __name__ == "__main__":
    # Quick test of the client
    client = GooglePlacesClient()
    success = client.test_connection()

    if success:
        print("\n=== Google Places Client Ready ===")
    else:
        print("\n=== Google Places Client Failed ===")
        print("Check your GOOGLE_MAPS_API_KEY in .env file")