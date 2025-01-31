from embeddings import CodeBERTEmbedder 
from vectorstore import VectorStore
from retriever import RAGRetriever
from chatbot import CPChatbot


vector_store = VectorStore(index_path=r"C:\Users\prane\Downloads\faiss_index.index")

# Sample questions corresponding to embeddings (replace with actual)
questions = [
    "how to solve outstanding impressionist"
]

# Initialize embedder
embedder = CodeBERTEmbedder()  #kuch jo bhi tu define kiya hoga embeddings create karne ke liye

# Initialize RAG Retriever
retriever = RAGRetriever(embedder, vector_store, questions)

# Initialize Chatbot
system_message = (
        "You are a smart chatbot which solves competitive programming problems from codeforces. You have been trained on question sets from codeforces along with their editorial. You have to provide model solutions and help me to figure out the solutions of the problems. Do not hallucinate.\n"
    )
chatbot = CPChatbot(retriever,system_message)

# Test Chatbot
response = chatbot.chat("how to solve outstanding impressionist")
print(response)