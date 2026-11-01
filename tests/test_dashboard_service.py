from backend.app.services.dashboard_service import DashboardService


def test_dashboard_returns_correct_summary():

    service = DashboardService()

    service.document_manager.list_documents = lambda: [
        {"document_id": "doc1", "filename": "doc1.txt", "chunks": 3},
        {"document_id": "doc2", "filename": "doc2.pdf", "chunks": 2}
    ]

    service.gap_tracker.get_gaps = lambda session_id=None: [
        {
            "question": "What is Machine Learning?",
            "session_id": "test-session",
            "created_at": "2026-10-31T04:00:00+00:00"
        }
    ]

    service.gap_analyzer.analyze = lambda session_id=None: {
        "total_questions": 1,
        "topics": ["Machine Learning"],
        "recommendations": [
            {
                "topic": "Machine Learning",
                "frequency": 1,
                "priority": "Normal"
            }
        ]
    }

    result = service.get_dashboard("test-session")

    assert result["summary"]["total_documents"] == 2
    assert result["summary"]["total_chunks"] == 5
    assert result["summary"]["total_knowledge_gaps"] == 1
    assert result["summary"]["total_topics_to_improve"] == 1


def test_dashboard_handles_empty_data():

    service = DashboardService()

    service.document_manager.list_documents = lambda: []
    service.gap_tracker.get_gaps = lambda session_id=None: []
    service.gap_analyzer.analyze = lambda session_id=None: {
        "total_questions": 0,
        "topics": [],
        "topic_frequency": {},
        "recommendations": []
    }

    result = service.get_dashboard()

    assert result["summary"]["total_documents"] == 0
    assert result["summary"]["total_chunks"] == 0
    assert result["summary"]["total_knowledge_gaps"] == 0
    assert result["summary"]["total_topics_to_improve"] == 0