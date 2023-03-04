"""
index of module persistence
"""
from .sqlite_database import SqliteDatabase # noqa
from .i_antispam_persistence import IAntiSpamPersistence # noqa
from .antispam_persistence_impl import AntiSpamPersistenceImpl # noqa
from .antispam_persistence_mock import AntiSpamPersistenceMock # noqa
from .antispam_persistence_factory import AntiSpamPersistenceFactory # noqa
