"""
provides test class for telegram_api_factory
"""
from unittest import TestCase
from telegram_api import TelegramAPIFactory
from telegram_api import TelegramAPIImpl
from telegram_api import TelegramAPIMock
from telegram_api import ITelegramAPI


class TelegramAPIFactoryTest(TestCase):
    """
    test class for telegram_api_factory
    """
    def test_new_impl(self) -> None:
        """
        uses TelegramAPIFactory.new_impl
        expects an instance of TelegramAPIImpl
        expects instance has correct api_token
        """
        api_token = "fake-token"
        handlers = []
        telegram_api = TelegramAPIFactory.new_impl(
            api_token=api_token,
            handlers=handlers
        )
        self.assertTrue(isinstance(telegram_api, TelegramAPIImpl))
        self.assertEqual(api_token, telegram_api.get_api_token())

    def test_new_mock(self) -> None:
        """
        uses TelegramAPIFactory.new_mock
        expects an instance of TelegramAPIMock
        expects instance has correct api_token
        """
        api_token = "fake-token"
        handlers = []
        telegram_api = TelegramAPIFactory.new_mock(
            api_token=api_token,
            handlers=handlers
        )
        self.assertTrue(isinstance(telegram_api, TelegramAPIMock))
        self.assertEqual(api_token, telegram_api.get_api_token())

    def test_new(self) -> None:
        """
        uses TelegramAPIFactory.new
        expects an instance of ITelegramAPI
        expects instance has correct api_token
        """
        api_token = "fake-token"
        handlers = []
        telegram_api = TelegramAPIFactory.new(
            api_token=api_token,
            handlers=handlers
        )
        self.assertTrue(isinstance(telegram_api, ITelegramAPI))
        self.assertEqual(api_token, telegram_api.get_api_token())
