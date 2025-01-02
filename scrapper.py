import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re
import time
import undetected_chromedriver as uc


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROBLEMS_DIR = os.path.join(DATA_DIR, "problems")
EDITORIALS_DIR = os.path.join(DATA_DIR, "editorials")



os.makedirs(PROBLEMS_DIR, exist_ok=True)
os.makedirs(EDITORIALS_DIR, exist_ok=True)


def alphabet_to_number(letter):
    return ord(letter.upper()) - ord('A')

def save_editorials(content,data_dir, problem_id):
    os.makedirs(data_dir, exist_ok=True)

    file_name = f"{problem_id}_editorials.txt"
    file_path = os.path.join(data_dir, file_name)
    data = (
        f" Problem_ID: {problem_id}\n"
        f"{content}"
    )
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(data)

    print(f"Editorials data saved to: {file_path}")



def save_problem_as_text(problem_id, title, time_limit, memory_limit, statement, input_spec, output_spec, data_dir):
    
    os.makedirs(data_dir, exist_ok=True)

    
    file_name = f"{problem_id}.txt"
    file_path = os.path.join(data_dir, file_name)

    
    problem_data = (
        f"Problem ID: {problem_id}\n"
        f"Title: {title}\n"
        f"Time Limit: {time_limit}\n"
        f"Memory Limit: {memory_limit}\n\n"
        f"Problem Statement:\n{statement}\n\n"
        f"Input Specifications:\n{input_spec}\n\n"
        f"Output Specifications:\n{output_spec}\n"
    )

    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(problem_data)

    print(f"Problem data saved to: {file_path}")

def  main(driver,problem_ids):
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, 'lxml')
    problem = soup.find("div",attrs={'class':'problem-statement'})

    title = problem.find("div",attrs={'class':'title'})
    time_ = problem.find("div",attrs={'class':'time-limit'})
    input_ = problem.find("div",attrs={'class':'input-specification'})
    output = problem.find("div",attrs={'class':'output-specification'})
    question = problem.find("div",class_=None)
    memory = problem.find("div",attrs={'class':'memory-limit'})

    paras1 = input_.find_all("p")
    paras2 = output.find_all("p")
    paras3 = question.find_all("p")

    dir_t_txt = time_.get_text(separator=" ",strip=True)
    nest_t_txt = time_.find("div",attrs={'class':'property-title'}).text

    dir_m_txt = memory.get_text(separator=" ",strip=True)
    nest_m_txt = memory.find("div",attrs={'class':'property-title'}).text

    inp_arr =[]
    out_arr =[]
    que_arr =[]
    for para in paras1:
        inp_arr.append(para.text.strip())

    for para in paras2:
        out_arr.append(para.text.strip())

    for para in paras3:
        que_arr.append(para.text.strip())



    Input = " ".join(inp_arr)
    Output = " ".join(out_arr)
    Title = title.text.strip()
    Question = " ".join(que_arr)
    Time = dir_t_txt.replace(nest_t_txt, "").strip()
    Memory = dir_m_txt.replace(nest_m_txt, "").strip()

    save_problem_as_text(problem_ids,Title,Time,Memory,Question,Input,Output,PROBLEMS_DIR)

def get_editorials(driver, letter, problem_id):
    box = driver.find_element(By.CLASS_NAME, "sidebar-menu")
    ul = box.find_element(By.TAG_NAME, "ul")
    links = ul.find_elements(By.TAG_NAME, "a")
    link = links[-1].get_attribute("href")
    driver.get(link)
    driver.implicitly_wait(5)
    contents = driver.find_element(By.CLASS_NAME, "content")
    headers = contents.find_elements(By.CLASS_NAME, "spoiler")
    solutions = []
    num = alphabet_to_number(letter)
    for header in headers:
        tag = header.text
        if (tag == "Tutorial"):
            b = header.find_element(By.TAG_NAME, "b")
            b.click()
            content = header.find_element(By.CLASS_NAME, "spoiler-content")
            raw = content.text
            cleaned = re.sub(r'\s+', ' ',raw,).strip()
            solutions.append(cleaned)
            time.sleep(2)
        elif (tag == "Solution"):
            b = header.find_element(By.TAG_NAME, "b")
            b.click()
            content = header.find_element(By.CLASS_NAME, "spoiler-content")
            raw = content.text
            cleaned = re.sub(r'\s+', ' ',raw,).strip()
            solutions.append(cleaned)
            time.sleep(2)
        else:
            continue
    Content = solutions[num]
    save_editorials(Content,EDITORIALS_DIR, problem_id)

options_ = Options()
options_.add_argument("--disable-notifications")

driver = uc.Chrome(options = options_)
driver.get("https://codeforces.com/problemset")
table = driver.find_element(By.CLASS_NAME, "problems")
rows = table.find_elements(By.CLASS_NAME, "id")
links = [row.find_element(By.TAG_NAME, "a").get_attribute("href") for row in rows]
for link in links:
    try:
        problem_code = link.split("/")[-2:]
        problem_id = "".join(problem_code)
        letter = problem_id[-1]
        driver.get(link)
        driver.implicitly_wait(10)
        time.sleep(2)

        main(driver, problem_ids= problem_id)
        get_editorials(driver, letter, problem_id)
        

        driver.back()
        time.sleep(2)

    except Exception as e:
        continue