import os
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver

def extract_text_with_formatting(node, text_parts):
    # Check if the node is a tag
    if hasattr(node, 'name') and node.name:  
        if node.name == 'div' and 'header' in node.get('class', ''):
            # Extract title, time limit, and memory limit
            title = node.find('div', class_='title')
            time_limit = node.find_next('div', class_='time-limit')
            memory_limit = node.find_next('div', class_='memory-limit') 
            if title:
                text_parts.append(f"{title.text.strip()}\n")
            if time_limit:
                text_parts.append(f"{time_limit.find('div', class_='property-title').text.strip()}: {time_limit.contents[-1].strip()}\n")
            if memory_limit:
                text_parts.append(f"{memory_limit.find('div', class_='property-title').text.strip()}: {memory_limit.contents[-1].strip()}")
        elif node.name == 'div' and 'sample-tests' in node.get('class', ''):
            # Find the <pre> tag inside the sample-tests
            text_parts.append("Example\n")
            text_parts.append("Input\n")
            pre_tag = node.find('div',class_='input').find('pre')
            if pre_tag:
                divs = pre_tag.find_all('div')  # Get all divs inside the <pre>
                for div in divs:
                    text_parts.append(f"{div.text.strip()}\n")  # Add each division's content on a new line
            text_parts.append("Output\n")
            output_div = node.find('div', class_='output')
            if output_div:
                pre_tag = output_div.find('pre')
                if pre_tag:
                    text_parts.append(pre_tag.text.strip() + "\n")  
        elif node.name == 'p':  # Preserve paragraphs
            text_parts.append(f"\n{''.join(extract_text_with_formatting(child, []) for child in node.children)}")
        elif node.name == 'b':  # Preserve bold text
            text_parts.append(f"*{''.join(extract_text_with_formatting(child, []) for child in node.children)}*")
        elif node.name == 'nobr':  # Handle <nobr> tag
            if node.get('aria-hidden') == 'true':  # Skip if aria-hidden="true"
                # print("t")
                # text_parts.append(" ")
                return ""
            text_parts.append(f" {''.join(extract_text_with_formatting(child, []) for child in node.children)}")
        elif node.name == 'script' and node.get('type') == 'math/tex' and node.get('id', '').startswith('MathJax-Element'):
            # text_parts.append(" ")
            return "" 
        elif node.name == 'span' and 'MJX_Assistive_MathML' in node.get('class', ''):
            text_parts.append(" ")  # Append space before text inside <span class="tt">
            text_parts.append(''.join(extract_text_with_formatting(child, []) for child in node.children))  # Add the content
            text_parts.append(" ")
        elif node.name == 'code' and 'tt' in node.get('class', ''):  # Check if class="tt"
            text_parts.append(" ")  # Append space before text inside <span class="tt">
            text_parts.append(''.join(extract_text_with_formatting(child, []) for child in node.children))  # Add the content
            text_parts.append(" ")
        else:  # Handle other tags
            for child in node.children:
                extract_text_with_formatting(child, text_parts)
    elif node.string:  # If it's plain text
        text_parts.append(node.string.strip())
    return ''.join(text_parts)

def format_code(element):
    lines = []
    for child in element.children:
        if child.name == 'span':
            text = child.get_text()
            if 'kwd' in child.get('class', []):  # Check if it has class 'kwd'
                lines.append(f"\n{text}")  # Add a new line before keywords
            else:
                lines.append(text)
        elif child.string:
            lines.append(child.string.strip())
    return ''.join(lines).strip()


def extract_details(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)

    soup=BeautifulSoup(driver.page_source,'lxml')

    problem=soup.find("div", class_="problem-statement")

    # Extract title
    title = soup.find("div", class_="title").text.strip()

    # Extract time Limit
    timeLimit=soup.find("div",class_="time-limit").get_text()
    timeLimit=timeLimit[19:]

    # Extract memory limit
    memoryLimit=soup.find("div",class_="memory-limit").get_text()
    memoryLimit=memoryLimit[21:]
    # print(memoryLimit)
    
    # Extract problem statement
    statement_div=soup.find("div", class_="problem-statement")
    statement= extract_text_with_formatting(statement_div,[])
    # print(statement)

    # Extract tags
    tags = [tag.text for tag in soup.find_all("span", class_="tag-box")]

    # Extract test cases
    # sample_tests=soup.find('div',class_='sample-test').get_text(separator='\n',strip=True)

    metadata = {
            "title": title,
            "tags": tags,
            "time_limit": timeLimit,
            "memory_limit": memoryLimit,
            # "sample_tests":sample_tests,
        }

    problem_id = url.replace("https://codeforces.com", "").strip("/")
    problem_id = problem_id.replace("/", "_")

    os.makedirs('PROBLEMS_DIR', exist_ok=True)
    os.makedirs('METADATA_DIR', exist_ok=True)
    
    with open(os.path.join('PROBLEMS_DIR', f"{problem_id}.txt"), "w", encoding="utf-8") as f:
            f.write(statement)
    with open(os.path.join('METADATA_DIR', f"{problem_id}.json"), "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)

    contest_materials=soup.find('div',class_="roundbox sidebox sidebar-menu borderTopRound")
    tutorial_directed_links = contest_materials.find_all('a')
    tutorial_directed_link=tutorial_directed_links[1]
    text=tutorial_directed_link.get_text().strip()

    if(tutorial_directed_link and 'Tutorial' in text ):
        tutorial_url='https://codeforces.com'+tutorial_directed_link['href']
        # print(tutorial_url)
        driver = webdriver.Chrome()
        driver.get(tutorial_url)
        time.sleep(2)
        soup=BeautifulSoup(driver.page_source,'lxml')
        linkSection=soup.find('div','ttypography')
        links=linkSection.find_all('p')
        # print(links)

        for p in links:
            link = 'https://codeforces.com'+p.a['href'] if p.a else None
            if link and link == url:  # Check if the link matches the desired URL
                current_div = p.find_next_sibling('div')
                # print(current_div)
                tutorial_section = current_div.find('div', class_='spoiler-content')
                os.makedirs('EDITORIAL_DIR', exist_ok=True)
                # Extract the content while preserving formatting
                if tutorial_section:
                        # print(tutorial_section)
                        preserved_format = extract_text_with_formatting(tutorial_section,[])  # Keeps all inner HTML structure
                        with open(os.path.join('EDITORIAL_DIR', f"{problem_id}_tutorial.txt"), "w", encoding="utf-8") as f:
                               f.write(preserved_format)
                spoiler_divs = []
                while current_div:
                    if current_div.name == 'div' and 'spoiler' in current_div.get('class', []):
                        spoiler_divs.append(current_div)
                        if len(spoiler_divs) == 2:  # Stop when we find the second div
                            break
                    current_div = current_div.find_next_sibling()  # Move to the next sibling

                if len(spoiler_divs) == 2:
                    second_spoiler_div = spoiler_divs[1]
                code_block = second_spoiler_div.find('pre').find('code',class_='prettyprint prettyprinted')
                # print(code_block)
                if code_block:
                    # solution_content = code_block.get_text(separator='\n', strip=True)
                    solution_content=format_code(code_block)
                    with open(os.path.join('EDITORIAL_DIR', f"{problem_id}_solution.txt"), "w", encoding="utf-8") as f:
                               f.write(solution_content)

                    # print(solution_content)

if __name__=='__main__':
    print("please type the link of the problem that you want to know the details with: ")
    url = input()
    # time.sleep(2)
    extract_details(url)