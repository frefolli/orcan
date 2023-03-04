"""
provides tests for antispam_persistence_test
"""
from unittest import TestCase
from persistence.antispam_persistence_mock import AntiSpamPersistenceMock


class AntiSpamPersistenceMockTest(TestCase):
    """
    test cases for AntiSpamPersistenceMock
    """
    def test_use_allowed_links(self):
        """
        tests getting links,
        adding a link,
        removing a link
        """
        persistence = AntiSpamPersistenceMock()
        self.assertEqual([], persistence.get_all_allowed_links())
        persistence.add_allowed_link("unimib.it")
        self.assertEqual(["unimib.it"], persistence.get_all_allowed_links())
        persistence.remove_allowed_link("unimib.it")
        self.assertEqual([], persistence.get_all_allowed_links())

    def test_use_banned_word(self):
        """
        tests getting words,
        adding a word,
        removing a word
        """
        persistence = AntiSpamPersistenceMock()
        self.assertEqual([], persistence.get_all_banned_words())
        persistence.add_banned_word("foti")
        self.assertEqual(["foti"], persistence.get_all_banned_words())
        persistence.remove_banned_word("foti")
        self.assertEqual([], persistence.get_all_banned_words())
