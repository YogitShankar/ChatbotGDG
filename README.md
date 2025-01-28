# Codeforces Problem Scraper Documentation

## Overview
This Python script scrapes problems from Codeforces contests. For a given contest ID, it extracts:

- **Problem Title**
- **Problem Statement**
- **Time and Memory Limits**
- **Tags**

The scraped data is saved in structured formats:

1. **Problem Statements**: Saved as `.txt` files in the `problems/` folder.
2. **Metadata**: Saved as `.json` files in the `metadata/` folder.

---

## Features
- **Input**: Enter the contest ID (e.g., `2043`).
- **Dynamic Problem Detection**: Automatically detects problems like `A`, `B`, `C`, etc., until no more problems are found.
- **Formatted Output**: Mathematical expressions (`$$$`) are converted to LaTeX-style `$` for readability.
- **Error Handling**: Gracefully handles missing problems or invalid contest IDs.

---

## Prerequisites
Ensure you have the following installed:

1. **Python 3.6+**
2. Python libraries:
   - `beautifulsoup4`
   - `urllib`

You can install the required library using:
```bash
pip install beautifulsoup4
```

---

## How to Use

1. Clone or download the script.
2. Navigate to the script's directory in your terminal or IDE.
3. Run the script:
   ```bash
   python scraper.py
   ```
4. When prompted, enter the contest ID (e.g., `2043`).

Example:
```
Enter a contest ID (e.g., 2043): 2043
```

5. The script will:
   - Scrape all available problems (`A`, `B`, `C`, ...) from the specified contest.
   - Save the problem statements and metadata to the respective folders.

---

## Output Directory Structure
```
project/
├── problems/         # Contains problem statements as .txt files
│   ├── 2043_A.txt
│   ├── 2043_B.txt
│   └── ...
├── metadata/         # Contains metadata as .json files
│   ├── 2043_A.json
│   ├── 2043_B.json
│   └── ...
└── scraper.py        # The main Python script
```

---

## Example Outputs

### Problem Statement (`problems/2043_A.txt`):
```
Problem Title: A. Coin Transformation
Time Limit: 2 seconds
Memory Limit: 512 megabytes
Tags: math, greedy

Problem Statement:
Initially, you have a coin with value $n$. You can perform the following operation any number of times (possibly zero): transform one coin with value $x$, where $x$ is greater than $3$ ($x > 3$), into two coins with value $\lfloor \frac{x}{4} \rfloor$.
...
```

### Metadata (`metadata/2043_A.json`):
```json
{
    "contest_id": "2043",
    "problem_id": "A",
    "title": "A. Coin Transformation",
    "tags": ["math", "greedy"],
    "time_limit": "2 seconds",
    "memory_limit": "512 megabytes"
}
```

---

## Limitations
- Requires an active internet connection.
- Stops scraping when it encounters missing problems or invalid contest IDs.
- LaTeX expressions are preserved as text (`$`) and not rendered visually.

---

## Notes
1. Be respectful of Codeforces’ terms of service when scraping.
2. Add delays between requests to avoid overwhelming their servers.

---

## Future Enhancements
- Add support for scraping editorials.
- Render mathematical expressions visually using a library like `sympy` or `MathJax`.
