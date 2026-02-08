import os
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional

class VectorStore:
    """Manages the ChromaDB vector store for LOGIK-PROJEKT."""

    def __init__(self, storage_path: str = ".chroma_db"):
        self.storage_path = storage_path
        self.client = chromadb.PersistentClient(path=self.storage_path)
        self.collection = self.client.get_or_create_collection(name="logik_projekt_context")

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        """Adds documents to the collection."""
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text: str, n_results: int = 5) -> Dict[str, Any]:
        """Queries the collection for similar documents."""
        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )

    def delete_all(self):
        """Deletes the entire collection (useful for re-indexing)."""
        self.client.delete_collection(name="logik_projekt_context")
        self.collection = self.client.get_or_create_collection(name="logik_projekt_context")
