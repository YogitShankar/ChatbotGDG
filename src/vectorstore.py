from langchain_core.documents import Document
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import json
class VectorStore:
    def __init__(self):
        self.faiss_index = None

    def create_store(self, embedder):
        folder1 = "/content/drive/My Drive/data/problem_statements"
        folder2 = "/content/drive/My Drive/data/editorials"
        folder3 = "/content/drive/My Drive/data/metadata"
        files1 = sorted([file for file in os.listdir(folder1) if file.endswith(".txt")])
        files2 = sorted([file for file in os.listdir(folder2) if file.endswith(".txt")])
        files3 = sorted([file for file in os.listdir(folder3) if file.endswith(".json")])
        documents = []
        # Use zip to iterate through the files simultaneously
        for file1, file2, file3 in zip(files1, files2, files3):
            page_content = ""
            with open(os.path.join(folder1, file1), "r", encoding="utf-8") as f1, \
                    open(os.path.join(folder2, file2), "r", encoding="utf-8") as f2,\
                    open(os.path.join(folder3, file3), "r", encoding="utf-8") as f3:
                page_content += f1.read() + "\n"  # Text from folder 1
                page_content += f2.read() + "\n"  # Text from folder 2
                metadata = json.load(f3)
                doc = Document(page_content=page_content, metadata=metadata)
                documents.append(doc)
        text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=400,
                chunk_overlap=100
        )
        # Split all concatenated documents into chunks
        splits = text_splitter.split_documents(documents)
        self.faiss_index = FAISS.from_documents(splits, embedder)
        return self.faiss_index

    def save_store(self, path):
        self.faiss_index.save_local(path)

    def load_store(self, path, embedder):
        self.faiss_index = FAISS.load_local(path, embedder)