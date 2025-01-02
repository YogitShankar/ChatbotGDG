import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json

#this is final 

def extract_problem_details(soup):
    """Extract all problem details from the problem page."""
    problem_data = {}

    # Helper function to add spaces around MathJax elements
    def add_spaces_around_mathjax_in_soup(soup_element):
        """Add spaces around MathJax elements in the given soup element."""
        for mathjax in soup_element.find_all(class_='MathJax'):
            if mathjax.string:  # Only proceed if the MathJax element has text content
                mathjax.string = f" {mathjax.string.strip()} "

    # Find the problem-statement div
    problem_statement = soup.find('div', class_='problem-statement')
    if not problem_statement:
        return None

    # Add spaces to MathJax elements in the problem statement
    add_spaces_around_mathjax_in_soup(problem_statement)

    # Extract header information
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

    # Extract examples
    sample_tests = problem_statement.find('div', class_='sample-tests')
    if sample_tests:
        examples = []
    sample_test_divs = sample_tests.find_all('div', class_='sample-test')
    for test_div in sample_test_divs:
        example = {}

        # Get input
        input_div = test_div.find('div', class_='input')
        if input_div:
            input_pre = input_div.find('pre')
            example['input'] = input_pre.get_text(separator="\n", strip=True) if input_pre else ''

        # Get output
        output_div = test_div.find('div', class_='output')
        if output_div:
            output_pre = output_div.find('pre')
            example['output'] = output_pre.get_text(separator="\n", strip=True) if output_pre else ''

        examples.append(example)
    problem_data['examples'] = examples


    # Extract note if exists
    note = problem_statement.find('div', class_='note')
    problem_data['note'] = note.get_text(strip=True).replace('Note', '', 1).strip() if note else ''

    return problem_data


def scrape_codeforces_problems(start_page, end_page, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize undetected ChromeDriver
    driver = uc.Chrome()
    
    base_url = "https://codeforces.com/problemset/page/"
    
    try:
        # First pass: Collect all problem links
        problem_links = []
        for page in range(start_page, end_page + 1):
            url = f"{base_url}{page}"
            print(f"Collecting links from page: {url}")
            
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "pageContent"))
            )
            
            soup = BeautifulSoup(driver.page_source, "html.parser")
            page_content = soup.find("div", {"id": "pageContent"})
            
            if page_content:
                table = page_content.find("table", {"class": "problems"})
                if table:
                    rows = table.find_all("tr")
                    for row in rows:
                        id_td = row.find("td", {"class": ["id left", "id dark left"]})
                        if id_td:
                            a_tag = id_td.find("a")
                            if a_tag:
                                problem_text = a_tag.text.strip()
                                problem_link = f"https://codeforces.com{a_tag['href']}"
                                problem_links.append((problem_text, problem_link))
            
            time.sleep(2)
        
        # Second pass: Visit each problem page and extract details
        print("\nCollecting problem details...")
        for problem_id, link in problem_links:
            try:
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
                driver.execute_script(
                    "MathJax.Hub.Queue(function () { console.log('MathJax Ready!'); });"
                )
                time.sleep(3)  # Allow rendering time
                
                # Extract problem details
                soup = BeautifulSoup(driver.page_source, "html.parser")
                problem_data = extract_problem_details(soup)
                
                if problem_data:
                    # Save problem data to JSON file
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(problem_data, f, ensure_ascii=False, indent=2)
                    
                    # Also save a formatted text version
                    text_file = os.path.join(output_dir, f"problem_{safe_filename}.txt")
                    with open(text_file, "w", encoding="utf-8") as f:
                        f.write(f"Title: {problem_data['title']}\n")
                        f.write(f"Time Limit: {problem_data['time_limit']}\n")
                        f.write(f"Memory Limit: {problem_data['memory_limit']}\n\n")
                        f.write("Problem Description:\n")
                        f.write(problem_data['description'] + "\n\n")
                        f.write("Input Specification:\n")
                        f.write(problem_data['input_specification'] + "\n\n")
                        f.write("Output Specification:\n")
                        f.write(problem_data['output_specification'] + "\n\n")
                        f.write("Examples:\n")
                        for i, example in enumerate(problem_data['examples'], 1):
                            f.write(f"Example {i}:\n")
                            f.write("Input:\n")
                            f.write(example['input'] + "\n")
                            f.write("Output:\n")
                            f.write(example['output'] + "\n\n")
                        if problem_data['note']:
                            f.write("Note:\n")
                            f.write(problem_data['note'] + "\n")
                
                time.sleep(2)
                
            except Exception as e:
                print(f"Error scraping problem {problem_id}: {str(e)}")
                continue
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    start_page = int(input("Enter the start page number: "))
    end_page = int(input("Enter the end page number: "))
    output_dir = "codeforces_problems2"
    
    # Clear existing directory if needed
    if os.path.exists(output_dir):
        import shutil
        shutil.rmtree(output_dir)
        print(f"Cleared existing {output_dir} directory")
    
    scrape_codeforces_problems(start_page, end_page, output_dir)
