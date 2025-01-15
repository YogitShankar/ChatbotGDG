project-directory/
│
├── chatbot/
│   ├── __init__.py
│   ├── embeddings.py           # Embedding generation logic (CodeBERTEmbedder)
│   ├── vector_store.py         # VectorStore implementation
│   ├── retriever.py            # RAGRetriever implementation
│   ├── chatbot.py              # CPChatbot implementation
│
├── scripts/
│   ├── main.py                 # Main entry point for the chatbot
│   ├── example_usage.py        # Example usage and testing
│
├── data/
│   └── combined.md             # Example Markdown file
│
├── notebooks/
│   └── demo.ipynb              # Jupyter Notebook demonstrating functionality
│
├── README.md                   # Setup and usage instructions
├── requirements.txt            # Python dependencies
└── setup.py                    # Package setup for installation