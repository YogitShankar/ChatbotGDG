import os

DATA_DIR = "data"
PROBLEMS_DIR = os.path.join(DATA_DIR, "problems")
EDITORIALS_DIR = os.path.join(DATA_DIR, "editorials")

os.makedirs(PROBLEMS_DIR, exist_ok=True)
os.makedirs(EDITORIALS_DIR, exist_ok=True)
