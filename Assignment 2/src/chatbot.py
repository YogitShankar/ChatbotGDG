from huggingface_hub import InferenceClient

class MistralChatbot:
    def __init__(self, model_name="mistralai/Mistral-7B-Instruct-v0.3", api_key=None):
        self.client = InferenceClient(api_key=api_key)
        self.model_name = model_name

    def generate_response(self, prompt, max_tokens=500):
        try:
            messages = [{"role": "user", "content": prompt}]
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=max_tokens
            )
            return completion["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error generating response: {e}"