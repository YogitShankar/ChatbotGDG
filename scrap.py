import selenium 
from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import json 
import undetected_chromedriver as uc

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

l="https://codeforces.com/contests?filterTypes=div2&filterRated=&filterSubstring="
base_url="https://codeforces.com"

driver = uc.Chrome()

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def scrape_problem(Link):
    driver.get(Link)
    driver.implicitly_wait(10)
    page_source=driver.page_source
    soup = BeautifulSoup(page_source,'html.parser')
    title=soup.find('div',class_ = "title").text
    sanitized_title = sanitize_filename(title)
    time_limit=soup.find('div', class_="time-limit").text
    memory_limit=soup.find('div',class_="memory-limit").text

    match_t = re.search(r'\d+', time_limit)
    if match_t:
        number_t = match_t.group(0)
        remaining_text_t = time_limit[match_t.end():].strip()
        time_l = f" {number_t} {remaining_text_t}"

    else:
        time_l = "NA"

    match_m = re.search(r'\d+', memory_limit)
    if match_m:
        number_m = match_m.group(0)
        remaining_text_m = memory_limit[match_m.end():].strip()
        memory_l = f" {number_m} {remaining_text_m}"
    else:
        memory_l = "NA"

    tags=soup.find_all('span',class_= "tag-box")
    tag_texts = [tag.text.strip() for tag in tags]
    
    problem_statement_elmnt = soup.find("div", class_="problem-statement")
    if (problem_statement_elmnt.find("div", class_="header").find_next_sibling("div")):
        statement = problem_statement_elmnt.find("div", class_="header").find_next_sibling("div").text.strip()
    if (soup.find("div", class_="input-specification")):    
        input_specs = soup.find("div", class_="input-specification").text.strip()[5:]
    if (soup.find("div", class_="output-specification")):    
        output_specs = soup.find("div", class_="output-specification").text.strip()[6:]
    else:
        output_specs = " "   
    problem = "\n\n".join([statement, input_specs, output_specs])

    input_cases = soup.find_all("div", class_="input")
    output_cases = soup.find_all("div", class_="output")

    inpcases = []
    opcases = []

    for icases in input_cases:
        icaseline = icases.find("pre").find_all("div")
        temp=[]
        for case in icaseline:
            temp.append(case.text.strip())
        temp = " ".join(temp)
        inpcases.append(temp)

    for ocases in output_cases:
        ocases = ocases.find("pre").text.strip()
        opcases.append(ocases)

    for i in range(len(inpcases)):
        problem += f"\n\nInput\n{inpcases[i]}\n\nOutput\n{opcases[i]}\n"

    with open(rf"C:\Users\mailt\Desktop\CB4CP\problems\{sanitized_title}.txt","w", encoding="utf-8") as f:
        f.write(problem)

    metadata = {
        "title": title,
        "time_limit": time_l,
        "memory_limit": memory_l,
        "tags": tag_texts
    }
    with open(rf"C:\Users\mailt\Desktop\CB4CP\problems\{sanitized_title}.json","w") as f:
        json.dump(metadata,f,indent=4)
    time.sleep(5)
    return sanitized_title

def get_editorial_link(e):
    try:
        driver.get(e)
        driver.implicitly_wait(10)
        page=driver.page_source
        so = BeautifulSoup(page,'html.parser')
        s=so.find('div',class_= 'roundbox sidebox sidebar-menu borderTopRound')
        ul = s.find('ul')   
        second_li = ul.find_all('li')[1]
        span=second_li.find('span')
        a=span.find('a')
        return a['href']
    except Exception as e:
        print(f"No editorial found")
        return 0

def scrape_editorial(q, title):
    try:
        driver.get(q)
        driver.implicitly_wait(10)
        html_ = driver.page_source
        soup_ = BeautifulSoup(html_, 'html.parser')
        ans = soup_.find_all('div', class_='spoiler')
        if not ans:
            print(f"No editorial content found for {title}.")
            return 0
        with open(rf"C:\Users\mailt\Desktop\CB4CP\editorials\{title}.txt", 'w', encoding="utf-8") as f:
            for answer in ans:
                f.write(answer.text)
                f.write("\n\n")
        print(f"Editorial for '{title}' has been saved successfully.")
        return 1
    except Exception as e:
        print(f"An error occurred while scraping the editorial for '{title}': {e}")
        return 0

def get_contests_link(l):
    base_url="https://codeforces.com"
    driver.get(l)
    driver.implicitly_wait(10)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    Tbody= soup.find('div',class_='contests-table')
    tbody = Tbody.find('tbody')
    rows = tbody.find_all('tr')[1:20]
    links=[]
    for row in rows:
        td=row.find('td',class_=['dark left','left'])
        if td:
            a_tag = td.find('a')
            if a_tag:
                link = a_tag['href']
                links.append(base_url+link)           
    return links               

links=get_contests_link(l)

with open (rf"C:\Users\mailt\Desktop\CB4CP\Contests_scrapped.txt",'w',encoding="utf-8") as g:
    for j in links:
        g.write(j+"\n")

for i in links:
    driver.get(i)
    driver.implicitly_wait(10)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    table=soup.find('table',class_='problems')
    tb=table.find('tbody')
    ro = tb.find_all('tr')[1:5]
    for r in ro:
        td=r.find('td',class_= ['id dark left','id left'])
        if(td):
            a_tag = td.find('a')
            if a_tag:
               ls = a_tag['href']
               url=base_url+ls
               title_p =scrape_problem(url)
               e_l=get_editorial_link(url)
               b_e_l= base_url+e_l
               scrape_editorial(b_e_l, title_p)

driver.quit()

            
