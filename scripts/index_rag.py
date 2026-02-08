#!/usr/bin/env python3
import os
import sys

# Ensure project root is on sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from api.core.rag.rag_manager import RAGManager

def main():
    print("Initializing LOGIK-PROJEKT RAG Index...")
    manager = RAGManager()
    manager.initialize_index()
    print("Indexing complete.")

if __name__ == "__main__":
    main()
