
# Web Scraping Code for Codeforces Problem Details and Editorials

This Python script is designed to scrape problem details and editorial solutions from Codeforces problem pages. It extracts essential problem information, such as the problem statement, time and memory limits, tags, and editorial content (if available), then saves these details into text and JSON files.

## Requirements

Before running the script, you need to install the following Python libraries:

```bash
pip install selenium beautifulsoup4 lxml
```
# Code Overview

The script performs the following operations:

## Extract Problem Details:
- **Problem Title**
- **Tags**
- **Time and Memory Limits**
- **Problem Statement**

## Store Problem Details:
- Saves the problem statement into a `.txt` file within the `PROBLEMS_DIR` directory.
- Saves metadata, such as the title, tags, time, and memory limits, into a `.json` file within the `METADATA_DIR` directory.

## Extract Editorial and Solution:
- If a tutorial is available, the script fetches it and saves the tutorial content into the `EDITORIAL_DIR`as `{problem_id}_tutorial.txt`.
- Extracts the solution code from the editorial and saves it as a `{problem_id}_solution.txt` file in the `EDITORIAL_DIR`.

# Functions

### Function Explanation: `extract_text_with_formatting`

This function is designed to traverse an HTML structure and extract well-formatted text based on specific rules for various HTML tags and classes. It handles:

1. **Headers (`header` class)**: Extracts the title, time limit, and memory limit, formatting them with appropriate labels and values.
2. **Sample Tests (`sample-tests` class)**: Processes input and output sections, ensuring each line in `<div>` or `<pre>` tags appears on a new line.
3. **Text Formatting**: Preserves the structure of paragraphs, bold text, and math/technical content while skipping unnecessary elements (e.g., hidden math or specific scripts).
4. **General Traversal**: Recursively traverses all child nodes, appending plain text or structured content for seamless formatting.

The function ensures accurate extraction of problem statements, sample inputs/outputs, and other important details from HTML documents.


#### Parameters:
- `element`: A BeautifulSoup element (part of the parsed HTML tree).

#### Returns:
- A string with the text extracted from the `element`, with formatting preserved.

---

### `format_code(element)`

This function processes the code and maintain the new lines and preserve the structure of the solution_code 

#### Parameters:
- `element`: A BeautifulSoup `span` element containing code.

#### Returns:
- A string with the formatted code.

---

### `extract_details(url)`

This is the main function of the script, which:
- Extracts problem details (title, tags, time and memory limits, problem statement).
- Saves the details in the appropriate files.
- Checks for a tutorial and extracts it (if available).
- Extracts the solution from the editorial page and saves it.

#### Parameters:
- `url`: The URL of the Codeforces problem page.

---

## Example Usage

```python
if __name__ == '__main__':
    print("Please type the link of the problem that you want to know the details about: ")
    url = input()
    extract_details(url)


