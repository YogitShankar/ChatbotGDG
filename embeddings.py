from transformers import AutoTokenizer, AutoModel
from langchain.text_splitter import RecursiveCharacterTextSplitter
import torch



def generate_embeddings_data(merged_text):

    text_splitter = RecursiveCharacterTextSplitter(    
    chunk_size = 550,
    chunk_overlap = 50,
    length_function = len,
    add_start_index = True,
    )

    chunks = text_splitter.split_text(merged_text)
    print(len(chunks))

    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    model = AutoModel.from_pretrained("microsoft/codebert-base")

    tokens = tokenizer(chunks, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**tokens)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings, chunks








