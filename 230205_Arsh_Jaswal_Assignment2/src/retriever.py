import os
import json
os.chdir("C:/Users/arshc/ChatbotGDG/230205_Arsh_Jaswal")


#Storing the files in form of dictionaries with keys as problem id
def retrieve(problem_dir, editorial_dir, metadata_dir):
    problems = {}
    solutions = {}
    metadata = {}

    print("Fetching files...")
    for filename in os.listdir(problem_dir):
        problem_id = os.path.splitext(filename)[0]
        with open(os.path.join(problem_dir, filename), "r", encoding="utf-8") as f:
            problems[problem_id] = f.read().strip()

    for filename in os.listdir(editorial_dir):
        problem_id = os.path.splitext(filename)[0]
        with open(os.path.join(editorial_dir, filename), "r", encoding="utf-8") as f:
            solutions[problem_id] = f.read().strip()

    for filename in os.listdir(metadata_dir):
        problem_id = os.path.splitext(filename)[0]
        with open(os.path.join(metadata_dir, filename), "r", encoding="utf-8") as f:
            metadata[problem_id] = json.load(f)
    print("Files fetched.")
    return problems, solutions, metadata
