from langchain.chains import RetrievalQA

class RAGRetriever:
    def __init__(self, embedder, vector_store):
        self.embedder = embedder
        self.vector_store = vector_store.create_store(embedder)
        self.retriever = self.vector_store.as_retriever()

    def retrieve(self, query):
        """
        Retrieves documents relevant to the query.
        Args:
            query: The user query as a string.
        Returns:
            List of documents most similar to the query.
        """
        try:
            # Use the retriever to get results
            results = self.retriever.get_relevant_documents(query)
            return results
        except Exception as e:
            print(f"Error during retrieval: {e}")
            return []