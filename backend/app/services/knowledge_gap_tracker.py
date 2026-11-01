import json
from datetime import datetime, timezone
from pathlib import Path


class KnowledgeGapTracker:

    def __init__(self):
        self.storage_directory = Path("outputs")
        self.storage_directory.mkdir(parents=True, exist_ok=True)

        self.storage_file = (
            self.storage_directory / "knowledge_gaps.json"
        )

        if not self.storage_file.exists():
            self._save_gaps([])

    def _load_gaps(self) -> list[dict]:

        with self.storage_file.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _save_gaps(self, gaps: list[dict]) -> None:

        with self.storage_file.open("w", encoding="utf-8") as file:
            json.dump(gaps, file, indent=4, ensure_ascii=False)

    def record_gap(
        self,
        question: str,
        session_id: str = "default"
    ) -> dict:

        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        if not session_id or not session_id.strip():
            raise ValueError("Session ID cannot be empty.")

        gaps = self._load_gaps()

        gap = {
            "question": question.strip(),
            "session_id": session_id.strip(),
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        gaps.append(gap)

        self._save_gaps(gaps)

        return gap

    def get_gaps(self, session_id: str | None = None) -> list[dict]:

        gaps = self._load_gaps()

        if session_id:
            gaps = [
                gap for gap in gaps
                if gap["session_id"] == session_id
            ]

        return gaps

    def clear_gaps(self, session_id: str | None = None) -> int:

        gaps = self._load_gaps()

        if session_id:
            remaining_gaps = [
                gap for gap in gaps
                if gap["session_id"] != session_id
            ]
        else:
            remaining_gaps = []

        deleted_count = len(gaps) - len(remaining_gaps)

        self._save_gaps(remaining_gaps)

        return deleted_count


knowledge_gap_tracker = KnowledgeGapTracker()