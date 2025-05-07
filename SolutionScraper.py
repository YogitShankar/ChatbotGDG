import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time
import os
import json
import requests
from requests.adapters import HTTPAdapter

class CodeforcesScraper:
    def __init__(self):
        self.base_url = "https://codeforces.com"
        self.max_retries = 3
        self.retry_delay = 5
        self.setup_browser()
        
class CodeforcesScraper:
    def __init__(self):
        self.base_url = "https://codeforces.com"
        self.max_retries = 3
        self.retry_delay = 5
        self.driver = None
        self.setup_browser()

    def setup_browser(self):
        """Setup browser with proper options"""
        options = uc.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        
        try:
            self.driver = uc.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 10)
        except Exception as e:
            print(f"Error initializing browser: {str(e)}")
            raise

    def close(self):
        """Close the browser safely"""
        try:
            if self.driver:
                # Store reference to driver and set instance variable to None
                driver = self.driver
                self.driver = None
                # Quit the stored reference
                driver.quit()
        except Exception as e:
            print(f"Error closing browser: {str(e)}")

    def retry_operation(self, operation, *args):
        """Simple retry mechanism for operations"""
        for attempt in range(self.max_retries):
            try:
                return operation(*args)
            except WebDriverException as e:
                if "net::ERR_NAME_NOT_RESOLVED" in str(e):
                    if attempt < self.max_retries - 1:
                        print(f"Network error occurred. Retrying in {self.retry_delay} seconds... (Attempt {attempt + 1}/{self.max_retries})")
                        time.sleep(self.retry_delay)
                        # Restart browser session
                        self.driver.quit()
                        self.setup_browser()
                        continue
                raise
            except Exception as e:
                if attempt < self.max_retries - 1:
                    print(f"Error occurred: {str(e)}. Retrying... (Attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(self.retry_delay)
                    continue
                raise
        return None

    def get_problem_links(self, page_number=None, problem_limit="all"):
        """Get problem links from a specific page with optional limit"""
        def _get_links():
            if page_number:
                url = f"{self.base_url}/problemset/page/{page_number}"
            else:
                url = f"{self.base_url}/problemset"
                
            self.driver.get(url)
            time.sleep(3)  # Increased wait time
            
            problems_table = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "problems"))
            )
            
            problem_links = []
            rows = problems_table.find_elements(By.TAG_NAME, "tr")
            
            rows = rows[1:]  # Skip header row
            if problem_limit != "all" and isinstance(problem_limit, int):
                rows = rows[:problem_limit]
                
            for row in rows:
                try:
                    td = row.find_element(By.CLASS_NAME, "id")
                    link = td.find_element(By.TAG_NAME, "a")
                    problem_links.append(link.get_attribute("href"))
                except Exception as e:
                    print(f"Error extracting problem link: {str(e)}")
                    continue
                    
            return problem_links

        return self.retry_operation(_get_links)


    def get_tutorial_link(self, problem_url):
        """Get the tutorial link for a specific problem"""
        def _get_tutorial():
            self.driver.get(problem_url)
            time.sleep(3)
            
            sidebar = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "sidebar-menu"))
            )
            
            tutorial_link = sidebar.find_element(
                By.XPATH, ".//a[contains(@title, 'Editorial') or contains(text(), 'Tutorial')]"
            )
            href = tutorial_link.get_attribute("href")
            
            # If the href is a relative path, prepend the base_url
            if href.startswith('/'):
                return self.base_url + href
            return href  # Return the full URL as is if it's already absolute

        return self.retry_operation(_get_tutorial)


    def get_solution(self, tutorial_url, problem_name):
        """Extract solution from tutorial page for specific problem"""
        def _get_solution():
            self.driver.get(tutorial_url)
            time.sleep(3)
            
            content = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "ttypography"))
            )
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            typography = soup.find('div', class_='ttypography')
            
            if not typography:
                print("Typography div not found")
                return None
                
            found_problem = False
            for element in typography.find_all(['p', 'div']):
                if not found_problem and element.name == 'p' and problem_name.lower() in element.text.lower():
                    found_problem = True
                    continue
                    
                if found_problem and element.name == 'div' and 'spoiler' in element.get('class', []):
                    spoiler_content = element.find('div', class_='spoiler-content')
                    if spoiler_content:
                        solution_texts = []
                        for p in spoiler_content.find_all('p'):
                            solution_texts.append(p.text.strip())
                        return '\n'.join(solution_texts)
            
            return None

        return self.retry_operation(_get_solution)

    def close(self):
        """Close the browser safely"""
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
        except Exception as e:
            print(f"Error closing browser: {str(e)}")

def get_user_input():
    """Get pagination and problem limit preferences from user"""
    try:
        start_page = int(input("Enter start page number (1 for first page): "))
        end_page = int(input("Enter end page number: "))
        problems_per_page = input("Enter number of problems to scrape per page (or 'all' for all problems): ")
        
        if problems_per_page.lower() != 'all':
            problems_per_page = int(problems_per_page)
            
        return start_page, end_page, problems_per_page
    except ValueError:
        print("Invalid input. Please enter valid numbers for pages and problems.")
        return get_user_input()

def main():
    scraper = None
    try:
        start_page, end_page, problems_per_page = get_user_input()
        
        scraper = CodeforcesScraper()
        
        os.makedirs("solutions", exist_ok=True)
        
        for page_num in range(start_page, end_page + 1):
            print(f"\nProcessing page {page_num}")
            
            try:
                if page_num == 1:
                    problem_links = scraper.get_problem_links(problem_limit=problems_per_page)
                else:
                    problem_links = scraper.get_problem_links(page_num, problems_per_page)
                
                if not problem_links:
                    print(f"No problems found on page {page_num}")
                    continue
                
                for problem_url in problem_links:
                    try:
                        problem_name = problem_url.split('/')[-1]
                        print(f"\nProcessing problem: {problem_name}")
                        
                        tutorial_link = scraper.get_tutorial_link(problem_url)
                        if tutorial_link:
                            solution = scraper.get_solution(tutorial_link, problem_name)
                            if solution:
                                print(f"Solution found for problem {problem_name}")
                                with open(f"solutions/solution_{problem_name}.txt", "w", encoding="utf-8") as f:
                                    f.write(f"Problem URL: {problem_url}\n")
                                    f.write(f"Tutorial URL: {tutorial_link}\n\n")
                                    f.write(solution)
                            else:
                                print(f"No solution found for problem {problem_name}")
                        else:
                            print(f"No tutorial link found for problem {problem_name}")
                    except Exception as e:
                        print(f"Error processing problem {problem_url}: {str(e)}")
                        continue
                
                print(f"Completed page {page_num}")
                
            except Exception as e:
                print(f"Error processing page {page_num}: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Fatal error: {str(e)}")
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main()