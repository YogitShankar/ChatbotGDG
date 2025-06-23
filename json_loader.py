import json
import os

def load_problem(problem_id, problem_path, editorial_path):
    problem_file = f"{problem_id}.json"
    editorial_file = f"{problem_id}_e.json"

    problem_data = {}
    editorial_data = {}

    try:
        with open(os.path.join(problem_path, problem_file), "r", encoding="utf-8") as f:
            problem_data = json.load(f)
    except FileNotFoundError:
        print(f"[!] Problem file not found: {problem_file}")

    try:
        with open(os.path.join(editorial_path, editorial_file), "r", encoding="utf-8") as f:
            editorial_data = json.load(f)

        if "Tutorial" in editorial_data:
            editorial_data["solution"] = editorial_data["Tutorial"]

        if "Solution/Code" in editorial_data:
            editorial_data["code"] = editorial_data["Solution/Code"]

    except FileNotFoundError:
        print(f"[!] Editorial file not found: {editorial_file}")

    return {**problem_data, **editorial_data}
