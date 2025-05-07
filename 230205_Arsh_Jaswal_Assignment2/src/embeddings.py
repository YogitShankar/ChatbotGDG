import numpy
import torch
from transformers import RobertaTokenizer, RobertaForMaskedLM

class CodeBERTEmbedder:
    def __init__(self):
        self.tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
        self.model = RobertaForMaskedLM.from_pretrained("microsoft/codebert-base")

    def generate_embedding(self, text):
        inputs = self.tokenizer(text, padding="max_length", truncation=True, max_length=512, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs, output_hidden_states=True)
        #last HS(important)
        lastHS = outputs.hidden_states[-1]

        #Attention masking
        attention_mask = inputs['attention_mask'].unsqueeze(-1)
        masked_embeddings = lastHS*attention_mask
        pooled_embedding = masked_embeddings.sum(dim=1)/attention_mask.sum(dim=1)  # Mean pooling

        return pooled_embedding.squeeze().numpy()

    def batch_generate_embeddings(self, texts):
        inputs = self.tokenizer(texts, padding=True, truncation=True, max_length=512, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs, output_hidden_states=True)
        #last hidden state (most important)
        lastHS = outputs.hidden_states[-1]

        #Attention masking to improve performance
        #excluding padding tokens
        attention_mask = inputs['attention_mask'].unsqueeze(-1)  # Shape: (batch size, seq len, 1)
        masked_embeddings = lastHS*attention_mask  # Zero out padding tokens
        pooled_embeddings = masked_embeddings.sum(dim=1)/attention_mask.sum(dim=1)

        return pooled_embeddings.numpy()