import os

class HuggingFaceChatbot:
    def __init__(self, retriever, system_message, model_name="distilgpt2"):
        self.retriever = retriever
        self.system_message = system_message
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        self.model = AutoModelForCausalLM.from_pretrained(model_name) 

    def chat(self, query):

        relevant_chunks = self.retriever.retrieve(query, top_k=5)

        if not relevant_chunks:
            return "Sorry, I couldn't find a relevant solution."

        context = "\n".join(relevant_chunks[:5])  
       

        prompt = f"{self.system_message}\n\nContext:\n{context}\n\nQuery: {query}\n\nAnswer:" 

        try:
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512, padding=True)
            attention_mask = inputs.attention_mask if "attention_mask" in inputs else None 

            outputs = self.model.generate(
                inputs.input_ids, 
                attention_mask=attention_mask, 
                max_new_tokens=100, 
                temperature=0.7, 
                top_p=0.9, 
                do_sample=True
            )

            # Decode and return the generated response
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            return "Sorry, there was an issue processing the request."
