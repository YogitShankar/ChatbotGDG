import os
import requests
from bs4 import BeautifulSoup
from scraper.utils import save_to_file, save_json, log_error

def scrape_problem(problem_url):
    try:
        print(f"Scraping problem URL: {problem_url}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Referer": "https://codeforces.com/",
        }
        response = requests.get(problem_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract problem title
        title = soup.find('div', class_='title').text.strip()
        print(f"Problem Title: {title}")

        # Extract problem statement
        statement = soup.find('div', class_='problem-statement')
        statement_text = statement.get_text(separator="\n").strip()
        print(f"Problem Statement:\n{statement_text}")

        # Extract tags
        tags = [tag.text for tag in soup.find_all('span', class_='tag-box')]
        print(f"Tags: {tags}")

        # Extract constraints
        time_limit = soup.find('div', class_='time-limit').text.strip()
        memory_limit = soup.find('div', class_='memory-limit').text.strip()
        print(f"Time Limit: {time_limit}")
        print(f"Memory Limit: {memory_limit}")

        # Save the data
        problem_dir = os.path.join('data', 'problems')
        metadata_dir = os.path.join('data', 'metadata')
        os.makedirs(problem_dir, exist_ok=True)
        os.makedirs(metadata_dir, exist_ok=True)

        save_to_file(title, statement_text, problem_dir)
        save_json(title, {
            'tags': tags,
            'time_limit': time_limit,
            'memory_limit': memory_limit
        }, metadata_dir)
    except requests.exceptions.HTTPError as e:
        log_error(problem_url, f"HTTP error: {e}")
        print(f"HTTP Error: {e}")
    except Exception as e:
        log_error(problem_url, f"Unexpected error: {e}")
        print(f"Error scraping problem: {e}")
