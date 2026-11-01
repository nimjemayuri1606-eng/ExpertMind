from backend.app.services.retriever import document_retriever
from backend.app.services.llm_service import llm_service
from backend.app.services.conversation_memory import conversation_memory
from backend.app.services.answerability_checker import answerability_checker
from backend.app.services.knowledge_gap_tracker import knowledge_gap_tracker


class RAGPipeline:

    def __init__(self):
        self.retriever = document_retriever
        self.llm = llm_service
        self.memory = conversation_memory
        self.answerability = answerability_checker
        self.gap_tracker = knowledge_gap_tracker

    def ask(
        self,
        question: str,
        session_id: str = "default"
    ) -> dict:

        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        if not session_id or not session_id.strip():
            raise ValueError("Session ID cannot be empty.")

        question = question.strip()
        session_id = session_id.strip()

        # 1. Retrieve conversation history
        history = self.memory.get_history(session_id)

        conversation_context = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in history[-6:]
        )

        # 2. Build contextual search query
        search_query = (
            f"{conversation_context}\nCurrent question: {question}"
            if conversation_context
            else question
        )

        # 3. Retrieve relevant document chunks
        retrieved_chunks = self.retriever.retrieve(search_query)

        # Handle empty retrieval
        if not retrieved_chunks:

            self.gap_tracker.record_gap(
                question=question,
                session_id=session_id
            )

            answer = (
                "The uploaded documents do not contain "
                "enough information to answer this question."
            )

            self.memory.add_message(session_id, "user", question)
            self.memory.add_message(session_id, "assistant", answer)

            return {
                "question": question,
                "answer": answer,
                "sources": []
            }

        # 4. Prepare document context
        evidence_context = "\n\n".join(
            chunk["text"] for chunk in retrieved_chunks
        )

        context = "\n\n".join(
            (
                f"Source: {chunk['source']}\n"
                f"Page: {chunk['page']}\n"
                f"Content: {chunk['text']}"
            )
            for chunk in retrieved_chunks
        )

        # 5. Check document answerability
        is_supported = self.answerability.is_answerable(
            question=question,
            context=evidence_context
        )

        if not is_supported:

            self.gap_tracker.record_gap(
                question=question,
                session_id=session_id
            )

            answer = (
                "The uploaded documents do not contain "
                "enough information to answer this question."
            )

        else:

            # 6. Generate answer using document context
            prompt = f"""
You are ExpertMind, a document-based AI Knowledge Mentor.

Answer the question using only the document context.

Rules:
1. Do not add facts from general knowledge.
2. Do not invent examples or information.
3. If information is missing, clearly say so.
4. Use conversation history only to understand follow-up questions.
5. Keep the answer simple and clear.

Conversation History:
{conversation_context}

Document Context:
{context}

Question:
{question}

Answer:
"""

            answer = self.llm.generate_response(prompt)

        # 7. Collect source references
        sources = []

        for chunk in retrieved_chunks:
            source = {
                "source": chunk["source"],
                "page": chunk["page"],
                "chunk": chunk["chunk"]
            }

            if source not in sources:
                sources.append(source)

        # 8. Save conversation history
        self.memory.add_message(session_id, "user", question)
        self.memory.add_message(session_id, "assistant", answer)

        # 9. Return response
        return {
            "question": question,
            "answer": answer,
            "sources": sources if is_supported else []
        }


rag_pipeline = RAGPipeline()