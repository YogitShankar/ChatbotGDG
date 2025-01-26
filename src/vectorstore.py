from sklearn.neighbors import NearestNeighbors

# Vector Store Implementation
class VectorStore:
    def __init__(self):
        self.data = []
        self.texts = []

    def add_embeddings(self, texts, embeddings):
        self.data = embeddings
        self.texts = texts
        self.nn = NearestNeighbors(n_neighbors=1, metric='cosine').fit(embeddings)

    def search(self, query_embedding, k=1):
        distances, indices = self.nn.kneighbors([query_embedding], n_neighbors=k)
        results = [(self.texts[idx], 1 - distances[0][i]) for i, idx in enumerate(indices[0])]
        return results
