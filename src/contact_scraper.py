"""
Contact scraper pour extraire numeros de reservation et emails depuis les sites web.
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
    """Scraper pour extraire les contacts depuis les sites web."""

    def __init__(self):
        self.phone_extractor = PhoneExtractor()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.timeout = 10

        # Mots-clés pour détecter les numéros de réservation
        self.reservation_keywords = [
            'reservation', 'réservation', 'réserver', 'reserver',
            'booking', 'book now', 'book a table', 'réserver une table',
            'contact', 'nous contacter', 'appelez', 'call us'
        ]

        # Pattern pour emails
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def scrape_contact_info(self, website_url: str) -> Dict[str, Optional[str]]:
        """
        Scrape un site web pour extraire numero de reservation et email.

        Args:
            website_url: URL du site web à scraper

        Returns:
            Dict avec 'reservation_phone' et 'email'
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
            print("ERREUR: URL invalide")
            return result

        try:
            # Télécharger la page avec retry sur certaines erreurs
            response = self._download_page_with_retry(website_url)
            if not response:
                return result

            # Vérifier le content-type
            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' not in content_type and 'application/xml' not in content_type:
                print("ERREUR: contenu non HTML")
                return result

            # Vérifier la taille de la réponse
            if len(response.content) > 5_000_000:  # 5MB max
                print("ERREUR: page trop volumineuse")
                return result

            # Parser le HTML avec gestion d'erreurs
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                print(f"ERREUR: parsing HTML - {str(e)[:50]}")
                return result

            # Extraire le numéro de réservation
            try:
                raw_phone = self._extract_reservation_phone(soup, response.text)
                if raw_phone:
                    cleaned_phone = self.phone_extractor.clean_phone(raw_phone)
                    if cleaned_phone:
                        result['reservation_phone'] = cleaned_phone
            except Exception as e:
                print(f"ERREUR extraction téléphone: {str(e)[:30]}")

            # Extraire l'email
            try:
                extracted_email = self._extract_email(soup, response.text)
                if extracted_email:
                    result['email'] = extracted_email
            except Exception as e:
                print(f"ERREUR extraction email: {str(e)[:30]}")

            print("OK" if result['reservation_phone'] or result['email'] else "Aucun contact trouvé")

        except requests.exceptions.Timeout:
            print("ERREUR: timeout (>10s)")
        except requests.exceptions.ConnectionError:
            print("ERREUR: connexion impossible")
        except requests.exceptions.HTTPError as e:
            status_code = getattr(e.response, 'status_code', 'Unknown')
            if status_code == 403:
                print("ERREUR: accès interdit (403)")
            elif status_code == 404:
                print("ERREUR: page non trouvée (404)")
            elif status_code == 503:
                print("ERREUR: service indisponible (503)")
            else:
                print(f"ERREUR: HTTP {status_code}")
        except requests.exceptions.TooManyRedirects:
            print("ERREUR: trop de redirections")
        except requests.exceptions.RequestException as e:
            print(f"ERREUR: réseau - {str(e)[:50]}")
        except Exception as e:
            print(f"ERREUR: inattendue - {str(e)[:50]}")

        # Sleep pour éviter de surcharger les serveurs
        time.sleep(2)

        return result

    def _download_page_with_retry(self, url: str, max_retries: int = 2):
        """Télécharge une page avec retry sur certaines erreurs."""
        for attempt in range(max_retries + 1):
            try:
                response = requests.get(
                    url,
                    headers=self.headers,
                    timeout=self.timeout,
                    allow_redirects=True,
                    verify=True  # Vérifier les certificats SSL
                )

                # Check for specific retry-able status codes
                if response.status_code == 503 and attempt < max_retries:
                    print(f"  Service indisponible, retry {attempt + 1}/{max_retries}...", end=" ")
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
                    print(f"  Connexion échouée, retry {attempt + 1}/{max_retries}...", end=" ")
                    time.sleep(2)
                    continue
                else:
                    raise e

        return None

    def _extract_reservation_phone(self, soup: BeautifulSoup, html_text: str) -> Optional[str]:
        """Extraire le numéro de réservation du HTML."""

        # 1. Chercher les liens tel: en priorité
        tel_links = soup.find_all('a', href=re.compile(r'^tel:'))
        if tel_links:
            for link in tel_links:
                phone = link['href'].replace('tel:', '').strip()
                cleaned_phone = self.phone_extractor.clean_phone(phone)
                if cleaned_phone:
                    return cleaned_phone

        # 2. Chercher les numéros près des mots-clés de réservation
        reservation_phone = self._find_phone_near_keywords(html_text)
        if reservation_phone:
            return reservation_phone

        # 3. Fallback: prendre le premier numéro français trouvé
        phones = self.phone_extractor.extract_phones(html_text)
        if phones:
            return phones[0]

        return None

    def _find_phone_near_keywords(self, text: str) -> Optional[str]:
        """Trouver un numéro de téléphone près des mots-clés de réservation."""

        # Nettoyer le texte
        text_lower = text.lower()

        # Pour chaque mot-clé de réservation
        for keyword in self.reservation_keywords:
            # Trouver toutes les positions du mot-clé
            keyword_positions = []
            start = 0
            while True:
                pos = text_lower.find(keyword, start)
                if pos == -1:
                    break
                keyword_positions.append(pos)
                start = pos + 1

            # Pour chaque position de mot-clé
            for pos in keyword_positions:
                # Extraire un contexte autour du mot-clé (200 caractères avant/après)
                start_context = max(0, pos - 200)
                end_context = min(len(text), pos + 200)
                context = text[start_context:end_context]

                # Chercher des numéros dans ce contexte
                phones = self.phone_extractor.extract_phones(context)
                if phones:
                    return phones[0]  # Prendre le premier numéro trouvé

        return None

    def _extract_email(self, soup: BeautifulSoup, html_text: str) -> Optional[str]:
        """Extraire l'adresse email du HTML."""

        # 1. Chercher les liens mailto: en priorité
        mailto_links = soup.find_all('a', href=re.compile(r'^mailto:'))
        if mailto_links:
            email = mailto_links[0]['href'].replace('mailto:', '').strip()
            # Nettoyer l'email (enlever les paramètres comme ?subject=...)
            email = email.split('?')[0]
            if self._is_valid_email(email):
                return email

        # 2. Chercher avec regex dans le texte
        emails = re.findall(self.email_pattern, html_text)

        # Filtrer les emails valides et exclure les emails génériques
        valid_emails = []
        excluded_patterns = [
            'example.com', 'test.com', 'lorem', 'ipsum',
            'noreply', 'no-reply', 'admin@', 'webmaster@',
            'utilisateur@domaine.com', 'user@domain.com',
            'contact@exemple.com', 'email@exemple.fr'
        ]

        for email in emails:
            email = email.lower()
            if self._is_valid_email(email):
                # Exclure les emails génériques
                if not any(pattern in email for pattern in excluded_patterns):
                    valid_emails.append(email)

        return valid_emails[0] if valid_emails else None

    def _is_valid_email(self, email: str) -> bool:
        """Vérifier si l'email est valide."""
        if not email or len(email) > 254:
            return False

        return re.match(self.email_pattern, email) is not None


# Pour les tests
if __name__ == "__main__":
    scraper = ContactScraper()

    # Test avec un site exemple
    test_url = "https://example.com"
    result = scraper.scrape_contact_info(test_url)
    print(f"Résultat: {result}")