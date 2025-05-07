class RAGRetriever:
    def __init__(self, embedder, vector_store, similarity_threshold=0.9):
        self.embedder = embedder
        self.vector_store = vector_store
        self.similarity_threshold = similarity_threshold  

    def retrieve(self, query, top_k=3):
        query_embedding = self.embedder.generate_embedding(query)

        results, distances = self.vector_store.search(query_embedding, top_k=top_k)


        relevant_chunks = []
        unique_chunks = set() 

        for result in results:
            with open(result, 'r', encoding='utf-8') as file:
                content = file.read()

                chunks = self.embedder._chunk_text(content)
                for chunk in chunks:
                    chunk_embedding = self.embedder.generate_embedding(chunk)
                    similarity = np.dot(query_embedding, chunk_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(chunk_embedding))

                    if similarity > self.similarity_threshold:  
                        if chunk not in unique_chunks:
                            relevant_chunks.append(chunk)
                            unique_chunks.add(chunk)

        if not relevant_chunks:
            return []

        return relevant_chunks[:top_k]