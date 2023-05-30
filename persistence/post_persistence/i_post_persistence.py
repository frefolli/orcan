"""
provides interface for AntiSpam Persistence
"""
from abc import ABC, abstractmethod
from post_bot.post import Post


class IPostPersistence(ABC):
    """
    interface for Persistence
    """
    @abstractmethod
    def get_post(self, hash : str) -> list[str]:
        """
        return all the post and delete it form db
        """

    @abstractmethod
    def add_post(self, post : Post) -> None:
        """
        adds new post
        """
        