"""
provide implementation for AntiSpam Persistence
"""
from persistence.post_persistence.i_post_persistence import IPostPersistence
from persistence.post_persistence.post_persistence_impl import PostPersistenceImpl
from persistence.post_persistence.post_persistence_mock import PostPersistenceMock


class PostPersistenceFactory(IPostPersistence):
    """
    factory for Persistence
    """
    @staticmethod
    def new() -> IPostPersistence:
        """
        instances a new IPostPersistence
        """
        return PostPersistenceFactory.new_impl()

    @staticmethod
    def new_impl() -> IPostPersistence:
        """
        instances a new PostPersistenceImpl
        """
        return PostPersistenceImpl()

    @staticmethod
    def new_mock() -> IPostPersistence:
        """
        instances a new PostPersistenceMock
        """
        return PostPersistenceMock()
