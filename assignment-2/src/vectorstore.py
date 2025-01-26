import faiss
import numpy as np

class VectorStore:
    def __init__(self, dimension=None):
        self.index = None
        self.file_mapping = []
        self.dimension = dimension

    def _initialize_index(self, dimension):
        if dimension is None:
            raise ValueError("Embedding dimension cannot be None")
        self.index = faiss.IndexFlatL2(dimension)  

    def add_vectors(self, embeddings, file_paths):
        """Add vectors and corresponding metadata (file paths)."""
        embeddings_array = np.array(embeddings, dtype="float32")

        if self.index is None or embeddings_array.shape[1] != self.index.d:
            self._initialize_index(embeddings_array.shape[1])

        embeddings_array /= np.linalg.norm(embeddings_array, axis=1, keepdims=True)
        self.index.add(embeddings_array)
        self.file_mapping.extend(file_paths)

    def search(self, query_vector, top_k=3):
        query_array = query_vector.reshape(1, -1).astype("float32")
        query_array /= np.linalg.norm(query_array, axis=1, keepdims=True)
        distances, indices = self.index.search(query_array, top_k)
        results = [self.file_mapping[i] for i in indices[0] if i >= 0 and i < len(self.file_mapping)]
        return results, distances[0]
