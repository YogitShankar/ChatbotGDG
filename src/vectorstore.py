import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)  # L2 distance metric
        self.metadata = []

    def add(self, embedding, metadata):
        # Ensure the embedding is 2D with shape (1, 768)
        embedding = np.array(embedding, dtype=np.float32)
        if len(embedding.shape) == 1:
            embedding = np.expand_dims(embedding, axis=0)  # Reshape if it's 1D
        self.index.add(embedding)
        self.metadata.append(metadata)

    def search(self, query_embedding, top_k):
        # Ensure query_embedding is 2D as well
        query_embedding = np.array(query_embedding, dtype=np.float32)
        if len(query_embedding.shape) == 1:
            query_embedding = np.expand_dims(query_embedding, axis=0)  # Reshape if it's 1D
        _, indices = self.index.search(query_embedding, top_k)
        return [self.metadata[i] for i in indices[0]]
