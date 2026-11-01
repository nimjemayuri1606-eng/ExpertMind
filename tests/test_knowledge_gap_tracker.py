from backend.app.services.knowledge_gap_tracker import KnowledgeGapTracker


def test_record_and_get_gap(tmp_path):

    tracker = KnowledgeGapTracker()

    tracker.storage_file = tmp_path / "knowledge_gaps.json"
    tracker.storage_file.write_text("[]", encoding="utf-8")

    gap = tracker.record_gap(
        question="What is machine learning?",
        session_id="test-session"
    )

    gaps = tracker.get_gaps("test-session")

    assert gap["question"] == "What is machine learning?"
    assert len(gaps) == 1
    assert gaps[0]["session_id"] == "test-session"


def test_clear_gaps(tmp_path):

    tracker = KnowledgeGapTracker()

    tracker.storage_file = tmp_path / "knowledge_gaps.json"
    tracker.storage_file.write_text("[]", encoding="utf-8")

    tracker.record_gap(
        question="What is deep learning?",
        session_id="test-session"
    )

    deleted_count = tracker.clear_gaps("test-session")

    assert deleted_count == 1
    assert tracker.get_gaps("test-session") == []