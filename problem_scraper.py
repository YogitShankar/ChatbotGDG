from urllib.parse import urljoin
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import json
import os

def create_directories():
    # Create the 'data' directory and its subdirectories if they do not exist
    os.makedirs("data/metadata", exist_ok=True)
    os.makedirs("data/problem_statements", exist_ok=True)
    os.makedirs("data/editorials", exist_ok=True)

def extract_problem_id(input_string):
    # Regex to capture the part before the period
    match = re.match(r'^([A-Za-z0-9]+)\.', input_string)
    if match:
        return match.group(1)  # Return the problem ID
    else:
        return None

def extract_name(input_string):
    # Regex to match a pattern with any alphanumeric character(s) followed by a period and space
    match = re.search(r'^[A-Za-z0-9]+\.\s*(.*)', input_string)
    if match:
        return match.group(1)
    else:
        return "No match found"

def extract_contest_id(input_string):
    # Use regex to extract the contest ID
    match = re.search(r'/contest/(\d+)', input_string)
    if match:
        return  match.group(1)  # Extract the contest ID
    else:
        return "No contest ID found in the URL"

def find_question_details(question_link):
    driver = webdriver.Chrome()
    driver.get(question_link)
    html_text =driver.page_source

    soup = BeautifulSoup(html_text,'lxml')

    for span in soup.find_all("span", {"class": "math"}):
        span.decompose()

    prob_name=soup.find("div", class_="title").text
    problem = soup.find("div", class_="problem-statement")
    question = problem.find("div", id=False, class_=False)
    problem_statement = "\n".join([p.text for p in question])
    with open(f"data/problem_statements/{prob_name}_statement.txt", "w", encoding="utf-8") as f:
        f.write(problem_statement)

    time_limit = soup.find("div", class_="time-limit").text.replace("time limit per test","")
    memory_limit = soup.find("div", class_="memory-limit").text.replace("memory limit per test","")

    tags=soup.find_all("span",class_="tag-box")
    problem_tags = [tag.text.replace(" ","").strip() for tag in tags]
    # Store the last tag in a variable to avoid accessing it multiple times
    last_tag = problem_tags[-1]

    if last_tag[0] != '*':
        difficulty = "unknown"
    else:
        difficulty = last_tag
        problem_tags = problem_tags[:-1]

    input_spec = soup.find("div", class_="input-specification")
    input_spec = "\n".join([p.text for p in input_spec])

    output_spec = soup.find("div", class_="output-specification")
    output_spec = "\n".join([p.text for p in output_spec])

    tests = soup.find("div", class_="sample-test")
    test_cases = "\n".join(
        div.get_text(separator="\n").strip() for div in tests
    )

    problem_metadata = {
        "problem_id": extract_problem_id(prob_name),
        "contest_id": extract_contest_id(question_link),
        "name": prob_name,
        "url": question_link,
        "difficulty": difficulty,
        "tags": problem_tags,
        "time_limit": time_limit,
        "memory_limit": memory_limit,
        "input_specification": input_spec,
        "output_specification": output_spec,
        "sample_tests": test_cases
    }

    # Convert dictionary to JSON
    problem_json = json.dumps(problem_metadata, indent=4)
    with open(f"data/metadata/{prob_name}_metadata.json", "w") as file:
        file.write(problem_json)

    driver.quit()

    return prob_name

def extract_editorial_link(question_link):
    driver = webdriver.Chrome()
    driver.get(question_link)
    html = driver.page_source

    soup = BeautifulSoup(html,'lxml')

    sidebar = soup.find("div",id="sidebar")
    req = sidebar.find_all("li")
    lang = ""
    href_val=""
    target=""
    temp=""
    for ele in req:
        # Check if <a> exists within <li> and then get the href attribute
        a_tag = ele.find('a')
        if a_tag:
            target = a_tag.text.lower()
        span = ele.find("span",class_="resource-locale")
        if span:
            lang = span.text
        if a_tag and a_tag.get('href'):  # Ensure <a> tag and href attribute exist
            href_val = a_tag.get('href')
            if lang == "(en)" and "tutorial" in target and "video" not in target:
                break
            elif lang == "(en)" and "editorial" in target:
                break
            elif span is None and "tutorial" in target:
                temp=href_val
    if lang=="(en)" and "tutorial" in target and "video" not in target:
        base_url = "https://codeforces.com"  # Replace with the actual base URL of the site
        full_url = urljoin(base_url, href_val)
        return full_url
    elif lang=="(en)" and "editorial" in target and "video" not in target:
        # print(href_val)
        base_url = "https://codeforces.com"  # Replace with the actual base URL of the site
        full_url = urljoin(base_url, href_val)
        return full_url
    elif temp!="":
        base_url = "https://codeforces.com"
        full_url = urljoin(base_url, temp)
        return full_url
    driver.quit()

def extract_editorial_content(link_editorial, problem_names):
    driver = webdriver.Chrome()
    driver.get(link_editorial)
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')

    for span in soup.find_all("span", {"class": "math"}):
        span.decompose()

    content = soup.find("div",class_="ttypography")
    collecting = False
    result = []
    headers = ["p","h1"]
    ind=0
    for ele in content:
        if ind < len(problem_names) and extract_name(problem_names[ind]) in ele.text :
            if ind>0:
                with open(f"data/editorials/{problem_names[ind-1]}_editorial.txt", "w", encoding="utf-8") as f:
                    for line in result:
                        f.write(line)
            result=[]
            ind=ind+1
            collecting = True
        elif collecting and ele.name not in headers:
            text_parts = []
            # Check if 'ele' itself is text
            if isinstance(ele, str):
                text_parts.append(ele.strip())
            elif hasattr(ele, 'children'):  # If 'ele' has children, process them
                for child in ele.children:
                    if isinstance(child, str):  # If the child is just text
                        text_parts.append(child.strip())
                    elif hasattr(child, 'text'):  # If the child has text (i.e., a tag with text content)
                        text_parts.append(child.text.strip())
                    text_parts.append("\n")
            else:
                pass
            # Combine the collected text parts
            result.append(' '.join(text_parts))
    with open(f"data/editorials/{problem_names[len(problem_names)-1]}_editorial.txt", "w", encoding="utf-8") as f:
        for line in result:
            f.write(line)


def get_all_prob(contest_link):
    driver = webdriver.Chrome()
    driver.get(contest_link)
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    problems=soup.find("table",class_="problems")
    all_hrefs = {a['href'] for a in problems.find_all('a', href=True)}
    # Filter distinct hrefs and include ones containing "problem" after "contest_id/"
    filtered_hrefs = {href for href in all_hrefs if '/problem/' in href}
    return sorted(filtered_hrefs)

if __name__ == '__main__':
    create_directories()
    cont_link = "https://codeforces.com/contest/1844"
    prob_names=[]
    for prob in get_all_prob(cont_link):
        problem_url = urljoin(cont_link, prob)
        prob_names.append(find_question_details(problem_url))
    editorial_link=extract_editorial_link(cont_link)
    extract_editorial_content(editorial_link,prob_names)
