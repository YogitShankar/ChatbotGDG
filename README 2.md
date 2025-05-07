# CodeForces Problem Scraper

A Python-based tool for scraping problems and editorials from CodeForces. This project provides automated collection of problem descriptions, specifications, and editorial content using Selenium and BeautifulSoup4.

## Features

- Scrapes problem details:
    - Problem titles and tags
    - Full descriptions
    - Input/Output specifications
    - Time and memory limits
    - Problem tags
- Extracts editorial content when available
- Saves data in both TXT and JSON formats
- Implements random delays and anti-bot measures
- Handles Unicode text cleaning
- Provides detailed logging and error handling

## Requirements

- Python 3.7+
- selenium
- undetected-chromedriver
- beautifulsoup4

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd codeforces-scraper
```

2. Install required packages:
```bash
pip install selenium undetected-chromedriver beautifulsoup4
```

## Project Structure

```
data/
├── problems/     # Contains scraped problem data
│   ├── [problem_tag].txt
│   └── [problem_tag].json
└── editorials/   # Contains scraped editorial content
    ├── [problem_tag].txt
    └── summary.txt
```

## Usage

1. To scrape problems:
```python
python problem_scraper.py
```

2. To scrape editorials:
```python
python editorial_scraper.py
```

The scraped data will be saved in the `data/` directory.

## Documentation

### Problem Scraper Functions

- `clean_unicode_text(text)`:
    - Cleans Unicode characters in scraped text
    - Replaces special characters with standard equivalents

- `create_problem_file(problem_dict, output_dir)`:
    - Creates text files for scraped problems
    - Saves formatted problem information

- `create_problem_json(problem_dict, output_dir)`:
    - Creates JSON files for scraped problems
    - Saves structured problem data

- `random_delay(min_delay=5, max_delay=10)`:
    - Implements random delays between requests
    - Helps avoid server overload

### Editorial Scraper Functions

- `check_editorial_exists(driver)`:
    - Checks if an editorial is available for a problem
    - Returns boolean indicating editorial presence

- `get_tutorial_link(driver)`:
    - Extracts the tutorial/editorial link from the problem page
    - Returns the editorial URL if found

- `get_editorial_content(driver, problem_tag, problem_title, problem_url)`:
    - Extracts and processes editorial content
    - Returns structured editorial data

- `test_editorials_from_problemset(problems)`:
    - Main function for testing editorial extraction
    - Processes multiple problems and saves results

## Output Format

### Problem Files
Each problem generates two files:

1. Text file (`[problem_tag].txt`):
```
Problem: [tag] - [title]
Link: [url]

Description:
[problem description]

Input Specification:
[input details]

Output Specification:
[output details]

Time Limit: [limit]
Memory Limit: [limit]

Tags: [tag1], [tag2], ...
```

2. JSON file (`[problem_tag].json`):
```json
{
    "problem_tag": "...",
    "title": "...",
    "link": "...",
    "description": "...",
    "input_specification": "...",
    "output_specification": "...",
    "time_limit": "...",
    "memory_limit": "...",
    "tags": [...]
}
```

### Editorial Files
- Individual text files for each editorial containing the solution explanation
- Summary file with scraping statistics and results

## Notes

- The scripts use random delays between requests to avoid overwhelming the server
- Currently configured to scrape a limited number of problems (5-10) by default
- Uses undetected ChromeDriver to bypass potential anti-bot measures
- All data is saved in UTF-8 encoding to handle special characters
- Implements comprehensive error handling and logging

## Limitations

- Requires stable internet connection
- Dependent on CodeForces' page structure
- Rate limited by random delays
- May need adjustments if CodeForces updates their website structure
- Currently only scrapes the first few problems by default

## Error Handling

The scripts include error handling for:
- Missing editorial content
- Connection issues
- Various page structure variations
- Unicode character conversion
- File I/O operations