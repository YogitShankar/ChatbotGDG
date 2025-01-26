import torch;
from transformers import AutoTokenizer, AutoModel;

from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

class CodeBERTEmbedder:
    def __init__(self, model_name="microsoft/codebert-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def generate_embedding(self, text):
        tokens = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**tokens)
        return outputs.last_hidden_state.mean(dim=1).numpy()

    def batch_generate_embeddings(self, texts):
        embeddings = [self.generate_embedding(text) for text in texts]
        return np.vstack(embeddings)

        

