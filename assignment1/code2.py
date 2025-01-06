import cloudscraper
from bs4 import BeautifulSoup
import os
import json

# Function to scrape problem links from the given range of pages
def fetch_problem_links(start_page, end_page):
    scraper = cloudscraper.create_scraper()  # Initialize CloudScraper
    base_url = "https://codeforces.com/problemset/page/"
    problem_links = []

    # Loop through each page in the range
    for page in range(start_page, end_page + 1):
        print(f"Fetching problem links from page: {page}")
        url = f"{base_url}{page}"
        response = scraper.get(url)

        # Parse the HTML response
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", {"class": "problems"})  # Locate the problem table

        if table:
            rows = table.find_all("tr")
            for row in rows:
                id_td = row.find("td", {"class": ["id", "id dark"]})  # Find the problem ID
                if id_td:
                    a_tag = id_td.find("a")
                    if a_tag:
                        problem_text = a_tag.text.strip()  # Extract problem ID (e.g., "A", "B")
                        problem_link = f"https://codeforces.com{a_tag['href']}"  # Construct full link
                        problem_links.append((problem_text, problem_link))
        else:
            print(f"No problems found on page {page}.")
    return problem_links

# Function to fetch details of a single problem
def fetch_problem_details(url):
    scraper = cloudscraper.create_scraper()  # Initialize CloudScraper
    response = scraper.get(url)

    # Parse the problem's HTML page
    soup = BeautifulSoup(response.content, "html.parser")
    problem_statement = soup.find("div", class_="problem-statement")  # Find problem statement div

    if not problem_statement:
        print(f"Problem content not found at {url}. It may require JavaScript rendering.")
        return None

    # Extract key problem details
    problem_data = {
        "name": problem_statement.find("div", class_="title").text.strip() if problem_statement.find("div", class_="title") else "N/A",
        "time_limit": problem_statement.find("div", class_="time-limit").text.strip() if problem_statement.find("div", class_="time-limit") else "N/A",
        "memory_limit": problem_statement.find("div", class_="memory-limit").text.strip() if problem_statement.find("div", class_="memory-limit") else "N/A",
        "input": problem_statement.find("div", class_="input-specification").text.strip() if problem_statement.find("div", class_="input-specification") else "N/A",
        "output": problem_statement.find("div", class_="output-specification").text.strip() if problem_statement.find("div", class_="output-specification") else "N/A",
        "description": problem_statement.find("div", class_="header").text.strip() if problem_statement.find("div", class_="header") else "N/A"
    }

    return problem_data

# Main function to scrape problems and save them in JSON files
def scrape_codeforces_problems(start_page, end_page, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Fetch problem links
    problem_links = fetch_problem_links(start_page, end_page)
    print(f"Collected {len(problem_links)} problems.")

    # Step 2: Fetch details for each problem
    for problem_id, problem_url in problem_links:
        print(f"Fetching details for problem: {problem_id}")
        problem_data = fetch_problem_details(problem_url)

        if problem_data:
            # Save problem data as a JSON file
            safe_filename = "".join(c for c in problem_id if c.isalnum() or c in (' ', '-', '_')).strip()
            output_file = os.path.join(output_dir, f"problem_{safe_filename}.json")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(problem_data, f, ensure_ascii=False, indent=2)
            print(f"Saved problem {problem_id} to {output_file}")
        else:
            print(f"Skipping problem {problem_id} due to missing content.")

    print("Scraping complete.")

# Run the script
if __name__ == "__main__":
    # Input the range of pages to scrape
    start_page = int(input("Enter the start page number: "))
    end_page = int(input("Enter the end page number: "))

    # Directory to save scraped problems
    output_dir = "codeforces_problems"

    # Call the main function
    scrape_codeforces_problems(start_page, end_page, output_dir)
