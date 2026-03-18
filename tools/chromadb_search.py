"""ChromaDB-based 3GPP spec vector search for Plan B local stack."""

import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path


class SpecSearcher:
    def __init__(self, db_path: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection("3gpp_specs")
        self.embedder = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5")
    
    def search(self, query: str, top_k: int = 10, spec_filter: str = None) -> list:
        """Semantic search over 3GPP spec chunks."""
        query_embedding = self.embedder.encode(query).tolist()
        where = {"spec_id": spec_filter} if spec_filter else None
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where
        )
        
        return [
            {"text": doc, "metadata": meta, "distance": dist}
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )
        ]
    
    def add_chunk(self, chunk_id: str, text: str, metadata: dict):
        """Add a spec chunk to the vector store."""
        embedding = self.embedder.encode(text).tolist()
        self.collection.add(
            ids=[chunk_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata]
        )
