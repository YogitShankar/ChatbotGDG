import os

# Directories for data storage
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROBLEMS_DIR = os.path.join(BASE_DIR, 'data', 'problems')
EDITORIALS_DIR = os.path.join(BASE_DIR, 'data', 'editorials')
METADATA_DIR = os.path.join(BASE_DIR, 'data', 'metadata')

# Create directories if they don't exist
os.makedirs(PROBLEMS_DIR, exist_ok=True)
os.makedirs(EDITORIALS_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)
