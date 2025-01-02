from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import configparser
from .utils import get_chromedriver_path

config = configparser.ConfigParser()
config.read('/Users/ayushagarwal/Documents/Python/config/config.ini')

def scrape_editorial(editorial_id):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless Chrome
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        driver_path = get_chromedriver_path()
    except ValueError as e:
        print(e)
        return None

    try:
        driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
    except Exception as e:
        print(f"Error initializing the Chrome driver: {e}")
        return None
    
    url = f"https://codeforces.com/blog/entry/{editorial_id}"
    try:
        driver.get(url)
    except Exception as e:
        print(f"Error fetching the editorial: {e}")
        driver.quit()
        return None
    
    # Add your scraping logic here
    editorial_content = driver.page_source
    driver.quit()
    
    return editorial_content

from bs4 import BeautifulSoup

def process_editorial(raw_editorial):
    # Process the raw editorial content
    # Add your processing logic here
    processed_editorial = raw_editorial  # Placeholder
    return processed_editorial

def save_editorial(editorial_id, data):
    editorial_storage = "data/editorials/"
    os.makedirs(editorial_storage, exist_ok=True)
    with open(f"{editorial_storage}{editorial_id}.txt", 'w', encoding='utf-8') as f:
        f.write(data)
