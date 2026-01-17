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

    BASE_URL = "https://maps.googleapis.com/maps/api/place"

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
            query = f"hotels and restaurants in {city}"
        else:
            query = f"{place_type}s in {city}"

        url = f"{self.BASE_URL}/textsearch/json"
        params = {
            'query': query,
            'key': self.api_key,
            'language': 'fr'
        }

        places = []
        next_page_token = None

        while len(places) < limit:
            if next_page_token:
                params['pagetoken'] = next_page_token
                # Wait 2 seconds before next page request (Google requirement)
                time.sleep(2)

            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                if data['status'] != 'OK':
                    print(f"Google API error: {data.get('status')} - {data.get('error_message', '')}")
                    break

                # Add places from this page
                page_places = data.get('results', [])
                places.extend(page_places[:limit - len(places)])

                # Check if we have more pages and need more results
                next_page_token = data.get('next_page_token')
                if not next_page_token or len(places) >= limit:
                    break

            except requests.RequestException as e:
                print(f"Error searching places: {e}")
                break

        # Sleep to respect API rate limits
        time.sleep(1)

        return places[:limit]

    def get_place_details(self, place_id: str) -> Optional[Dict]:
        """
        Get detailed information for a place using Place Details API.

        Args:
            place_id: Google Places ID

        Returns:
            Dictionary with detailed place information or None if error
        """
        url = f"{self.BASE_URL}/details/json"
        params = {
            'place_id': place_id,
            'fields': 'name,formatted_address,formatted_phone_number,website,rating,user_ratings_total',
            'key': self.api_key,
            'language': 'fr'
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data['status'] == 'OK':
                # Sleep to respect API rate limits
                time.sleep(1)
                return data['result']
            else:
                print(f"Place details error: {data.get('status')} - {data.get('error_message', '')}")
                return None

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
            # Simple test search
            test_places = self.search_places("Paris", "restaurant", 1)
            if test_places:
                print(f"✓ Google Places API connection successful")
                print(f"  Test result: {test_places[0]['name']}")
                return True
            else:
                print("✗ Google Places API returned no results")
                return False

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