import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import PROBLEM_URL, EDITORIAL_DIR, DELAY_BETWEEN_REQUESTS
from scraper.utils import save_file, apply_delay
import time


def patched_del(self):
    try:
        self.quit()
    except Exception:
        pass

uc.Chrome.__del__ = patched_del
def scrape_editorial(contest_id, problem_index):
    url = f"{PROBLEM_URL}/{contest_id}/problem/{problem_index}"
    CAPTCHA_API_KEY = "d15958dc07d8a75b83c8497522372ec1"
    solution_index = ord(problem_index) - 65

    # Setup Selenium with proper options
    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")
    driver = uc.Chrome(options=options)
    # options.add_argument("--headle ss")  # Optional: Run in headless mode

    try:
        # Navigate to the problem URL
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Tutorial'))
        )
        editorial_link = driver.find_element(By.PARTIAL_LINK_TEXT, 'Tutorial')
        editorial_link_url = editorial_link.get_attribute('href')
        print(f"Navigating to: {editorial_link_url}")
        driver.get(editorial_link_url)
        time.sleep(3)
        # Extract the editorial content
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'spoiler'))
        )
        solutions = driver.find_elements(By.CLASS_NAME, 'spoiler')
        solution = solutions[2 * solution_index + 1]
        solution_container = solution.find_element(By.CSS_SELECTOR, 'pre')
        solution_text = solution_container.get_attribute("textContent")

        # # Save the solution text
        save_file(f"{EDITORIAL_DIR}/{contest_id}_{problem_index}.txt", solution_text)

    except Exception as e:
        print(f"Error scraping editorial: {e}")
        import traceback
        traceback.print_exc()
    finally:       
        if driver:
            try:
                driver.quit()
            except Exception as quit_error:
                print(f"Error during WebDriver quit: {quit_error}")

            # Apply delay between requests
            apply_delay(DELAY_BETWEEN_REQUESTS)
