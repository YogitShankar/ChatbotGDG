from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Setup ChromeDriver and options
path = "chromedriver.exe"  # Path to your ChromeDriver executable
service = Service(path)
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--user-data-dir=C:/Users/prane/AppData/Local/Google/Chrome/User Data")
options.add_argument("--profile-directory=Default")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the Codeforces problemset page
    url = "https://codeforces.com/problemset"
    driver.get(url)

    # Wait for the page to load completely
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "minDifficulty"))
    )

    # Input difficulty range
    a = input("Enter minimum rating: ")
    b = input("Enter maximum rating: ")

    # Enter difficulty range in the input fields
    min_diff = driver.find_element(By.NAME, "minDifficulty")
    min_diff.clear()
    min_diff.send_keys(str(a))

    max_diff = driver.find_element(By.NAME, "maxDifficulty")
    max_diff.clear()
    max_diff.send_keys(str(b))

    # Submit the form
    search = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    search.click()

    # Wait for the results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "tr"))
    )

    # Collect problem names and links
    problem_rows = driver.find_elements(By.TAG_NAME, "tr")[1:6]  # Limit to the first 5 rows for demonstration
    problems = []
    for row in problem_rows:
        try:
            title_cell = row.find_elements(By.TAG_NAME, "td")[1]
            problem_link = title_cell.find_element(By.TAG_NAME, "a")
            problems.append({
                "name": problem_link.text,
                "link": problem_link.get_attribute("href")
            })
        except Exception as e:
            print(f"Error processing problem row: {str(e)}")

    # List to store problem metadata
    data = []

    # Process each problem
    for i, problem in enumerate(problems):
        try:
            # Navigate to the problem page
            driver.get(problem["link"])

            # Wait for the problem statement to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "problem-statement"))
            )

            # Extract problem details
            problem_statement = driver.find_element(By.CLASS_NAME, "problem-statement")
            title = problem_statement.find_element(By.CLASS_NAME, "title").text
            statement = "\n".join([p.text for p in problem_statement.find_elements(By.TAG_NAME, "p")])
            input_spec = problem_statement.find_element(By.CLASS_NAME, "input-specification").text
            output_spec = problem_statement.find_element(By.CLASS_NAME, "output-specification").text
            sample_tests = problem_statement.find_element(By.CLASS_NAME, "sample-tests").text
             # Extract tags
            tags = [tag.text for tag in driver.find_elements(By.CLASS_NAME, "tag-box")]

            # Extract constraints
            time_limit = problem_statement.find_element(By.CLASS_NAME, "time-limit").text
            memory_limit = problem_statement.find_element(By.CLASS_NAME, "memory-limit").text

           

            # Try to get the editorial link
            editorial_content = ""
            try:
                editorial_link = driver.find_element(By.PARTIAL_LINK_TEXT, 'Tutorial')
                if not editorial_link:
                    editorial_link = driver.find_element(By.PARTIAL_LINK_TEXT, 'Editorial')

                if editorial_link:
                    editorial_link.click()
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "spoiler"))
                    )
                    editorial_content = driver.find_element(By.CLASS_NAME, "spoiler").text
                    driver.back()  # Return to the problem page
            except Exception:
                print(f"No editorial found for: {title}")

            # Save the problem details to a text file
            with open(f"problem_{i + 1}.txt", "w", encoding='utf-8') as f:
                f.write(f"Title: {title}\n\n")
                f.write(f"Statement:\n{statement}\n\n")
                f.write(f"Input Specification:\n{input_spec}\n\n")
                f.write(f"Output Specification:\n{output_spec}\n\n")
                f.write(f"Sample Tests:\n{sample_tests}\n\n")
                f.write(f"Constraints:\nTime: {time_limit}\nMemory: {memory_limit}\n\n")
                f.write(f"Tags: {', '.join(tags)}\n\n")
                f.write(f"Editorial:\n{editorial_content}\n")

            # Store metadata for JSON
            problem_data = {
                "title": title,
                "statement": statement,
                "constraints": {
                    "time": time_limit,
                    "memory": memory_limit
                },
                "tags": tags,
                "editorial": editorial_content
            }
            data.append(problem_data)

        except Exception as e:
            print(f"Error processing problem {problem['name']}: {str(e)}")

    # Save metadata to a JSON file
    with open("problems_metadata.json", "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

finally:
    # Quit the WebDriver
    driver.quit()
