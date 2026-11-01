from pathlib import Path
from pydantic_settings import BaseSettings


# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):

    PROJECT_NAME: str = "ExpertMind"

    API_VERSION: str = "v1"

    # Ollama configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    LLM_MODEL: str = "qwen2.5:3b"

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Directory configuration
    DATA_DIR: Path = BASE_DIR / "data"

    RAW_DATA_DIR: Path = DATA_DIR / "raw"

    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"

    VECTOR_STORE_DIR: Path = BASE_DIR / "vector_store"

    # RAG configuration
    CHUNK_SIZE: int = 500

    CHUNK_OVERLAP: int = 100

    TOP_K: int = 4


settings = Settings()