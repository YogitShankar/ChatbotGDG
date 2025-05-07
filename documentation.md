# How the Scraper Works
This scraper fetches problem statements and editorials from Codeforces contests using the following process:

# Setup and Initialization:

The script uses undetected_chromedriver with Selenium to interact with the Codeforces website.
BeautifulSoup is employed for parsing the HTML source.

Directory structures (scraped_data/problems and scraped_data/editorials) are created dynamically to store the results.

# Contest List Extraction:

The main contest page is scraped to extract contest links.
A limit is set to process a specific number of contests.


# Problem Scraping:

Each problem's page is accessed, and the script extracts:
Title, statement, input/output specifications, sample tests, and tags.
Time and memory limits.
Missing elements are skipped gracefully to avoid interruptions.


# Editorial Scraping:

Editorial links are parsed, and spoiler hints are extracted where available.
Content is saved in a structured text file for offline reference.
LaTeX Conversion:

Any LaTeX found in the scraped content is converted to a readable format for better accessibility.


# Error Handling:

Missing elements or links do not stop the scraping; the script proceeds to the next available item.


# saving the extracted data:

Problem statements are saved as text files.
Metadata is stored in JSON format.
Editorial are saved in a dedicated text file.


This implementation is efficient and ensures robustness against incomplete or malformed HTML elements.

