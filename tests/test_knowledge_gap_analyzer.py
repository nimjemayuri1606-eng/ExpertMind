
from backend.app.services.knowledge_gap_analyzer import KnowledgeGapAnalyzer


def test_analyze_knowledge_gaps(tmp_path):
    analyzer = KnowledgeGapAnalyzer()

    # Keep test cache separate from the real application cache.
    analyzer.cache_file = tmp_path / "topic_analysis_cache.json"

    analyzer.gap_tracker.get_gaps = lambda session_id=None: [
        {"question": "What is machine learning?"},
        {"question": "Explain machine learning."},
        {"question": "What is deep learning?"}
    ]

    analyzer.topic_extractor.extract_topics_by_question = (
        lambda questions: [
            {"question_number": 1, "topics": ["Machine Learning"]},
            {"question_number": 2, "topics": ["Machine Learning"]},
            {"question_number": 3, "topics": ["Deep Learning"]}
        ]
    )

    result = analyzer.analyze("test-session")

    assert result["total_questions"] == 3
    assert result["topic_frequency"]["Machine Learning"] == 2
    assert result["topic_frequency"]["Deep Learning"] == 1
    assert result["recommendations"][0]["priority"] == "High"


def test_analyze_empty_gaps(tmp_path):
    analyzer = KnowledgeGapAnalyzer()
    analyzer.cache_file = tmp_path / "topic_analysis_cache.json"

    analyzer.gap_tracker.get_gaps = lambda session_id=None: []

    result = analyzer.analyze("test-session")

    assert result["total_questions"] == 0
    assert result["topics"] == []
    assert result["topic_frequency"] == {}
    assert result["recommendations"] == []
