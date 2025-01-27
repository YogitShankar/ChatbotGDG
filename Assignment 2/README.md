# CB4CP
CB4CP : ChatBot for Codeforces

CB4CP is a chatbot designed to assist with competitive programming problems from Codeforces. It uses advanced AI models and tools to provide accurate answers to queries related to problem statements, editorials, and metadata.

### Features

Retrieve and understand problem statements from Codeforces.
Answer questions based on problem editorials and metadata.
Efficiently handle large datasets with FAISS for similarity search.

### Setup Instructions

1. Create the Conda Environment
To get started, create a Conda environment and install the required libraries.

```bash
$ conda create --name cb4cp --file requirements.txt
conda activate cb4cp
```

2. Run the Examples
The examples are provided in a Jupyter Notebook file (examples.ipynb). Use the created Conda environment to execute the notebook.

```bash
jupyter notebook examples.ipynb
```

3. Configure Hugging Face API
To use the chatbot, you need to provide your Hugging Face API key.

Visit Hugging Face to get your API key if you don’t have one.
Input the key when prompted during execution.

### How to Use

Start the Chatbot
Run the provided notebook or script and follow the prompts.

#### Ask Questions

You can ask questions related to:
Problem statements.
Editorial explanations.
Metadata such as time limits, memory limits, and tags.

#### Get Responses

The chatbot uses embeddings generated with sentence-transformers/all-MiniLM-L6-v2 and FAISS for similarity-based retrieval to provide accurate answers.

Example Query

```plaintext
Q: What is the time limit for problem XYZ?
A: The time limit for problem XYZ is 2 seconds.
```

## Dataset Structure

The chatbot uses a structured dataset organized as follows:

- `data/`
  - `problems/` – Contains problem statements as text files (e.g., `problem_name.txt`).
  - `metadata/` – Contains JSON files with metadata (e.g., `problem_name.json`).
  - `editorials/` – Contains editorials as text files (e.g., `problem_name.txt`).


## Technologies Used

**Sentence-Transformers** – Using sentence-transformers/all-MiniLM-L6-v2 for creating embeddings.

**FAISS** – For efficient similarity-based retrieval.

**Mistral** – For answering queries based on retrieved chunks.