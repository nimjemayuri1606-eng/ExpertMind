import json

from backend.app.services.llm_service import llm_service


class TopicExtractor:

    def __init__(self):
        self.llm = llm_service

    def extract_topics_by_question(
        self, questions: list[str]
    ) -> list[dict]:

        if not questions:
            return []

        questions_text = "\n".join(
            f"{index}. {question}"
            for index, question in enumerate(questions, start=1)
        )

        prompt = f"""
You are an expert educational topic classifier.

Identify the main specific subject or concept in each question.

Rules:
1. Return one result for every input question.
2. Identify only the main topic directly asked about.
3. Do not add unrelated or broader topics.
4. Keep topic names short and clear.
5. Preserve specific concepts.
6. Return only valid JSON.

Questions:
{questions_text}

Required JSON format:
{{
    "results": [
        {{
            "question_number": 1,
            "topics": ["Convolutional Neural Network (CNN)"]
        }}
    ]
}}

IMPORTANT:
- "Convolutional Neural Network (CNN)" is an example of a real topic name.
- Never return placeholder names such as "Topic 1", "Topic 2", or "Topic 3".
- Return the actual subject or concept from each input question.
- Do not invent topic names.

"""

        response = self.llm.generate_response(prompt)

        try:
            result = json.loads(response)
            results = result.get("results", [])

            if not isinstance(results, list):
                return []

            output = []

            for item in results:
                if not isinstance(item, dict):
                    continue

                topics = item.get("topics", [])

                if not isinstance(topics, list):
                    topics = []

                clean_topics = list(dict.fromkeys(
                    topic.strip()
                    for topic in topics
                    if isinstance(topic, str) and topic.strip()
                ))

                output.append({
                    "question_number": item.get("question_number"),
                    "topics": clean_topics
                })

            return output

        except (json.JSONDecodeError, AttributeError, TypeError):
            return []


topic_extractor = TopicExtractor()