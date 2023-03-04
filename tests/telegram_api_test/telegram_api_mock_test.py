"""
provides test class for telegram_api_mock
"""
from unittest import TestCase
from telegram.ext import MessageHandler
from telegram_api import TelegramAPIMock


class TelegramAPIMockTest(TestCase):
    """
    test class for telegram_api_mock
    """
    def test_constructor_with_empty_handlers(self) -> None:
        """
        creates an instance of TelegramAPIMock
        with handlers as empty list
        expects correct api token
        """
        api_token = "fake-token"
        handlers = {}
        telegram_api = TelegramAPIMock(
            api_token=api_token,
            handlers=handlers
        )
        self.assertEqual(api_token, telegram_api.get_api_token())

    def test_constructor_with_none_handlers(self) -> None:
        """
        creates an instance of TelegramAPIMock
        with handlers as None
        expects correct api token
        """
        api_token = "fake-token"
        handlers = None
        telegram_api = TelegramAPIMock(
            api_token=api_token,
            handlers=handlers
        )
        self.assertEqual(api_token, telegram_api.get_api_token())

    def test_constructor_with_some_handlers(self) -> None:
        """
        creates an instance of TelegramAPIMock
        with handlers as a meaningful list
        expects correct api token
        """
        api_token = "fake-token"
        handlers = [
            MessageHandler(filters=None, callback=(lambda u, c: None))
        ]
        telegram_api = TelegramAPIMock(
            api_token=api_token,
            handlers=handlers
        )
        self.assertEqual(api_token, telegram_api.get_api_token())
