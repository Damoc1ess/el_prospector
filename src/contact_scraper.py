"""
Contact scraper for extracting reservation phone numbers and emails from websites.
"""

import re
import time
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict
try:
    from .phone_extractor import PhoneExtractor
except ImportError:
    from phone_extractor import PhoneExtractor


class ContactScraper:
    """Scraper for extracting contacts from websites."""

    def __init__(self):
        self.phone_extractor = PhoneExtractor()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.timeout = 10

        # Keywords to detect reservation phone numbers
        self.reservation_keywords = [
            'reservation', 'reservations', 'reserver',
            'booking', 'book now', 'book a table',
            'contact', 'call us', 'phone'
        ]

        # Email pattern
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def scrape_contact_info(self, website_url: str) -> Dict[str, Optional[str]]:
        """
        Scrape a website to extract reservation phone and email.

        Args:
            website_url: URL of the website to scrape

        Returns:
            Dict with 'reservation_phone' and 'email'
        """
        result = {
            'reservation_phone': None,
            'email': None
        }

        if not website_url or not website_url.strip():
            return result

        # Normalize URL
        try:
            if not website_url.startswith(('http://', 'https://')):
                website_url = 'https://' + website_url
        except Exception:
            print("ERROR: Invalid URL")
            return result

        try:
            # Download page with retry on certain errors
            response = self._download_page_with_retry(website_url)
            if not response:
                return result

            # Check content-type
            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' not in content_type and 'application/xml' not in content_type:
                print("ERROR: Non-HTML content")
                return result

            # Check response size
            if len(response.content) > 5_000_000:  # 5MB max
                print("ERROR: Page too large")
                return result

            # Parse HTML with error handling
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                print(f"ERROR: HTML parsing - {str(e)[:50]}")
                return result

            # Extract reservation phone
            try:
                raw_phone = self._extract_reservation_phone(soup, response.text)
                if raw_phone:
                    cleaned_phone = self.phone_extractor.clean_phone(raw_phone)
                    if cleaned_phone:
                        result['reservation_phone'] = cleaned_phone
            except Exception as e:
                print(f"ERROR: Phone extraction: {str(e)[:30]}")

            # Extract email
            try:
                extracted_email = self._extract_email(soup, response.text)
                if extracted_email:
                    result['email'] = extracted_email
            except Exception as e:
                print(f"ERROR: Email extraction: {str(e)[:30]}")

            print("OK" if result['reservation_phone'] or result['email'] else "No contact found")

        except requests.exceptions.Timeout:
            print("ERROR: Timeout (>10s)")
        except requests.exceptions.ConnectionError:
            print("ERROR: Connection failed")
        except requests.exceptions.HTTPError as e:
            status_code = getattr(e.response, 'status_code', 'Unknown')
            if status_code == 403:
                print("ERROR: Access forbidden (403)")
            elif status_code == 404:
                print("ERROR: Page not found (404)")
            elif status_code == 503:
                print("ERROR: Service unavailable (503)")
            else:
                print(f"ERROR: HTTP {status_code}")
        except requests.exceptions.TooManyRedirects:
            print("ERROR: Too many redirects")
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Network - {str(e)[:50]}")
        except Exception as e:
            print(f"ERROR: Unexpected - {str(e)[:50]}")

        # Sleep to avoid overloading servers
        time.sleep(2)

        return result

    def _download_page_with_retry(self, url: str, max_retries: int = 2):
        """Download a page with retry on certain errors."""
        for attempt in range(max_retries + 1):
            try:
                response = requests.get(
                    url,
                    headers=self.headers,
                    timeout=self.timeout,
                    allow_redirects=True,
                    verify=True  # Verify SSL certificates
                )

                # Check for specific retry-able status codes
                if response.status_code == 503 and attempt < max_retries:
                    print(f"  Service unavailable, retry {attempt + 1}/{max_retries}...", end=" ")
                    time.sleep(3)  # Wait before retry
                    continue
                elif response.status_code == 429 and attempt < max_retries:  # Rate limit
                    print(f"  Rate limit, retry {attempt + 1}/{max_retries}...", end=" ")
                    time.sleep(5)  # Wait longer for rate limits
                    continue

                response.raise_for_status()
                return response

            except requests.exceptions.Timeout as e:
                if attempt < max_retries:
                    print(f"  Timeout, retry {attempt + 1}/{max_retries}...", end=" ")
                    time.sleep(2)
                    continue
                else:
                    raise e
            except requests.exceptions.ConnectionError as e:
                if attempt < max_retries:
                    print(f"  Connection failed, retry {attempt + 1}/{max_retries}...", end=" ")
                    time.sleep(2)
                    continue
                else:
                    raise e

        return None

    def _extract_reservation_phone(self, soup: BeautifulSoup, html_text: str) -> Optional[str]:
        """Extract reservation phone number from HTML."""

        # 1. Search for tel: links as priority
        tel_links = soup.find_all('a', href=re.compile(r'^tel:'))
        if tel_links:
            for link in tel_links:
                phone = link['href'].replace('tel:', '').strip()
                cleaned_phone = self.phone_extractor.clean_phone(phone)
                if cleaned_phone:
                    return cleaned_phone

        # 2. Search for phone numbers near reservation keywords
        reservation_phone = self._find_phone_near_keywords(html_text)
        if reservation_phone:
            return reservation_phone

        # 3. Fallback: take the first French phone number found
        phones = self.phone_extractor.extract_phones(html_text)
        if phones:
            return phones[0]

        return None

    def _find_phone_near_keywords(self, text: str) -> Optional[str]:
        """Find a phone number near reservation keywords."""

        # Clean the text
        text_lower = text.lower()

        # For each reservation keyword
        for keyword in self.reservation_keywords:
            # Find all positions of the keyword
            keyword_positions = []
            start = 0
            while True:
                pos = text_lower.find(keyword, start)
                if pos == -1:
                    break
                keyword_positions.append(pos)
                start = pos + 1

            # For each keyword position
            for pos in keyword_positions:
                # Extract context around the keyword (200 characters before/after)
                start_context = max(0, pos - 200)
                end_context = min(len(text), pos + 200)
                context = text[start_context:end_context]

                # Search for phone numbers in this context
                phones = self.phone_extractor.extract_phones(context)
                if phones:
                    return phones[0]  # Take the first phone number found

        return None

    def _extract_email(self, soup: BeautifulSoup, html_text: str) -> Optional[str]:
        """Extract email address from HTML."""

        # 1. Search for mailto: links as priority
        mailto_links = soup.find_all('a', href=re.compile(r'^mailto:'))
        if mailto_links:
            email = mailto_links[0]['href'].replace('mailto:', '').strip()
            # Clean email (remove parameters like ?subject=...)
            email = email.split('?')[0]
            if self._is_valid_email(email):
                return email

        # 2. Search with regex in text
        emails = re.findall(self.email_pattern, html_text)

        # Filter valid emails and exclude generic ones
        valid_emails = []
        excluded_patterns = [
            'example.com', 'test.com', 'lorem', 'ipsum',
            'noreply', 'no-reply', 'admin@', 'webmaster@',
            'user@domain.com', 'email@example.com'
        ]

        for email in emails:
            email = email.lower()
            if self._is_valid_email(email):
                # Exclude generic emails
                if not any(pattern in email for pattern in excluded_patterns):
                    valid_emails.append(email)

        return valid_emails[0] if valid_emails else None

    def _is_valid_email(self, email: str) -> bool:
        """Check if email is valid."""
        if not email or len(email) > 254:
            return False

        return re.match(self.email_pattern, email) is not None


# For testing
if __name__ == "__main__":
    scraper = ContactScraper()

    # Test with an example site
    test_url = "https://example.com"
    result = scraper.scrape_contact_info(test_url)
    print(f"Result: {result}")
