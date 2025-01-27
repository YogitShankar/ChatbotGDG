import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
from typing import List, Union

class CodeBERTEmbedder:
    def __init__(self, model_name: str = "microsoft/codebert-base"):
        """Initialize CodeBERT embedder with specified model."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.model.eval()

    def _tokenize(self, text: str) -> dict:
        """Tokenize input text with special tokens and padding."""
        return self.tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        )

    def _process_batch(self, batch_texts: List[str]) -> np.ndarray:
        """Process a batch of texts to generate embeddings."""
        encoded_input = self._tokenize(batch_texts)
        encoded_input = {k: v.to(self.device) for k, v in encoded_input.items()}
        
        with torch.no_grad():
            # Get model outputs
            outputs = self.model(**encoded_input)
            # Use attention mask to get better embeddings
            attention_mask = encoded_input['attention_mask']
            # Average pooling of token embeddings
            token_embeddings = outputs.last_hidden_state
            input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
            embeddings = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
            return embeddings.cpu().numpy()

    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for single text input with attention-based pooling."""
        embeddings = self._process_batch([text])
        return embeddings[0]

    def batch_generate_embeddings(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Generate embeddings for multiple texts in batches."""
        embeddings = []
        
        # Process texts in batches
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_embeddings = self._process_batch(batch_texts)
            embeddings.append(batch_embeddings)
            
        return np.vstack(embeddings)

    def get_embedding_dim(self) -> int:
        """Return embedding dimension."""
        return self.model.config.hidden_size
