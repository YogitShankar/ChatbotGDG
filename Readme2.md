# Competitive Programming Chatbot

This project is a chatbot built to assist in solving competitive programming problems. It uses a combination of problem statements and their associated editorials to provide contextual help to users based on their queries.

The chatbot leverages advanced Natural Language Processing (NLP) techniques, including CodeBERT for embedding generation and nearest neighbor search for retrieving relevant information. The goal of this chatbot is to help users understand the editorial of a problem without writing or debugging code.

## Features

- Retrieves the most relevant editorial for a given query from a set of problem statements and editorials.
- Uses a pre-trained CodeBERT model to generate embeddings for problems and editorials.
- Searches for the closest matching editorial using nearest neighbor techniques (Cosine Similarity).
- Simple and intuitive chatbot interaction for users seeking help with competitive programming problems.

## Requirements

- Python 3.x
- PyTorch
- Transformers library
- Scikit-learn
- NumPy

## Setup Instructions

1. **Clone the Repository**
    ```bash
    git clone https://github.com/[username]/competitive-programming-chatbot.git
    cd competitive-programming-chatbot
    ```

2. **Install Dependencies**
    Install the required Python libraries using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

3. **Prepare the Data**
    The chatbot requires two sets of data:
    - **Problem Statements**: A directory of text files containing competitive programming problem statements.
    - **Editorials**: A directory of text files containing editorials for the respective problems.
    
    Ensure you have your data organized in the following way:
    ```
    data/
        problem_statements/
            problem1.txt
            problem2.txt
            ...
        editorials/
            editorial1.txt
            editorial2.txt
            ...
    ```

4. **Run the Chatbot**
    To run the chatbot, simply execute the following command:
    ```bash
    python main.py
    ```

    Enter a query when prompted, and the chatbot will provide a response based on the context retrieved from the problem statements and editorials.

## How It Works

- **Embedding Generation**: The `CodeBERTEmbedder` class uses the pre-trained `microsoft/codebert-base` model to generate embeddings for both problem statements and editorials.
- **Vector Store**: Embeddings are stored in a vector store using the `VectorStore` class, and nearest neighbor search is performed to find the most relevant editorial for a user's query.
- **RAG (Retrieval-Augmented Generation)**: The `RAGRetriever` class retrieves the most relevant editorial context for a given query.
- **Chatbot Interaction**: The `CPChatbot` class takes care of interacting with the user, retrieving relevant information, and displaying it in a chatbot format.

## Code Structure

- `main.py`: The main script that loads the data, initializes components, generates embeddings, and runs the chatbot.
- `embedding.py`: Contains classes related to embedding generation and vector store functionality.
- `README.md`: This file with instructions on setting up and running the chatbot.
- `data/`: Contains the directory structure for problem statements and editorials.

## Example

- After running the script, the user will be prompted to enter a query, for example:
- Enter your query: Can you explain the editorial for problem 1?

- The chatbot will respond with the most relevant context based on the editorial for that problem.

## Notes

- Ensure your problem statements and editorials are organized correctly in the `data/` directory.
- The CodeBERT model may require substantial memory; make sure your environment can handle it.
- This project is a simple retrieval-based chatbot, so it won't generate new editorial content but will only retrieve and display pre-existing information.


