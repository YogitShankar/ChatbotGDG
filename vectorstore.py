from sklearn.neighbors import NearestNeighbors

# Vector Store Implementation
class VectorStore:
    def __init__(self, index_path=None):
        self.data = []
        self.texts = []
        self.index_path = index_path

    def add_embeddings(self, texts, embeddings):
        self.data = embeddings
        self.texts = texts
        self.nn = NearestNeighbors(n_neighbors=1, metric='euclidean').fit(embeddings)

    def search(self, query_embedding, k=1):
        distances, indices = self.nn.kneighbors([query_embedding], n_neighbors=k)
        results = [(self.texts[idx], distances[0][i]) for i, idx in enumerate(indices[0])]
        return results

# Example usage:
# vector_store = VectorStore(index_path='path/to/index/file')
# vector_store.add_embeddings(texts, embeddings)
# results = vector_store.search(query_embedding)
