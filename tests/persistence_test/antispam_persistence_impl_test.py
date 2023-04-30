"""
provides tests for antispam_persistence_test
"""
import tempfile
import os
from unittest import TestCase
from persistence.antispam_persistence.antispam_persistence_impl import AntiSpamPersistenceImpl


class AntiSpamPersistenceImplTest(TestCase):
    """
    test cases for AntiSpamPersistenceImpl
    """
    def test_use_allowed_links(self):
        """
        tests getting links,
        adding a link,
        removing a link
        creates the database in a tmp folder
        """
        with tempfile.TemporaryDirectory() as dir_path:
            persistence = AntiSpamPersistenceImpl(
                os.path.join(dir_path, "antispam.db"))
            self.assertEqual([], persistence.get_all_allowed_links())
            persistence.add_allowed_link("unimib.it")
            self.assertEqual(["unimib.it"],
                             persistence.get_all_allowed_links())
            persistence.remove_allowed_link("unimib.it")
            self.assertEqual([], persistence.get_all_allowed_links())

    def test_use_banned_word(self):
        """
        tests getting words,
        adding a word,
        removing a word
        creates the database in a tmp folder
        """
        with tempfile.TemporaryDirectory() as dir_path:
            persistence = AntiSpamPersistenceImpl(
                os.path.join(dir_path, "antispam.db"))
            self.assertEqual([], persistence.get_all_banned_words())
            persistence.add_banned_word("foti")
            self.assertEqual(["foti"],
                             persistence.get_all_banned_words())
            persistence.remove_banned_word("foti")
            self.assertEqual([], persistence.get_all_banned_words())
