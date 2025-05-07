from langchain.vectorstores import Chroma

vector_store = Chroma(embedding_function=embedder.encode, persist_directory="chroma_db")

documents = [
    {"id": "doc1", "page_content": "Find the maximum subarray sum", "metadata": {"source": "problem1"}},
    {"id": "doc2", "page_content": "Implement a segment tree", "metadata": {"source": "problem2"}},
    {"id": "doc3", "page_content": "Solve the knapsack problem", "metadata": {"source": "problem3"}}
]

texts = [doc['page_content'] for doc in documents]
metadatas = [doc['metadata'] for doc in documents]
ids = [doc['id'] for doc in documents]

vector_store.add_texts(texts, metadatas=metadatas, ids=ids)
vector_store.persist()  
print(f"{len(documents)} documents added to the vector store.")
