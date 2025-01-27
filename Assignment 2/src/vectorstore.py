import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from embeddings import EmbeddingModel

class VectorStoreManager:
    def __init__(self, data_folder="../data", output_folder="../processed_data"):
        self.data_folder = data_folder
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=500)
        self.embedding_model = EmbeddingModel().get_embedding_model()

    def combine_data(self):
        file_groups = {}
        for subfolder in ["problems", "editorials", "metadata"]:
            subfolder_path = os.path.join(self.data_folder, subfolder)
            if os.path.exists(subfolder_path):
                for file_name in os.listdir(subfolder_path):
                    file_path = os.path.join(subfolder_path, file_name)
                    base_name, _ = os.path.splitext(file_name)
                    if base_name not in file_groups:
                        file_groups[base_name] = {"problems": None, "editorials": None, "metadata": None}
                    file_groups[base_name][subfolder] = file_path

        for base_name, files in file_groups.items():
            combined_text = []
            if files["problems"]:
                with open(files["problems"], 'r', encoding='utf-8') as f:
                    combined_text.append(f"Problem:\n{f.read()}")
            if files["editorials"]:
                with open(files["editorials"], 'r', encoding='utf-8') as f:
                    combined_text.append(f"Editorial:\n{f.read()}")
            if files["metadata"]:
                with open(files["metadata"], 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                    metadata_text = "\n".join(f"{key}:\n{value}" for key, value in json_data.items())
                    combined_text.append(f"Metadata:\n{metadata_text}")

            combined_text_str = "\n".join(combined_text).strip()
            if combined_text_str:
                output_path = os.path.join(self.output_folder, f"{base_name}.txt")
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(combined_text_str)

    def create_vector_store(self):
        documents = []
        for file_name in os.listdir(self.output_folder):
            file_path = os.path.join(self.output_folder, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                chunks = self.text_splitter.split_text(content)
                documents.extend([{"text": chunk, "source": file_name} for chunk in chunks])

        texts = [doc["text"] for doc in documents]
        metadatas = [{"source": doc["source"]} for doc in documents]
        vector_store = FAISS.from_texts(texts, self.embedding_model, metadatas=metadatas)
        vector_store.save_local("../vectorstore")

    def load_vector_store(self):
        return FAISS.load_local("../vectorstore", self.embedding_model, allow_dangerous_deserialization=True)