from backend.app.services.learning_recommender import LearningRecommender


def test_only_analyzer_approved_topics_are_returned():
    recommender = LearningRecommender()

    recommender.analyzer.analyze = lambda session_id=None: {
        "total_questions": 2,
        "recommendations": [
            {"topic": "Machine Learning", "frequency": 2, "priority": "High"}
        ]
    }

    recommender.llm.generate_response = lambda prompt: """
    {
        "recommendations": [
            {
                "topic": "Machine Learning",
                "reason": "Important topic to understand.",
                "activity": "Build a simple ML model."
            },
            {
                "topic": "Artificial Intelligence",
                "reason": "Explore AI concepts.",
                "activity": "Study AI applications."
            }
        ]
    }
    """

    result = recommender.generate_recommendations()

    assert result["total_questions"] == 2
    assert len(result["recommendations"]) == 1
    assert result["recommendations"][0]["topic"] == "Machine Learning"


def test_duplicate_topics_are_removed():
    recommender = LearningRecommender()

    recommender.analyzer.analyze = lambda session_id=None: {
        "total_questions": 2,
        "recommendations": [
            {"topic": "Machine Learning", "frequency": 2, "priority": "High"}
        ]
    }

    recommender.llm.generate_response = lambda prompt: """
    {
        "recommendations": [
            {
                "topic": "Machine Learning",
                "reason": "Understand ML fundamentals.",
                "activity": "Build a prediction model."
            },
            {
                "topic": " machine learning ",
                "reason": "Learn ML applications.",
                "activity": "Practice with a dataset."
            }
        ]
    }
    """

    result = recommender.generate_recommendations()

    assert len(result["recommendations"]) == 1


def test_invalid_llm_response_is_handled():
    recommender = LearningRecommender()

    recommender.analyzer.analyze = lambda session_id=None: {
        "total_questions": 1,
        "recommendations": [
            {"topic": "Machine Learning", "frequency": 1, "priority": "Normal"}
        ]
    }

    recommender.llm.generate_response = lambda prompt: "Invalid JSON"

    result = recommender.generate_recommendations()

    assert result["total_questions"] == 1
    assert result["recommendations"] == []
    assert "message" in result


def test_empty_knowledge_gaps_return_empty_recommendations():
    recommender = LearningRecommender()

    recommender.analyzer.analyze = lambda session_id=None: {
        "total_questions": 0,
        "topics": [],
        "topic_frequency": {},
        "recommendations": []
    }

    result = recommender.generate_recommendations()

    assert result == {
        "total_questions": 0,
        "recommendations": []
    }