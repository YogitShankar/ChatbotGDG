class CPChatbot:
    def __init__(self, retriever, system_message):
        self.retriever = retriever
        self.system_message = system_message

    def chat(self, query):
        context = self.retriever.retrieve(query)
        return f"Retrieved context: {context}"
