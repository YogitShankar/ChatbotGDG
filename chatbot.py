import requests
from retreiver import retrieve_and_generate
from transformers import AutoTokenizer, AutoModel
from utils import load_documents

API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom" 
API_TOKEN = "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"  

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}"
}

PROMPT_TEMPLATE = """
Answer the question using the provided context.

Context:
{context}

Question: {question}

Answer:
"""



def query_huggingface_api(payload):
    """Send request to Hugging Face Inference API."""
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()


def generate_response_with_prompt(query, context_chunks):
    context = "\n".join(context_chunks)
    prompt = PROMPT_TEMPLATE.format(context=context, question=query)

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens":125,
            "temperature": 0.7,
            "top_p": 0.7,
            "do_sample": True
        }
    }
    response = query_huggingface_api(payload)
    return response[0]["generated_text"]

if __name__ == "__main__":
    query = "How do I solve Problem ID 2053D?"
    DATA_PATH = "Project\data\problems"
    EDITORIAL_PATH = "Project\data\editorials"
    docs = load_documents(DATA_PATH, EDITORIAL_PATH)
    merged_text = "\n".join(doc.page_content for doc in docs)
    

    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    model_e = AutoModel.from_pretrained("microsoft/codebert-base")

    context_chunks = retrieve_and_generate(tokenizer, model_e, merged_text, query, k=5)
    
    response = generate_response_with_prompt(query, context_chunks)
    print("Chatbot Response:")
    print(response)


