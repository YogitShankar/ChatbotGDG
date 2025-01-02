import os
import json

def save_to_file(file_path, content, mode='w'):
    with open(file_path, mode, encoding='utf-8') as f:
        f.write(content)

def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def log_error(url, error_message):
    log_file = "error.log"
    with open(log_file, "a") as f:
        f.write(f"Error scraping {url}: {error_message}\n")
