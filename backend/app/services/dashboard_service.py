from backend.app.services.document_manager import document_manager
from backend.app.services.knowledge_gap_tracker import knowledge_gap_tracker
from backend.app.services.knowledge_gap_analyzer import knowledge_gap_analyzer


class DashboardService:

    def __init__(self):
        self.document_manager = document_manager
        self.gap_tracker = knowledge_gap_tracker
        self.gap_analyzer = knowledge_gap_analyzer

    def get_dashboard(self, session_id: str | None = None) -> dict:

        # 1. Get uploaded documents
        documents = self.document_manager.list_documents()

        total_documents = len(documents)

        total_chunks = sum(
            document["chunks"] for document in documents
        )

        # 2. Get knowledge gaps
        gaps = self.gap_tracker.get_gaps(session_id)

        # 3. Analyze knowledge gaps
        analysis = self.gap_analyzer.analyze(session_id)

        # 4. Get the five most recent unanswered questions
        recent_gaps = sorted(
            gaps,
            key=lambda gap: gap.get("created_at", ""),
            reverse=True
        )[:5]

        # 5. Prepare dashboard response
        return {
            "summary": {
                "total_documents": total_documents,
                "total_chunks": total_chunks,
                "total_knowledge_gaps": len(gaps),
                "total_topics_to_improve": len(analysis["topics"])
            },
            "documents": documents,
            "knowledge_gaps": {
                "total_questions": len(gaps),
                "recent_questions": recent_gaps
            },
            "learning_topics": analysis["recommendations"]
        }


dashboard_service = DashboardService()