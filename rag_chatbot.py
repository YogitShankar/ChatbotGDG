import os
import faiss
import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer
from base_chatbot import ProblemChatbot, PROBLEM_PATH, EDITORIAL_PATH
from json_loader import load_problem

class Chatbot(ProblemChatbot):
    def __init__(self):
        super().__init__()
        
        self.problem_ids = []
        self.problem_data_map = {}
        self.retrieval_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.retrieval_model = AutoModel.from_pretrained("bert-base-uncased")
        self.retrieval_model.eval()

        self.index = faiss.IndexFlatIP(768)  # BERT embedding dimension

        self._build_knowledge_base()

    def _get_bert_embedding(self, text):
        """Generate BERT embedding for text"""
        inputs = self.retrieval_tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding="max_length"
        )
        with torch.no_grad():
            outputs = self.retrieval_model(**inputs)
        
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    def _create_problem_context(self, problem_data):
        return (
            f"Title: {problem_data.get('title', '')}\n"
            f"Statement: {problem_data.get('statement', '')}\n"
            f"Input: {problem_data.get('input', '')}\n"
            f"Output: {problem_data.get('output', '')}\n"
            f"Solution: {problem_data.get('solution', '')}"
        )

    def _build_knowledge_base(self):
        print("Building knowledge base...")
        embeddings = []
        
        for p_file in os.listdir(PROBLEM_PATH):
            if p_file.endswith('.json'):
                problem_id = os.path.splitext(p_file)[0]
                try:
                    problem_data = load_problem(problem_id, PROBLEM_PATH, EDITORIAL_PATH)
                    context = self._create_problem_context(problem_data)
                    embedding = self._get_bert_embedding(context)
                    
                    embeddings.append(embedding)
                    self.problem_ids.append(problem_id)
                    self.problem_data_map[problem_id] = problem_data
                except Exception as e:
                    print(f"Error loading problem {problem_id}: {str(e)}")
                    continue
        
        if embeddings:
            self.index.add(np.array(embeddings))
        print(f"Knowledge base built with {len(self.problem_ids)} problems")

    def _retrieve_relevant_info(self, query, top_k=3):
        try:
            query_embedding = self._get_bert_embedding(query)
            query_embedding = np.expand_dims(query_embedding, axis=0)

            distances, indices = self.index.search(query_embedding, top_k)
            
            results = []
            for idx, score in zip(indices[0], distances[0]):
                if idx >= 0:  
                    problem_id = self.problem_ids[idx]
                    results.append((
                        problem_id,
                        float(score),
                        self.problem_data_map[problem_id]
                    ))
            return results
        except Exception as e:
            print(f"Retrieval error: {str(e)}")
            return []

    def respond(self, user_input):
        user_input = user_input.strip()
        
        if any(greet in user_input.lower() for greet in ["hi", "hello", "hey"]):
            return super().respond(user_input)
            
        problem_id = self._extract_problem_id(user_input)
        if problem_id:
            return super().respond(user_input)

        retrieved = self._retrieve_relevant_info(user_input)
        rag_context = "\n".join(
            f"Relevant Problem {pid} (score: {score:.2f}):\n"
            f"{self._create_problem_context(data)}"
            for pid, score, data in retrieved
        )

        current_context = ""
        if self.current_problem and self.problem_data:
            current_context = f"\nCurrent Problem Context:\n{self._build_context()}"

        prompt = (
            f"You are a competitive programming assistant. Use the following relevant problems "
            f"and current problem context to answer the question.\n\n"
            f"Retrieved relevant information:\n{rag_context}\n"
            f"{current_context}\n"
            f"User question: {user_input}\n\n"
            f"Provide a detailed, accurate response that:\n"
            f"1. Directly addresses the user's question\n"
            f"2. References relevant information from similar problems when helpful\n"
            f"3. Maintains focus on competitive programming best practices\n"
            f"4. Provides clear explanations and examples when appropriate"
        )
        
        return self.model.generate_response(prompt)