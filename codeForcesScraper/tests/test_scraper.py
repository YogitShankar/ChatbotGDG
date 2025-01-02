import os
import unittest
from scraper.problem_scraper import scrape_problem

class TestScraper(unittest.TestCase):
    def test_scrape_problem(self):
        # Example: Test problem scraping for a known problem
        contest_id = 1
        problem_index = "A"
        scrape_problem(contest_id, problem_index)
        # Verify files exist
        self.assertTrue(os.path.exists(f"data/problems/{contest_id}_{problem_index}.txt"))
        self.assertTrue(os.path.exists(f"data/metadata/{contest_id}_{problem_index}.json"))

if __name__ == "__main__":
    unittest.main()
