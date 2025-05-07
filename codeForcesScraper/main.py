from scraper.problem_scraper import scrape_problem
from scraper.editorial_scraper import scrape_editorial

if __name__ == "__main__":
    # Example: Scrape a single problem and its editorial
    contest_id = 2050
    problem_index = "B"
    scrape_problem(contest_id, problem_index)
    scrape_editorial(contest_id, problem_index) 