from pathlib import Path

from pypdf import PdfReader


def load_pdf(file_path: str) -> list[dict]:
    """
    Extract text from a PDF file, page by page.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    reader = PdfReader(str(path))

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        if text.strip():

            documents.append({
                "text": text,
                "source": path.name,
                "page": page_number
            })

    return documents


def load_txt(file_path: str) -> list[dict]:
    """
    Extract text from a TXT file.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    text = path.read_text(encoding="utf-8")

    if not text.strip():
        return []

    return [{
        "text": text,
        "source": path.name,
        "page": None
    }]


def load_document(file_path: str) -> list[dict]:
    """
    Select the appropriate loader based on file extension.
    """

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return load_pdf(file_path)

    elif extension == ".txt":
        return load_txt(file_path)

    else:
        raise ValueError("Only PDF and TXT files are supported.")