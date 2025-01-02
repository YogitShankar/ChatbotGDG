import os
import json
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import re

# Convert LaTeX to readable
def latex_to_readable(latex):
    replacements = {
        r"\\leq": "≤",
        r"\\geq": "≥",
        r"\^": "^",
        r"\\times": "×",
        r"\\frac{(\w+)}{(\w+)}": r"(\1/\2)",
        r"\\": ""
    }
    for latex_symbol, readable in replacements.items():
        latex = re.sub(latex_symbol, readable, latex)
    return latex

def process_scraped_text(text):
    latex_parts = re.findall(r"\$\$\$(.+?)\$\$\$", text)
    for latex in latex_parts:
        readable = latex_to_readable(latex)
        text = text.replace(f"$$${latex}$$$", readable)
    return text

BASE_DIR = "scraped_data"
PROBLEMS_DIR = os.path.join(BASE_DIR, "problems")
EDITORIALS_DIR = os.path.join(BASE_DIR, "editorials")
os.makedirs(PROBLEMS_DIR, exist_ok=True)
os.makedirs(EDITORIALS_DIR, exist_ok=True)

# Selenium setup
def get_selenium_driver():
    try:
        driver = uc.Chrome()
        return driver
    except Exception as e:
        print(f"Error initializing ChromeDriver: {e}")
        exit(1)

def create_problem_directory(problem_id, contest_name, base_path=PROBLEMS_DIR):
    problem_dir = os.path.join(base_path, contest_name)
    os.makedirs(problem_dir, exist_ok=True)
    return {
        "statement": os.path.join(problem_dir, f"{problem_id}_statement.txt"),
        "metadata": os.path.join(problem_dir, f"{problem_id}_metadata.json")
    }

def update_metadata(metadata_path, data):
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = {}
    existing_data.update(data)
    with open(metadata_path, 'w') as f:
        json.dump(existing_data, f, indent=4)

def scrape_problem(problem_url, problem_id, contest_name):
    driver = get_selenium_driver()
    driver.get(problem_url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "problem-statement"))
        )
    except Exception as e:
        print(f"Problem page loading failed for {problem_url}: {e}")
        driver.quit()
        return

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract elements 
    title = soup.find("div", class_="title")
    title_text = title.text if title else f"Problem {problem_id}"
    
    statement = soup.select_one("#pageContent > div.problemindexholder > div.ttypography > div > div:nth-child(2)")
    input_spec = soup.find("div", class_="input-specification")
    output_spec = soup.find("div", class_="output-specification")
    sample_texts = soup.find("div", class_="sample-test")
    tags = [tag.get_text(strip=True) for tag in soup.find_all("span", class_="tag-box")] if soup.find_all("span", class_="tag-box") else []
    time_limit = soup.find("div", class_="time-limit")
    memory_limit = soup.find("div", class_="memory-limit")

    paths = create_problem_directory(problem_id, contest_name)

    # Write problem details
    with open(paths["statement"], 'w', encoding='utf-8') as f:
        if statement:
            f.write(process_scraped_text(statement.get_text()) + "\n")
        if input_spec:
            f.write(process_scraped_text(input_spec.get_text()) + "\n")
        if output_spec:
            f.write(process_scraped_text(output_spec.get_text()) + "\n")
        if sample_texts:
            for lines in sample_texts.find_all("div"):
                f.write(lines.get_text() + "\n")

    update_metadata(paths["metadata"], {
        "title": title_text,
        "tags": tags,
        "time_limit": time_limit.get_text(strip=True) if time_limit else "N/A",
        "memory_limit": memory_limit.get_text(strip=True) if memory_limit else "N/A"
    })
    print(f"Problem {problem_id} saved successfully.")

    driver.quit()

def scrape_editorial(editorial_url, contest_name):
    driver = get_selenium_driver()
    driver.get(editorial_url)

    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    except Exception as e:
        print(f"Editorial page loading failed for {editorial_url}: {e}")
        driver.quit()
        return

    hints = soup.find_all("div", class_="spoiler-content")

    editorial_dir = os.path.join(EDITORIALS_DIR, contest_name)
    os.makedirs(editorial_dir, exist_ok=True)
    editorial_path = os.path.join(editorial_dir, "editorial.txt")

    with open(editorial_path, 'w', encoding='utf-8') as f:
        if hints:
            for hint in hints:
                f.write(process_scraped_text(hint.get_text()) + "\n")
        else:
            f.write("No editorial content found.\n")

    print(f"Editorial for {contest_name} saved successfully.")
    driver.quit()

if __name__ == "__main__":
    codeforces_page = "https://codeforces.com/contests?complete=true"
    driver = get_selenium_driver()
    driver.get(codeforces_page)

    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        contestlist = soup.find("div", class_="contests-table").find_all("tr", limit=30)
    except Exception as e:
        print(f"Failed to load contest list: {e}")
        driver.quit()
        exit(1)

    for contest in contestlist:
        link = contest.find('a')
        if not link:
            continue

        contest_name = link.get('href').strip('/')
        contest_url = "https://codeforces.com" + link.get('href')
        print(f"Scraping contest: {contest_name} ({contest_url})")

        driver.get(contest_url)

        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            problems_table = soup.find("table", class_="problems")
        except Exception as e:
            print(f"Failed to load contest page {contest_url}: {e}")
            continue

        if not problems_table:
            print(f"No problems found for contest: {contest_name}")
            continue

        problems = problems_table.find_all("tr")[1:] 
        for problem in problems:
            problem_link = problem.find('a')
            if not problem_link:
                continue

            problem_id = problem_link.get_text(strip=True)
            problem_url = "https://codeforces.com" + problem_link.get('href')
            scrape_problem(problem_url, problem_id, contest_name)

        editorial_link = soup.select_one(
            "#sidebar > div.roundbox.sidebox.sidebar-menu.borderTopRound > ul > li:nth-child(2) > span:nth-child(1) > a"
        )
        if editorial_link:
            editorial_url = "https://codeforces.com" + editorial_link.get('href')
            scrape_editorial(editorial_url, contest_name)

    driver.quit()
