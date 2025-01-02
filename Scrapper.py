from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json

class CFProblemScraper:
    def __init__(self, chromedriver_path):
        self.chromedriver_path = chromedriver_path
        self.base_url = "https://codeforces.com"
        self.output_directory = "ScrapedProblems"
        os.makedirs(self.output_directory, exist_ok=True)

    def setup_driver(self):
        """Set up the Selenium WebDriver."""
        options = Options()
        options.add_argument("--window-size=1920,1080")
        service = Service(executable_path=self.chromedriver_path)
        return webdriver.Chrome(service=service, options=options)

    def scrape_problem(self, problem_identifier):
        """Retrieve problem details and save them."""
        problem_link = f"{self.base_url}/problemset/problem/{problem_identifier}"
        driver = self.setup_driver()

        try:
            driver.get(problem_link)
            wait = WebDriverWait(driver, 15)
            problem_content = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "problem-statement"))
            )

            # Parse the page content
            page_soup = BeautifulSoup(driver.page_source, 'html.parser')
            problem_section = page_soup.find('div', class_='problem-statement')
            if not problem_section:
                raise RuntimeError("Problem details could not be located.")

            # Extract and organize the problem data
            data = self.collect_problem_data(problem_identifier, problem_section, page_soup)

            # Save problem content and metadata
            self.save_statement(problem_identifier, data["title"], data["description"])
            self.save_metadata(problem_identifier, data)

            return data

        except Exception as ex:
            print(f"Error scraping problem {problem_identifier}: {ex}")
            return None
        finally:
            driver.quit()

    def collect_problem_data(self, problem_identifier, problem_section, page_soup):
        """Extract key problem details."""
        details = {}

        # Retrieve problem title
        title_element = problem_section.find('div', class_='title')
        details["title"] = title_element.text.strip() if title_element else "No Title"

        # Retrieve the problem description
        details["description"] = self.get_problem_description(problem_section)

        # Extract metadata
        details["time_limit"] = self.get_text_by_class(problem_section, 'time-limit')
        details["memory_limit"] = self.get_text_by_class(problem_section, 'memory-limit')
        details["tags"] = self.extract_tags(page_soup)
        details["samples"] = self.get_samples(problem_section)

        return details

    def get_problem_description(self, problem_section):
        """Compile the problem description without duplicates."""
        description = []
        seen_content = set()  # Track seen content to prevent duplication

        # Include LaTeX sections
        for latex in problem_section.find_all('span', class_='math'):
            latex_text = f"$$ {latex.text.strip()} $$"
            if latex_text not in seen_content:
                description.append(latex_text)
                seen_content.add(latex_text)

        # Include standard text but skip metadata-related sections and duplicates
        for content in problem_section.find_all(['p', 'div']):
            content_text = content.text.strip()

            # Skip metadata content like "time limit", "memory limit", "input", "output"
            if any(keyword in content_text.lower() for keyword in ["time limit", "memory limit", "input", "output"]):
                continue

            # Add the content if it hasn't been added before
            if content_text and content_text not in seen_content:
                description.append(content_text)
                seen_content.add(content_text)

        # Return description as a single string with newline separation
        return '\n'.join(filter(None, description))

    def get_text_by_class(self, section, class_name):
        """Retrieve text content for a specified class."""
        element = section.find('div', class_=class_name)
        return element.text.strip() if element else "N/A"

    def extract_tags(self, soup):
        """Identify problem tags."""
        return [tag.text.strip() for tag in soup.find_all('span', class_='tag-box')]

    def get_samples(self, problem_section):
        """Collect sample inputs and outputs."""
        samples = []
        for example in problem_section.find_all('div', class_='sample-test'):
            input_block = example.find('div', class_='input').find('pre').text.strip()
            output_block = example.find('div', class_='output').find('pre').text.strip()
            samples.append({"input": input_block, "output": output_block})
        return samples

    def save_statement(self, problem_identifier, title, description):
        """Store the problem description in a text file."""
        filename = f"Problem_{problem_identifier.replace('/', '_')}.txt"
        filepath = os.path.join(self.output_directory, filename)

        description_lines = description.split('\n')

        description_lines = description_lines[2:]

        # Join the remaining lines back together
        updated_description = '\n'.join(description_lines)

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(f"Title: {title}\n\n")
            file.write(updated_description)

    def save_metadata(self, problem_identifier, metadata):
        """Store metadata in JSON format, excluding the description."""
        filename = f"Metadata_{problem_identifier.replace('/', '_')}.json"
        filepath = os.path.join(self.output_directory, filename)

        # Remove description from metadata before saving it to the JSON file
        metadata_without_description = {key: value for key, value in metadata.items() if key != "description"}

        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(metadata_without_description, file, indent=2, ensure_ascii=False)

# Demonstration of functionality
if __name__ == "__main__":
    chromedriver_location = "C:\\Program Files (x86)\\chromedriver-win64\\chromedriver.exe"
    scraper = CFProblemScraper(chromedriver_location)
    for identifier in ['1/A', '1/B', '1/C', '2/A', '2/B', '2/C','3/A', '3/B', '3/C','4/A', '4/B', '4/C']:
        result = scraper.scrape_problem(identifier)
        if result:
            print(f"Scraped {identifier}: {result['title']}")
        else:
            print(f"Failed to scrape {identifier}")
