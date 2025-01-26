# ChatbotGDG
Project Submission repository 

# Codeforces Problem Scraper

This is a Python-based scraper that extracts problem details from the Codeforces problem set. It uses **Selenium** and **BeautifulSoup** to retrieve the problem statement, metadata, and sample inputs/outputs for a specified problem on Codeforces. The extracted data is then saved into text and JSON files.

## Features

- Scrapes problem titles, descriptions, time and memory limits, tags, and sample inputs/outputs.
- Saves the problem statement as a `.txt` file.
- Stores metadata (excluding the description) in a `.json` file.
- Automates browser interaction with **Selenium** to handle dynamic content on Codeforces.
  
## Requirements

To run this scraper, you need to install the following dependencies:

- **Selenium**: For automating web browser interaction.
- **BeautifulSoup**: For parsing the HTML content.
- **ChromeDriver**: For the Selenium WebDriver.

### Installing Dependencies

You can install the required Python packages using `pip`:

```bash
pip install selenium beautifulsoup4
