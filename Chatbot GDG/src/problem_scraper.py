from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
import json
import configparser
import random

config = configparser.ConfigParser()
config.read('/Users/ayushagarwal/Documents/Python/config/config.ini')

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:89.0) Gecko/20100101 Firefox/89.0'
]

def scrape_problem(problem_id):
    config = configparser.ConfigParser()
    config.read('/Users/ayushagarwal/Documents/Python/config/config.ini')
    base_url = config['DEFAULT']['base_url']
    url = f"{base_url}{problem_id}"

    chrome_options = Options()
    # Remove the headless argument or comment it out:
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        from .utils import get_chromedriver_path
        driver_path = get_chromedriver_path()
    except Exception as e:
        print(f"ChromeDriver error: {e}")
        return None

    try:
        driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
    except Exception as e:
        print(f"Error initializing Chrome driver: {e}")
        return None

    try:
        driver.get(url)
        # Removed the captcha prompt:
        # input("If a captcha is displayed, solve it in the opened browser and then press Enter here...")

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
    except Exception as e:
        print(f"Error fetching the problem page: {e}")
        driver.quit()
        return None

    try:
        title_elem = soup.find('div', class_='title')
        if not title_elem:
            print("Unable to locate the problem title.")
            return None
        title = title_elem.text.strip()
        
        statement_elem = soup.find('div', class_='problem-statement')
        if not statement_elem:
            print("Unable to locate the problem statement.")
            return None
        statement = statement_elem.text.strip()
        
        examples = []
        sample_tests = soup.find_all('div', class_='sample-test')
        for sample in sample_tests:
            input_data = sample.find('div', class_='input').text.strip()
            output_data = sample.find('div', class_='output').text.strip()
            examples.append({'input': input_data, 'output': output_data})
        return {"title": title, "statement": statement, "examples": examples}
    except AttributeError as e:
        print(f"Error parsing the problem: {e}")
        return None

def save_problem(problem_id, data):
    problem_storage = "data/problems/"
    metadata_storage = "data/metadata/"
    
    # Ensure the directory exists
    os.makedirs(problem_storage, exist_ok=True)
    os.makedirs(metadata_storage, exist_ok=True)
    
    # Save problem statement
    with open(f"{problem_storage}{problem_id}.txt", 'w', encoding='utf-8') as f:
        f.write(data['statement'])
    
    # Save metadata
    metadata = {
        'title': data['title'],
        'tags': data.get('tags', []),
        'time_limit': data.get('time_limit', ''),
        'memory_limit': data.get('memory_limit', ''),
        'test_cases': data.get('examples', [])
    }
    with open(f"{metadata_storage}{problem_id}.json", 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4)

