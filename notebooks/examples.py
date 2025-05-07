import sys
from pathlib import Path

# Add the src directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

# Import necessary classes
from embedding import CodeBERTEmbedder
from vectorstore import VectorStore
from retriever import RAGRetriever
from chatbot import CPChatbot
import numpy as np

# Initialize the embedder, vector store, and retriever
embedder = CodeBERTEmbedder()
vector_store = VectorStore(dim=768)
retriever = RAGRetriever(embedder, vector_store)

# Add sample data
vector_store.add(np.random.rand(1, 768), {"title": "Problem 1", "content": "Subarray Sum"})
vector_store.add(np.random.rand(1, 768), {"title": "Problem 2", "content": "Knapsack"})

# Create the chatbot
system_message = "I am solving a Competitive Programming problem. Answer my questions."
chatbot = CPChatbot(retriever, system_message)

# Query the chatbot
response = chatbot.chat("How do I solve problem C?")
print(response)

