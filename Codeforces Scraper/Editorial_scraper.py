import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import os

def clean_unicode_text(text):
    replacements = {
        '\u2009': ' ',
        '\u2014': '-',
        '\u2264': '<=',
        '\u00ab': '"',
        '\u00bb': '"'
    }
    for code, replacement in replacements.items():
        text = text.replace(code, replacement)
    return text

def random_delay(min_delay=5, max_delay=10):
    delay = random.uniform(min_delay, max_delay)
    print(f"Delaying for {delay:.2f} seconds...")
    time.sleep(delay)

def check_editorial_exists(driver):
    try:
        side_bar = driver.find_element(By.ID, "sidebar")
        editorial_headings = side_bar.find_elements(By.CLASS_NAME, "caption")
        caption_titles = [heading.text.strip() for heading in editorial_headings]

        if '→ Contest materials' in caption_titles:
            return True
        return False
    except NoSuchElementException:
        print("Sidebar not found")
        return False
    except Exception as e:
        print(f"Error checking editorial: {e}")
        return False

def get_tutorial_link(driver):
    try:
        side_bar = driver.find_element(By.ID, "sidebar")
        tutorial_link = side_bar.find_element(By.XPATH, ".//a[contains(text(), 'Tutorial')]")
        if tutorial_link:
            return tutorial_link.get_attribute("href")
        return None
    except NoSuchElementException:
        print("Tutorial link not found")
        return None
    except Exception as e:
        print(f"Error getting tutorial link: {e}")
        return None

def get_problem_index(problem_tag):
    """Extract problem index (A, B, C, etc.) from problem tag"""
    for char in problem_tag:
        if char.isalpha():
            return char
    return None

def extract_solution_content(element, problem_index):
    """Extract only the relevant solution content starting from the problem index"""
    # [Previous implementation remains the same]
    full_text = element.text

    start_markers = [
        f"{problem_index}. ",
        f"{problem_index}.",
        f"Problem {problem_index}",
        f"{problem_index}) ",
        f"Division 2, problem {problem_index}",
        f"Division 1, problem {problem_index}",
        f"Division 2, Problem {problem_index}",
        f"Division 1, Problem {problem_index}"
    ]

    start_pos = -1
    for marker in start_markers:
        pos = full_text.find(marker)
        if pos != -1:
            start_pos = pos
            break

    if start_pos == -1:
        return full_text

    next_index = chr(ord(problem_index) + 1)
    end_markers = [
        f"\n{next_index}. ",
        f"\n{next_index}.",
        f"\nProblem {next_index}",
        f"\n{next_index}) ",
        f"\nDivision 2, problem {next_index}",
        f"\nDivision 1, problem {next_index}",
        f"\nDivision 2, Problem {next_index}",
        f"\nDivision 1, Problem {next_index}",
        "\nAuthor:",
        "\nTags:",
        "\nDifficulty:"
    ]

    end_pos = len(full_text)
    for marker in end_markers:
        pos = full_text.find(marker, start_pos)
        if pos != -1:
            end_pos = min(end_pos, pos)

    solution_content = full_text[start_pos:end_pos].strip()

    lines = solution_content.split('\n')
    cleaned_lines = []
    started = False

    for line in lines:
        line = line.strip()
        if not started and not line:
            continue
        if line:
            started = True
        if started:
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)

def extract_contest_info(problem_tag):
    """Extract contest number and problem part from problem tag"""
    match = re.match(r'(\d+)([A-Za-z]+)', problem_tag)
    if match:
        contest_number = match.group(1)
        problem_part = match.group(2)
        return contest_number, problem_part
    return None, None

def get_editorial_content(driver, problem_tag, problem_title, problem_url):
    """Enhanced function to extract editorial content using multiple approaches"""
    # [Previous implementation remains the same]
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ttypography'))
        )

        contest_number, problem_part = extract_contest_info(problem_tag)
        if not contest_number or not problem_part:
            print(f"Could not extract contest info from {problem_tag}")
            return {
                "pattern": "invalid_tag",
                "content": "Could not parse problem tag",
                "has_solution": False
            }

        soup = BeautifulSoup(driver.page_source, "html.parser")
        typography = soup.find('div', class_='ttypography')

        if not typography:
            return {
                "pattern": "no_typography",
                "content": "No typography element found",
                "has_solution": False
            }

        for element in typography.find_all(['script', 'math']):
            element.decompose()

        full_text = typography.get_text(strip=False)

        solution = ""
        start = full_text.find(contest_number + problem_part)
        if start != -1:
            next_part = chr(ord(problem_part) + 1)
            end = full_text.find(contest_number + next_part, start)

            if end != -1:
                solution = full_text[start:end].strip()
            else:
                solution = full_text[start:].strip()

            if solution:
                return {
                    "pattern": "contest_number_match",
                    "content": clean_unicode_text(solution),
                    "has_solution": True
                }

        if not solution:
            links = typography.find_all('a', href=True)
            for link in links:
                if link['href'].endswith(problem_url.split("problem/")[-1]):
                    next_p = link.find_next('p')
                    if next_p:
                        solution = next_p.get_text(strip=False)
                        return {
                            "pattern": "url_match",
                            "content": clean_unicode_text(solution),
                            "has_solution": True
                        }

        if not solution:
            problem_index = get_problem_index(problem_tag)
            content = extract_solution_content(typography, problem_index)
            if content and len(content) > 50:
                return {
                    "pattern": "fallback_pattern",
                    "content": clean_unicode_text(content),
                    "has_solution": True
                }

        return {
            "pattern": "no_match",
            "content": "No solution found with any approach",
            "has_solution": False
        }

    except Exception as e:
        print(f"Error extracting editorial content: {e}")
        return {
            "pattern": "error",
            "content": f"Error: {str(e)}",
            "has_solution": False
        }

def test_editorials_from_problemset(problems):
    """Test editorial extraction and save to files"""
    results = []
    driver = uc.Chrome()

    # Create the directory if it doesn't exist
    os.makedirs("Scraped_Sample_Data\Editorials_Scraped", exist_ok=True)

    try:
        for problem in problems[:]:
            print(f"\n{'='*80}")
            print(f"Testing Problem {problem['problem_tag']}: {problem['title']}")

            # Create a file for this problem regardless of editorial status
            filename = f"Scraped_Sample_Data\Editorials_Scraped/{problem['problem_tag']}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                # Write problem information
                f.write(f"Problem: {problem['problem_tag']} - {problem['title']}\n")
                f.write(f"Problem Link: {problem['link']}\n")

                if problem['editorial_link'] == "N/A":
                    print("No editorial available - recording in file")
                    f.write("\n" + "="*80 + "\n\n")
                    f.write("NO EDITORIAL AVAILABLE FOR THIS PROBLEM")
                    results.append({
                        "problem_tag": problem['problem_tag'],
                        "title": problem['title'],
                        "status": "no_editorial"
                    })
                    print(f"Status saved to {filename}")
                    continue

                f.write(f"Editorial Link: {problem['editorial_link']}\n")
                print(f"Editorial Link: {problem['editorial_link']}")
                print(f"Problem Link: {problem['link']}")
                print(f"{'='*80}")

                try:
                    driver.get(problem['editorial_link'])
                    random_delay(3, 7)

                    result = get_editorial_content(
                        driver,
                        problem['problem_tag'],
                        problem['title'],
                        problem['link']
                    )

                    test_result = {
                        "problem_tag": problem['problem_tag'],
                        "title": problem['title'],
                        "pattern_detected": result['pattern'],
                        "has_solution": result['has_solution'],
                        "content_length": len(result['content']),
                        "status": "success" if result['has_solution'] else "no_solution",
                        "content": result['content']
                    }

                    # Write separator and content/status to file
                    f.write("\n" + "="*80 + "\n\n")
                    if result['has_solution'] and result['content']:
                        f.write(result['content'])
                        print(f"Editorial content saved to {filename}")
                    else:
                        f.write("NO SOLUTION FOUND IN THE EDITORIAL PAGE")
                        print(f"No solution status saved to {filename}")

                    print(f"\nPattern detected: {result['pattern']}")
                    print(f"Has solution: {result['has_solution']}")
                    print(f"Content length: {len(result['content'])} characters")
                    if result['content']:
                        print("\nFirst 200 characters of content:")
                        print("-" * 50)
                        print(result['content'][:200] + "...")

                except Exception as e:
                    error_message = f"Error processing editorial: {str(e)}"
                    print(error_message)
                    f.write("\n" + "="*80 + "\n\n")
                    f.write(f"ERROR PROCESSING EDITORIAL: {str(e)}")
                    test_result = {
                        "problem_tag": problem['problem_tag'],
                        "title": problem['title'],
                        "pattern_detected": "error",
                        "has_solution": False,
                        "content_length": 0,
                        "status": "error",
                        "error": str(e)
                    }

                results.append(test_result)
                random_delay(2, 5)

        # Print summary
        print("\n" + "="*80)
        print("TESTING SUMMARY")
        print("="*80)

        total = len(results)
        no_editorial = sum(1 for r in results if r['status'] == "no_editorial")
        successful = sum(1 for r in results if r['status'] == "success")
        failed = sum(1 for r in results if r['status'] == "error")
        no_solution = sum(1 for r in results if r['status'] == "no_solution")

        print(f"\nTotal problems tested: {total}")
        print(f"No editorial available: {no_editorial}")
        print(f"Successfully scraped: {successful}")
        print(f"No solution found: {no_solution}")
        print(f"Errors encountered: {failed}")
        print(f"\nAll results have been saved to the Scraped_Sample_Data\Editorials_Scraped directory")

        # Write summary file
        with open("Scraped_Sample_Data\Editorials_Scraped/summary.txt", 'w', encoding='utf-8') as f:
            f.write("EDITORIAL SCRAPING SUMMARY\n")
            f.write("="*80 + "\n\n")
            f.write(f"Total problems tested: {total}\n")
            f.write(f"No editorial available: {no_editorial}\n")
            f.write(f"Successfully scraped: {successful}\n")
            f.write(f"No solution found: {no_solution}\n")
            f.write(f"Errors encountered: {failed}\n\n")

            f.write("Detailed Results:\n")
            f.write("-"*80 + "\n")
            for r in results:
                f.write(f"\nProblem {r['problem_tag']}: {r['title']}\n")
                f.write(f"Status: {r['status']}\n")
                if 'pattern_detected' in r:
                    f.write(f"Pattern: {r['pattern_detected']}\n")
                if 'error' in r:
                    f.write(f"Error: {r['error']}\n")

    finally:
        driver.quit()
        return results
if __name__ == "__main__":
    # Main execution code remains the same
    driver = uc.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://codeforces.com/problemset?order=BY_RATING_ASC")
        random_delay()

        problems_table = driver.find_element(By.CLASS_NAME, "problems")
        problem_rows = problems_table.find_elements(By.TAG_NAME, "tr")

        problems = []
        for row in problem_rows[1:]:
            try:
                link_tags = row.find_elements(By.TAG_NAME, "a")
                problem_tag = link_tags[0].text.strip()
                title = link_tags[1].text.strip()
                link = link_tags[1].get_attribute("href")
                problem_data = {
                    "problem_tag": problem_tag,
                    "title": title,
                    "link": link,
                    "editorial_link": "N/A"
                }
                problems.append(problem_data)
            except Exception as e:
                print(f"Error extracting data for a row: {e}")

        for problem in problems[:]:
            try:
                print(f"Checking editorial for problem {problem['problem_tag']}...")
                driver.get(problem['link'])
                random_delay()

                if check_editorial_exists(driver):
                    tutorial_link = get_tutorial_link(driver)
                    if tutorial_link:
                        problem['editorial_link'] = tutorial_link
                        print(f"Editorial found for {problem['problem_tag']}")
                else:
                    print(f"No editorial for {problem['problem_tag']}")

            except Exception as e:
                print(f"Error processing problem {problem['problem_tag']}: {e}")
                continue

    finally:
        driver.quit()

    # Test and save editorials
    test_editorials_from_problemset(problems)