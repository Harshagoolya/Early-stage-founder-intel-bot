from abc import ABC, abstractmethod


class BaseChannel(ABC):
    """
    Base class for all delivery channels.
    To add a new channel, subclass this and implement post().
    """

    @abstractmethod
    def post(self, content: dict) -> bool:
        """
        Post content to the channel.

        Args:
            content: dict with keys:
                - markdown: str  (for Discord/Slack)
                - plain:    str  (for Telegram/SMS)
                - html:     str  (for email)
                - topic:    dict (topic metadata)
                - articles: list (source articles)

        Returns:
            True if post succeeded, False otherwise.
        """
        pass
