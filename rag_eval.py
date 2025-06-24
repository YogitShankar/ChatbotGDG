import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import nltk
nltk.download('punkt')

class SimpleChatbotEvaluator:
    def __init__(self, chatbot, test_queries):
        """
        Simplified evaluator for RAG chatbot
        
        Args:
            chatbot: Your RAG chatbot instance
            test_queries: List of (query, [expected_problem_ids]) tuples
        """
        self.chatbot = chatbot
        self.test_queries = test_queries
    
    def evaluate(self):
        """Run all evaluations and return summary"""
        diversity = self.check_response_diversity()
        context_use = self.check_context_usage()
        
        return {
            'diversity': diversity,
            'context_usage': context_use,
            'summary': self.get_summary(diversity, context_use)
        }
    
    def check_response_diversity(self, num_queries=20):
        """
        Check if responses are varied (not repetitive)
        Returns average similarity score (lower is better)
        """
        responses = [self.chatbot.respond(q[0]) for q in self.test_queries[:num_queries]]
        
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf = vectorizer.fit_transform(responses)

        similarities = cosine_similarity(tfidf)
        np.fill_diagonal(similarities, 0) 
        
        return {
            'avg_similarity': np.mean(similarities),
            'num_responses': len(responses)
        }
    
    def check_context_usage(self):
        """
        Check if responses properly use the retrieved context
        Returns precision and recall scores
        """
        scores = {'precision': [], 'recall': []}
        
        for query, expected_ids in self.test_queries:

            retrieved = self.chatbot._retrieve_relevant_info(query)
            retrieved_ids = [pid for pid, _, _ in retrieved]
            
            relevant = set(retrieved_ids) & set(expected_ids)
            precision = len(relevant) / len(retrieved_ids) if retrieved_ids else 0
            recall = len(relevant) / len(expected_ids) if expected_ids else 0
            
            scores['precision'].append(precision)
            scores['recall'].append(recall)
        
        return {
            'avg_precision': np.mean(scores['precision']),
            'avg_recall': np.mean(scores['recall']),
            'num_queries': len(self.test_queries)
        }
    
    def get_summary(self, diversity, context_use):
        """Generate simple text summary"""
        return (
            f"Evaluation Summary:\n"
            f"- Response diversity: {(1 - diversity['avg_similarity']):.2f} score (higher is better)\n"
            f"- Context precision: {context_use['avg_precision']:.2f} (higher is better)\n"
            f"- Context recall: {context_use['avg_recall']:.2f} (higher is better)\n"
            f"Based on {context_use['num_queries']} test queries"
        )

if __name__ == "__main__":
    test_queries = [
        ("How to solve DP problems?", ["2087E", "2087F"]),
        ("Best way to solve greedy problems?", ["2087C", "2087G"]),
    ]
    
    from rag_chatbot import Chatbot
    chatbot = Chatbot()
    
    evaluator = SimpleChatbotEvaluator(chatbot, test_queries)
    results = evaluator.evaluate()
    
    print(results['summary'])
    print("\nDetailed results:")
    print(f"Diversity: {results['diversity']}")
    print(f"Context Usage: {results['context_usage']}")