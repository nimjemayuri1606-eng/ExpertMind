import json

from backend.app.services.knowledge_gap_analyzer import knowledge_gap_analyzer
from backend.app.services.llm_service import llm_service


class LearningRecommender:

    def __init__(self):
        self.analyzer = knowledge_gap_analyzer
        self.llm = llm_service

    def generate_recommendations(
        self,
        session_id: str | None = None
    ) -> dict:

        # 1. Analyze knowledge gaps
        analysis = self.analyzer.analyze(session_id)

        if analysis["total_questions"] == 0:
            return {
                "total_questions": 0,
                "recommendations": []
            }

        # 2. Get only topics identified by the analyzer
        topics = analysis["recommendations"]

        allowed_topics = {
            item["topic"].strip().casefold(): item
            for item in topics
        }

        if not allowed_topics:
            return {
                "total_questions": analysis["total_questions"],
                "recommendations": []
            }

        # 3. Prepare the LLM prompt
        prompt = f"""
You are ExpertMind, an AI learning mentor.

Generate learning recommendations for ONLY these topics:

{json.dumps(topics, indent=2)}

Rules:
1. Use exactly the supplied topic names.
2. Do not introduce additional topics.
3. Explain why each topic should be studied.
4. Suggest one practical learning activity per topic.
5. Return valid JSON only.

Required format:
{{
    "recommendations": [
        {{
            "topic": "Exact supplied topic name",
            "reason": "Why to study this topic",
            "activity": "Suggested learning activity"
        }}
    ]
}}
"""

        # 4. Generate recommendations
        response = self.llm.generate_response(prompt)

        # 5. Parse and validate the response
        try:
            result = json.loads(response)

            generated = result.get("recommendations", [])

            if not isinstance(generated, list):
                raise ValueError("Invalid recommendations format.")

            validated = []
            used_topics = set()

            for item in generated:

                if not isinstance(item, dict):
                    continue

                topic = item.get("topic", "")

                if not isinstance(topic, str):
                    continue

                topic_key = topic.strip().casefold()

                # Reject topics not identified by the analyzer
                if topic_key not in allowed_topics:
                    continue

                # Avoid duplicate recommendations
                if topic_key in used_topics:
                    continue

                reason = item.get("reason", "")
                activity = item.get("activity", "")

                if not isinstance(reason, str) or not reason.strip():
                    continue

                if not isinstance(activity, str) or not activity.strip():
                    continue

                validated.append({
                    "topic": allowed_topics[topic_key]["topic"],
                    "reason": reason.strip(),
                    "activity": activity.strip()
                })

                used_topics.add(topic_key)

            return {
                "total_questions": analysis["total_questions"],
                "recommendations": validated
            }

        except (json.JSONDecodeError, AttributeError, ValueError):
            return {
                "total_questions": analysis["total_questions"],
                "recommendations": [],
                "message": "Could not generate valid recommendations."
            }


learning_recommender = LearningRecommender()