import os
import time
import random
import re
import json
import cloudscraper
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def sanitize_filename(filename):
    """Sanitize the filename by removing invalid characters."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def extract(start_page=4, end_page=5, base_url='https://codeforces.com/problemset/page/'):
    # Prepare output directories
    text_output_dir = "./data/problem_statement"
    json_output_dir = "./data/problems_metadata"
    os.makedirs(json_output_dir, exist_ok=True)
    os.makedirs(text_output_dir, exist_ok=True)

    # Initialize a list to store problem metadata
    metadata = []

    # Create cloudscraper instance for bypassing CAPTCHA
    scraper = cloudscraper.create_scraper()

    # Set up Selenium WebDriver
    driver_path = '/Users/shivalasya/Desktop/chatbot/chromedriver-mac-arm64/chromedriver'
    service = Service(driver_path)

    def create_driver():
        return webdriver.Chrome(service=service)

    # Initialize the driver for Selenium
    driver = create_driver()

    def format_mathjax(element):
        math_content = ""
        mathml_data = element.get('data-mathml')

        if mathml_data:
            math_soup = BeautifulSoup(mathml_data, 'xml')
            for part in math_soup.find_all(['msub', 'msup', 'mn', 'mi', 'mo']):
                if part.name == 'msub':  # Subscript
                    base = part.find('mi').get_text(strip=True)
                    sub = part.find(['mn', 'mi']).get_text(strip=True)
                    math_content += f"{base}_{sub}"
                elif part.name == 'msup':  # Superscript
                    base = part.find(['mn', 'mi']).get_text(strip=True)
                    sup = part.find(['mn', 'mi']).get_text(strip=True)
                    math_content += f"{base}^{sup}"
                else:
                    math_content += part.get_text(strip=True)
        else:
            for part in element.descendants:
                if part.name == 'sup':
                    math_content += f"^{part.get_text(strip=True)}"
                elif part.name == 'sub':
                    math_content += f"_{part.get_text(strip=True)}"
                elif part.string:
                    math_content += part.string.strip()

        return math_content

    for page in range(start_page, end_page + 1):
        page_url = f"{base_url}{page}"
        print(f"Processing page {page_url}...")

        try:
            # Use cloudscraper to get the HTML of the page (to bypass CAPTCHA)
            page_html = scraper.get(page_url).text

            # Parse the page source using BeautifulSoup
            soup = BeautifulSoup(page_html, 'html.parser')

            # Find all <td> elements containing problem details
            td_elements = soup.find_all('td')

            if not td_elements:
                print(f"No problem entries found on page {page}")
                continue

            for td in td_elements:
                # Extract problem URL
                left_div = td.find('div', style="float: left;")
                if left_div and left_div.a:
                    relative_url = left_div.a['href']  # Relative URL
                    full_url = f"https://codeforces.com{relative_url}"  # Absolute URL
                    problem_title = left_div.a.text.strip()
                    print(f"Processing problem: {full_url}")

                    # Split the URL by '/' to get its components
                    parts = full_url.split('/')
                    # Identify the indices based on the structure of the URL
                    contest_id = parts[5]  
                    problem_index = parts[6]

                    # Extract problem tags (right side)
                    right_div = td.find('div', style="float: right; font-size: 1.1rem; padding-top: 1px; text-align: right;")
                    tags = [a.text.strip() for a in right_div.find_all('a')] if right_div else []
                    if not tags:  # If no tags, set to "NA"
                        tags = ["NA"]

                    try:
                        # Use cloudscraper to get the problem page (to bypass CAPTCHA)
                        problem_html = scraper.get(full_url).text

                        # Parse the problem page
                        problem_soup = BeautifulSoup(problem_html, 'html.parser')

                        # Extract header details
                        header_section = problem_soup.find('div', class_='header')
                        time_limit = ""
                        memory_limit = ""
                        title = ""

                        if header_section:
                            time_limit_elem = header_section.find('div', class_='time-limit')
                            memory_limit_elem = header_section.find('div', class_='memory-limit')
                            title_elem = header_section.find('div', class_='title')

                            time_limit = time_limit_elem.get_text(strip=True) if time_limit_elem else "Not available"
                            memory_limit = memory_limit_elem.get_text(strip=True) if memory_limit_elem else "Not available"
                            title = title_elem.get_text(strip=True) if title_elem else "Not available"

                         # Prepare metadata entry
                        problem_metadata = {
                        "contest_id_problem_index": f"{contest_id}-{problem_index}",
                        "title": problem_title,
                        "url": full_url,
                        "tags": tags,
                        "time_limit": time_limit,
                        "memory_limit": memory_limit
                        }
                        metadata.append(problem_metadata)

                        # Problem statement
                        problem_statement = ""
                        problem_statement_element = problem_soup.find('div', class_='problem-statement')

                        if problem_statement_element:
                            for div in problem_statement_element.find_all('div'):
                                for content in div.contents:
                                    if content.name == 'ul' or content.name == 'ol':
                                        for li in content.find_all('li'):
                                            text_parts = []
                                            for sub_content in li.contents:
                                                if sub_content.name == 'span' and 'mathjax' in sub_content.get('class', []):
                                                    mathjax_output = format_mathjax(sub_content) 
                                                    text_parts.append(mathjax_output)
                                                elif sub_content.string:
                                                    text_parts.append(sub_content.string.strip())
                                            problem_statement += "- " + " ".join(text_parts) + "\n"

                                    elif content.name == 'p':
                                        text_parts = []
                                        for sub_content in content.contents:
                                            if sub_content.name == 'span' and 'mathjax' in sub_content.get('class', []):
                                                mathjax_output =  format_mathjax(sub_content) 
                                                text_parts.append(mathjax_output)
                                            elif sub_content.string:
                                                text_parts.append(sub_content.string.strip())
                                        problem_statement += " ".join(text_parts) + "\n\n"

                        # Sample Input and Output
                        sample_tests = ""
                        tests = problem_soup.find('div', class_="sample-test")

                        if tests:
                            for test in tests.find_all('div'):
                                if 'input' in test.get('class', []):
                                    sample_tests += "\nSample Input:\n"
                                    for pre in test.find_all('pre'):
                                        divs = pre.find_all('div', class_='test-example-line')
                                        if divs:
                                            # Iterate over the divs and output them line by line
                                            for i in range(0, len(divs), 2):
                                                sample_tests += divs[i].get_text(strip=True) + "\n"  # Value line
                                                if i + 1 < len(divs):  # Ensure i+1 is within bounds
                                                    sample_tests += divs[i + 1].get_text(strip=True) + "\n"  # Direction line
                                        else:
                                            # If no divs found, just output the <pre> content
                                            sample_tests += pre.get_text(strip=True) + "\n\n"
                                        
                                elif 'output' in test.get('class', []):
                                    sample_tests += "\nSample Output:\n"
                                    for pre in test.find_all('pre'):
                                        output_data = pre.get_text(strip=True).splitlines()
                                        for line in output_data:
                                            sample_tests += line.strip() + "\n"
                        
                        latex_replacements = [
                        ("\\le", "≤"),("\\ge", "≥"), ("\\neq", "≠"),  ("\\in", "∈"),  ("\\notin", "∉"),  ("\\subset", "⊂"),  ("\\supset", "⊃"),  ("\\subseteq", "⊆"),  
                        ("\\cup", "∪"),  ("\\cap", "∩"),  ("\\implies", "⇒"), ("\\iff", "⇔"),  ("\\forall", "∀"),  ("\\exists", "∃"),  ("\\nexists", "∄"),  
                        ("\\cdot", "·"),  ("\\to", "→"), ("\\leftarrow", "←"),  ("\\rightarrow", "→"),  ("\\Rightarrow", "⇒"), ("\\leftrightarrow", "↔"),  
                        ("\\sim", "∼"), ("\\approx", "≈"), ("\\angle", "∠"),  ("\\infty", "∞"),  ("\\partial", "∂"),  ("\\sum", "∑"),
                        ("\\equiv","≡"),("\not \equiv","≢"),("\\ldots","...") ,("\\ne","≠"),("\\times","x"), ("\\supseteq", "⊇"),
                        ]

                        for latex, symbol in latex_replacements:
                            problem_statement = problem_statement.replace(latex, symbol)

                        problem_statement = problem_statement.replace("$$$", "")
                        # Save results to a text file
                        if title:  # Only save if title is extracted successfully
                            
                            problem_filename = os.path.join(text_output_dir, f"{sanitize_filename(problem_title)}.txt")
                            with open(problem_filename, "w", encoding="utf-8") as f:
                                f.write(f"Title: {title}\n\n")
                                f.write(f"Time Limit: {time_limit}\n")
                                f.write(f"Memory Limit: {memory_limit}\n\n")
                                f.write(f"Statement:\n{problem_statement}\n\n")
                                f.write(f"Sample Tests:{sample_tests}\n")

                            # Save metadata in JSON file
                            json_filename = os.path.join(json_output_dir, "metadata.json")
                            with open(json_filename, "w", encoding="utf-8") as json_file:
                                json.dump(metadata, json_file, indent=4)
                                
                            print(f"Fetched problem details for: {title}")
                        else:
                            print(f"Failed to fetch details for problem at {full_url}")

                        # Random delay after processing each problem
                        time.sleep(random.uniform(5, 10))

                    except Exception as e:
                        print(f"Error processing problem {full_url}: {e}")

        except Exception as e:
            print(f"Error processing page {page}: {e}")

    driver.quit()

extract()
