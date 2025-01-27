from langchain.vectorstores import FAISS

class RAGRetriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(self, query, k=5):
        docs = self.vector_store.similarity_search(query, k=k)
        return docs