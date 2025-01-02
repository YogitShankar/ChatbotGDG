from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import PROBLEM_URL, PROBLEM_DIR, METADATA_DIR, DELAY_BETWEEN_REQUESTS
from scraper.utils import save_file, apply_delay
import time


def scrape_problem(contest_id, problem_index):
    url = f"{PROBLEM_URL}/{contest_id}/problem/{problem_index}"
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver_service = Service('C:\Program Files (x86)\chromedriver.exe')  # Update this with your ChromeDriver path
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(2)  # Allow the page to load completely

        # Extract problem details using Selenium
        title_element = WebDriverWait(driver, 10).until(
              EC.presence_of_element_located((By.CLASS_NAME, "title"))
        )
        title = title_element.text.strip()
        statement_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "problem-statement"))
        )
        tags_elements = driver.find_elements(By.CLASS_NAME, "tag-box")
        tags = [tag.text.strip() for tag in tags_elements]
        # Prepare metadata
        metadata = {
            "contest_id": contest_id,
            "problem_index": problem_index,
            "title": title,
            "tags": tags,
        } 
        save_file(f"{PROBLEM_DIR}/{contest_id}_{problem_index}.txt", statement_element.text)
        save_file(f"{METADATA_DIR}/{contest_id}_{problem_index}.json",metadata)

        print(f"Scraped problem {contest_id}{problem_index} successfully!")

        # Delay to avoid being flagged
        time.sleep(DELAY_BETWEEN_REQUESTS)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()
