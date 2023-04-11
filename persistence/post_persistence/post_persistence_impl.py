"""
provide implementation for Post Persistence
"""
from persistence.post_persistence.i_post_persistence import IPostPersistence
from persistence.sqlite_database import SqliteDatabase
from post_bot.post import Post


class PostPersistenceImpl(IPostPersistence):
    """
    implementation for post Persistence
    """
    def __init__(self,
                 file_path: str = "persistence.db") -> None:
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
                CREATE TABLE IF NOT EXISTS POSTS (
                    hash TEXT PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    file_id TEXT,
                    author_id TEXT
                );
                """)

    def get_post(self, hash : str) -> list[str]:
        """
        returns a list of post with the spacified hash
        """
        with SqliteDatabase(self.__file_path) as database:
            ris = [
                    _[0] for _ in
                    database.get_all(
                        "SELECT * FROM POSTS WHERE hash = ?",
                        (hash,))]
            database.execute_query(
                "DELETE FROM POSTS WHERE hash = ?",
                (hash,)
            )
            return ris

    def add_post(self, post : Post) -> list[str]:
        """
        adds a post in the database
        """
        with SqliteDatabase(self.__file_path) as database:
            database.execute_query(
                """
                INSERT INTO POSTS VALUES (?, ?, ?, ?, ?)
                """,
                (
                    hash(post), 
                    post.get_title(), 
                    post.get_description(), 
                    post.get_file_id(), 
                    post.get_author_id()
                )
            )
