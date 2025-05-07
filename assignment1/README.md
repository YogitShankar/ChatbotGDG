# Web Scraper for Problem Statement Extraction

This web scraper is built to extract key details from a problem page on a competitive programming platform. It automatically collects the **Problem Statement**, **Time and Memory Limits**, **Problem Title**, and **Editorial**. The scraper is designed to be flexible and scalable for different problem pages, depending on their structure.

## Features

- **Problem Statement**: Extracts the problem statement text, cleans it by removing unwanted line breaks and unnecessary whitespace, and formats it into a single continuous block.
- **Time and Memory Limits**: Gathers the time and memory limits set for solving the problem.
- **Problem Title**: Captures the problem title displayed on the page.
- **Editorial**: If available, the scraper also fetches the editorial section, which provides hints or a solution for the problem.

## How It Works

### 1. Problem Statement Extraction
The scraper first locates the main container for the problem statement. It navigates through all the `div` elements within that container, extracting the text while avoiding unnecessary line breaks or new lines. The text is concatenated into a single string that forms the problem statement, ensuring that there is no unwanted whitespace or newlines.

### 2. Time and Memory Limits Extraction
The scraper identifies the elements containing the time and memory limits specified for solving the problem. These elements are typically located in a specific section of the problem page, and their text is extracted and stored for later use.

### 3. Problem Title Extraction
The title of the problem is also captured. The scraper extracts the title from the corresponding element, which is usually located at the top of the problem page.

### 4. Editorial Extraction
If the platform provides an editorial or solution to the problem, the scraper will attempt to locate and extract that section. The editorial section usually contains insights into solving the problem and is useful for learning.

## Usage

To use this scraper, you need a working installation of Python 3 and the `selenium` library, which facilitates web automation by controlling a web browser.

### Installation
The required Python dependencies for this scraper include:
- **selenium**: A library for automating web browsers.

You can install the required library using the following pip command:

```bash
pip install selenium
