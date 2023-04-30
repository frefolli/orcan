"""
provides sqlite database abstraction
"""
import sqlite3


class SqliteDatabase:
    """
    sqlite database abstraction
    """
    def __init__(self, file_path: str) -> None:
        """
        default constructor

        Args:
            file_path (str): _description_
        """
        self.__file_path = file_path
        self.__connection = None
        self.__cursor = None

    def __enter__(self) -> "SqliteDatabase":
        """
        open connection and load cursor
        for with-as semantic
        """
        self.__connection = sqlite3.connect(self.__file_path)
        self.__cursor = self.__connection.cursor()
        return self

    def execute_script(self, sql_script: str) -> None:
        """
        execute a sql script

        Args:
            sql_script (str): _description_
        """
        self.__cursor.executescript(sql_script)

    def execute_query(self, sql_query: str,
                      parameters: list = []) -> None:
        """
        execute a sql query

        Args:
            sql_query (str): _description_
        """
        self.__cursor.execute(sql_query, parameters)
        self.__connection.commit()

    def get_all(self, sql_query: str,
                parameters: list = []) -> list:
        """
        execute a sql query and return rows

        Args:
            sql_query (str): _description_
        """
        return (self.__cursor
                .execute(sql_query, parameters)
                .fetchall())

    def __exit__(self,
                 exception_type,
                 exception_value,
                 exception_traceback) -> None:
        """
        closes application
        """
        self.__connection.close()
