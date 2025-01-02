import os

DATA_DIR = "Scraped_Sample_Data"
PS_DIR = os.path.join(DATA_DIR, "Problems_Scraped")
EDITORIALS_DIR = os.path.join(DATA_DIR, "Editorials_Scraped")

os.makedirs(PS_DIR, exist_ok=True)
os.makedirs(EDITORIALS_DIR, exist_ok=True)
