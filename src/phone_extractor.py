#!/usr/bin/env python3
"""
French phone number extraction and formatting module.

Supported formats:
- +33 X XX XX XX XX
- 0X XX XX XX XX
- 0X.XX.XX.XX.XX
- 0X-XX-XX-XX-XX
- 0123456789
"""

import re
from typing import List, Optional


class PhoneExtractor:
    """French phone number extractor."""

    # Regex pattern for French phone numbers
    PHONE_PATTERN = r'(?:\+33|0)\s*[1-9](?:[\s.-]*\d{2}){4}'

    # Keywords to detect reservation phone numbers
    RESERVATION_KEYWORDS = [
        'reservation', 'reservations', 'reserver',
        'booking', 'book now', 'book a table', 'book',
        'contact', 'contactez',
        'tel', 'telephone', 'phone',
        'call us', 'call'
    ]

    def __init__(self):
        self.phone_regex = re.compile(self.PHONE_PATTERN, re.IGNORECASE)

    def extract_phones(self, text: str) -> List[str]:
        """
        Extract all French phone numbers from text.

        Args:
            text: Text to analyze

        Returns:
            List of found phone numbers (raw)
        """
        if not text:
            return []

        phones = self.phone_regex.findall(text)
        return phones

    def clean_phone(self, phone: str) -> str:
        """
        Clean and format a phone number.

        Args:
            phone: Raw phone number

        Returns:
            Cleaned phone number in format +33 X XX XX XX XX
        """
        if not phone:
            return ""

        # Remove all non-numeric characters except +
        cleaned = re.sub(r'[^\d+]', '', phone)

        # Convert 0X to +33X
        if cleaned.startswith('0'):
            cleaned = '+33' + cleaned[1:]

        # Check that number starts with +33
        if not cleaned.startswith('+33'):
            return ""

        # Check length (must be +33XXXXXXXXX = 12 characters)
        if len(cleaned) != 12:
            return ""

        # Format: +33 X XX XX XX XX
        formatted = f"+33 {cleaned[3]} {cleaned[4:6]} {cleaned[6:8]} {cleaned[8:10]} {cleaned[10:12]}"

        return formatted

    def find_reservation_phone(self, html_content: str, tel_links: List[str] = None) -> Optional[str]:
        """
        Find the most likely phone number for reservations.

        Logic:
        1. Search in tel: links if provided
        2. Search for phone numbers near "reservation", "booking" keywords
        3. Otherwise take the first valid phone number on the page

        Args:
            html_content: HTML content of the page
            tel_links: List of phone numbers found in tel: links (optional)

        Returns:
            Formatted reservation phone number or None
        """
        # 1. Priority to tel: links if they exist
        if tel_links:
            for tel_phone in tel_links:
                cleaned = self.clean_phone(tel_phone)
                if cleaned:
                    return cleaned

        # 2. Search for phone numbers near reservation keywords
        reservation_phone = self._find_phone_near_keywords(html_content)
        if reservation_phone:
            return reservation_phone

        # 3. Fallback: first valid phone number on the page
        all_phones = self.extract_phones(html_content)
        for phone in all_phones:
            cleaned = self.clean_phone(phone)
            if cleaned:
                return cleaned

        return None

    def _find_phone_near_keywords(self, text: str) -> Optional[str]:
        """
        Search for a phone number near reservation keywords.

        Args:
            text: Text to analyze

        Returns:
            Formatted phone number or None
        """
        text_lower = text.lower()

        # For each keyword, search for phone numbers within 200 characters
        for keyword in self.RESERVATION_KEYWORDS:
            keyword_positions = []
            start = 0

            # Find all occurrences of the keyword
            while True:
                pos = text_lower.find(keyword, start)
                if pos == -1:
                    break
                keyword_positions.append(pos)
                start = pos + 1

            # For each occurrence, search for phone numbers around it
            for pos in keyword_positions:
                # Analysis zone: 200 characters before and after the keyword
                start_range = max(0, pos - 200)
                end_range = min(len(text), pos + len(keyword) + 200)
                context = text[start_range:end_range]

                # Search for phone numbers in this zone
                phones = self.extract_phones(context)
                for phone in phones:
                    cleaned = self.clean_phone(phone)
                    if cleaned:
                        return cleaned

        return None


def test_phone_extraction():
    """Unit tests for phone number extraction."""
    extractor = PhoneExtractor()

    test_cases = [
        "+33 1 23 45 67 89",
        "01 23 45 67 89",
        "01.23.45.67.89",
        "01-23-45-67-89",
        "0123456789",
        "+33123456789",
        "Call 01 23 45 67 89 to book",
        "Reservation: 06 12 34 56 78",
        "Tel: +33 4 56 78 90 12",
        "Invalid number: 123",
        "Contact: 01 23 45 67 89 or email@test.fr"
    ]

    print("=== Phone Number Extraction Test ===")
    for i, text in enumerate(test_cases, 1):
        phones = extractor.extract_phones(text)
        print(f"Test {i}: '{text}'")
        print(f"  Found: {phones}")

        for phone in phones:
            cleaned = extractor.clean_phone(phone)
            print(f"  Cleaned: '{phone}' -> '{cleaned}'")
        print()


if __name__ == "__main__":
    test_phone_extraction()
