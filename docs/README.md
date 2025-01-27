 Codeforces Chatbot with CodeBERT for Competitive Programming

## Overview
This tool leverages pre-scraped Codeforces problems, their editorials, and metadata to create an intelligent assistant powered by CodeBERT that helps users understand and solve competitive programming problems.

## Features
- Embedding generation using CodeBERT for problem texts and editorials
- Vector store management for efficient search and retrieval
- RAG (Retrieval-Augmented Generation) implementation for context-aware response generation
- Chatbot interface for user interaction with real-time responses
- Example usage to showcase the functionality

## Project Structure
```
project/
├── data/
│   ├── problems/        # Scraped problem data
│   ├── editorials/      # Problem editorials
│   └── metadata/        # Problem metadata
├── src/
│   ├── embeddings.py     # CodeBERT embedding generation
│   ├── vectorstore.py    # Vector database management
│   ├── retriever.py      # RAG implementation
│   └── chatbot.py        # Chatbot interface
├── notebooks/
│   └── examples.ipynb    # Usage examples
└── docs/
```

## Usage
Run `main.py` to start the chatbot interface and interact with the assistant:
```bash
python main.py
```

### **Testing the Embedder**
```python
# Test single embedding
embedder = CodeBERTEmbedder()
test_text = "Find the maximum subarray sum"
embedding = embedder.generate_embedding(test_text)
print(f"Embedding shape: {embedding.shape}")

# Test batch embedding
texts = [
    "Find the maximum subarray sum",
    "Implement a segment tree",
    "Solve the knapsack problem"
]
embeddings = embedder.batch_generate_embeddings(texts)
print(f"Batch embeddings shape: {embeddings.shape}")
```

### **Example Chatbot Usage**
```python
# Initialize components
embedder = CodeBERTEmbedder()
vector_store = VectorStore()
retriever = RAGRetriever(embedder, vector_store)

# Create chatbot
system_message = '''I am solving a competitive programming problem and need help understanding its editorial.
Answer my questions regarding the editorial. Let me know if I'm misunderstanding anything.
Do not write or debug code.'''
chatbot = CPChatbot(retriever, system_message)

# Chat
response = chatbot.chat("How do I solve problem C from Contest #792?")
print(response)
```

## Configuration
Settings can be modified in `config.json` to adjust paths, system behavior, or other parameters.
