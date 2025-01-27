from typing import List, Dict, Tuple, Optional
import numpy as np
from dataclasses import dataclass
from .embeddings import CodeBERTEmbedder
from .vectorstore import VectorStore, Document

@dataclass
class RetrievedContext:
    """Enhanced context class with source tracking."""
    content: str
    metadata: Dict
    relevance_score: float
    source_type: str  # 'problem', 'editorial', or 'solution'
    confidence: float  # Confidence score for the retrieval

class RAGRetriever:
    def __init__(
        self,
        embedder: CodeBERTEmbedder,
        vector_store: VectorStore,
        max_context_length: int = 2000,
        min_confidence: float = 0.7
    ):
        self.embedder = embedder
        self.vector_store = vector_store
        self.max_context_length = max_context_length
        self.min_confidence = min_confidence
        self.context_cache = {}  # Cache for frequently accessed contexts

    def _process_query(self, query: str) -> Dict:
        """Process and analyze query to determine retrieval strategy."""
        # Extract key information from query
        query_info = {
            'type': self._detect_query_type(query),
            'difficulty': self._extract_difficulty(query),
            'topics': self._extract_topics(query),
            'embedding': self.embedder.generate_embedding(query)
        }
        return query_info

    def _detect_query_type(self, query: str) -> str:
        """Detect type of query for specialized handling."""
        query = query.lower()
        if any(word in query for word in ['how', 'approach', 'solve']):
            return 'solution_request'
        if any(word in query for word in ['explain', 'understand', 'mean']):
            return 'explanation_request'
        if any(word in query for word in ['similar', 'like', 'related']):
            return 'similar_problems'
        return 'general'

    def _extract_difficulty(self, query: str) -> Optional[str]:
        """Extract difficulty level from query if mentioned."""
        difficulties = ['800', '1000', '1200', '1400', '1600', '1800', '2000']
        for diff in difficulties:
            if diff in query:
                return diff
        return None

    def _extract_topics(self, query: str) -> List[str]:
        """Extract programming topics from query."""
        topics = ['dp', 'graph', 'tree', 'string', 'math', 'greedy']
        return [topic for topic in topics if topic in query.lower()]

    def _filter_by_metadata(self, doc: Document, query_info: Dict) -> bool:
        """Filter documents based on query metadata."""
        if query_info['difficulty'] and 'difficulty' in doc.metadata:
            if abs(int(doc.metadata['difficulty']) - int(query_info['difficulty'])) > 200:
                return False
        if query_info['topics'] and 'tags' in doc.metadata:
            if not any(topic in doc.metadata['tags'] for topic in query_info['topics']):
                return False
        return True

    def retrieve(self, query: str, k: int = 3) -> List[RetrievedContext]:
        """Enhanced context retrieval with query analysis."""
        # Process query
        query_info = self._process_query(query)
        
        # Create filter function based on query info
        filter_fn = lambda doc: self._filter_by_metadata(doc, query_info)
        
        # Search vector store
        results = self.vector_store.search(
            query_info['embedding'],
            k=k,
            filter_fn=filter_fn
        )
        
        # Process results
        contexts = []
        for doc, score in results:
            if score < self.min_confidence:
                continue
                
            # Determine source type from metadata
            source_type = doc.metadata.get('type', 'general')
            
            # Calculate confidence based on score and metadata match
            confidence = score * self._calculate_metadata_confidence(doc, query_info)
            
            context = RetrievedContext(
                content=doc.content[:self.max_context_length],
                metadata=doc.metadata,
                relevance_score=score,
                source_type=source_type,
                confidence=confidence
            )
            contexts.append(context)
            
            # Cache frequently accessed contexts
            if score > 0.9:
                self.context_cache[doc.id] = context
        
        return contexts

    def _calculate_metadata_confidence(self, doc: Document, query_info: Dict) -> float:
        """Calculate confidence boost based on metadata matching."""
        confidence = 1.0
        
        # Boost if difficulty matches
        if query_info['difficulty'] and 'difficulty' in doc.metadata:
            diff_delta = abs(int(doc.metadata['difficulty']) - int(query_info['difficulty']))
            confidence *= max(0.5, 1 - (diff_delta / 1000))
            
        # Boost if topics match
        if query_info['topics'] and 'tags' in doc.metadata:
            matching_topics = sum(1 for topic in query_info['topics'] if topic in doc.metadata['tags'])
            if matching_topics:
                confidence *= 1 + (0.1 * matching_topics)
                
        return min(1.0, confidence)

    def batch_index_documents(self, contents: List[str], metadata_list: List[Dict],
                            batch_size: int = 32):
        """Batch index documents with metadata."""
        # Generate embeddings
        embeddings = self.embedder.batch_generate_embeddings(contents, batch_size)
        
        # Create documents
        documents = [
            Document(id=str(i), content=content, metadata=metadata)
            for i, (content, metadata) in enumerate(zip(contents, metadata_list))
        ]
        
        # Add to vector store
        self.vector_store.add_documents(documents, embeddings)
