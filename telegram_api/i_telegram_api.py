"""
provides interface for TelegramAPI
"""
from abc import ABC, abstractmethod
from telegram.ext import BaseHandler


class ITelegramAPI(ABC):
    """
    interface for TelegramAPI

    should:
    - maintain api_token
    - be startable with "with-as" semantic
    - use handlers to provide service on demand
    """
    @abstractmethod
    def __init__(self,
                 api_token: str,
                 handlers: dict[str, BaseHandler] = None) -> None:
        """
        default constructor
        """

    @abstractmethod
    def start(self) -> None:
        """
        start telegram api
        """

    @abstractmethod
    def __enter__(self) -> None:
        """
        should be able to __enter__ with "with-as"
        """

    @abstractmethod
    def __exit__(self,
                 exception_type,
                 exception_value,
                 exception_traceback) -> None:
        """
        should be able to __exit__ with "with-as"
        """

    @abstractmethod
    def get_api_token(self) -> str:
        """
        should return api token passed as input
        """
