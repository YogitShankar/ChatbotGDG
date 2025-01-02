import os
import time
import json

def save_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    # Check file extension to determine how to save
    if filepath.endswith('.json'):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

def apply_delay(seconds):
    time.sleep(seconds)
