import unittest
from unittest import TestCase

from van.message_formatting import format_user, format_users
from van.users import Users


class MessageFormattingTest(TestCase):

    def setUp(self):
        self.users = Users(None)
        self.users.users['12345'] = {'name': 'John Smith'}

    def test_format_user(self):
        """
        Test the user name formatting function when an active "link" is desired
        """
        self.assertEqual('<@12345>',
                         format_user('12345'))
        self.assertIsNone(format_user(None))

    def test_inactive_format_user(self):
        """
        Test the user name formatting function when just the user name is desired
        """
        self.assertEqual('John Smith',
                         format_user(
                             '12345', active=False, users=self.users))
        self.assertIsNone(format_user(None, active=False, users=self.users))

    def test_format_users(self):
        """
        Test formatting multiple user IDs
        """
        ids = ['12345', '67890', None, '12345']
        self.assertEqual(['<@12345>', '<@67890>', '<@12345>'],
                         format_users(ids))
        self.assertEqual(['John Smith', 'John Smith'],
                         format_users(ids, active=False, users=self.users))


if __name__ == '__main__':
    unittest.main()
