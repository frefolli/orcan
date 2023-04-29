"""
provide implementation for Segnalazioni Persistence
"""
from .i_segnalazioni_persistence import ISegnalazioniPersistence
from .sqlite_database import SqliteDatabase


class SegnalazioniPersistenceImpl(ISegnalazioniPersistence):
    """
    implementation for Segnalazioni Persistence
    """
    def __init__(self,
                 file_path: str = "Segnalazioni.db") -> None:
        """
        default constructor

        Args:
            file_path (str, optional): _description_. Defaults to in-memory.
        """
        self.__file_path = file_path
        self.__create_tables_if_not_exist()

    def __create_tables_if_not_exist(self) -> None:
        """
        ensure tables exist
        """
        with SqliteDatabase(self.__file_path) as database:
            database.execute_script(
                """
                CREATE TABLE IF NOT EXISTS BANNED_WORDS (
                    word TEXT PRIMARY KEY
                );
                CREATE TABLE IF NOT EXISTS ALLOWED_LINKS (
                    link TEXT PRIMARY KEY
                );
                """)

    def get_all_banned_words(self) -> list[str]:
        """
        returns a list of all banned words in database
        """
        with SqliteDatabase(self.__file_path) as database:
            return [
                _[0] for _ in
                database.get_all(
                    """
                    SELECT word FROM BANNED_WORDS
                    """
                )]

    def add_banned_word(self, word: str) -> None:
        """
        adds a word in database
        """
        with SqliteDatabase(self.__file_path) as database:
            database.execute_query(
                """
                INSERT INTO BANNED_WORDS VALUES (?)
                """,
                (word,)
            )

    def remove_banned_word(self, word: str) -> None:
        """
        remove a word from database
        """
        with SqliteDatabase(self.__file_path) as database:
            database.execute_query(
                """
                DELETE FROM BANNED_WORDS WHERE word = ?
                """,
                (word,)
            )

    def get_all_allowed_links(self) -> list[str]:
        """
        returns a list of all alowed links in database
        """
        with SqliteDatabase(self.__file_path) as database:
            return [
                _[0] for _ in
                database.get_all(
                    """
                    SELECT link FROM ALLOWED_LINKS
                    """
                )]

    def add_allowed_link(self, link: str) -> None:
        """
        adds a link in database
        """
        with SqliteDatabase(self.__file_path) as database:
            database.execute_query(
                """
                INSERT INTO ALLOWED_LINKS VALUES (?)
                """,
                (link,)
            )

    def remove_allowed_link(self, link: str) -> None:
        """
        remove a link from database
        """
        with SqliteDatabase(self.__file_path) as database:
            database.execute_query(
                """
                DELETE FROM ALLOWED_LINKS WHERE link = ?
                """,
                (link,)
            )
