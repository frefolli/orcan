"""
provides factory of TelegramAPI
"""
from telegram.ext import BaseHandler
from telegram_api.i_telegram_api import ITelegramAPI
from telegram_api.telegram_api_impl import TelegramAPIImpl
from telegram_api.telegram_api_mock import TelegramAPIMock


class TelegramAPIFactory:
    """
    factory of TelegramAPI
    """
    @staticmethod
    def new_impl(api_token: str,
                 handlers: list[BaseHandler] = None) -> TelegramAPIImpl:
        """
        creates a new TelegramAPIImpl by api_token
        """
        return TelegramAPIImpl(
            api_token=api_token,
            handlers=handlers
        )

    @staticmethod
    def new_mock(api_token: str,
                 handlers: list[BaseHandler] = None) -> TelegramAPIMock:
        """
        creates a new TelegramAPIMock by api_token
        """
        return TelegramAPIMock(
            api_token=api_token,
            handlers=handlers
        )

    @staticmethod
    def new(api_token: str,
            handlers: list[BaseHandler] = None) -> ITelegramAPI:
        """
        creates a new TelegramAPI by api_token
        """
        return TelegramAPIFactory.new_impl(
            api_token=api_token,
            handlers=handlers
        )
