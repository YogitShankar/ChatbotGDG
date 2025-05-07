import os
import faiss
import warnings
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Suppress TensorFlow warnings and others
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*tf.losses.sparse_softmax_cross_entropy.*")
warnings.filterwarnings("ignore", category=UserWarning, message=".*Torch was not compiled with flash attention.*")

class CodeEmbedder:
    def __init__(self, model_name="microsoft/codebert-base", chunk_size=1024):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})

        self.model = AutoModel.from_pretrained(model_name) 
        self.model.config.pad_token_id = self.tokenizer.pad_token_id 

        self.chunk_size = chunk_size 
        self.chunk_overlap = 50
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

    def _chunk_text(self, text):
        return self.text_splitter.split_text(text) if text.strip() else []

    def generate_embedding(self, text):

        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()
        return embeddings.numpy()


