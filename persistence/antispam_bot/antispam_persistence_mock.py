"""
provide implementation for AntiSpam Persistence
"""
from persistence.i_antispam_persistence import IAntiSpamPersistence


class AntiSpamPersistenceMock(IAntiSpamPersistence):
    """
    interface for Persistence
    """
    def __init__(self) -> None:
        """
        default constructor
        """
        self.__banned_words = []
        self.__allowed_links = []

    def get_all_banned_words(self) -> list[str]:
        """
        returns a list of all banned words in database
        """
        return list(self.__banned_words)

    def add_banned_word(self, word: str) -> None:
        """
        adds a word in database
        """
        if word not in self.__banned_words:
            self.__banned_words.append(word)

    def remove_banned_word(self, word: str) -> None:
        """
        remove a word from database
        """
        if word in self.__banned_words:
            self.__banned_words.remove(word)

    def get_all_allowed_links(self) -> list[str]:
        """
        returns a list of all swears in database
        """
        return list(self.__allowed_links)

    def add_allowed_link(self, link: str) -> None:
        """
        adds a link in database
        """
        if link not in self.__allowed_links:
            self.__allowed_links.append(link)

    def remove_allowed_link(self, link: str) -> None:
        """
        remove a link from database
        """
        if link in self.__allowed_links:
            self.__allowed_links.remove(link)
