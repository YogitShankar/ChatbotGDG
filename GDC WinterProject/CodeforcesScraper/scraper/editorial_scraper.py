from selenium import webdriver
from bs4 import BeautifulSoup
import os
from config import EDITORIALS_DIR
from scraper.utils import save_to_file, save_json, log_error


def scrape_editorial(editorial_url):
    try:
        # Selenium setup
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(editorial_url)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        
        # Extract editorial content
        editorial_content = soup.find('div', class_='editorial').prettify()
        
        # Save editorial
        title = editorial_url.split("/")[-1]
        save_to_file(os.path.join(EDITORIALS_DIR, f"{title}.html"), editorial_content)
        print(f"Successfully scraped and saved editorial: {title}")
    except Exception as e:
        log_error(f"Error scraping {editorial_url}: {e}")
        
