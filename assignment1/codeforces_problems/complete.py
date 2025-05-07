import cloudscraper
from bs4 import BeautifulSoup
import os
import json
import time

def fetch_problem_links(start_page, end_page):
    scraper = cloudscraper.create_scraper()
    base_url = "https://codeforces.com/problemset/page/"
    problem_links = []
    
    for page in range(start_page, end_page + 1):
        print(f"Fetching problem links from page: {page}")
        url = f"{base_url}{page}"
        response = scraper.get(url)
        time.sleep(1)  # Rate limiting to avoid server overload

        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", {"class": "problems"})

        if table:
            rows = table.find_all("tr")
            for row in rows:
                id_td = row.find("td", {"class": ["id", "id dark"]})
                tag_td = row.find("td", {"class": "tags"})  # Extract problem tags
                
                if id_td:
                    a_tag = id_td.find("a")
                    if a_tag:
                        problem_text = a_tag.text.strip()
                        problem_link = f"https://codeforces.com{a_tag['href']}"
                        tags = [tag.text.strip() for tag in tag_td.find_all("a")] if tag_td else []
                        problem_links.append((problem_text, problem_link, tags))
        else:
            print(f"No problems found on page {page}.")
    return problem_links

def fetch_problem_details(url):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    time.sleep(1)  # Rate limiting
    
    soup = BeautifulSoup(response.content, "html.parser")
    problem_statement = soup.find("div", class_="problem-statement")
    
    if not problem_statement:
        print(f"Problem content not found at {url}.")
        return None

    # Extracting LaTeX Math (if any)
    mathjax = problem_statement.find_all("span", class_="mathjax")
    for math in mathjax:
        math.replace_with(f"$$ {math.text} $$")
    
    problem_text = problem_statement.get_text(separator="\n").strip()
    problem_metadata = {
        "name": problem_statement.find("div", class_="title").text.strip() if problem_statement.find("div", class_="title") else "N/A",
        "time_limit": problem_statement.find("div", class_="time-limit").text.strip() if problem_statement.find("div", class_="time-limit") else "N/A",
        "memory_limit": problem_statement.find("div", class_="memory-limit").text.strip() if problem_statement.find("div", class_="memory-limit") else "N/A",
        "input": problem_statement.find("div", class_="input-specification").text.strip() if problem_statement.find("div", class_="input-specification") else "N/A",
        "output": problem_statement.find("div", class_="output-specification").text.strip() if problem_statement.find("div", class_="output-specification") else "N/A",
    }
    return problem_text, problem_metadata

def fetch_editorial_details(problem_url):
    editorial_url = problem_url.replace("/problem/", "/problemset/problem/") + "/tutorial"
    scraper = cloudscraper.create_scraper()
    response = scraper.get(editorial_url)
    time.sleep(1)  # Rate limiting
    
    soup = BeautifulSoup(response.content, "html.parser")
    editorial_content = soup.find("div", class_="content")
    
    return editorial_content.get_text(separator="\n").strip() if editorial_content else "No editorial available."

def scrape_codeforces_problems(start_page, end_page, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    problem_links = fetch_problem_links(start_page, end_page)
    print(f"Collected {len(problem_links)} problems.")
    
    for problem_id, problem_url, tags in problem_links:
        print(f"Fetching details for problem: {problem_id}")
        problem_text, problem_metadata = fetch_problem_details(problem_url) or (None, None)
        
        if problem_text and problem_metadata:
            editorial_text = fetch_editorial_details(problem_url)
            
            safe_filename = "".join(c for c in problem_id if c.isalnum() or c in (' ', '-', '_')).strip()
            problem_txt_file = os.path.join(output_dir, f"problem_{safe_filename}.txt")
            problem_json_file = os.path.join(output_dir, f"problem_{safe_filename}.json")
            editorial_txt_file = os.path.join(output_dir, f"editorial_{safe_filename}.txt")
            
            with open(problem_txt_file, "w", encoding="utf-8") as f:
                f.write(problem_text)
            
            problem_metadata["tags"] = tags
            with open(problem_json_file, "w", encoding="utf-8") as f:
                json.dump(problem_metadata, f, ensure_ascii=False, indent=2)
            
            with open(editorial_txt_file, "w", encoding="utf-8") as f:
                f.write(editorial_text)
            
            print(f"Saved problem {problem_id} and editorial.")
        else:
            print(f"Skipping problem {problem_id} due to missing content.")

if __name__ == "__main__":
    start_page = int(input("Enter the start page number: "))
    end_page = int(input("Enter the end page number: "))
    output_dir = "codeforces_problems"
    scrape_codeforces_problems(start_page, end_page, output_dir)
