import unittest
from unittest import TestCase

from mock import MagicMock
from slack import WebClient

from van.message_formatting import format_user, format_users
from van.userstore import UserStore

from tests.conftest import MOCK_USERS


class MessageFormattingTest(TestCase):

    # TODO: Convert to pytest

    def setUp(self):
        self.mocked_client = MagicMock()
        self.users = UserStore(self.mocked_client)
        self.users.users = {user['id']: user for user in MOCK_USERS}

    def test_format_user(self):
        """
        Test the user name formatting function when an active "link" is desired
        """
        self.assertEqual('<@12345>', format_user('12345', self.users, WebClient()))
        self.assertIsNone(format_user(None, self.users, WebClient()))

    def test_inactive_format_user(self):
        """
        Test the user name formatting function when just the user name is desired
        """
        self.assertEqual(
            'User 1',
            format_user('user_1', self.users, WebClient(), active=False)
        )
        self.assertIsNone(format_user(None, self.users, WebClient()))

    def test_format_users(self):
        """
        Test formatting multiple user IDs
        """
        ids = ['user_1', 'user_2', None, 'user_3']
        self.assertEqual(
            ['<@user_1>', '<@user_2>', '<@user_3>'],
            format_users(ids, self.users, WebClient())
        )
        self.assertEqual(
            ['User 1', 'User 2', 'User 3'],
            format_users(ids, self.users, WebClient(), active=False)
        )


if __name__ == '__main__':
    unittest.main()
