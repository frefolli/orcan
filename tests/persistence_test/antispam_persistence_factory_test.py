"""
provides test class for telegram_api_factory
"""
from unittest import TestCase
from persistence.antispam_persistence_factory import AntiSpamPersistenceFactory
from persistence.i_antispam_persistence import IAntiSpamPersistence
from persistence.antispam_persistence_impl import AntiSpamPersistenceImpl
from persistence.antispam_persistence_mock import AntiSpamPersistenceMock


class AntiSpamPersistenceFactoryTest(TestCase):
    """
    test class for telegram_api_factory
    """
    def test_new_impl(self) -> None:
        """
        uses AntiSpamPersistenceFactory.new_impl
        expects an instance of AntiSpamPersistenceImpl
        """
        telegram_api = AntiSpamPersistenceFactory.new_impl()
        self.assertTrue(isinstance(telegram_api, AntiSpamPersistenceImpl))

    def test_new_mock(self) -> None:
        """
        uses AntiSpamPersistenceFactory.new_mock
        expects an instance of AntiSpamPersistenceMock
        """
        telegram_api = AntiSpamPersistenceFactory.new_mock()
        self.assertTrue(isinstance(telegram_api, AntiSpamPersistenceMock))

    def test_new(self) -> None:
        """
        uses AntiSpamPersistenceFactory.new
        expects an instance of IAntiSpamPersistence
        """
        telegram_api = AntiSpamPersistenceFactory.new()
        self.assertTrue(isinstance(telegram_api, IAntiSpamPersistence))
