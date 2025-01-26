import numpy as np
import faiss

class VectorDatabase:
    def __init__(self, index_type="IndexFlatIP", num_clusters=100):
        self.index_type = index_type
        self.num_clusters = num_clusters
        self.index = None

    def create_index(self, embeddings):
        embeddings = np.array(embeddings, dtype="float32")
        embedding_dim = embeddings.shape[1]
        if self.index_type == "IndexFlatIP":
            self.index = faiss.IndexFlatIP(embedding_dim)
        elif self.index_type == "IndexFlatL2":
            self.index = faiss.IndexFlatL2(embedding_dim)
        else:
            raise ValueError(f"Unsupported index_type: {self.index_type}")

        self.index.add(embeddings)

    def save_index(self, file_path):
        if self.index:
            faiss.write_index(self.index, file_path)

    def load_index(self, file_path):
        self.index = faiss.read_index(file_path)

    def search(self, query_embedding, top_k=5):
        query_embedding = np.array(query_embedding, dtype="float32")
        distances, indices = self.index.search(query_embedding, top_k)
        return indices, distances
