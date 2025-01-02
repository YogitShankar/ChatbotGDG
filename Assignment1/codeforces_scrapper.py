import os
import json
import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Configuration for storage paths
DATA_DIR = "data"
PROBLEMS_DIR = os.path.join(DATA_DIR, "problems")
EDITORIALS_DIR = os.path.join(DATA_DIR, "editorials")

# Ensure directories exist
os.makedirs(PROBLEMS_DIR, exist_ok=True)
os.makedirs(EDITORIALS_DIR, exist_ok=True)

# Setup Selenium WebDriver
def setup_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver_path = "chromedriver"  # Update path to chromedriver if needed
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=options)

def scrape_problem(problem_url):
    """Scrape problem details from Codeforces"""
    response = requests.get(problem_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract problem title
    title = soup.find('div', class_='title').text.strip()

    # Extract problem statement
    statement_div = soup.find('div', class_='problem-statement')
    statement_html = str(statement_div)

    # Extract tags
    tags = [tag.text.strip() for tag in soup.find_all('span', class_='tag-box')]

    # Extract time and memory limits
    limits = soup.find('div', class_='time-limit').text.strip()
    time_limit, memory_limit = limits.split(',')

    # Save problem statement to file
    problem_file_path = os.path.join(PROBLEMS_DIR, f"{title}.txt")
    with open(problem_file_path, 'w', encoding='utf-8') as f:
        f.write(statement_html)

    # Save metadata to JSON
    metadata = {
        "title": title,
        "tags": tags,
        "time_limit": time_limit,
        "memory_limit": memory_limit,
        "url": problem_url
    }
    metadata_file_path = os.path.join(PROBLEMS_DIR, f"{title}.json")
    with open(metadata_file_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4)

    print(f"Scraped problem: {title}")

def scrape_editorial(editorial_url):
    """Scrape editorial content from Codeforces"""
    driver = setup_driver()
    driver.get(editorial_url)

    # Extract editorial content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    editorial_content = soup.find('div', class_='ttypography')
    if not editorial_content:
        print("Editorial content not found.")
        return

    # Handle code blocks and LATEX
    editorial_html = str(editorial_content)

    # Save editorial to file
    editorial_file_path = os.path.join(EDITORIALS_DIR, "editorial.html")
    with open(editorial_file_path, 'w', encoding='utf-8') as f:
        f.write(editorial_html)

    print(f"Scraped editorial content from {editorial_url}")
    driver.quit()

if __name__ == "__main__":
    # Example URLs (replace with actual ones)
    problem_url = "https://codeforces.com/problemset/problem/1/A"
    editorial_url = "https://codeforces.com/blog/entry/552"  # Replace with a valid editorial link

    scrape_problem(problem_url)
    scrape_editorial(editorial_url)

    print("Scraping completed.")
