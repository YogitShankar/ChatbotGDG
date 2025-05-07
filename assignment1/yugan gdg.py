import os
import requests
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re
import time
from selenium.common.exceptions import StaleElementReferenceException
geckodriver_path = r"C:\Program Files (x86)\geckodriver.exe"

def setup_firefox_driver():
    firefox_options = Options()
    firefox_options.headless = True  
    service = Service(geckodriver_path)
    driver = webdriver.Firefox(service=service, options=firefox_options)
    return driver

def clean_whitespace(text):
    return "\n".join([line.strip() for line in text.splitlines() if line.strip()])

def extract_problem_statement(driver):
    try:
        problem_statement_div = driver.find_element(By.CLASS_NAME, 'problem-statement')
        all_divs = problem_statement_div.find_elements(By.TAG_NAME, 'div')
        problem_text = ""

        for div in all_divs:
            # If the div does not have a class attribute
            if not div.get_attribute("class"):
                # Add the text of the div, preserving spaces, avoiding new lines
                problem_text += " " + div.text.strip().replace("\n", " ")

                # Now handle child elements, ensuring no new line is introduced
                for child in div.find_elements(By.XPATH, ".//*"):
                    problem_text += " " + child.text.strip().replace("\n", " ")  # Remove newlines but keep spaces

        return clean_whitespace(problem_text)
    except Exception as e:
        print(f"Error extracting problem statement: {e}")
        return "Problem statement not found."


def extract_solution_from_tutorial(driver, tutorial_url, title):
    try:

        print(f"Navigating to tutorial URL: {tutorial_url}")
        driver.get(tutorial_url)
        
     
        print("Waiting for ttypography class...")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'ttypography')))
     
        print("Checking for ttypography class...")
        typography_div = driver.find_element(By.CLASS_NAME, 'ttypography')

        print("Searching for h1 elements within ttypography...")
        all_h1_elements = typography_div.find_elements(By.TAG_NAME, 'h1')
        
        if not all_h1_elements:
            print("No h1 elements found in ttypography!")
            return "Solution not found."

        solution_text = ""
        found_title = False
        
        for h1 in all_h1_elements:
            print(f"Checking h1: {h1.text}")
            if h1.text.strip() == title:
           
                found_title = True
                solution_text = h1.text.strip() + "\n" 
                
            
                sibling_elements = h1.find_elements(By.XPATH, "following-sibling::*")
                
                for elem in sibling_elements:
                    if elem.tag_name == 'h1':  
                        break
                    
                    try:
                        solution_text += extract_text_from_element(elem) + "\n"
                    except StaleElementReferenceException:
                        print("StaleElementReferenceException encountered. Re-locating the element...")
                        solution_text += extract_text_from_element(elem) + "\n" 

            if found_title:
                break
        
        if not solution_text:
            print(f"Solution text not found after matching h1: {title}")
        return clean_whitespace(solution_text) if solution_text else "Solution not found."

    except Exception as e:
        print(f"Error extracting solution from tutorial URL: {e}")
        return "Solution not found."

def extract_text_from_element(element):
    text = element.text.strip()
    
    children = element.find_elements(By.XPATH, "./*")
    for child in children:
        text += " " + extract_text_from_element(child)  
    
    return text


def scrape_problem_data(contest_id, problem_id):
    problem_url = f"https://codeforces.com/contest/{contest_id}/problem/{problem_id}"
    
    driver = setup_firefox_driver()
    driver.get(problem_url)
    
    problem_statement = ""
    title = ""
    time_limit = ""
    memory_limit = ""
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'problem-statement')))
        
     
        try:
            title = driver.find_element(By.CLASS_NAME, 'title').text
        except:
            title = "Title not found"
        
       
        try:
            time_limit_text = driver.find_element(By.CLASS_NAME, "time-limit").text
            time_limit = re.search(r'(\d+)\s*second', time_limit_text).group(1) + " second"
        except:
            time_limit = "Time limit not found"
        
       
        try:
            memory_limit_text = driver.find_element(By.CLASS_NAME, "memory-limit").text
            memory_limit = re.search(r'(\d+)\s*megabytes', memory_limit_text, re.IGNORECASE).group(1) + " MB"
        except:
            memory_limit = "Memory limit not found"
        
      
        problem_statement = extract_problem_statement(driver)
        
    except Exception as e:
        print(f"Error extracting problem details: {e}")
    finally:
        driver.quit()
    
    return problem_statement, title, time_limit, memory_limit

def save_problem_data(contest_id, problem_id, problem_data):
    problem_path = f"data/problems/{contest_id}/{problem_id}"
    os.makedirs(problem_path, exist_ok=True)
    
    with open(os.path.join(problem_path, f"problem_{problem_id}.txt"), 'w', encoding="utf-8") as f:
        f.write(problem_data['statement'])
    
    with open(os.path.join(problem_path, f"solution_{problem_id}.txt"), 'w', encoding="utf-8") as f:
        f.write("Solution:\n")
        f.write(problem_data['tutorial_solution'])
  
    metadata = {
        "title": problem_data['title'],
        "time_limit": problem_data['time_limit'],
        "memory_limit": problem_data['memory_limit']
    }
    
    with open(os.path.join(problem_path, "metadata.json"), 'w', encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)


def scrape_problem_and_editorial(contest_id, problem_id, tutorial_url):
    problem_statement, title, time_limit, memory_limit = scrape_problem_data(contest_id, problem_id)

    driver = setup_firefox_driver()
    tutorial_solution = extract_solution_from_tutorial(driver, tutorial_url, title)
    driver.quit()
    
    problem_metadata = {
        'title': title,
        'time_limit': time_limit,
        'memory_limit': memory_limit,
        'statement': problem_statement,
        'tutorial_solution': tutorial_solution
    }
    
    save_problem_data(contest_id, problem_id, problem_metadata)
    print(f"Successfully scraped problem {problem_id} and its tutorial solution!")

contest_id = "2020"
problem_id = "B"
tutorial_url = "https://codeforces.com/blog/entry/134516"  
scrape_problem_and_editorial(contest_id, problem_id, tutorial_url)
