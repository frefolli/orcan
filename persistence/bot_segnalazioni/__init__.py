"""
index of module persistence
"""
from .sqlite_database import SqliteDatabase # noqa
from .i_segnalazioni_persistence import ISegnalazioniPersistence # noqa
from .segnalazioni_persistence_impl import SegnalazioniPersistenceImpl # noqa
from .segnalazioni_persistence_mock import SegnalazioniPersistenceMock # noqa
from .segnalazioni_persistence_factory import SegnalazioniPersistenceFactory # noqa
