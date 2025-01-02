import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

def fetch_problem_data(problem_url):
    options = Options()
    driver = uc.Chrome(options=options)

    probid = problem_url.replace("https://codeforces.com/", "")

    try:
        driver.get(problem_url)
        driver.implicitly_wait(10)

        # Wait for the time limit element to load
        wait = WebDriverWait(driver, 10)
        TL_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "time-limit")))

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        listun= soup.find("div", class_="roundbox sidebox sidebar-menu borderTopRound").find_all("a", href=True)[1]["href"]
        #check if this link is a pdf
        if listun[-4:] == ".pdf":
            print("PDF link found")
            return

        if not listun:
            print("List of problems not found")
            return
        listun = "https://codeforces.com" + listun
        title = soup.find("div", class_="title").text.strip()

        x = scrape_editorial(listun, title)
        if not x:
            print("Editorial not found")
            return

        # Extract problem metadata
        time_limit = TL_element.text.strip().replace("time limit per test", "").strip()
        memory_limit = soup.find("div", class_="memory-limit").text.strip().replace("memory limit per test", "").strip()
        tags = [tag.text.strip() for tag in soup.find_all("span", class_="tag-box")]

        # Extract problem statement, input, and output specifications
        problem_statement_element = soup.find("div", class_="problem-statement")
        statement = problem_statement_element.find("div", class_="header").find_next_sibling("div").text.strip()
        input_specs = soup.find("div", class_="input-specification").text.strip()[5:]
        output_specs = soup.find("div", class_="output-specification").text.strip()[6:]

        problem = "\n\n".join([statement, input_specs, output_specs])

        # Extract input-output test cases
        input_cases = soup.find_all("div", class_="input")
        output_cases = soup.find_all("div", class_="output")

        inpcases = []
        opcases = []

        for icases in input_cases:
            icaseline = icases.find("pre").find_all("div")
            temp = []
            for case in icaseline:
                temp.append(case.text.strip())
            temp = " ".join(temp)
            inpcases.append(temp)

        for ocases in output_cases:
            ocases = ocases.find("pre").text.strip()
            opcases.append(ocases)

        # Create metadata dictionary
        metadata = {
            "title": title,
            "tags": tags,
            "time_limit": time_limit,
            "memory_limit": memory_limit,
        }

        # Save problem metadata to a JSON file
        with open(f"data/problems/{title}.json", "w") as file:
            json.dump(metadata, file, indent=4)

        # Save problem details (statement, input, output) to a text file
        for i in range(len(inpcases)):
            problem += f"\n\nInput\n{inpcases[i]}\n\nOutput\n{opcases[i]}\n"

        note = soup.find("div", class_="note").text.strip()
        if note:
            problem += f"\n\nNote\n{note}\n"

        with open(f"data/problems/{title}.txt", "w") as file:
            file.write(problem)
        
        print(f"Data for problem '{title}' has been saved.")
    
    finally:
        driver.quit()

def fetch_editorial(edi_url, problem_url, title):
    options = Options()

    driver = uc.Chrome(options=options)
    
    try:
        # Open the editorial URL
        driver.get(edi_url)
        driver.implicitly_wait(10)

        # Wait for the editorial page to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title")))

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        try:
            # Find the link to the problem in the editorial page
            anchor_tag = soup.find("a", href=lambda href: href and problem_url in href)
            
            if not anchor_tag:
                print("Could not find the problem link in the editorial page.")
                return
            
            # Find the parent and fetch the sibling divs containing the editorial
            data = anchor_tag.parent
            editorial = ""
            data = data.find_next_sibling("div")
            
            while data and data.name == "div":
                editorial += data.text.strip()
                editorial += "\n"
                data = data.find_next_sibling()
            
            if editorial.strip() == "":
                print("Editorial content is empty or not found.")
                return
            
            # Save the editorial to a file
            with open(f"data/editorials/{title}.txt", "w") as file:
                file.write(editorial)
                return 1
            
            print(f"Editorial for problem '{title}' has been saved.")
        
        except Exception as e:
            print(f"An error occurred while fetching the editorial: {e}")
    
    finally:
        driver.quit()

def scrape_editorial(q, title):
    options = Options()
    driver = None
    try:
        # Initialize Chrome driver
        driver = uc.Chrome(options=options)
        driver.get(q)
        driver.implicitly_wait(10)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
        
        time.sleep(2)

        # Parse the page source with BeautifulSoup
        html_ = driver.page_source
        soup_ = BeautifulSoup(html_, 'html.parser')

        # Find the editorial content
        ans = soup_.find_all('div', class_='spoiler')
        if not ans:
            print(f"No editorial content found for {title}.")
            return 0

        # Save the editorial content to a file
        with open(f"data/editorials/{title}.txt", 'w', encoding="utf-8") as f:
            for answer in ans:
                f.write(answer.text)
                f.write("\n\n")

        print(f"Editorial for '{title}' has been saved successfully.")
        return 1

    except Exception as e:
        # Print error details and return failure
        print(f"An error occurred while scraping the editorial for '{title}': {e}")
        return 0

    finally:
        # Ensure the driver is closed
        if driver:
            driver.quit()

options = Options()
drivermain = uc.Chrome(options=options)

try:
    url = "https://codeforces.com/problemset?tags=1600-2000"
    drivermain.get(url)
    drivermain.implicitly_wait(10)
    
    wait = WebDriverWait(drivermain, 15)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "datatable")))
    
    soupmain = BeautifulSoup(drivermain.page_source, "html.parser")
    problems = soupmain.find_all("tr")[1:]  # Assuming table rows contain problems
    
    i = 0
    for problem in problems[6:]:
        try:
            # Extract the problem URL
            problem_url = "https://codeforces.com" + problem.find("a", href=True)["href"]
            print(f"Processing: {problem_url}")
            fetch_problem_data(problem_url)  # Call your problem fetching function
            i += 1
            if i == 20:  # Limit to first 5 problems for testing
                break
            time.sleep(2)  # Small delay to avoid getting flagged
        except Exception as e:
            print(f"Error processing problem: {e}")
except Exception as e:
    print(f"An error occurred while fetching the problemset page: {e}")
finally:
    drivermain.quit()

scrape_editorial("https://codeforces.com/blog/entry/136886", "test")