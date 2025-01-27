{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Codeforces Programming Assistant Example Usage\n",
    "\n",
    "This notebook demonstrates how to use the Codeforces Programming Assistant system."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "import os\n",
    "import sys\n",
    "sys.path.append('../')\n",
    "\n",
    "from src.embeddings import CodeBERTEmbedder\n",
    "from src.vectorstore import VectorStore, Document\n",
    "from src.retriever import RAGRetriever\n",
    "from src.chatbot import CPChatbot"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Initialize Components"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Initialize CodeBERT embedder\n",
    "embedder = CodeBERTEmbedder()\n",
    "\n",
    "# Initialize vector store\n",
    "vector_store = VectorStore(dimension=embedder.get_embedding_dim())\n",
    "\n",
    "# Initialize RAG retriever\n",
    "retriever = RAGRetriever(embedder, vector_store)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Load Sample Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Sample problem and editorial data\n",
    "sample_problems = [\n",
    "    {\n",
    "        \"content\": \"Given an array of integers, find the maximum subarray sum...\",\n",
    "        \"metadata\": {\"problem_id\": \"792A\", \"difficulty\": \"800\", \"tags\": [\"dp\"]}\n",
    "    },\n",
    "    {\n",
    "        \"content\": \"Implement a segment tree to handle range minimum queries...\",\n",
    "        \"metadata\": {\"problem_id\": \"792B\", \"difficulty\": \"1400\", \"tags\": [\"data structures\"]}\n",
    "    }\n",
    "]\n",
    "\n",
    "# Index sample data\n",
    "contents = [p[\"content\"] for p in sample_problems]\n",
    "metadata_list = [p[\"metadata\"] for p in sample_problems]\n",
    "\n",
    "retriever.batch_index_documents(contents, metadata_list)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Initialize Chatbot"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "system_message = \"\"\"\n",
    "I am solving a Competitive Programming problem, and I need help understanding its editorial.\n",
    "Answer my questions regarding the editorial.\n",
    "Let me know if I'm misunderstanding anything.\n",
    "Do not write or debug code.\n",
    "\"\"\"\n",
    "\n",
    "chatbot = CPChatbot(retriever, system_message)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Example Interactions"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Example 1: Ask about a specific problem\n",
    "query = \"How do I solve problem A from Contest #792?\"\n",
    "response = chatbot.chat(query)\n",
    "print(f\"Query: {query}\\nResponse: {response}\\n\")\n",
    "\n",
    "# Example 2: Ask for clarification\n",
    "query = \"Could you explain the dynamic programming approach in more detail?\"\n",
    "response = chatbot.chat(query)\n",
    "print(f\"Query: {query}\\nResponse: {response}\\n\")\n",
    "\n",
    "# Example 3: Ask about problem difficulty\n",
    "query = \"What's the difficulty rating of problem B?\"\n",
    "response = chatbot.chat(query)\n",
    "print(f\"Query: {query}\\nResponse: {response}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Save and Load Conversation"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Save conversation\n",
    "chatbot.save_conversation(\"conversation.json\")\n",
    "\n",
    "# Clear conversation\n",
    "chatbot.clear_conversation()\n",
    "\n",
    "# Load conversation\n",
    "chatbot.load_conversation(\"conversation.json\")\n",
    "\n",
    "# View conversation history\n",
    "history = chatbot.get_conversation_history()\n",
    "for message in history:\n",
    "    print(f\"{message['role']}: {message['content']}\\n\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
