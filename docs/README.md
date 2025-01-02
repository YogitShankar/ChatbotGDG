# Codeforces Problem Scraper

## Overview
This tool scrapes problem statements and editorials from Codeforces, preserving LaTeX formatting and code blocks.

## Features
- Extracts problem statements with preserved LaTeX formatting
- Captures test cases and sample inputs/outputs
- Preserves code blocks with proper formatting
- Stores metadata in JSON format
- Includes editorial content with proper section handling

## Project Structure
```
project/
├── data/
│   ├── problems/
│   ├── editorials/
│   ├── metadata/
│   └── samples/
└── docs/
```

## Usage
Run `main.py` to start the scraper:
```bash
python main.py
```

## Configuration
Settings can be modified in `config.json`
