class RAGRetriever:
    def __init__(self, embedder, vector_store,query):
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve_context(self, query, top_k=1):
        query_embedding = self.embedder.generate_embedding(query)
        results = self.vector_store.search(query_embedding, k=top_k)
        return results