from pathlib import Path

from backend.app.config import settings
from backend.app.services.vector_store import vector_store


class DocumentManager:

    def __init__(self):
        self.vector_store = vector_store
        self.upload_directory = settings.RAW_DATA_DIR

    def list_documents(self) -> list[dict]:

        results = self.vector_store.collection.get(
            include=["metadatas"]
        )

        document_summary = {}

        for metadata in results["metadatas"]:

            document_id = metadata.get(
                "document_id",
                metadata["source"]
            )

            if document_id not in document_summary:
                document_summary[document_id] = {
                    "document_id": document_id,
                    "filename": metadata["source"],
                    "chunks": 0
                }

            document_summary[document_id]["chunks"] += 1

        return list(document_summary.values())

    def delete_document(self, document_id: str) -> dict:

        if not document_id or Path(document_id).name != document_id:
            raise ValueError("Invalid document ID.")

        results = self.vector_store.collection.get(
            where={"document_id": document_id},
            include=["metadatas"]
        )

        document_ids = results["ids"]

        if not document_ids:
            raise FileNotFoundError(
                f"Document not found: {document_id}"
            )

        storage_filename = results["metadatas"][0].get(
            "storage_filename"
        )

        self.vector_store.collection.delete(ids=document_ids)

        if storage_filename:
            file_path = self.upload_directory / storage_filename
            file_path.unlink(missing_ok=True)

        return {
            "message": "Document deleted successfully.",
            "document_id": document_id,
            "chunks_deleted": len(document_ids)
        }


document_manager = DocumentManager()