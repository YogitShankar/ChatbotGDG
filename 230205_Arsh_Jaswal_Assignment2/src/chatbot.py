
from embeddings import CodeBERTEmbedder
from vectorstore import VectorStore

from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

from retriever import retrieve


def search_problem_context(query_statement):
    query_problem = query_statement
    query_problem_embedding = embedder.generate_embedding(query_problem)
    results = vector_store.search(query_question=query_problem_embedding, top_k=2)
    
    context = ""
    temp = 1
    for result in results:
        context = "\n".join([
            context,
            f"""
Context Number {temp}
Problem Number: {result[0]}

Problem statement: {result[1]}

Tags: {result[2]["tags"]}

Solution: {result[3]}
            """
        ])
        temp += 1
    return context


if __name__ == "__main__":
    embedder = CodeBERTEmbedder()
    problem_dir = "data/problems"
    editorial_dir = "data/editorials"
    metadata_dir = "data/metadata"

    problems, solutions, metadata = retrieve(problem_dir, editorial_dir, metadata_dir)

    # Generate embeddings and store them
    vector_store = VectorStore(embedding_dim=768)  # CodeBERT output size
    t=0
    for problem_id in problems:
        if t%10 == 0:
            print("Fetching embeddings...")
        if problem_id in solutions and problem_id in metadata:
            problem_embedding = embedder.generate_embedding(problems[problem_id])
            problem_text = problems[problem_id]
            metadata_text = ", ".join(metadata[problem_id].get("tags", []))
            metadata_embedding = embedder.generate_embedding(metadata_text)
            solution_embedding = embedder.generate_embedding(solutions[problem_id])

            vector_store.add_embeddings(
                problem_id=problem_id,
                question_embedding=problem_embedding,
                metadata_embedding=metadata_embedding,
                answer_embedding=solution_embedding,
                problem=problems[problem_id],
                metadata=metadata[problem_id],
                solution=solutions[problem_id],
            )
        t+=1


    from embeddings import CodeBERTEmbedder
    embedder = CodeBERTEmbedder()
    from vectorstore import VectorStore
    vector_store = VectorStore()


template="""
You are a competitive programming assistant bot.
Below are three sections: "Query", "Similar Problem", "Chat History".

If "Query" is normal conversation, continue chat, you can also use chat history.

If "Query" is a question statement, Use "Similar Problem" below as well as your own database to answer the query.
"Similar Problem" section has same or similar problem statement to query. And also has its OFFICIAL solution.
If it's similar or same, return this solution or answer.



Query: 
{user_input}



Similar Problem:

{Similar_Problem}



Chat History: {history}

"""



model=OllamaLLM(model="llama3.2")

prompt=ChatPromptTemplate.from_template(template)

chain=prompt | model

def handle_convo():
    history=""
    print("Welcome to the chatbot for CP, Type 'exit' or 'quit' to terminate the conversation.")
    while True:
        user_input=input("You: ")
        if user_input.lower() in ["exit","quit"]:
            break
        out=chain.invoke({"history":history,"user_input":user_input,"context":search_problem_context(user_input)})
        print("Bot: ", out)
        history += f"\nUser: {user_input}\nAI: {out}"

if __name__ == "__main__":
    handle_convo()