import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import os
import json
import time
import random
from selenium.webdriver.support.ui import WebDriverWait

def clean_unicode_text(text):

    replacements = {
        '\u2009': ' ',
        '\u2014': '-',
        '\u2264': '<=',
        '\u00ab': '"',
        '\u00bb': '"'
    }
    for code, replacement in replacements.items():
        text = text.replace(code, replacement)
    return text

def create_problem_file(problem_dict, output_dir='data/problems'):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"{output_dir}/{problem_dict['problem_tag']}.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Problem: {problem_dict['problem_tag']} - {problem_dict['title']}\n")
        f.write(f"Link: {problem_dict['link']}\n\n")

        f.write("Description:\n")
        f.write(clean_unicode_text(problem_dict.get('description', 'N/A')))
        f.write("\n\n")

        f.write("Input Specification:\n")
        f.write(clean_unicode_text(problem_dict.get('input_specification', 'N/A')))
        f.write("\n\n")

        f.write("Output Specification:\n")
        f.write(clean_unicode_text(problem_dict.get('output_specification', 'N/A')))
        f.write("\n\n")

        f.write(f"Time Limit: {problem_dict.get('time_limit', 'N/A')}\n")
        f.write(f"Memory Limit: {problem_dict.get('memory_limit', 'N/A')}\n")

        f.write("\nTags: ")
        f.write(", ".join(problem_dict.get('tags', [])))
def create_problem_json(problem_dict, output_dir='data/problems'):
    """Create a JSON file for a problem in the same directory as text files"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"{output_dir}/{problem_dict['problem_tag']}.json"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(problem_dict, f, ensure_ascii=False, indent=4)
def random_delay():
    delay = random.uniform(5, 10)
    time.sleep(delay)

driver = uc.Chrome()

driver.get("https://codeforces.com/problemset?order=BY_RATING_ASC")
wait = WebDriverWait(driver, 10)
random_delay()

problems_table = driver.find_element(By.CLASS_NAME, "problems")

problem_rows = problems_table.find_elements(By.TAG_NAME, "tr")

problems = []

for row in problem_rows[1:]:
    try:
        link_tags = row.find_elements(By.TAG_NAME, "a")
        problem_tag = link_tags[0].text.strip()
        title = link_tags[1].text.strip()
        link = link_tags[1].get_attribute("href")
        problem_data = {
            "problem_tag": problem_tag,
            "title": title,
            "link": link
        }
        problems.append(problem_data)
    except Exception as e:
        print(f"Error extracting data for a row: {e}")

def random_delay(min_delay=5, max_delay=10):
    delay = random.uniform(min_delay, max_delay)
    print(f"Delaying for {delay:.2f} seconds...")
    time.sleep(delay)

for idx, problem in enumerate(problems[:]):
    try:

        random_delay()

        link = problem["link"]
        driver.get(link)

        problem_data = {}
        random_delay()

        # Description
        problem_statement_div = driver.find_element(By.CLASS_NAME, "problem-statement")
        random_delay(1, 3)  # Small delay before accessing problem description
        problem_statement = problem_statement_div.find_element(By.XPATH, "./div[not(@class)][1]")
        paragraphs = problem_statement.find_elements(By.TAG_NAME, "p")
        problem_paragraphs = [p.text for p in paragraphs]
        problem_data["description"] = "\n".join(problem_paragraphs)

        # Input specification
        input_spec = problem_statement_div.find_element(By.CLASS_NAME, "input-specification")
        random_delay(1, 3)  # Small delay before accessing input specification
        input_para = input_spec.find_elements(By.TAG_NAME, "p")
        problem_data["input_specification"] = "\n".join([p.text for p in input_para])

        # Output specification
        output_spec = problem_statement_div.find_element(By.CLASS_NAME, "output-specification")
        random_delay(1, 3)  # Small delay before accessing output specification
        output_para = output_spec.find_elements(By.TAG_NAME, "p")
        problem_data["output_specification"] = "\n".join([p.text for p in output_para])

        # Time and memory limits
        time_limit_div = problem_statement_div.find_element(By.CLASS_NAME, "time-limit")
        time_value = time_limit_div.text.split("time limit per test")[-1].strip().replace('\n', '').strip()
        random_delay(1, 3)  # Small delay before accessing time limits
        problem_data["time_limit"] = time_value

        memory_limit_div = problem_statement_div.find_element(By.CLASS_NAME, "memory-limit")
        memory_value = memory_limit_div.text.split("memory limit per test")[-1].strip().replace('\n', '').strip()
        random_delay(1, 3)  # Small delay before accessing memory limits
        problem_data["memory_limit"] = memory_value

        # Problem tags
        side_bar = driver.find_element(By.ID, "sidebar")
        problem_tags = side_bar.find_elements(By.CLASS_NAME, "tag-box")
        problem_data["tags"] = [t.text for t in problem_tags]

        problems[idx].update(problem_data)

        print(f"Extracted data for problem {idx + 1} successfully!")

        random_delay(7, 12)

    except Exception as e:
        print(f"Error extracting information for problem {idx + 1}: {e}")

print(json.dumps(problems[:], ensure_ascii=False, indent=4))

for problem in problems[:]:
    create_problem_file(problem)
    create_problem_json(problem)

driver.quit()