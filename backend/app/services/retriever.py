from backend.app.config import settings
from backend.app.services.vector_store import vector_store


class DocumentRetriever:

    def __init__(self):
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int | None = None) -> list[dict]:
        """
        Retrieve relevant document chunks for a user question.
        """

        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        number_of_results = top_k or settings.TOP_K

        if number_of_results < 1:
            raise ValueError("top_k must be at least 1.")

        results = self.vector_store.search(
            query=query,
            top_k=number_of_results
        )

        return results


document_retriever = DocumentRetriever()