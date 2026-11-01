from collections import defaultdict


class ConversationMemory:

    def __init__(self, max_messages: int = 10):

        # Store conversation history separately for each session
        self.history = defaultdict(list)

        # Maximum number of messages to retain per session
        self.max_messages = max_messages

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str
    ) -> None:
        """
        Add a user or assistant message to conversation history.
        """

        if not session_id.strip():
            raise ValueError("Session ID cannot be empty.")

        if role not in ["user", "assistant"]:
            raise ValueError("Role must be user or assistant.")

        if not content.strip():
            raise ValueError("Message content cannot be empty.")

        self.history[session_id].append({
            "role": role,
            "content": content
        })

        # Keep only the most recent messages
        self.history[session_id] = self.history[session_id][
            -self.max_messages:
        ]

    def get_history(self, session_id: str) -> list[dict]:
        """
        Return conversation history for a session.
        """

        return self.history.get(session_id, []).copy()

    def clear_history(self, session_id: str) -> None:
        """
        Clear conversation history for a session.
        """

        self.history.pop(session_id, None)


conversation_memory = ConversationMemory()