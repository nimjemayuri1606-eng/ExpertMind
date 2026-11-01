from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from backend.app.config import settings
from backend.app.services.document_loader import load_document
from backend.app.services.text_chunker import split_documents
from backend.app.services.vector_store import vector_store


class DocumentService:

    def __init__(self):
        self.vector_store = vector_store
        self.upload_directory = settings.RAW_DATA_DIR

    async def upload_and_process(self, file: UploadFile) -> dict:

        if not file.filename:
            raise ValueError("File name is required.")

        original_filename = Path(file.filename).name
        extension = Path(original_filename).suffix.lower()

        if extension not in [".pdf", ".txt"]:
            raise ValueError("Only PDF and TXT files are supported.")

        self.upload_directory.mkdir(parents=True, exist_ok=True)

        document_id = uuid4().hex
        storage_filename = f"{document_id}{extension}"
        file_path = self.upload_directory / storage_filename

        try:
            file_content = await file.read()

            if not file_content:
                raise ValueError("Uploaded file is empty.")

            file_path.write_bytes(file_content)

            documents = load_document(str(file_path))

            if not documents:
                raise ValueError("No readable text found in the uploaded document.")

            chunks = split_documents(documents)

            if not chunks:
                raise ValueError("No text chunks were generated.")

            for chunk in chunks:
                chunk["source"] = original_filename
                chunk["document_id"] = document_id
                chunk["storage_filename"] = storage_filename

            stored_chunks = self.vector_store.add_documents(chunks)

            return {
                "message": "Document uploaded and processed successfully.",
                "document_id": document_id,
                "filename": original_filename,
                "chunks_created": len(chunks),
                "chunks_stored": stored_chunks
            }

        except Exception:
            file_path.unlink(missing_ok=True)
            raise

        finally:
            await file.close()


document_service = DocumentService()