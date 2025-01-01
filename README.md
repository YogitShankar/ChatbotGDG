# ChatbotGDG
Project Submission repository 

# Codeforces Problem Scraper

## Overview
This project is a web scraper designed to extract problems, metadata, and editorials from Codeforces contests. The scraped data is organized and saved  a structured format for easy reference .

The scraper performs the following tasks:
- Retrieves links to contests from the Codeforces contests page.
- Extracts problem statements, input/output examples, and metadata (such as tags, time limits, and memory limits) from individual problems.
- Scrapes and saves editorials (if available) for each problem.

## Features
- **Scrape Contest Links**: Extracts links to contests from the Codeforces contests page.
- **Scrape Problem Statements**: Downloads problem statements, input/output examples, and stores them in `.txt` files.
- **Save Metadata**: Extracts metadata like time limits, memory limits, and tags and saves them in `.json` files.
- **Scrape Editorials**: Retrieves editorials (if available) and saves them as `.txt` files.
- **Organized Storage**: All problems and editorials are saved in their respective folders with descriptive filenames.

## Explanation of Functions in `scrap.py`

1. **`sanitize_filename(filename)`**:
   - Cleans up a string to make it safe for use as a filename by replacing invalid characters with underscores.

2. **`scrape_problem(Link)`**:
   - Navigates to a problem's page on Codeforces.
   - Scrapes the problem title, time and memory limits, tags, and problem statement with test cases.
   - Saves the problem statement as a `.txt` file and metadata as a `.json` file.

3. **`get_editorial_link(e)`**:
   - Finds the editorial link for a given problem (if available).
   - Returns the URL of the editorial or `0` if no editorial exists.

4. **`scrape_editorial(q, title)`**:
   - Navigates to the editorial page using the link provided.
   - Scrapes the content of the editorial and saves it as a `.txt` file.

5. **`get_contests_link(l)`**:
   - Navigates to the Codeforces contests page.
   - Extracts and returns a list of contest links based on the filters applied.

6. **Main Logic**:
   - Retrieves contest links using `get_contests_link()`.
   - Iterates through contests, extracting problems and their metadata using `scrape_problem()`.
   - Retrieves and saves editorials for problems using `get_editorial_link()` and `scrape_editorial()`.
