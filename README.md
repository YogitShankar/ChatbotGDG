# ChatbotGDG
Project Submission repository 

***
### Problem Statement
***
We were asked to analyze Codeforces webpage to scrape the webpage for problem data which include problem name, problem statement, memory & time limit, tags,  and also look for official editorial.

We had to save the problem statement in .txt file and other metadata in .json files.
***
### Approach & Implementation
***
Used selenium to navigate through the webpages and extract html code and BeautifulSoup to extract information from the html codes.
All codes are in an .ipynb file which makes it easier to run on VSCode. 

After extraction saved the data in two separate folders named **problems_text** and **problems_metadata**.

***
### Result
***
Succesfully scraped 400+ problems with their respective data stored in files named after the problem's titles.

***
### Difficulties
***
Could not scrape tutorial for some problems because the editorial page's html structure vary from contest to contest so the scraper could not respond to every editorial page to search for solution.