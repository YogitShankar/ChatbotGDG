import os
from embeddings import CodeBERTEmbedder
from vectorstore import VectorStore
from retriever import RAGRetriever

# Chatbot Integration
class CPChatbot:
    def __init__(self, retriever, system_message):
        self.retriever = retriever
        self.system_message = system_message

    def chat(self, user_query):
        contexts = self.retriever.retrieve_context(user_query)
        response = f"System: {self.system_message}\n\n"
        response += f"Context: {contexts[0][0]}"
        return response

# Helper functions
def load_text_files_from_directory(directory):
    files_content = []
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path) and file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                files_content.append(file.read().strip())
    return files_content

def combine_problems_and_editorials(problem_statements_path, editorials_path):
    problems = load_text_files_from_directory(problem_statements_path)
    editorials = load_text_files_from_directory(editorials_path)
    combined = [f"Problem: {p}\n\nEditorial: {e}" for p, e in zip(problems, editorials)]
    return combined

if __name__ == "__main__":
    # Set paths
    EDITORIALS_PATH = "data/editorials"
    PROBLEM_STATEMENTS_PATH = "data/problem_statements"

    # Combine problem statements and editorials
    documents = combine_problems_and_editorials(PROBLEM_STATEMENTS_PATH, EDITORIALS_PATH)

    # Initialize components
    embedder = CodeBERTEmbedder()
    vector_store = VectorStore()
    retriever = RAGRetriever(embedder, vector_store)

    # Generate embeddings and populate the vector store
    embeddings = embedder.batch_generate_embeddings(documents)
    vector_store.add_embeddings(documents, embeddings)

    # Create chatbot
    system_message = (
        "I am solving a Competitive Programming problem, and I need help understanding its editorial.\n"
        "Answer my questions regarding the editorial.\n"
    )
    chatbot = CPChatbot(retriever, system_message)

    # Single query input
    user_query = input("Enter your query: ")
    print(chatbot.chat(user_query))
