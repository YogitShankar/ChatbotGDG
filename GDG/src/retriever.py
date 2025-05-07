
query = "How do I solve problem C from Contest #792?"

query_embedding = embedder.encode([query])

retrieved_docs = vector_store.similarity_search_by_vector(query_embedding[0], k=3)  # Top 3 documents

print("Retrieved documents:")
for doc in retrieved_docs:
    print(doc.page_content)
