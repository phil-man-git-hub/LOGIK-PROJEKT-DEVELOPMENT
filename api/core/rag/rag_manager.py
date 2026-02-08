import os
from typing import List, Dict, Any
from api.core.rag.vector_store import VectorStore
from api.core.rag.indexer import Indexer

class RAGManager:
    """Orchestrates the RAG operations for LOGIK-PROJEKT."""

    def __init__(self, root_dir: str = ".", storage_path: str = ".chroma_db"):
        self.root_dir = root_dir
        self.vector_store = VectorStore(storage_path=storage_path)
        self.indexer = Indexer(vector_store=self.vector_store)

    def initialize_index(self):
        """Performs a full re-indexing of the repository."""
        self.vector_store.delete_all()
        self.indexer.index_repository(self.root_dir)

    def query_context(self, query: str, n_results: int = 5) -> str:
        """Queries the RAG system and returns a formatted context string."""
        results = self.vector_store.query(query, n_results=n_results)
        
        context_parts = []
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            metadata = results['metadatas'][0][i]
            source = metadata.get('source', 'Unknown')
            context_parts.append(f"--- Source: {source} ---\n{doc}")
            
        return "\n\n".join(context_parts)
