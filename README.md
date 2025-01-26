
# Competitive Programming Chatbot with Retrieval-Augmented Generation (RAG)

This repository implements a Competitive Programming (CP) Chatbot that leverages a Retrieval-Augmented Generation (RAG) approach to provide accurate and contextually relevant answers to queries related to competitive programming problems and editorials.

## Overview

The system consists of several components:

1. **VectorStore**: Responsible for creating, saving, and loading the vector store (FAISS) that holds indexed documents for fast retrieval.
2. **CPChatbot**: A chatbot that uses a language model (CodeBERT) and the vector store to answer user queries by retrieving relevant documents and generating responses based on that context.
3. **CodeBERTEmbedder**: A custom embedding model that uses CodeBERT to generate embeddings for code-related texts and queries.
4. **RAGRetriever**: Responsible for retrieving relevant documents using the vector store and the embedder.

## Components

### 1. **VectorStore**

The `VectorStore` class is used to create a FAISS-based vector store that holds the indexed documents. It reads documents from multiple directories containing problem statements, editorials, and metadata, and then splits them into smaller chunks before embedding them using a specified embedder.

**Methods**:
- `create_store(embedder)`: Creates and returns a FAISS index from the documents.
- `save_store(path)`: Saves the FAISS index to a specified path.
- `load_store(path, embedder)`: Loads an existing FAISS index from a specified path.

### 2. **CPChatbot**

The `CPChatbot` class is the core of the chatbot. It combines the retrieval of relevant documents with a language model to answer user queries. It uses the `RAGRetriever` to fetch relevant documents and the `LLMChain` from Langchain to generate responses.

**Methods**:
- `chat(query)`: Takes a query from the user, retrieves relevant documents, and generates a response using the LLM model.

### 3. **CodeBERTEmbedder**

The `CodeBERTEmbedder` class uses the CodeBERT model to embed code-related texts and queries into fixed-size vectors. The embedder supports both document and query embedding.

**Methods**:
- `embed_documents(texts)`: Embeds a list of documents.
- `embed_query(text)`: Embeds a single query.

### 4. **RAGRetriever**

The `RAGRetriever` class uses the vector store to retrieve documents relevant to the user's query. It interacts with the FAISS index and returns the most similar documents based on the input query.

**Methods**:
- `retrieve(query)`: Retrieves the relevant documents based on the input query.

## Requirements

- `torch`
- `transformers`
- `langchain_core`
- `langchain_community`
- `faiss-cpu` or `faiss-gpu` (depending on your system)
- `json`

You can install the required dependencies by running:

```bash
pip install -r requirements.txt
```

## Usage

1. **Initialize Vector Store**: Create a vector store and index your documents.

```python
from vector_store import VectorStore
from code_bert_embedder import CodeBERTEmbedder

embedder = CodeBERTEmbedder()
vector_store = VectorStore()
faiss_index = vector_store.create_store(embedder)
vector_store.save_store("path_to_save_faiss_index")
```

2. **Initialize Chatbot**: Initialize the `CPChatbot` with the retriever and a system message.

```python
from cp_chatbot import CPChatbot
from rag_retriever import RAGRetriever

retriever = RAGRetriever(embedder, vector_store)
chatbot = CPChatbot(retriever, system_message="You are a competitive programming assistant.")
```

3. **Chat with the Bot**: Use the `chat` method to interact with the chatbot.

```python
response = chatbot.chat("How do I solve the knapsack problem?")
print(response)
```

## File Structure
In folder data we have the scraped data from the codeforces contests
and in folder src we have the file for the chatbot
```
.
├── vector_store.py      # Contains VectorStore class for managing FAISS index
├── cp_chatbot.py        # Contains CPChatbot class for chatbot functionality
├── code_bert_embedder.py# Contains CodeBERTEmbedder class for embedding documents and queries
├── rag_retriever.py     # Contains RAGRetriever class for document retrieval
├── requirements.txt     # List of dependencies
└── README.md            # This file
```