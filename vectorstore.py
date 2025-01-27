import faiss
import numpy as np
from typing import List, Tuple, Dict, Optional
import pickle
from dataclasses import dataclass

@dataclass
class Document:
    """Document class with enhanced metadata support."""
    id: str
    content: str
    metadata: Dict
    embedding: Optional[np.ndarray] = None
    
    def to_dict(self) -> Dict:
        """Convert document to dictionary format."""
        return {
            'id': self.id,
            'content': self.content,
            'metadata': self.metadata
        }

class VectorStore:
    def __init__(self, dimension: int = 768, index_type: str = "hnsw"):
        """Initialize vector store with specified index type."""
        self.dimension = dimension
        self.index_type = index_type
        self.index = self._create_index()
        self.documents = []
        self.id_to_index = {}  # Maps document IDs to their index positions

    def _create_index(self) -> faiss.Index:
        """Create FAISS index based on type."""
        if self.index_type == "flat":
            return faiss.IndexFlatIP(self.dimension)
        elif self.index_type == "hnsw":
            # HNSW index for better performance
            index = faiss.IndexHNSWFlat(self.dimension, 32)  # 32 neighbors
            index.hnsw.efConstruction = 64  # Higher accuracy during construction
            index.hnsw.efSearch = 32  # Higher accuracy during search
            return index
        elif self.index_type == "ivf":
            # IVF index for large-scale search
            nlist = 100  # Number of clusters
            quantizer = faiss.IndexFlatL2(self.dimension)
            index = faiss.IndexIVFFlat(quantizer, self.dimension, nlist)
            index.nprobe = 10  # Number of clusters to visit during search
            return index
        raise ValueError(f"Unsupported index type: {self.index_type}")

    def add_documents(self, documents: List[Document], embeddings: Optional[np.ndarray] = None):
        """Add documents and their embeddings to the store."""
        if embeddings is not None:
            assert len(documents) == embeddings.shape[0]
            faiss.normalize_L2(embeddings)
            self.index.add(embeddings)
            
        # Update document storage and mapping
        start_idx = len(self.documents)
        for i, doc in enumerate(documents):
            self.id_to_index[doc.id] = start_idx + i
            if embeddings is not None:
                doc.embedding = embeddings[i]
            self.documents.append(doc)

    def search(self, query_embedding: np.ndarray, k: int = 5, 
               filter_fn: Optional[callable] = None) -> List[Tuple[Document, float]]:
        """Search for similar documents with optional filtering."""
        # Normalize query embedding
        query_embedding = query_embedding.reshape(1, -1)
        faiss.normalize_L2(query_embedding)
        
        # Initial search
        distances, indices = self.index.search(query_embedding, k * 2)  # Get more results for filtering
        
        # Process results
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx != -1:  # Valid index
                doc = self.documents[idx]
                if filter_fn is None or filter_fn(doc):
                    results.append((doc, float(distance)))
                    if len(results) == k:
                        break
                        
        return results[:k]

    def update_document(self, doc_id: str, new_content: str, new_metadata: Dict,
                       new_embedding: Optional[np.ndarray] = None):
        """Update existing document with new content and metadata."""
        if doc_id in self.id_to_index:
            idx = self.id_to_index[doc_id]
            if new_embedding is not None:
                # Remove old embedding and add new one
                old_embeddings = self.index.reconstruct_n(idx, 1)
                self.index.remove_ids(np.array([idx]))
                faiss.normalize_L2(new_embedding.reshape(1, -1))
                self.index.add(new_embedding.reshape(1, -1))
            
            # Update document
            self.documents[idx] = Document(
                id=doc_id,
                content=new_content,
                metadata=new_metadata,
                embedding=new_embedding
            )

    def save(self, path: str):
        """Save vector store state to disk."""
        faiss.write_index(self.index, f"{path}/index.faiss")
        with open(f"{path}/store.pkl", "wb") as f:
            # Save everything except the FAISS index
            state = {
                'documents': self.documents,
                'id_to_index': self.id_to_index,
                'dimension': self.dimension,
                'index_type': self.index_type
            }
            pickle.dump(state, f)

    def load(self, path: str):
        """Load vector store state from disk."""
        self.index = faiss.read_index(f"{path}/index.faiss")
        with open(f"{path}/store.pkl", "rb") as f:
            state = pickle.load(f)
            self.documents = state['documents']
            self.id_to_index = state['id_to_index']
            self.dimension = state['dimension']
            self.index_type = state['index_type']
