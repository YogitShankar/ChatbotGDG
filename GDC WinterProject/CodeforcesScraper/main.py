from scraper.problem_scraper import scrape_problem
from scraper.editorial_scraper import scrape_editorial

if __name__ == "__main__":
    problem_urls = [
        "https://codeforces.com/problemset/problem/1/A",  # Example problem
        "https://codeforces.com/problemset/problem/4/A",  # Example problem
    ]
    editorial_urls = [
        "https://codeforces.com/blog/entry/13538",        # Example editorial
        "https://codeforces.com/blog/entry/63724",        # Example editorial
    ]

    print("Scraping problems...")
    for url in problem_urls:
        scrape_problem(url)

    print("Scraping editorials...")
    for url in editorial_urls:
        scrape_editorial(url)
