import chromadb

from backend.app.config import settings
from backend.app.services.embedding_service import embedding_service


class VectorStore:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=str(settings.VECTOR_STORE_DIR)
        )

        self.collection = self.client.get_or_create_collection(
            name="expertmind_documents",
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, chunks: list[dict]) -> int:

        if not chunks:
            return 0

        texts = [chunk["text"] for chunk in chunks]

        embeddings = embedding_service.generate_embeddings(texts)

        ids = [
            f"{chunk.get('document_id', chunk['source'])}_{chunk['page']}_{chunk['chunk']}"
            for chunk in chunks
        ]

        metadatas = [
            {
                "source": chunk["source"],
                "document_id": chunk.get("document_id", chunk["source"]),
                "storage_filename": chunk.get("storage_filename", chunk["source"]),
                "page": chunk["page"] if chunk["page"] is not None else 0,
                "chunk": chunk["chunk"]
            }
            for chunk in chunks
        ]

        self.collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )

        return len(chunks)

    def search(self, query: str, top_k: int = 4) -> list[dict]:

        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        total_chunks = self.collection.count()

        if total_chunks == 0:
            return []

        query_embedding = embedding_service.generate_embeddings([query])

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=min(top_k, total_chunks)
        )

        documents = []

        for index, text in enumerate(results["documents"][0]):

            metadata = results["metadatas"][0][index]

            documents.append({
                "text": text,
                "source": metadata["source"],
                "document_id": metadata.get("document_id", metadata["source"]),
                "page": metadata["page"],
                "chunk": metadata["chunk"]
            })

        return documents


vector_store = VectorStore()