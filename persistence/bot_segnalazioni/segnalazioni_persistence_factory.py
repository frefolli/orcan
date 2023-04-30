"""
provide implementation for Segnalazioni Persistence
"""
from .i_segnalazioni_persistence import ISegnalazioniPersistence
from .segnalazioni_persistence_impl import SegnalazioniPersistenceImpl
from .segnalazioni_persistence_mock import SegnalazioniPersistenceMock


class SegnalazioniPersistenceFactory(ISegnalazioniPersistence):
    """
    factory for Persistence
    """
    @staticmethod
    def new() -> ISegnalazioniPersistence:
        """
        instances a new ISegnalazioniPersistence
        """
        return SegnalazioniPersistenceFactory.new_impl()

    @staticmethod
    def new_impl() -> SegnalazioniPersistenceImpl:
        """
        instances a new SegnalazioniPersistenceImpl
        """
        return SegnalazioniPersistenceImpl()

    @staticmethod
    def new_mock() -> SegnalazioniPersistenceMock:
        """
        instances a new SegnalazioniPersistenceMock
        """
        return SegnalazioniPersistenceMock()
