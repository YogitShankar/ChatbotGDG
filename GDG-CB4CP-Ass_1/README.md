# GDG-CB4CP-Ass_1

# **Codeforces Problem Scraper**

This script automates the process of scraping problems from the Codeforces problem set, extracting their details, and saving them in a structured text format.

---

## **Features**
- Extracts problem details, including:
  - Title
  - Problem statement
  - Time and memory limits
  - Sample input and output
- Formats mathematical expressions from LaTeX to readable symbols.
- Bypasses CAPTCHA using `cloudscraper`.
- Saves problem statements in text files.

---

## **Setup Instructions**

### **1. Install Required Libraries**
Install the necessary Python libraries:
```bash
pip install cloudscraper beautifulsoup4 selenium
```

### **2. Download ChromeDriver**
- Ensure you have ChromeDriver compatible with your version of Chrome.
- Update the `driver_path` variable in the script with the path to your ChromeDriver binary.

### **3. Run the Script**
Execute the script using:
```bash
python problem_scraper.py
```

---

## **Code Structure**

### **1. Import Dependencies**
The script uses the following libraries:
- `os`, `time`, `random`, `re`: For file handling, delays, and regular expressions.
- `cloudscraper`: Bypasses CAPTCHA protection.
- `BeautifulSoup`: Parses HTML content.
- `selenium`: Automates browser interactions.

---

### **2. Helper Functions**

#### **Sanitize Filename**
Replaces invalid characters in filenames with underscores:
```python
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)
```

#### **Format MathJax**
Converts MathJax LaTeX elements into readable symbols:
```python
def format_mathjax(element):
    ...
```

---

### **3. Main Function: `extract`**

#### **Parameters**:
- `start_page`: The starting page number for scraping.
- `end_page`: The ending page number for scraping.
- `base_url`: The base URL for Codeforces problem sets.

#### **Workflow**:
1. Initialize `cloudscraper` and Selenium WebDriver.
2. Loop through pages from `start_page` to `end_page`.
3. For each problem:
   - Fetch problem details: Title, tags, url, statement, limits, and samples.
   - Replace LaTeX commands with symbols.
   - Save data in text files.
   - Save metadata in json file.

---

## **Output**
- Problem statements are saved in the `./data/problems` directory.
- Metadata is saved in the `./data/metadata` directory.
- Text file contains:
  - Title
  - Time and memory limits
  - Problem statement
  - Sample tests (input and output)
- Json file contains:
  - Contest ID
  - Problem Title
  - Url
  - Tags
  - Time and memory limits

---

## **Error Handling**
- Logs errors for pages or problems that fail to process.
- Ensures the Selenium driver closes properly after execution.

---
