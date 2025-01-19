from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time
import os
import json
import cloudscraper
from seleniumbase import Driver
from selenium.webdriver.common.by import By
path="chromedriver.exe"
serv=Service(path)
opt=Options()
driver=webdriver.Chrome(service=serv,options=opt)

driver=Driver(uc=True)
url="https://codeforces.com/problemset"
driver.uc_open_with_reconnect(url,10)
driver.uc_gui_click_captcha()


outer_tags=driver.find_elements(By.TAG_NAME,'tr')[1:50]

tags=[]

for tag in outer_tags:
    tr_tags=tag.find_elements(By.TAG_NAME,'td')[1]
    tr_tags=tr_tags.find_element(By.TAG_NAME,'a').text
    tags.append(tr_tags)

data=[]
for i, t in enumerate(tags):
    try:
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, t))
        )
        link.click()

        # Wait for the new page to load and access elements on the new page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "problem-statement"))
        )

        problem_statement = driver.find_element(By.CLASS_NAME, "problem-statement")
        title = problem_statement.find_element(By.CLASS_NAME, "title").text

        statement = "\n".join([para.text for para in problem_statement.find_elements(By.TAG_NAME, 'p')])

        input = problem_statement.find_element(By.CLASS_NAME, "input-specification").text
        output = problem_statement.find_element(By.CLASS_NAME, "output-specification").text
        sample_tests = problem_statement.find_element(By.CLASS_NAME, "sample-tests").text

        tag_text= [tag.text for tag in driver.find_elements(By.CLASS_NAME, "tag-box")]

        time_limit = problem_statement.find_element(By.CLASS_NAME, "time-limit").text
        memory_limit = problem_statement.find_element(By.CLASS_NAME, "memory-limit").text

        # Store problem statement in text format
        with open(f"problem_{i+1}.txt", "w", encoding='utf-8') as f:
            f.write(f"Title: {title}\n")
            f.write(f"Statement:\n{statement}\n")
            f.write(f"Input Specification:\n{input}\n")
            f.write(f"Output Specification:\n{output}\n")
            f.write(f"Sample Tests:\n{sample_tests}\n")
            f.write(f"Constraints: {time_limit} {memory_limit}\n")

        # Store metadata in JSON format
        problem_data = {
            "title": title,
            
            "constraints": {
                "time": time_limit,
                "memory": memory_limit
            },
            "tags": tag_text
        }
        data.append(problem_data)

        # Navigate back to the problem set page
        driver.back()
        # Ensure elements are fully loaded before proceeding
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'dark'))
        )

    except Exception as e:
        print(f"Couldn't click the link: {t}, error: {str(e)}")

# Save metadata to JSON file
with open("problems_metadata.json", "w", encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

driver.get("https://codeforces.com/blog/entry/138119")
time.sleep(10)



# Locate the body element by ID
body = driver.find_element(By.ID, "body")

# Locate the child element with a specific style (use CSS selectors for styles)
style_element = body.find_element(By.CSS_SELECTOR, "[style*='position: relative;']")

# Locate the element with ID "pageContent"
page_content = style_element.find_element(By.ID, "pageContent")

# Locate the element with a margin of 0 (using CSS selector for styles)
margin = page_content.find_element(By.CSS_SELECTOR, "[style*='margin:0;']")

# Locate the element with margin-top: 2em
margin_top = margin.find_element(By.CSS_SELECTOR, "[style*='margin-top:2em;']")

# Locate the topic element by its class name
topic_id = margin_top.find_element(By.CLASS_NAME, "has-topic-id topic")

# Locate the content element by its class name
content = topic_id.find_element(By.CLASS_NAME, "content")

# Locate the typography element
typography = content.find_element(By.CLASS_NAME, "ttypography")

# Locate the spoiler element
spoiler = typography.find_element(By.CLASS_NAME, "spoiler spoiler-open")

# Retrieve the text inside the spoiler content
spoiler_content = spoiler.find_element(By.CLASS_NAME, "spoiler-content").text


driver.quit()

 
