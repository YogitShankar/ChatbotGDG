import faiss
import numpy as np

class VectorStore:
    def __init__(self, embedding_dim):
        #FAISS L2 to store problem embeddings only
        self.index = faiss.IndexFlatL2(embedding_dim)  # Onlyquestion embedding dimension
        self.problem_store = {}
        self.metadata_store = {}
        self.solution_store = {}
        self.prob_store = {}
        self.meta_store = {}
        self.soln_store = {}

    def add_embeddings(self, problem_id, question_embedding, metadata_embedding, answer_embedding, problem, metadata, solution):

        #Normalizing (L2 normalization)
        question_embedding = question_embedding / np.linalg.norm(question_embedding)
        question_embedding = np.array([question_embedding], dtype=np.float32)
        self.index.add(question_embedding)

        #STORING EMBEDDINGS AND TEXT
        self.problem_store[problem_id] = question_embedding
        self.metadata_store[problem_id] = metadata_embedding
        self.solution_store[problem_id] = answer_embedding
        self.prob_store[problem_id] = problem
        self.meta_store[problem_id] = metadata
        self.soln_store[problem_id] = solution

    def search(self, query_question, top_k=2):

        query_question = query_question / np.linalg.norm(query_question)
        query_embedding = np.array([query_question], dtype=np.float32)
        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.problem_store):
                problem_id = list(self.problem_store.keys())[idx]
                problem = self.prob_store[problem_id]
                metadata = self.meta_store[problem_id]
                solution = self.soln_store[problem_id]
                distance = distances[0][indices[0].tolist().index(idx)]
                results.append((problem_id,problem, metadata, solution, distance))

        return results
