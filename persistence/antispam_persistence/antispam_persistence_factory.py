"""
provide implementation for AntiSpam Persistence
"""
from persistence.antispam_persistence.i_antispam_persistence import IAntiSpamPersistence
from persistence.antispam_persistence.antispam_persistence_impl import AntiSpamPersistenceImpl
from persistence.antispam_persistence.antispam_persistence_mock import AntiSpamPersistenceMock


class AntiSpamPersistenceFactory(IAntiSpamPersistence):
    """
    factory for Persistence
    """
    @staticmethod
    def new() -> IAntiSpamPersistence:
        """
        instances a new IAntiSpamPersistence
        """
        return AntiSpamPersistenceFactory.new_impl()

    @staticmethod
    def new_impl() -> AntiSpamPersistenceImpl:
        """
        instances a new AntiSpamPersistenceImpl
        """
        return AntiSpamPersistenceImpl()

    @staticmethod
    def new_mock() -> AntiSpamPersistenceMock:
        """
        instances a new AntiSpamPersistenceMock
        """
        return AntiSpamPersistenceMock()
