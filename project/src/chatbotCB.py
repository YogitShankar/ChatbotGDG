# import transformers
class Chatbot:
    def __init__(self, retriever, system_message):
        self.retriever = retriever
        self.system_message = system_message
        self.history = []

    def generate_response(self, user_query):
        self.history.append({"user": user_query})
        results = self.retriever.retrieve(user_query, top_k=3)

        if results:
            response_content = "\n".join([f"{i+1}. {content}" for i, (_, content, _) in enumerate(results)])
            response = f"{self.system_message}\n\nHere are some relevant responses:\n{response_content}"
        else:
            response = f"{self.system_message}\n\nSorry, I couldn't find anything relevant."

        self.history.append({"bot": response})
        return response

    def get_chat_history(self):
        return self.history