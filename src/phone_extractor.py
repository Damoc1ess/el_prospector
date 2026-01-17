#!/usr/bin/env python3
"""
Module d'extraction et formatage des numéros de téléphone français.

Formats supportés :
- +33 X XX XX XX XX
- 0X XX XX XX XX
- 0X.XX.XX.XX.XX
- 0X-XX-XX-XX-XX
- 0123456789
"""

import re
from typing import List, Optional


class PhoneExtractor:
    """Extracteur de numéros de téléphone français."""

    # Pattern regex pour numéros français
    PHONE_PATTERN = r'(?:\+33|0)\s*[1-9](?:[\s.-]*\d{2}){4}'

    # Mots-clés pour détecter les numéros de réservation
    RESERVATION_KEYWORDS = [
        'reservation', 'reservations', 'reserver', 'réserver', 'réservation',
        'booking', 'book now', 'book a table', 'book',
        'contact', 'nous contacter', 'contactez',
        'tel', 'telephone', 'téléphone', 'phone',
        'appelez', 'call us', 'call'
    ]

    def __init__(self):
        self.phone_regex = re.compile(self.PHONE_PATTERN, re.IGNORECASE)

    def extract_phones(self, text: str) -> List[str]:
        """
        Extrait tous les numéros de téléphone français du texte.

        Args:
            text: Texte à analyser

        Returns:
            Liste des numéros trouvés (bruts)
        """
        if not text:
            return []

        phones = self.phone_regex.findall(text)
        return phones

    def clean_phone(self, phone: str) -> str:
        """
        Nettoie et formate un numéro de téléphone.

        Args:
            phone: Numéro brut

        Returns:
            Numéro nettoyé au format +33 X XX XX XX XX
        """
        if not phone:
            return ""

        # Supprimer tous les caractères non-numériques sauf +
        cleaned = re.sub(r'[^\d+]', '', phone)

        # Convertir 0X en +33X
        if cleaned.startswith('0'):
            cleaned = '+33' + cleaned[1:]

        # Vérifier que le numéro commence bien par +33
        if not cleaned.startswith('+33'):
            return ""

        # Vérifier la longueur (doit être +33XXXXXXXXX = 12 caractères)
        if len(cleaned) != 12:
            return ""

        # Formater : +33 X XX XX XX XX
        formatted = f"+33 {cleaned[3]} {cleaned[4:6]} {cleaned[6:8]} {cleaned[8:10]} {cleaned[10:12]}"

        return formatted

    def find_reservation_phone(self, html_content: str, tel_links: List[str] = None) -> Optional[str]:
        """
        Trouve le numéro de téléphone le plus probable pour les réservations.

        Logique :
        1. Chercher dans les liens tel: si fournis
        2. Chercher les numéros près des mots "réservation", "booking"
        3. Sinon prendre le premier numéro valide de la page

        Args:
            html_content: Contenu HTML de la page
            tel_links: Liste des numéros trouvés dans les liens tel: (optionnel)

        Returns:
            Numéro de réservation formaté ou None
        """
        # 1. Priorité aux liens tel: s'ils existent
        if tel_links:
            for tel_phone in tel_links:
                cleaned = self.clean_phone(tel_phone)
                if cleaned:
                    return cleaned

        # 2. Chercher les numéros près des mots-clés de réservation
        reservation_phone = self._find_phone_near_keywords(html_content)
        if reservation_phone:
            return reservation_phone

        # 3. Fallback : premier numéro valide de la page
        all_phones = self.extract_phones(html_content)
        for phone in all_phones:
            cleaned = self.clean_phone(phone)
            if cleaned:
                return cleaned

        return None

    def _find_phone_near_keywords(self, text: str) -> Optional[str]:
        """
        Cherche un numéro proche des mots-clés de réservation.

        Args:
            text: Texte à analyser

        Returns:
            Numéro formaté ou None
        """
        text_lower = text.lower()

        # Pour chaque mot-clé, chercher les numéros dans un rayon de 200 caractères
        for keyword in self.RESERVATION_KEYWORDS:
            keyword_positions = []
            start = 0

            # Trouver toutes les occurrences du mot-clé
            while True:
                pos = text_lower.find(keyword, start)
                if pos == -1:
                    break
                keyword_positions.append(pos)
                start = pos + 1

            # Pour chaque occurrence, chercher des numéros autour
            for pos in keyword_positions:
                # Zone d'analyse : 200 caractères avant et après le mot-clé
                start_range = max(0, pos - 200)
                end_range = min(len(text), pos + len(keyword) + 200)
                context = text[start_range:end_range]

                # Chercher des numéros dans cette zone
                phones = self.extract_phones(context)
                for phone in phones:
                    cleaned = self.clean_phone(phone)
                    if cleaned:
                        return cleaned

        return None


def test_phone_extraction():
    """Tests unitaires pour l'extraction de numéros."""
    extractor = PhoneExtractor()

    test_cases = [
        "+33 1 23 45 67 89",
        "01 23 45 67 89",
        "01.23.45.67.89",
        "01-23-45-67-89",
        "0123456789",
        "+33123456789",
        "Appelez le 01 23 45 67 89 pour réserver",
        "Réservation : 06 12 34 56 78",
        "Tel: +33 4 56 78 90 12",
        "Numéro invalide : 123",
        "Contact : 01 23 45 67 89 ou email@test.fr"
    ]

    print("=== Test d'extraction de numéros ===")
    for i, text in enumerate(test_cases, 1):
        phones = extractor.extract_phones(text)
        print(f"Test {i}: '{text}'")
        print(f"  Trouvés: {phones}")

        for phone in phones:
            cleaned = extractor.clean_phone(phone)
            print(f"  Nettoyé: '{phone}' → '{cleaned}'")
        print()


if __name__ == "__main__":
    test_phone_extraction()