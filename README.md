Name: Yuvraj Singh, 
Roll no.- 221236

# Codeforces Problem Scraper

A Python-based web scraper for collecting programming problems and their editorials from Codeforces. This tool automatically scrapes problem statements, metadata, and editorial solutions while organizing them into a structured format.

## Features

- Scrapes problems based on difficulty rating range
- Collects problem statements, time limits, memory limits, and tags
- Saves editorial solutions when available
- Handles rate limiting and page loading issues
- Organizes data into separate files for easy access
- Uses undetected-chromedriver to avoid blocking

## Directory Structure

```
.
├── data/
│   ├── problems/      # Contains problem statements as text files
│   └── editorials/    # Contains editorial solutions as text files
├── metadata.json      # Problem metadata in JSON format
├── scraper.py         # Main scraper script
└── README.md         # This file
```

## Requirements

- Python 3.6+
- Chrome browser installed
- Required Python packages:
  - beautifulsoup4
  - undetected-chromedriver
  - selenium

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd codeforces-scraper
```

2. Install required packages:
```bash
pip install beautifulsoup4 undetected-chromedriver selenium
```

## Usage

1. Basic usage with default settings:
```python
from scraper import CodeforcesScraper

scraper = CodeforcesScraper()
scraper.scrape_problem_set((1000, 1350))  # Scrape problems rated 1000-1350
```

2. Customize the rating range and page number:
```python
scraper.scrape_problem_set((800, 1000), page=2)  # Scrape second page of problems rated 800-1000
```

## Output Format

### metadata.json
```json
{
    "1234A": {
        "title": "Problem Title",
        "time_limit": "1 second",
        "memory_limit": "256 megabytes",
        "tags": ["implementation", "math"]
    }
}
```

### Problem Files (data/problems/)
Each problem is saved as a text file named `[contest_id][problem_id].txt` containing:
- Problem title
- Time and memory limits
- Tags
- Full problem description

### Editorial Files (data/editorials/)
When available, editorials are saved as text files named `[contest_id][problem_id].txt` containing:
- Problem title
- Problem ID
- Complete editorial solution

## Error Handling

The scraper includes several error handling mechanisms:
- Automatic retry on page load failures
- Graceful handling of missing editorials
- Skip already processed problems
- Chrome driver cleanup on script termination

## Limitations

- Respects Codeforces' rate limiting
- May need to handle CAPTCHAs manually in some cases
- Editorial extraction might be incomplete for some problems
- Some math formulas might not render properly in text format

## License

This project is free and open to use without any restrictions.

## Disclaimer

This tool is for educational purposes only. Please respect Codeforces' terms of service and rate limiting policies when using this scraper.
