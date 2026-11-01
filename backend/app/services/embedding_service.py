import warnings

warnings.filterwarnings(
    "ignore",
    message=".*unauthenticated requests to the HF Hub.*"
)

from sentence_transformers import SentenceTransformer

from backend.app.config import settings


class EmbeddingService:

    def __init__(self):

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Convert text into numerical vectors.
        """

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings.tolist()


embedding_service = EmbeddingService()