import json
from transformers import RobertaTokenizer, RobertaModel
import torch
import faiss
import numpy as np

class CodeBERTEmbedder:
    def __init__(self):
        model_name = "microsoft/codebert-base"
        self.tokenizer = RobertaTokenizer.from_pretrained(model_name)
        self.model = RobertaModel.from_pretrained(model_name)

    def generate_embedding(self, text):
        tokens = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            output = self.model(**tokens)
        return output.last_hidden_state.mean(dim=1)

    def batch_generate_embeddings(self, texts):
        embeddings = [self.generate_embedding(text) for text in texts]
        return torch.cat(embeddings, dim=0)
    
class VectorStore:
    def __init__(self):
        self.dim = 768
        self.index = faiss.IndexFlatIP(self.dim)

    def add_vectors(self, embeddings):
        if isinstance(embeddings, torch.Tensor):
            embeddings = embeddings.cpu().numpy()
        self.index.add(embeddings)

    def search(self, query_embedding, top_k=5):
        if isinstance(query_embedding, torch.Tensor):
            query_embedding = query_embedding.cpu().numpy()
        distances, indices = self.index.search(query_embedding, top_k)
        return distances, indices
    
class RAGRetriever:
    def __init__(self):
        self.embedder = CodeBERTEmbedder()
        self.vector_store = VectorStore()

    def add_contexts(self, texts):
        embeddings = self.embedder.batch_generate_embeddings(texts)
        self.vector_store.add_vectors(embeddings)

    def retrieve_context(self, query, top_k=5):
        query_embedding = self.embedder.generate_embedding(query)
        distances, indices = self.vector_store.search(query_embedding, top_k)
        return distances, indices

class CPChatbot:
    def __init__(self):
        self.retriever = RAGRetriever()
        self.system_message = "I am here to assist with Competitive Programming problems."

    def add_knowledge_base(self, contexts):
        self.retriever.add_contexts(contexts)

    def chat(self, query):
        distances, indices = self.retriever.retrieve_context(query, top_k=1)
        
        most_relevant_problem = data[indices[0][0]]

        response = "Most relevant problem:\n"
        response += f"Title: {most_relevant_problem['title']}\n"
        response += f"Description: {most_relevant_problem['description']}\n"
        response += f"Time Limit: {most_relevant_problem['time_limit']}\n"
        response += f"Memory Limit: {most_relevant_problem['memory_limit']}\n"
        response += f"Tags: {', '.join(most_relevant_problem['tags'])}\n"
        response += f"Solution: {most_relevant_problem['solution']}\n"
        
        return response

with open('Problem-Data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

chatbot = CPChatbot()
chatbot.add_knowledge_base(data)