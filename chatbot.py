from transformers import AutoTokenizer,AutoModelForSequenceClassification
import torch


class CPChatbot:
    def _init_(self, retriever,system_message, model_name="bert-base-uncased"):
        self.retriever = retriever
        self.system_message = system_message
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        system_message = (
        "You are a smart chatbot which solves competitive programming problems from codeforces. You have been trained on question sets from codeforces along with their editorial. You have to provide model solutions and help me to figure out the solutions of the problems. Do not hallucinate.\n"
    )


    def chat(self, query):
        retrieved_contexts = self.retriever.retrieve(query, k=3)
        context_text = "\n".join(retrieved_contexts)
        
        prompt = f"Context:\n{context_text}\n\nUser Query: {query}\nAnswer: "
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        
        output = self.model(input_ids)
        response = torch.argmax(output.logits, dim=1)
        
        return response