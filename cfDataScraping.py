import os
import json
import cloudscraper
from bs4 import BeautifulSoup

# File paths
data_dir = "data"
problem_file = os.path.join(data_dir, "problems.txt")
metadata_file = os.path.join(data_dir, "metadata.json")
editorial_file = os.path.join(data_dir, "editorials.txt")

# Create data directory and files if they don't exist
os.makedirs(data_dir, exist_ok=True)

for file_path in [problem_file, metadata_file, editorial_file]:
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            # Initialize metadata file with an empty JSON array
            if file_path == metadata_file:
                json.dump([], f)
            else:
                f.write("")

# Create a cloudscraper instance to bypass CAPTCHA
scraper = cloudscraper.create_scraper()

# Load existing metadata
if os.path.exists(metadata_file):
    with open(metadata_file, "r", encoding="utf-8") as meta_file:
        metadata_list = json.load(meta_file)
else:
    metadata_list = []

for page in range(1, 20):
    page_link = f"https://codeforces.com/problemset/page/{page}"
    try:
        prob_page_html = scraper.get(page_link).text
        soup_prob_list = BeautifulSoup(prob_page_html, 'html.parser')
        table = soup_prob_list.find("table", class_="problems")
        href_links = [
            a['href'] for td in table.find_all("td", class_="id")
            for a in td.find_all('a')
        ]
    except Exception as e:
        print(f"Error fetching problem list on page {page}: {e}")
        continue

    with open(problem_file, "a", encoding="utf-8") as prob_file:
        with open(editorial_file, "a", encoding="utf-8") as ed_file:
            for links in href_links:
                problem_link = f"https://codeforces.com{links}"  # Full URL
                problem_id = [links.split('/')[-2], links.split('/')[-1]]
                id = "".join(problem_id)

                try:
                    # Fetch the problem page
                    page_html = scraper.get(problem_link).text
                    soup = BeautifulSoup(page_html, 'html.parser')

                    # Extract problem details
                    problem_title = soup.find("div", class_="title").text.strip() if soup.find("div", class_="title") else "Problem title not found"
                    time_limit = soup.find("div", class_="time-limit").text.strip() if soup.find("div", class_="time-limit") else "Time limit not found"
                    memory_limit = soup.find("div", class_="memory-limit").text.strip() if soup.find("div", class_="memory-limit") else "Memory limit not found"
                    prob_statement = " ".join(p.text.strip() for p in soup.find('div', {'class': 'problem-statement'}).find_all('p')) if soup.find('div', {'class': 'problem-statement'}) else "Problem statement not found"
                    input_specs = soup.find('div', class_="input-specification").text.strip() if soup.find('div', class_="input-specification") else "Input specification not found"
                    output_specs = soup.find('div', class_="output-specification").text.strip() if soup.find('div', class_="output-specification") else "Output specification not found"
                    sample_tests = soup.find('div', class_="sample-tests").text.strip() if soup.find('div', class_="sample-tests") else "Sample tests not found"
                    prob_tags = " ".join(tag.text.strip() for tag in soup.find_all('span', class_="tag-box")) if soup.find_all('span', class_="tag-box") else "Problem tags not found"

                    # Write problem details to file
                    prob_file.write(f"Problem ID: {id}\n")
                    prob_file.write(f"Problem Statement:\n{prob_statement}\n")
                    prob_file.write(f"Input Specification:\n{input_specs}\n")
                    prob_file.write(f"Output Specification:\n{output_specs}\n")
                    prob_file.write(f"Sample Tests:\n{sample_tests}\n")
                    prob_file.write("-" * 50 + "\n")

                    # Add metadata
                    metadata_list.append({
                        "problem_id": id,
                        "problem_title": problem_title,
                        "time_limit": time_limit,
                        "memory_limit": memory_limit,
                        "problem_tags": prob_tags,
                    })

                    # Extract editorial link
                    try:
                        a = soup.find("div", class_="roundbox sidebox sidebar-menu borderTopRound")
                        b = a.find_all("li")
                        editorial_link = None

                        for li in b:
                            span1 = li.find('span')
                            span2 = span1.text
                            if ('Editorial' in span2) or ('Tutorial' in span2):
                                link = span1.find('a')['href']
                                editorial_link = f"https://codeforces.com{link}"
                                break  # Exit the loop after finding the first editorial link

                        if editorial_link:
                            try:
                                # Fetch the editorial link and check the content type
                                response = scraper.get(editorial_link)
                                if "text/html" not in response.headers.get("Content-Type", ""):
                                    raise ValueError("Editorial link leads to a non-HTML resource")

                                # Process the HTML content
                                page_html = response.text
                                tutorial_soup = BeautifulSoup(page_html, 'html.parser')
                                content = tutorial_soup.find('div', class_="content")
                                new_content = content.find_all()

                                collected_text = []
                                flag = False

                                for index in range(1, len(new_content)):
                                    tag = new_content[index]
                                    if ((tag.name == 'a') and (id in tag.text)):
                                        #print("yes")
                                        flag = True
                                        collected_text.append(tag.get_text(separator='\n', strip=True))
                                    elif ((tag.name == 'a') and (id not in tag.text) and ("/contest/" in tag['href'])):
                                        #print("no")
                                        flag = False
                                        
                                    elif flag:
                                        if 'spoiler' in tag.get('class', []):
                                            #print("hua")
                                            #print(tag.get_text(separator='\n', strip=True))
                                            collected_text.append(tag.get_text(separator='\n', strip=True))

                                ed_file.write(f"Problem ID: {id}\n")
                                ed_file.write("Editorial Content:\n")
                                ed_file.write("\n".join(collected_text))
                                ed_file.write("\n" + "-" * 50 + "\n")
                                print(f"Editorial data saved for problem {id}.")

                            except Exception as editorial_error:
                                print(f"Error processing editorial content for problem {id}: {editorial_error}")
                                ed_file.write(f"Problem ID: {id}\n")
                                ed_file.write("Editorial data not available.\n")
                                ed_file.write("-" * 50 + "\n")

                        else:
                            print(f"No editorial link found for problem {id}")
                            ed_file.write(f"Problem ID: {id}\n")
                            ed_file.write("Editorial data not available.\n")
                            ed_file.write("-" * 50 + "\n")

                    except Exception as e:
                        print(f"Error finding editorial section for problem {id}: {e}")
                        ed_file.write(f"Problem ID: {id}\n")
                        ed_file.write("Editorial data not available.\n")
                        ed_file.write("-" * 50 + "\n")

                except Exception as e:
                    print(f"Error fetching or processing problem {id}: {e}")
                    continue

# Write updated metadata to JSON file
try:
    with open(metadata_file, "w", encoding="utf-8") as meta_file:
        json.dump(metadata_list, meta_file, indent=4, ensure_ascii=False)
except Exception as e:
    print(f"Error writing metadata file: {e}")

print("Data extraction complete!")
