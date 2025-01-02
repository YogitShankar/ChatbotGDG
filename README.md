# Documentation: CodeForces Web Scraper

## Overview
This project implements a web scraper for Codeforces to extract problem statements, metadata, and editorial content. It uses **BeautifulSoup** for static scraping and **Selenium** for dynamic content handling. Scraped data is stored in structured formats for easy access and analysis.

---

## Features
1. **Problem Scraper**:
   - Extracts problem title, statement, tags, time, and memory constraints.
   - Stores problem statement in a `.txt` file and metadata in a `.json` file.

2. **Editorial Scraper**:
   - Extracts editorial content including formatted explanations and code blocks.
   - Preserves LATEX expressions and code formatting.
   - Saves editorial content in an `.html` file.

3. **Error Handling and Rate Limiting**:
   - Ensures robust scraping without overwhelming the server.
   - Implements random delays and anti-bot measures
   - Handles Unicode text cleaning
   - Provides detailed logging and error handling

---

## Dependencies
- Python 3.8+
- Libraries:
  - `BeautifulSoup` (from `bs4`)
  - `requests`
  - `selenium`
  - `os`, `json`, and `time`
  - `undetected-chromedriver`
- ChromeDriver: Compatible with the installed version of Google Chrome.

---

## Directory Structure
```plaintext
ChatBotGDG/
|
├── Scraped_Sample_Data/
│   ├── Problems_Scraped/
│       ├── <problem-title>.txt
│   ├── Editorials_Scraped/
│       ├── <editorial-title>.txt
│   ├── Metadata/
│       ├── <problem-title>.json
│  
├── Codeforces Scraper/
│       ├── Problem_scraper.py
│       ├── Editorial_scraper.py
│
├── config.py
├── requirement.txt
├── README.md    # Documentation file
```

---

## Usage

### Setup
1. Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Place `chromedriver` in the system PATH or project directory.

### Running the Script
1. Update the URLs in the script with valid Codeforces problem and editorial URLs.
2. Execute the script:
   ```bash
   python scraper.py
   ```
3. Scraped data will be saved in the `data/` directory.

---

## Scraped Sample Data

### Problem Metadata (`Problems_Scraped/<problem-title>.json`)
```json
{
    "title": "Theatre Square",
    "tags": ["math", "geometry"],
    "time_limit": "1 second",
    "memory_limit": "256 megabytes",
    "url": "https://codeforces.com/problemset/problem/1/A"
}
```

### Problem Statement (`Problems_Scraped/<problem-title>.txt`)
```plaintext
<div class="problem-statement">
    <div class="title">A. Theatre Square</div>
    <div class="content">
        The description of the problem...
    </div>
</div>
```

### Editorial Content (`Editorials_Scraped/editorial.txt`)
```html
<div class="ttypography">
    <h3>Editorial for Theatre Square</h3>
    <p>Explanation with LATEX: $a^2 + b^2 = c^2$</p>
    <pre><code>// Solution code here</code></pre>
</div>
```

---

## Recommendations
- Be mindful of Codeforces’ scraping policies and implement rate limiting if scraping large datasets.
- Validate the scraped data for accuracy and completeness.

---

