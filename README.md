# Codeforces Problem Scraper

This document provides a detailed guide to setting up, running, and understanding the Codeforces Problem Scraper program, a Python script that uses Selenium to extract problem statements and metadata from Codeforces.

## Features
- Extracts problem titles and statements from Codeforces.
- Saves problem data in a text file (`problem_statement.txt`).
- Stores metadata (e.g., problem title) in a JSON file (`metadata.json`).
- Programmed to run in Google Colab using a virtual display.

## Code Walkthrough

### 1. Setup Virtual Display
The `setup_virtual_display` function uses `pyvirtualdisplay` to create a virtual screen for headless browsing. This is needed in Google Colab where no graphical interface is available.

### 2. Initialize Firefox Driver
The `init_firefox_driver` function sets up the Firefox web driver in headless mode (no visible browser window).

### 3. Scrape Problem Data
The `scrape_problem` function:
- Opens the Codeforces problem URL.
- Extracts the problem title and statement using Selenium.

### 4. Save Problem Data
Two sub-functions save the scraped data:
- `store_problem_statement`: Saves the problem statement in a text file.
- `store_metadata`: Saves the problem title in a JSON file.

### 5. Main Execution
The program:
1. Starts a virtual display.
2. Initializes the web driver.
3. Scrapes the problem from the provided URL.
4. Saves the scraped data.
5. Closes the driver and stops the virtual display.

## Acknowledgments
This script uses:
- **Selenium** for web automation.
- **pyvirtualdisplay** and **xvfb** for virtual display management.
- **Firefox** as the browser for scraping.
