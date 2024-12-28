# from selenium import webdriver
# path="C:\\Program Files (x86)\\chromedriver-win64\\chromedriver.exe"
# driver=webdriver.Chrome(path)

# driver.get("https://pingala.iitk.ac.in/IITK-0/logincheck")

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service



# # Set up the ChromeDriver service
# service = Service(executable_path=path)

# # Initialize the Chrome WebDriver
# driver = webdriver.Chrome(service=service)


# # Navigate to the desired URL
# driver.get("https://pingala.iitk.ac.in/IITK-0/logincheck")

# print(driver.title)

# # Keep the browser open until you press Enter
# input("Press Enter to close the browser...")
# driver.quit() # it closes the browser and to close the tab driver.close()

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import time

class CodeforcesScraper:
    def __init__(self, chrome_driver_path):
        self.chrome_driver_path = chrome_driver_path
        self.base_url = "https://codeforces.com"
        
        # Create data directory if it doesn't exist
        self.data_dir = "scraped_data"
        os.makedirs(self.data_dir, exist_ok=True)
    
    def setup_driver(self):
        """Setup and return Chrome WebDriver"""
        options = Options()
        options.add_argument("--start-maximized")
        service = Service(executable_path=self.chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    
    def scrape_problem(self, problem_id):
        """
        Scrape basic problem information
        For now, we'll just get the problem statement and examples
        """
        # Format URL
        url = f"{self.base_url}/problemset/problem/{problem_id}"
        print(f"Accessing URL: {url}")
        
        driver = self.setup_driver()
        try:
            # Load the page
            driver.get(url)
            print(f"Current URL: {driver.current_url}")
            
            # Wait for problem statement to load
            wait = WebDriverWait(driver, 20)
            problem_div = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "problem-statement"))
            )
            
            print("Problem statement found, extracting content...")
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            problem_statement = soup.find('div', class_='problem-statement')
            
            if not problem_statement:
                raise Exception("Could not find problem statement")
            
            # Extract basic information
            data = {}
            
            # Get problem title
            title_div = problem_statement.find('div', class_='title')
            if title_div:
                data['title'] = title_div.text.strip()
                print(f"Found title: {data['title']}")
            
            # Get problem limits
            limits = problem_statement.find_all('div', class_='time-limit')
            if limits:
                data['time_limit'] = limits[0].text.strip()
                print(f"Found time limit: {data['time_limit']}")
            
            memory_limit = problem_statement.find('div', class_='memory-limit')
            if memory_limit:
                data['memory_limit'] = memory_limit.text.strip()
                print(f"Found memory limit: {data['memory_limit']}")
            
            # # Get problem statement text


            # statement_div = problem_statement.find('div', recursive=False)
            # if statement_div:
            #     # Skip the first elements which contain title and limits
            #     problem_text = []
            #     for p in statement_div.find_all(['p', 'div']):
            #         if not any(c in p.get('class', []) for c in ['title', 'time-limit', 'memory-limit']):
            #             problem_text.append(p.text.strip())
            #     data['statement'] = '\n'.join(filter(None, problem_text))
            #     print("Found problem statement")


            # onemore_div=soup.find('div',class_='ttypography')
            # target_div = onemore_div.find_all("div")[2]
            # #text=target_div.get_text(strip=True)  # Prints text inside the div (if any)
            # if target_div:
            #  print("Target div found:", target_div)  # Debugging: Check what is inside target_div
            # else:
            #  print("Target div not found!")

            # data['statement']=target_div.text.strip()

            reference_div = soup.find('div', class_='header')  # Find reference div

            target_div = reference_div.find_next_sibling('div')  # Get the next sibling div
            question_statement=target_div.text.strip()
            print(question_statement)  # Extract text content
            data['statement']=question_statement



                 

                

            
            # Get sample tests
            samples = []
            sample_tests = problem_statement.find_all('div', class_='sample-test')
            for test in sample_tests:
                input_div = test.find('div', class_='input')
                output_div = test.find('div', class_='output')
                
                if input_div and output_div:
                    input_pre = input_div.find('pre')
                    output_pre = output_div.find('pre')
                    
                    if input_pre and output_pre:
                        samples.append({
                            'input': input_pre.text.strip(),
                            'output': output_pre.text.strip()
                        })
            
            data['samples'] = samples
            print(f"Found {len(samples)} sample tests")

            # getting tags
            tag_divs=soup.find_all('div',class_='roundbox borderTopRound borderBottomRound')
            tagss=[]
            if tag_divs:
                for tag_div in tag_divs:
                    span = tag_div.find('span', class_='tag-box')  # Find the nested span
                    if span:
                        tagss.append(span.text.strip())
            data['tags']=tagss

            
            # Save the data
            output_file = os.path.join(self.data_dir, f"problem_{problem_id.replace('/', '_')}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Data saved to {output_file}")
            return data
            
        except Exception as e:
            print(f"Error scraping problem {problem_id}: {str(e)}")
            try:
                print(f"Failed URL: {driver.current_url}")
            except:
                pass
            return None
            
        finally:
            time.sleep(3)  # Wait a bit before closing
            driver.quit()

# Example usage
if __name__ == "__main__":
    chrome_driver_path = "C:\\Program Files (x86)\\chromedriver-win64\\chromedriver.exe"
    scraper = CodeforcesScraper(chrome_driver_path)

    problem_array=['1/A','1/B','1/C','2/A','2/B','2/C']
    #problem_array=['2/A']
    
    # Test with problem 4A
    for problem in problem_array:
     print(f"\nTesting scraper with problem {problem}...")
     result = scraper.scrape_problem(problem)
    
     if result:
        print("\nSuccessfully scraped problem data:")
        print(f"Title: {result.get('title', 'Not found')}")
        print(f"Time Limit: {result.get('time_limit', 'Not found')}")
        print(f"Memory Limit: {result.get('memory_limit', 'Not found')}")
        print(f"Number of sample tests: {len(result.get('samples', []))}")
     else:
        print("\nFailed to scrape problem data")