from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json


class Problem:
    def __init__(self, title, memory, time_limit, statement, editorial_link=None):
        self.title = title
        self.memory = memory
        self.time_limit = time_limit
        self.statement = statement
        self.editorial_link = editorial_link

    def to_dict(self):
        return {
            "title": self.title,
            "memory": self.memory,
            "time_limit": self.time_limit,
            "statement": self.statement,
            "editorial_link": self.editorial_link
        }


class CodeforcesScraper:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()

    def get_page_source(self):
        self.driver.get(self.url)
        time.sleep(3) 
        return BeautifulSoup(self.driver.page_source, "lxml")

    def extract_problem_details(self, soup):

        problem_title = soup.find("div", class_="title").text.strip()

        memory_limit = soup.find("div", class_="memory-limit")
        memory = memory_limit.get_text().replace(memory_limit.div.get_text(), "").strip()

        time_limit = soup.find("div", class_="time-limit")
        timelimit = time_limit.get_text().replace(time_limit.div.get_text(), "").strip()


        problem_statement = soup.find("div", class_="problem-statement")
        contents = problem_statement.find("div", class_=False).find_all("p")
        statement = "\n".join([content.get_text().strip() for content in contents])


        editorial_link = self.extract_editorial_link(soup)

        return Problem(problem_title, memory, timelimit, statement, editorial_link)

    def save_problem_metadata(self, problem):

        data = {
            "Memory Limit": problem.memory,
            "Time Limit": problem.time_limit
        }
        with open("metadata.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

    def save_problem_statement(self, problem):

        with open("problem.txt", "w") as P:
            P.write(f"{problem.title}\n")
            P.write(f"{problem.statement}\n")

    def extract_editorial_link(self, soup):
        editorial = soup.find("a", string="Tutorial #1")
        if editorial:
            return editorial["href"]
        else:
            print("No tutorial link found.")
            return None

    def store_editorials(self, link):
        scraper = CodeforcesScraper(link)
        time.sleep(3)
        soup = scraper.get_page_source()

        solutions = soup.find_all("code", class_="prettyprint prettyprinted")
        
        if solutions:
            with open("editorials.txt", "w") as ed:
                for solution in solutions:
                    ed.write(f"solution :{solution.text.strip()}")
        else:
            print("Solution not found in the editorial.")

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    url = "https://codeforces.com/problemset/problem/2042/A"
    scraper = CodeforcesScraper(url)

    soup = scraper.get_page_source()

    problem = scraper.extract_problem_details(soup)

    scraper.save_problem_metadata(problem)
    scraper.save_problem_statement(problem)

    if problem.editorial_link:
        scraper.store_editorials(f"https://codeforces.com{problem.editorial_link}")

    scraper.close()
