from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceEmbeddings

class EmbeddingModel:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def get_embedding_model(self):
        return HuggingFaceEmbeddings(model_name=self.model_name)