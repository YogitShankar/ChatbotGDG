import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import json
import time
import cloudscraper
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModel
import torch
import faiss
from complete import scrape_codeforces_problems


# 1. Fetch and store problem data

def fetch_problem_links(start_page, end_page):
    scraper = cloudscraper.create_scraper()
    base_url = "https://codeforces.com/problemset/page/"
    problem_links = []
    
    for page in range(start_page, end_page + 1):
        print(f"Fetching problem links from page: {page}")
        url = f"{base_url}{page}"
        response = scraper.get(url)
        time.sleep(1)

        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", {"class": "problems"})

        if table:
            rows = table.find_all("tr")
            for row in rows:
                id_td = row.find("td", {"class": ["id", "id dark"]})
                tag_td = row.find("td", {"class": "tags"})
                
                if id_td:
                    a_tag = id_td.find("a")
                    if a_tag:
                        problem_text = a_tag.text.strip()
                        problem_link = f"https://codeforces.com{a_tag['href']}"
                        tags = [tag.text.strip() for tag in tag_td.find_all("a")] if tag_td else []
                        problem_links.append((problem_text, problem_link, tags))
        else:
            print(f"No problems found on page {page}.")
    return problem_links


def fetch_problem_details(url):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    time.sleep(1)
    
    soup = BeautifulSoup(response.content, "html.parser")
    problem_statement = soup.find("div", class_="problem-statement")
    
    if not problem_statement:
        print(f"Problem content not found at {url}.")
        return None

    mathjax = problem_statement.find_all("span", class_="mathjax")
    for math in mathjax:
        math.replace_with(f"$$ {math.text} $$")
    
    problem_text = problem_statement.get_text(separator="\n").strip()
    problem_metadata = {
        "name": problem_statement.find("div", class_="title").text.strip() if problem_statement.find("div", class_="title") else "N/A",
        "time_limit": problem_statement.find("div", class_="time-limit").text.strip() if problem_statement.find("div", class_="time-limit") else "N/A",
        "memory_limit": problem_statement.find("div", class_="memory-limit").text.strip() if problem_statement.find("div", class_="memory-limit") else "N/A",
        "input": problem_statement.find("div", class_="input-specification").text.strip() if problem_statement.find("div", class_="input-specification") else "N/A",
        "output": problem_statement.find("div", class_="output-specification").text.strip() if problem_statement.find("div", class_="output-specification") else "N/A",
    }
    return problem_text, problem_metadata


# 2. CodeBERT Embeddings

def generate_embedding(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()


# 3. Store embeddings in FAISS

def store_embeddings(problems, tokenizer, model):
    dimension = 768
    index = faiss.IndexFlatL2(dimension)
    id_map = {}
    
    for i, (problem_id, problem_text) in enumerate(problems.items()):
        embedding = generate_embedding(problem_text, tokenizer, model)
        index.add(embedding)
        id_map[i] = problem_id
    
    faiss.write_index(index, "faiss_index.idx")
    with open("id_map.json", "w") as f:
        json.dump(id_map, f)
    print("FAISS index saved.")


# 4. RAG-based Retrieval

def retrieve_problem(query, tokenizer, model):
    index = faiss.read_index("faiss_index.idx")
    with open("id_map.json") as f:
        id_map = json.load(f)
    
    query_embedding = generate_embedding(query, tokenizer, model)
    distances, indices = index.search(query_embedding, 3)
    retrieved_problems = [id_map[str(idx)] for idx in indices[0]]
    return retrieved_problems


# 5. Chatbot Implementation

def chatbot():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    model = AutoModel.from_pretrained("microsoft/codebert-base")
    
    while True:
        query = input("Ask a question about a problem (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break
        relevant_problems = retrieve_problem(query, tokenizer, model)
        print(f"Relevant problems: {relevant_problems}")


output_dir = "codeforces_problems"

# Check if data already exists
if os.path.exists(output_dir) and len(os.listdir(output_dir)) > 0:
    print("Skipping scraping... Using existing problem data.")
else:
    start_page = int(input("Enter the start page number: "))
    end_page = int(input("Enter the end page number: "))
    scrape_codeforces_problems(start_page, end_page, output_dir)
    
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base")
    
    #problems = {pid: fetch_problem_details(url)[0] for pid, url, _ in fetch_problem_links(start_page, end_page)}
problems = {}    
problem_files = [f for f in os.listdir(output_dir) if f.endswith(".json")]

if len(problem_files) > 0:
    print("Loading problems from saved JSON files...")
    
    for file in problem_files:
        with open(os.path.join(output_dir, file), "r", encoding="utf-8") as f:
            data = json.load(f)
        problems[file.replace(".json", "")] = data["name"]  # Store problem title
else:
    print("No saved problems found. You may need to scrape again.")
    


store_embeddings(problems, tokenizer, model)
chatbot()
