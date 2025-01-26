
response = "Here’s what I found:\n"
for doc in retrieved_docs:
    response += f"- {doc.page_content}\n"

print("Chatbot response:")
print(response)
