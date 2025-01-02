from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import os
import time
import re


class CodeforcesData:
    def __init__(self):
        self.data_file = 'metadata.json'
        self.problems_dir = 'data/problems'
        self.editorials_dir = 'data/editorials'

        os.makedirs(self.problems_dir, exist_ok=True)
        os.makedirs(self.editorials_dir, exist_ok=True)

    def save_problem_data(self, problem_data, contest_id, problem_id):
        # Storing problem data in JSON and text files
        problem_key = f"{contest_id}{problem_id}"

        metadata = {
            'title': problem_data['title'],
            'time_limit': problem_data['time_limit'],
            'memory_limit': problem_data['memory_limit'],
            'tags': problem_data['tags']
        }

        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
        else:
            existing_data = {}

        existing_data[problem_key] = metadata

        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, indent=4, ensure_ascii=False)

        # Saving problem statement
        problem_filename = os.path.join(self.problems_dir, f"{problem_key}.txt")
        problem_content = [
            f"Problem: {problem_data['title']}",
            f"Time Limit: {problem_data['time_limit']}",
            f"Memory Limit: {problem_data['memory_limit']}",
            f"Tags: {', '.join(problem_data['tags'])}",
            "\nDescription:",
            problem_data['description']
        ]

        with open(problem_filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(problem_content))

        # Save editorial if it exists and is valid
        if problem_data.get('editorial') and isinstance(problem_data['editorial'], str) and len(
                problem_data['editorial'].strip()) > 0:
            editorial_filename = os.path.join(self.editorials_dir, f"{problem_key}.txt")
            editorial_content = [
                f"Editorial for Problem: {problem_data['title']}",
                f"Problem ID: {problem_key}",
                "\nSolution:",
                problem_data['editorial']
            ]

            with open(editorial_filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(editorial_content))


class CodeforcesScraper:
    def __init__(self):
        self.driver = None
        self.data_manager = CodeforcesData()

    def initialize_driver(self):
        self.driver = uc.Chrome()

    def _wait_for_element(self, by, value, timeout=10):
        # Helper method to wait for element with better error handling
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            return None

    def extract_editorial(self, problem_url, contest_id, problem_id):
        # Extract problem solution from editorial page with improved reliability
        try:
            editorial_url = None
            links = self.driver.find_elements(By.TAG_NAME, 'a')
            for link in links:
                try:
                    href = link.get_attribute('href')
                    text = link.text.lower()
                    if href and ('tutorial' in text or 'editorial' in text):
                        editorial_url = href
                        break
                except:
                    continue

            if not editorial_url:
                return ""

            self.driver.get(editorial_url)
            time.sleep(2)

            content_element = self._wait_for_element(By.CLASS_NAME, 'content')
            if not content_element:
                return ""

            # Parse content
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            content_div = soup.find('div', class_='content')

            if not content_div:
                return ""

            problem_marker = f"{contest_id}{problem_id}"
            paragraphs = content_div.find_all(['p', 'div'])

            editorial_content = []
            found_section = False

            for p in paragraphs:
                text = p.get_text(strip=True)
                if problem_marker in text:
                    found_section = True
                    editorial_content.append(p.get_text())
                elif found_section:
                    if any(marker in text for marker in
                          [f"{contest_id}A", f"{contest_id}B", f"{contest_id}C", f"{contest_id}D", f"{contest_id}E"]):
                        break
                    editorial_content.append(p.get_text())

            return "\n".join(editorial_content) if editorial_content else ""

        except Exception as e:
            print(f"Error extracting editorial: {str(e)}")
            return ""

    def scrape_problem(self, url):
        try:
            self.driver.get(url)
            time.sleep(2)

            # Wait for problem statement
            if not self._wait_for_element(By.CLASS_NAME, 'problem-statement'):
                self.driver.refresh()
                time.sleep(2)
                if not self._wait_for_element(By.CLASS_NAME, 'problem-statement'):
                    raise Exception("Problem statement not found")

            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            # Get problem identifiers from URL
            url_parts = url.split('/')
            problem_id = url_parts[-1]
            contest_id = url_parts[-2]

            problem_data = {
                'title': soup.find('div', class_='title').text.strip(),
                'description': self._extract_description(soup),
                'time_limit': soup.find(class_="time-limit").get_text(strip=True),
                'memory_limit': soup.find(class_="memory-limit").get_text(strip=True),
                'tags': [tag.text.strip() for tag in soup.find_all('span', class_='tag-box')],
                'editorial': self.extract_editorial(url, contest_id, problem_id)
            }

            # Save the collected data
            self.data_manager.save_problem_data(problem_data, contest_id, problem_id)

        except Exception as e:
            print(f"Error processing problem {url}: {str(e)}")

    def _extract_description(self, soup):
        # Extract and clean problem description
        description_div = soup.find('div', class_='problem-statement')
        if not description_div:
            return ""

        description_paras = description_div.find_all('p')
        cleaned_paras = []

        for para in description_paras:
            # Remove script and math elements but preserve text
            for element in para.find_all(['script', 'math']):
                element.decompose()
            cleaned_text = para.get_text(strip=False)
            if cleaned_text:
                cleaned_paras.append(cleaned_text)

        return '\n'.join(cleaned_paras)

    def scrape_problem_set(self, rating_range, page=1):
        try:
            self.initialize_driver()
            start_rating, end_rating = rating_range
            url = f"https://codeforces.com/problemset/page/{page}?tags={start_rating}-{end_rating}"

            self.driver.get(url)
            if not self._wait_for_element(By.CLASS_NAME, 'problems'):
                raise Exception("Problem set page failed to load")

            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            processed_urls = set()

            for link in soup.find_all('a', href=True):
                if link['href'].startswith("/problemset/problem"):
                    problem_url = f"https://codeforces.com{link['href']}"
                    if problem_url not in processed_urls:
                        print(f"Processing: {problem_url}")
                        self.scrape_problem(problem_url)
                        processed_urls.add(problem_url)
                        time.sleep(2)

        finally:
            if self.driver:
                self.driver.quit()


if __name__ == "__main__":
    scraper = CodeforcesScraper()
    scraper.scrape_problem_set((1000, 1350))  # Scrape problems rated 1000-1350
