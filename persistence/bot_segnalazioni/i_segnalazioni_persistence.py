"""
provides interface for Segnalazioni Persistence
"""
from abc import ABC, abstractmethod


class ISegnalazioniPersistence(ABC):
    """
    interface for Persistence
    """
    @abstractmethod
    def get_all_banned_words(self) -> list[str]:
        """
        returns a list of all banned words in database
        """

    @abstractmethod
    def add_banned_word(self, word: str) -> None:
        """
        adds a word in database
        """

    @abstractmethod
    def remove_banned_word(self, word: str) -> None:
        """
        remove a word from database
        """

    @abstractmethod
    def get_all_allowed_links(self) -> list[str]:
        """
        returns a list of all swears in database
        """

    @abstractmethod
    def add_allowed_link(self, link: str) -> None:
        """
        adds a link in database
        """

    @abstractmethod
    def remove_allowed_link(self, link: str) -> None:
        """
        remove a link from database
        """
