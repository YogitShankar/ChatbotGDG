import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROBLEMS_DIR = os.path.join(    DATA_DIR, "problems")
if not os.path.exists(PROBLEMS_DIR):
    os.makedirs(PROBLEMS_DIR)
METADATA_DIR= os.path.join(DATA_DIR, "metadata")
if not os.path.exists(METADATA_DIR):
    os.makedirs(METADATA_DIR)