from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.app.config import settings


def split_documents(documents: list[dict]) -> list[dict]:
    """
    Split extracted documents into smaller text chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = []

    for document in documents:

        text_chunks = splitter.split_text(document["text"])

        for chunk_number, text in enumerate(text_chunks, start=1):

            chunks.append({
                "text": text,
                "source": document["source"],
                "page": document["page"],
                "chunk": chunk_number
            })

    return chunks