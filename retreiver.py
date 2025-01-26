from embeddings import generate_embeddings_data
from vectorstore import vectorstore
import torch

def retrieve_and_generate(tokenizer, model, merged_text, query_text, k):
    
    embeddings, chunks = generate_embeddings_data(merged_text)

    query_tokens = tokenizer(query_text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        query_outputs = model(**query_tokens)
    query_embed = query_outputs.last_hidden_state.mean(dim=1)

    distances, indices = vectorstore(embeddings, query_embed, k)

    top_chunks = [chunks[i] for i in indices[0]]
    return top_chunks