from src.problem_scraper import scrape_problem, save_problem
from src.editorial_scraper import scrape_editorial, process_editorial, save_editorial
import time

if __name__ == "__main__":
    # Scrape a problem
    problem_id = "1/A"
    problem_data = scrape_problem(problem_id)
    if problem_data:
        save_problem(problem_id.replace("/", "_"), problem_data)
        print(f"Problem {problem_id} scraped and saved!")
    else:
        print(f"Error fetching the problem: {problem_id}")
    
    # Scrape an editorial
    editorial_id = "1234"
    raw_editorial = scrape_editorial(editorial_id)
    if raw_editorial:
        processed_editorial = process_editorial(raw_editorial)
        save_editorial(editorial_id, processed_editorial)
        print(f"Editorial {editorial_id} scraped and saved!")
    else:
        print(f"Error fetching the editorial: {editorial_id}")
