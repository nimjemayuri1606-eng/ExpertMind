import hashlib
import json
from collections import Counter
from pathlib import Path

from backend.app.services.knowledge_gap_tracker import knowledge_gap_tracker
from backend.app.services.topic_extractor import topic_extractor


class KnowledgeGapAnalyzer:

    TOPIC_ALIASES = {
        "k-nearest neighbors": "KNN",
        "k-nearest neighbors (knn)": "KNN",
        "knn": "KNN",
        "k-means clustering": "K-means",
        "kmeans clustering": "K-means",
        "k-means": "K-means",
        "kmeans": "K-means",
        "convolutional neural networks (cnn)": "CNN",
        "convolutional neural network (cnn)": "CNN",
        "convolutional neural networks": "CNN",
        "convolutional neural network": "CNN",
        "cnn": "CNN",
    }

    def __init__(self):
        self.gap_tracker = knowledge_gap_tracker
        self.topic_extractor = topic_extractor
        self.cache_directory = Path("outputs")
        self.cache_directory.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_directory / "topic_analysis_cache.json"

    def normalize_topic(self, topic: str) -> str:
        normalized = " ".join(topic.strip().lower().split())
        return self.TOPIC_ALIASES.get(normalized, topic.strip())

    def _get_signature(self, gaps: list[dict]) -> str:
        relevant_data = [
            {
                "question": gap.get("question", ""),
                "session_id": gap.get("session_id", ""),
                "created_at": gap.get("created_at", "")
            }
            for gap in gaps
        ]

        serialized = json.dumps(
            relevant_data,
            sort_keys=True,
            ensure_ascii=False
        )

        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def _load_cache(self) -> dict:
        if not self.cache_file.exists():
            return {}

        try:
            with self.cache_file.open("r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return {}

    def _save_cache(self, cache: dict) -> None:
        with self.cache_file.open("w", encoding="utf-8") as file:
            json.dump(cache, file, indent=4, ensure_ascii=False)

    def analyze(self, session_id: str | None = None) -> dict:

        gaps = self.gap_tracker.get_gaps(session_id)

        if not gaps:
            return {
                "total_questions": 0,
                "topics": [],
                "topic_frequency": {},
                "recommendations": []
            }

        signature = self._get_signature(gaps)
        cache_key = session_id or "all_sessions"

        cache = self._load_cache()
        cached_result = cache.get(cache_key)

        if (
            cached_result
            and cached_result.get("signature") == signature
        ):
            return cached_result["analysis"]

        questions = [
            gap["question"]
            for gap in gaps
            if gap.get("question")
        ]

        extracted_results = (
            self.topic_extractor.extract_topics_by_question(questions)
        )

        frequency = Counter()

        for item in extracted_results:
            topics = item.get("topics", [])

            normalized_topics = {
                self.normalize_topic(topic)
                for topic in topics
                if isinstance(topic, str) and topic.strip()
            }

            frequency.update(normalized_topics)

        recommendations = [
            {
                "topic": topic,
                "frequency": count,
                "priority": "High" if count >= 2 else "Normal"
            }
            for topic, count in frequency.most_common()
        ]

        analysis = {
            "total_questions": len(gaps),
            "topics": list(frequency.keys()),
            "topic_frequency": dict(frequency),
            "recommendations": recommendations
        }

        cache[cache_key] = {
            "signature": signature,
            "analysis": analysis
        }

        self._save_cache(cache)

        return analysis


knowledge_gap_analyzer = KnowledgeGapAnalyzer()