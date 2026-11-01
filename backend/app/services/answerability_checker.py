import re

from backend.app.services.llm_service import llm_service


class AnswerabilityChecker:

    def __init__(self):
        self.llm = llm_service

    def is_answerable(self, question: str, context: str) -> bool:

        if not question.strip() or not context.strip():
            return False

        prompt = f"""
You are a strict document evidence checker.

Determine whether the document directly contains information
that answers the user's question.

Rules:
1. Use ONLY the document context.
2. Never use outside knowledge.
3. Never invent information.
4. If the document supports the answer, copy one complete,
   exact sentence from the context.
5. Never return instruction text or placeholder text.
6. If unsupported, return exactly: NOT_SUPPORTED.

Document Context:
{context}

User Question:
{question}

Required response format:

If the document supports the user's question, return:
SUPPORTED: followed by one complete, exact sentence copied from the document context.

If the document does not support the question, return:
NOT_SUPPORTED

Never return only SUPPORTED.
Never return explanations or additional text.
"""

        response = self.llm.generate_response(prompt).strip()

        print("Answerability checker raw response:", repr(response))

        if not response.startswith("SUPPORTED:"):
            return False

        quotation = response[len("SUPPORTED:"):].strip()

        normalised_context = re.sub(r"\s+", " ", context).strip()
        normalised_quotation = re.sub(r"\s+", " ", quotation).strip()

        if not normalised_quotation:
            return False

        if normalised_quotation not in normalised_context:
            return False

        return True


answerability_checker = AnswerabilityChecker()