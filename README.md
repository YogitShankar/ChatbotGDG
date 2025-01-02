# ChatbotGDG
Project Submission repository 

## Directory Structure
The scraped data is saved in the following structure:
```
data/
├── problems/
│   ├── <problem_title>.json  # Problem metadata
│   └── <problem_title>.txt   # Problem statement and test cases
└── editorials/
    └── <problem_title>.txt   # Editorial content
```

## Libraries Used
- Selenium
- BeautifulSoup (bs4)
- Undetected ChromeDriver (`undetected-chromedriver`) (to bypass captchas)

Install the required Python packages using:
```bash
pip install selenium beautifulsoup4 undetected-chromedriver
```

## Usage
### Setup
1. Ensure Google Chrome is installed on your system.
2. Download and install the required Python packages.
3. Create the following directories for storing scraped data:
   ```bash
   mkdir -p data/problems data/editorials
   ```

### Run the Scraper
1. Add the target URL of the Codeforces problem set in the `url` variable in the code.
2. Execute the script:
   ```bash
   python3 scraper.py
   ```
   Problems can be scrapped individually using the fetch_problems function

### Output
- Problem statements, test cases, and metadata will be saved in the `data/problems` directory.
- Editorials will be saved in the `data/editorials` directory.

### Example Output
- `data/problems/ProblemTitle.json`:
  ```json
  {
      "title": "ProblemTitle",
      "tags": ["dp", "greedy"],
      "time_limit": "2 seconds",
      "memory_limit": "256 MB"
  }
  ```
- `data/problems/ProblemTitle.txt`:
  ```
  <Problem Statement>

  Input
  <Input Description>

  Output
  <Output Description>

  Input
  <Input Test Case>

  Output
  <Output Test Case>
  ```
- `data/editorials/ProblemTitle.txt`:
  ```
  <Editorial Content>
  ```

## Functions
### `fetch_problem_data(problem_url)`
- Scrapes problem metadata, statement, input/output specs, and test cases.
- Saves metadata as a JSON file and problem details as a text file.

### `scrape_editorial(editorial_url, title)`
- Extracts editorial content from the provided URL.
- Saves the editorial in a text file.


## Notes
- For large-scale scraping, adjust the delay (`time.sleep()`) to avoid being flagged.
- The code detects if the editorial link directs to a pdf and rejects the problem
- The code doesn't work if the editorial is on a different website or the structure of the editorial is far unusual.

