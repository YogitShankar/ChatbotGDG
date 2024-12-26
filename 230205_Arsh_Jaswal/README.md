
# Codeforces Scraper


This Python project is a web scraper designed to extract problem details from Codeforces, including problem statements, editorials, metadata (tags, time and memory limits), and solutions.

The scraper uses **BeautifulSoup** for parsing HTML and **undetected-chromedriver** to deal with Codeforces' anti-bot measures. The same can be achieved using Selenium chromedriver.

**Disclaimer**: This assignment is only for ethical purposes.

## Features

- Extracts problem statements, editorials, and metadata (tags, time and memory limits).
- Text and code has been formatted. Shows pretty good result on printing.
- Stores Problem statement (description) in **text files** and metadata, solutions, etc. in **JSON** format.
- Implements **error handling** using try-except in every possible case and **rate-limiting** to avoid overwhelming Codeforces servers.
- Uses **undetected-chromedriver** instead of the regular **selenium chromedriver** to bypass detection mechanisms. The usage of undetected-chromedriver is similar to the standard selenium chromedriver, but in addition, it offers enhanced compatibility for handling detection issues.
- Undetected-chromedriver was compatible with all selenium functions, providing same functionality.



## My Implementation

- Implemented the scraper using a **Jupyter notebook** (`.ipynb`), which allows for easy debugging and testing.
- Called functions sequentially rather than using a loop to minimize the risk of errors or unexpected behavior during scraping.
- Generated **problem statement text files** from the stored JSON data at the end of the process.
- Focused only on **Codeforces editorials**, excluding non-Codeforces sources like Google Drive or GitHub editorials to maintain a generic and consistent editorial scraper.
- Extracted only **text-based solutions**, even though video solutions can be included at any time by adding their links to the JSON file.
- Scraped over **700 questions**. Beyond that, the questions started becoming outdated, affecting the relevancy of the data.

## Results and Observations

- There were only **89 "No solution found"** entries in the JSON file out of **700** questions.
- A total of **611 solutions were found**, indicating a high success rate in retrieving solutions.
- The **percentage of solutions found** is approximately **87.14%**.
- The **text file** was successfully generated with **readable** and **well formatted** content.
- The **code structure** was maintained and organized throughout the scraping process.
- The scraper took an **average of 5-12 seconds per question**, ensuring efficient data collection.


## Requirements

To run the scraper, you'll need Python 3 and the following dependencies:

- `undetected-chromedriver`
- `beautifulsoup4`
- `selenium`
- `re` (for regular expressions)

Install the required libraries using:

```bash
pip install -r requirements.txt

