"""
provides a mock implementation of TelegramAPI
"""
from telegram.ext import BaseHandler
from telegram_api import ITelegramAPI


class TelegramAPIMock(ITelegramAPI):
    """
    mock TelegramAPI implementation
    """
    def __init__(self,
                 api_token: str,
                 handlers: list[BaseHandler] = None) -> None:
        """
        default constructor
        """
        self.__assign_api_token(api_token)
        self.__assign_handlers(handlers)

    def __assign_api_token(self, api_token: str) -> None:
        """
        assigns api token
        """
        self.__api_token = api_token

    def __assign_handlers(self,
                          handlers: list[BaseHandler] = None
                          ) -> None:
        """
        assigns handlers
        """
        if handlers is not None:
            self.__hanlers = handlers

    def start(self) -> None:
        """
        starts application
        """

    def __enter__(self) -> None:
        """
        starts application
        """
        return self

    def __exit__(self,
                 exception_type,
                 exception_value,
                 exception_traceback) -> None:
        """
        closes application
        """

    def get_api_token(self) -> str:
        """
        returns api token passed as input
        """
        return self.__api_token

    async def is_admin(self, user_id: str) -> bool:
        """
        should True if a user_id is an admin
        """
        return False
