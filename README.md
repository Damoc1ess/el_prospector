# Hotel & Restaurant Prospector

![Ralph Wiggum Coding](ralph_coding_for_me.webp)

CLI tool for prospecting hotels and restaurants via Google Maps API with automated web scraping for reservation phone numbers and emails.

## Features

- **Google Maps Search**: Find establishments by city via Google Places API
- **Smart Scraping**: Visit websites to extract reservation phone numbers and emails
- **Multi-format Export**: CSV and JSON with enriched data
- **Performance**: Timeout handling, rate limiting, and automatic retry
- **Robust**: Complete error handling and data validation

## Installation

### Prerequisites
- Python 3.10 or higher
- Google Maps API key with Places API access

### Install dependencies
```bash
pip install requests beautifulsoup4 python-dotenv
```

### Google API Configuration
1. Create a `.env` file in the project folder
2. Add your Google Maps API key:
```
GOOGLE_MAPS_API_KEY=your_api_key_here
```

**Getting a Google Maps API key:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Enable "Places API (New)"
4. Create an API key and copy it to the `.env` file

## Usage

### Basic command
```bash
python src/prospector.py --city "Paris" --type restaurant
```

### Available options

| Option | Description | Default |
|--------|-------------|---------|
| `--city` | City to prospect (required) | - |
| `--type` | Establishment type (`hotel`, `restaurant`, `all`) | `all` |
| `--limit` | Maximum number of results | `20` |
| `--no-scrape` | Disable scraping (faster) | `False` |
| `--output` | Output filename without extension | `prospection` |
| `--format` | Export format (`csv`, `json`, `both`) | `csv` |

### Usage examples

```bash
# Basic search - restaurants in Paris
python src/prospector.py --city "Paris" --type restaurant

# Hotels in Lyon with limit
python src/prospector.py --city "Lyon" --type hotel --limit 10

# All establishment types in Nice, without scraping
python src/prospector.py --city "Nice" --type all --no-scrape

# JSON export only
python src/prospector.py --city "Marseille" --format json

# Complete export with scraping
python src/prospector.py --city "Bordeaux" --format both --limit 30
```

## Extracted Data

### Data sources

| Field | Source | Description |
|-------|--------|-------------|
| `name` | Google Places | Establishment name |
| `address` | Google Places | Full address |
| `google_phone` | Google Place Details | Official Google phone number |
| `website` | Google Place Details | Official website |
| `**reservation_phone**` | **Website scraping** | **Reservation phone number** |
| `email` | Website scraping | Contact email address |
| `rating` | Google Places | Rating (out of 5) |
| `reviews` | Google Places | Number of reviews |
| `type` | Auto-detection | hotel/restaurant |

### CSV output example
```csv
name,address,google_phone,reservation_phone,email,website,rating,reviews,type
Le Petit Bistro,"12 rue de la Paix, 75001 Paris",+33 1 23 45 67 89,+33 1 98 76 54 32,contact@petitbistro.fr,https://petitbistro.fr,4.5,120,restaurant
Hotel Royal,"5 avenue des Champs, 75008 Paris",+33 4 56 78 90 12,+33 4 11 22 33 44,,https://hotelroyal.fr,4.2,89,hotel
```

## Reservation Phone Extraction

The scraper automatically visits websites and uses smart logic:

### 1. Phone link detection
Searches for `<a href="tel:+33123456789">` links as priority.

### 2. Contextual analysis
Looks for phone numbers near keywords:
- **French**: "reservation", "reserver", "contact", "appelez"
- **English**: "booking", "book now", "book a table", "call us"

### 3. Smart fallback
If no reservation context found, takes the first valid French phone number.

### Supported formats
- `+33 X XX XX XX XX`
- `0X XX XX XX XX`
- `0X.XX.XX.XX.XX`
- `0X-XX-XX-XX-XX`
- `0123456789`

## Performance and Limits

### Rate limiting
- **Google API**: 1 second between requests
- **Scraping**: 2 seconds between websites
- **Timeout**: 10 seconds per website

### Error handling
- Automatic retry on temporary errors (503, timeout)
- Continues on individual site failure
- SSL validation and content filtering
- Protection against oversized pages (>5MB)

### Limitations
- Maximum 20 results per Google Places request
- Respectful scraping (realistic User-Agent)
- No more than 60 sites scraped per minute

## Architecture

```
src/
├── prospector.py       # Main CLI with argparse
├── google_places.py    # Google Places API v1 client
├── contact_scraper.py  # Website scraping + contact extraction
├── phone_extractor.py  # French phone number detection and formatting
└── exporter.py         # CSV/JSON export
```

### Main modules

#### `GooglePlacesClient`
- Text Search API to find establishments by city
- Place Details API to get phone and website
- API error handling and rate limiting

#### `ContactScraper`
- Web page download with retry
- Reservation phone extraction by context
- Email extraction with spam filtering

#### `PhoneExtractor`
- Optimized regex for French phone numbers
- Automatic cleaning and formatting
- Contextual detection of reservation numbers

#### `Exporter`
- CSV export with standardized headers
- JSON export with metadata
- Data validation before export

## Troubleshooting

### Common errors

**"Invalid or missing API key"**
```bash
# Check the .env file
cat .env
# Should contain: GOOGLE_MAPS_API_KEY=your_key
```

**"No establishments found"**
- Check the city spelling
- Try a more well-known city (Paris, Lyon, Marseille...)
- Change the establishment type

**"Timeout during scraping"**
- Normal for some slow sites
- Use `--no-scrape` for a quick test
- Scraping continues with other sites

**"API quota exceeded"**
- Check quotas in Google Cloud Console
- Wait for quota reset (24h)
- Optimize with lower `--limit`

### Status messages

| Message | Meaning |
|---------|---------|
| `OK` | Scraping successful with contacts found |
| `No contact found` | Site accessible but no phone number |
| `ERROR: timeout` | Site too slow (>10s) |
| `ERROR: 403` | Site blocks bots |
| `ERROR: 404` | Page not found |

## Testing

### Quick test
```bash
# Test Google API
python src/google_places.py

# Test scraper
python src/contact_scraper.py

# Test phone extractor
python src/phone_extractor.py

# Test exporter
python src/exporter.py
```

### Full test
```bash
# Test with 5 Parisian restaurants (quick)
python src/prospector.py --city "Paris" --type restaurant --limit 5
```

## Advanced Examples

### Luxury hotel prospecting
```bash
python src/prospector.py --city "Cannes" --type hotel --limit 15 --format both
```

### Restaurant audit without scraping (fast)
```bash
python src/prospector.py --city "Toulouse" --type restaurant --no-scrape --limit 50
```

### Custom export
```bash
python src/prospector.py --city "Strasbourg" --output "hotels_strasbourg" --format json
```

## Best Practices

- Respectful rate limiting
- Realistic User-Agent
- Proper SSL handling
- Configured timeouts (10s)
- No server overload
- Pseudonymized data in logs

## License

This project is intended for professional commercial prospecting use.
Respect website terms of service and GDPR regulations.

---

## Built with Ralph Wiggum

This project was **100% autonomously coded** using the **Ralph Wiggum** methodology - an agentic loop technique for Claude Code CLI.

| Metric | Value |
|--------|-------|
| **AI Model** | Claude Opus 4.5 (`claude-opus-4-5-20251101`) |
| **Technique** | Ralph Wiggum autonomous loop |
| **Iterations** | 11 tours |
| **Duration** | 26 minutes |
| **Commits** | 15 |

### What is Ralph Wiggum?

Ralph Wiggum is a methodology for running Claude Code in autonomous mode with:
- **PROMPT.md** - Instructions and specifications
- **TODO.md** - State persistence and progress tracking
- **loop.sh** - Orchestration script with circuit breakers
- **HARD STOP** - Automatic termination when complete

The AI reads the specifications, plans the work, implements features, tests them, and commits - all autonomously without human intervention.

*"I'm helping!"* - Ralph Wiggum

---

**Developed with [Claude Code](https://claude.ai/code)** - Automated prospecting tool for professionals.
