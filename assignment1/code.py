# Import necessary libraries
import undetected_chromedriver as uc  # For avoiding detection during web scraping
from bs4 import BeautifulSoup  # For parsing HTML content
from selenium.webdriver.common.by import By  # For locating elements by attributes
from selenium.webdriver.support.ui import WebDriverWait  # For waiting until an element appears
from selenium.webdriver.support import expected_conditions as EC  # For defining wait conditions
import time  # For adding delays between operations
import os  # For handling file and directory operations
import json  # For saving data in JSON format

def extract_problem_details(soup):
    """
    Extracts all problem details (title, description, input/output specs, examples, etc.) 
    from a Codeforces problem page.
    """
    problem_data = {}  # Dictionary to store problem details

    # Helper function to add spaces around MathJax elements
    def add_spaces_around_mathjax_in_soup(soup_element):
        """Add spaces around MathJax elements in the given soup element."""
        for mathjax in soup_element.find_all(class_='MathJax'):
            if mathjax.string:  # Only proceed if the MathJax element has text content
                mathjax.string = f" {mathjax.string.strip()} "

    # Find the problem-statement div
    problem_statement = soup.find('div', class_='problem-statement')
    if not problem_statement:
        return None  # Return None if problem statement is not found

    # Add spaces to MathJax elements in the problem statement
    add_spaces_around_mathjax_in_soup(problem_statement)

    # Extract header information (title, time limit, memory limit)
    header = problem_statement.find('div', class_='header')
    if header:
        # Get title
        title_div = header.find('div', class_='title')
        problem_data['title'] = title_div.text.strip() if title_div else ''

        # Get time limit
        time_limit = header.find('div', class_='time-limit')
        problem_data['time_limit'] = time_limit.text.replace('time limit per test', '').strip() if time_limit else ''

        # Get memory limit
        memory_limit = header.find('div', class_='memory-limit')
        problem_data['memory_limit'] = memory_limit.text.replace('memory limit per test', '').strip() if memory_limit else ''

    # Extract problem description
    description = []
    for p in problem_statement.find_all('p'):
        if not any(p.find_parents(class_=['input-specification', 'output-specification', 'sample-tests', 'note'])):
            description.append(p.get_text(strip=True))
    problem_data['description'] = '\n'.join(description)

    # Extract input specification
    input_spec = problem_statement.find('div', class_='input-specification')
    problem_data['input_specification'] = input_spec.get_text(strip=True).replace('Input', '', 1).strip() if input_spec else ''

    # Extract output specification
    output_spec = problem_statement.find('div', class_='output-specification')
    problem_data['output_specification'] = output_spec.get_text(strip=True).replace('Output', '', 1).strip() if output_spec else ''

    # Extract examples (input-output pairs)
    sample_tests = problem_statement.find('div', class_='sample-tests')
    examples = []
    if sample_tests:
        sample_test_divs = sample_tests.find_all('div', class_='sample-test')
        for test_div in sample_test_divs:
            example = {}

            # Get input example
            input_div = test_div.find('div', class_='input')
            if input_div:
                input_pre = input_div.find('pre')
                example['input'] = input_pre.get_text(separator="\n", strip=True) if input_pre else ''

            # Get output example
            output_div = test_div.find('div', class_='output')
            if output_div:
                output_pre = output_div.find('pre')
                example['output'] = output_pre.get_text(separator="\n", strip=True) if output_pre else ''

            examples.append(example)
    problem_data['examples'] = examples

    # Extract note if it exists
    note = problem_statement.find('div', class_='note')
    problem_data['note'] = note.get_text(strip=True).replace('Note', '', 1).strip() if note else ''

    return problem_data


def scrape_codeforces_problems(start_page, end_page, output_dir):
    """
    Scrapes problem data from Codeforces problemset pages.
    Args:
    - start_page (int): Starting page number of the problemset.
    - end_page (int): Ending page number of the problemset.
    - output_dir (str): Directory to save the scraped data.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize undetected ChromeDriver
    driver = uc.Chrome()
    
    base_url = "https://codeforces.com/problemset/page/"  # Base URL for problem pages
    
    try:
        # First pass: Collect all problem links
        problem_links = []  # List to store problem links and IDs
        for page in range(start_page, end_page + 1):
            url = f"{base_url}{page}"
            print(f"Collecting links from page: {url}")
            
            # Open the page in the browser
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "pageContent"))
            )
            
            # Parse page content
            soup = BeautifulSoup(driver.page_source, "html.parser")
            page_content = soup.find("div", {"id": "pageContent"})
            
            if page_content:
                table = page_content.find("table", {"class": "problems"})
                if table:
                    rows = table.find_all("tr")  # Extract all rows in the problems table
                    for row in rows:
                        id_td = row.find("td", {"class": ["id left", "id dark left"]})
                        if id_td:
                            a_tag = id_td.find("a")
                            if a_tag:
                                problem_text = a_tag.text.strip()
                                problem_link = f"https://codeforces.com{a_tag['href']}"
                                problem_links.append((problem_text, problem_link))
            
            time.sleep(2)  # Pause to avoid being flagged as a bot
        
        # Second pass: Visit each problem page and extract details
        print("\nCollecting problem details...")
        for problem_id, link in problem_links:
            try:
                # Sanitize problem ID for use as a filename
                safe_filename = "".join(c for c in problem_id if c.isalnum() or c in (' ', '-', '_')).strip()
                output_file = os.path.join(output_dir, f"problem_{safe_filename}.json")
                
                # Skip if we already have this problem
                if os.path.exists(output_file):
                    print(f"Skipping {problem_id} - already scraped")
                    continue
                
                print(f"Scraping problem {problem_id} from {link}")
                driver.get(link)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "problem-statement"))
                )
                
                # Wait for MathJax to fully render
                time.sleep(3)  # Allow rendering time
                
                # Extract problem details
                soup = BeautifulSoup(driver.page_source, "html.parser")
                problem_data = extract_problem_details(soup)
                
                if problem_data:
                    # Save problem data to JSON file
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(problem_data, f, ensure_ascii=False, indent=2)
                
                time.sleep(2)  # Pause between requests
                
            except Exception as e:
                print(f"Error scraping problem {problem_id}: {str(e)}")
                continue
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        driver.quit()  # Close the browser


if __name__ == "__main__":
    # Collect user input for page range
    start_page = int(input("Enter the start page number: "))
    end_page = int(input("Enter the end page number: "))
    output_dir = "codeforces_problems2"  # Directory to store scraped problems
    
    # Clear existing directory if needed
    if os.path.exists(output_dir):
        import shutil
        shutil.rmtree(output_dir)
        print(f"Cleared existing {output_dir} directory")
    
    # Start the scraping process
    scrape_codeforces_problems(start_page, end_page, output_dir)
