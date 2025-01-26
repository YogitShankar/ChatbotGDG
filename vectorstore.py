import numpy as np
import faiss

def vectorstore(embed, query_embed, k):
    np_embed = embed.numpy()
    np.save("embeddings.npy", np_embed)
    embeddings = np.load("embeddings.npy")

    np_query_embed = query_embed.numpy()
    np.save("query.npy", np_query_embed)
    query_vector = np.load("query.npy")

    if len(query_vector.shape) == 1:
        query_vector = np.expand_dims(query_vector, axis=0)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, "vector_store.index")

    index = faiss.read_index("vector_store.index")
    distances, indices = index.search(query_vector, k)

    return distances, indices



