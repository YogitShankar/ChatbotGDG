import numpy as np

class RAGRetriever:
    def __init__(self, embedder, vector_store):
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(self, query, top_k=5):
        query_embedding = self.embedder.generate_embedding(query)
        
        # Ensure query_embedding is 2D
        query_embedding = np.squeeze(query_embedding, axis=0)  # Remove extra dimensions

        print("Query embedding shape:", query_embedding.shape)  # Debug print
        
        return self.vector_store.search(query_embedding, top_k)
