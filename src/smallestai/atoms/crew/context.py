from typing import Any, Dict, List


class ContextManager:
    def __init__(self):
        self._messages: List[Dict[str, Any]] = []

    @property
    def messages(self) -> List[Dict[str, Any]]:
        return self._messages

    def add_message(self, message_dict: Dict[str, Any]):
        self._messages.append(message_dict)

    def add_messages(self, messages: List[Dict[str, Any]]):
        self._messages.extend(messages)

    def set_messages(self, messages: List[Dict[str, Any]]):
        """Replace the whole message list (e.g. sync to the platform's
        authoritative conversation carried on an LLM-request event)."""
        self._messages = list(messages)
