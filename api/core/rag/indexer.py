import os
import glob
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from api.core.rag.vector_store import VectorStore

class Indexer:
    """Handles the loading and indexing of repository content."""

    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""]
        )

    def index_repository(self, root_dir: str):
        """Indexes all supported files in the repository."""
        file_patterns = [
            "docs/**/*.md",
            "README.md",
            "CHANGELOG.md",
            "TO-DO.md",
            "src/**/*.py",
            ".ai-context/**/*.md",
            ".ai-context/**/*.json",
            ".gemini/antigravity/**/*.md"
        ]

        for pattern in file_patterns:
            full_pattern = os.path.join(root_dir, pattern)
            for file_path in glob.glob(full_pattern, recursive=True):
                if os.path.isfile(file_path):
                    self._index_file(file_path, root_dir)

    def _index_file(self, file_path: str, root_dir: str):
        """Processes and adds a single file to the vector store."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = os.path.relpath(file_path, root_dir)
            chunks = self.text_splitter.split_text(content)
            
            documents = []
            metadatas = []
            ids = []
            
            for i, chunk in enumerate(chunks):
                documents.append(chunk)
                metadatas.append({
                    "source": relative_path,
                    "chunk": i,
                    "extension": os.path.splitext(file_path)[1]
                })
                ids.append(f"{relative_path}_{i}")
            
            if documents:
                self.vector_store.add_documents(documents, metadatas, ids)
                print(f"Indexed: {relative_path} ({len(chunks)} chunks)")
                
        except Exception as e:
            print(f"Error indexing {file_path}: {e}")
