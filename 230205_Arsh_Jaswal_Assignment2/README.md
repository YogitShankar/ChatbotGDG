# README

## ChatBot for Competitive Programming

This project demonstrates a Retrieval-Augmented Generation (RAG) system designed to assist with competitive programming. It integrates various tools and models to retrieve and analyze programming problems and generate helpful solutions or context-aware responses using scraped data from [CodeForces](https://codeforces.com).

---
## Virtual Enviornment

The project mentioned is made over venv (Python virtual environment), therefore most of the requirements and dependencies are already downloaded inside the folder.

---
## Features

1. **Text Generation**: Utilizes [Ollama's Llama 3.2](https://ollama.com/) for text generation.
2. **Embedding Generation**: Employs CodeBERT to generate embeddings for problem statements, inputs, outputs, and notes.
3. **Vector Search**: Implements FAISS for efficient similarity search and retrieval of related problems.
4. **Dynamic Chatbot**: A chatbot template is provided that leverages LangChain for conversational interactions, allowing context-aware and memory-retentive discussions.

---

## Overview

This project provides a unique and efficient approach to solving common challenges faced in competitive programming by leveraging advanced AI technologies. Here are some reasons why this project stands out:

1. **Enhanced Problem Solving**:
   - It helps programmers quickly find similar problems or solutions by analyzing problem descriptions and retrieving relevant examples.

2. **Time-Saving**:
   - By automating the search and retrieval process, the system reduces the time spent on finding references or related problems.

3. **Context-Aware Responses**:
   - The chatbot tries that responses are relevant to the query, provided with an emotional and strong prompt template.

4. **Local Model Usage**:
   - Using a local model like Ollama's Llama 3.2 ensures privacy and control over data while providing high-quality results.

5. **Foundation for Future Development**:
   - The modular design and integration with FAISS, CodeBERT, and LangChain make it a strong foundation for further improvements and scalability.

6. **Maintains Chat History**:
   - Able to maintain and recall previous chat history.


---

## Installation and Setup

1. **Install Ollama's Llama 3.2**:
   - Download and install the [Ollama](https://ollama.com/) application for your operating system.
   - Install the Llama 3.2 model using the command in terminal:
     ```bash
     ollama run llama3.2
     ```

2. **Install Required Libraries**:
   Install the dependencies listed in `requi.txt` using pip:
   ```bash
   pip install -r requi.txt
   ```

3. **Set Up the Environment**:
   - Ensure FAISS is installed for vector indexing and searching.

4. **Prepare Data**:
   - Preprocessed problem statements, editorials, and metadata files in appropriate directories.

---

## Issues and Known Limitations

1. **Accuracy**:
   - The accuracy is not exceptionally good, as Llama 3.2 was used. 
   _**Solution**: This could be improved by using models like CodeLlama or similar for text generation._
   

2. **Index Search Dependency**:
   - The index search relies heavily on the problem description. If the description is trimmed or incomplete, the index fails to recognize the problem accurately.
   - If the query is very vague, it may give very random answer (sometimes answer to the retrieved similar problem)
    _**Solution**: We can generate **dummy questions** for every question using Llama3.2 or other text generation models, so that if question different from original question, can match with the corresponding dummy question. I have not done this as I wanted to demonstrate the model only, Also I already had a huge pile of CF scraped questions, So implementing this would have been a very intensive task._

3. **Query Guidelines**:
   - When typing a query, always prefer including the text with the problem description (excluding test cases) for better results.
    _**Solution**: Same as above._

4. **Value of k**:
   - The system uses `k=1` for nearest neighbor search. A higher value of `k` would yield more similar problems, but this could exceed the model's context limit, **leading to truncation**.

5. **Context Length**:
   - The inclusion of chat history leads to an exponential increase in context, which may result in truncation when the context becomes too long. 

6. **Model Choice**:
   - Although APIs/transformers could be used for text generation, this project uses Ollama's local model (Llama 3.2) as a personal preference.

---

## Credits

- **Arsh Jaswal** (230205)
- Tools and libraries used: Ollama's Llama 3.2, CodeBERT, FAISS, LangChain.

---

## Contact

For query or feedback, please reach out to arshj23@iitk.ac.in.

---

Thank you for exploring this project!