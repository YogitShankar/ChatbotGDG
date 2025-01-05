import os
import json
import cloudscraper
from bs4 import BeautifulSoup

problem_file = "problems.txt"
metadata_file = "metadata.json"

# Create a cloudscraper instance to bypass CAPTCHA
scraper = cloudscraper.create_scraper()

# Initialize metadata list if the file exists
if os.path.exists(metadata_file):
    with open(metadata_file, "r", encoding="utf-8") as meta_file:
        metadata_list = json.load(meta_file)
else:
    metadata_list = []

for page in range(1, 50):
    page_link = f"https://codeforces.com/problemset/page/{page}"
    try:
        prob_page_html = scraper.get(page_link).text
        soup_prob_list = BeautifulSoup(prob_page_html, 'html.parser')
        table = soup_prob_list.find("table", class_="problems")
        href_links = [
            a['href'] for td in table.find_all("td", class_="id")
            for a in td.find_all('a')
        ]
    except Exception as e:
        print(f"Error fetching problem list on page {page}: {e}")
        continue

    with open(problem_file, "a", encoding="utf-8") as prob_file:
        for links in href_links:
            problem_link = f"https://codeforces.com{links}"  # Full URL
            problem_id = [links.split('/')[-2],links.split('/')[-1]]
            problem_id = " ".join(problem_id)

            try:
                # Fetch the problem page
                page_html = scraper.get(problem_link).text
                soup = BeautifulSoup(page_html, 'html.parser')

                # Extract data
                try:
                    time_limit = soup.find("div", class_="time-limit").text.strip()
                except AttributeError:
                    time_limit = "Time limit not found"
                
                try:
                    memory_limit = soup.find("div", class_="memory-limit").text.strip()
                except AttributeError:
                    memory_limit = "Memory limit not found"

                try:
                    problem_title = soup.find("div", class_="title").text.strip()
                except AttributeError:
                    problem_title = "Problem title not found"

                try:
                    parent_div = soup.find('div', {'class': 'problem-statement'})
                    all_ps = parent_div.find_all('p')
                    prob_statement = " ".join(p.text.strip() for p in all_ps)
                except AttributeError:
                    prob_statement = "Problem statement not found"

                try:
                    input_specs = soup.find('div', class_="input-specification").text.strip()
                except AttributeError:
                    input_specs = "Input specification not found"

                try:
                    output_specs = soup.find('div', class_="output-specification").text.strip()
                except AttributeError:
                    output_specs = "Output specification not found"

                try:
                    sample_tests = soup.find('div', class_="sample-tests").text.strip()
                except AttributeError:
                    sample_tests = "Sample tests not found"

                try:
                    prob_tags = soup.find_all('span', class_="tag-box")
                    problem_tags = " ".join(tag.text.strip() for tag in prob_tags)
                except AttributeError:
                    problem_tags = "Problem tags not found"

                # Write to problem file
                prob_file.write(f"Problem ID: {problem_id}\n")
                prob_file.write(f"Problem Statement:\n{prob_statement}\n")
                prob_file.write(f"Input Specification:\n{input_specs}\n")
                prob_file.write(f"Output Specification:\n{output_specs}\n")
                prob_file.write(f"Sample Tests:\n{sample_tests}\n")
                prob_file.write("-" * 50 + "\n")

                # Add metadata if it doesn't already exist

                
                metadata_list.append({
                    "problem_id": problem_id,
                    "problem_title": problem_title,
                    "time_limit": time_limit,
                    "memory_limit": memory_limit,
                    "problem_tags": problem_tags,
                    })

            except Exception as e:
                print(f"Error fetching or processing problem {problem_id}: {e}")
                continue

# Write updated metadata to JSON file
try:
    with open(metadata_file, "w", encoding="utf-8") as meta_file:
        json.dump(metadata_list, meta_file, indent=4, ensure_ascii=False)
except Exception as e:
    print(f"Error writing metadata file: {e}")

print("Data extraction complete!")
