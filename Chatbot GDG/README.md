# Codeforces Scraper

A Python-based scraping tool for retrieving problems and editorials from Codeforces.

## Setup

1. Install required dependencies:

```bash
pip install selenium beautifulsoup4
```

2. Download ChromeDriver matching your Chrome browser version and place it in one of:

   - Project root directory
   - `drivers/` directory

3. Configure settings in `config/config.ini` or `config/config.json`

## Usage

Run the main script to scrape problems and editorials:

```bash
python main.py
```

### Custom Problem/Editorial IDs

Modify `main.py` to scrape specific problems/editorials:

```python
problem_id = "1/A"  # Format: "contest/problem"
editorial_id = "1234"  # Format: numerical ID
```

## Project Structure

```
.
├── config/
│   ├── config.ini
│   └── config.json
├── data/
│   ├── problems/
│   ├── metadata/
│   └── editorials/
├── src/
│   ├── problem_scraper.py
│   ├── editorial_scraper.py
│   └── utils.py
└── main.py
```

## Features

- Problem scraping with metadata extraction
- Editorial content retrieval
- Configurable rate limiting and retry mechanisms
- ChromeDriver auto-setup
- Data storage in organized directory structure

## Configuration

Key settings in config files:

- Base URLs for problems and editorials
- Storage paths for scraped data
- Rate limiting parameters
- ChromeDriver path
