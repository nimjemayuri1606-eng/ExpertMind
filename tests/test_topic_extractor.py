
import json

from backend.app.services.topic_extractor import TopicExtractor


def test_extract_topics_by_question():
    extractor = TopicExtractor()

    extractor.llm.generate_response = lambda prompt: json.dumps({
        "results": [
            {
                "question_number": 1,
                "topics": ["Machine Learning"]
            },
            {
                "question_number": 2,
                "topics": ["Deep Learning"]
            }
        ]
    })

    results = extractor.extract_topics_by_question([
        "What is machine learning?",
        "What is deep learning?"
    ])

    assert results == [
        {
            "question_number": 1,
            "topics": ["Machine Learning"]
        },
        {
            "question_number": 2,
            "topics": ["Deep Learning"]
        }
    ]


def test_empty_questions():
    extractor = TopicExtractor()

    results = extractor.extract_topics_by_question([])

    assert results == []


def test_invalid_llm_response():
    extractor = TopicExtractor()

    extractor.llm.generate_response = lambda prompt: "Invalid response"

    results = extractor.extract_topics_by_question([
        "What is machine learning?"
    ])

    assert results == []


def test_invalid_results_format():
    extractor = TopicExtractor()

    extractor.llm.generate_response = lambda prompt: (
        '{"results": "invalid"}'
    )

    results = extractor.extract_topics_by_question([
        "What is machine learning?"
    ])

    assert results == []
