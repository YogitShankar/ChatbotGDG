from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm
import numpy as np
class RAGRetriever:
    def __init__(self, embedder, vector_db, chunk_size=350, chunk_overlap=70):
        self.embedder = embedder
        self.vector_db = vector_db
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.index_to_content_mapping = {}

    def load_and_process_data(self, loaders):
        data = []
        for loader in loaders:
            data.extend(loader.load())

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        splits = text_splitter.split_documents(data)
        self.index_to_content_mapping = {i: split.page_content for i, split in enumerate(splits)}

        texts = [split.page_content for split in splits]
        embeddings = []

        batch_size = 16
        for i in tqdm(range(0, len(texts), batch_size), desc="Processing batches"):
            batch_texts = texts[i:i+batch_size]
            batch_embeddings = self.embedder.generate_embeddings(batch_texts)
            embeddings.append(batch_embeddings)

        embeddings = np.vstack(embeddings)
        self.vector_db.create_index(embeddings)

    def retrieve(self, query_text, top_k=2):
        query_embedding = self.embedder.generate_embeddings([query_text])
        indices, distances = self.vector_db.search(query_embedding, top_k)
        results = [(index, self.index_to_content_mapping.get(index, "Content not found"), score) for index, score in zip(indices[0], distances[0])]
        return results