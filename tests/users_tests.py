import unittest
from unittest import TestCase
from mock import patch
from van.users import Users


class TestUsers(TestCase):

    def setUp(self):
        self.users = Users(None)
        self.users.users['12345'] = {'name': 'John Smith'}

    def test_cached_user(self):
        """
        Tests the case when a user's info has been cached        
        """
        self.assertEqual({'name': 'John Smith'},
                         self.users.get_user_info('12345'))

    def test_lookup_user(self):
        """
        Tests the look up process for a user's info
        """
        with patch('slackclient.SlackClient') as MockedSlackClient:
            instance = MockedSlackClient.return_value
            instance.api_call.return_value = {
                'ok': True,
                'user': {'name': 'John Smith'}
            }
            self.users.slack_client = instance
            self.assertEqual({'name': 'John Smith'},
                             self.users.lookup_user_info('12345'))

    def test_uncached_user(self):
        """
        Tests the case when a user's info has not been cached, so a lookup
        is involved.
        """
        with patch('slackclient.SlackClient') as MockedSlackClient:
            instance = MockedSlackClient.return_value
            instance.api_call.return_value = {
                'ok': True,
                'user': {'name': 'John Smith'}
            }
            self.users.slack_client = instance
            self.assertEqual({'name': 'John Smith'},
                             self.users.get_user_info('12345'))

    def test_no_slack(self):
        """
        Tests the case when a SlackClient has not been initialized with the
        Users instance
        """
        self.assertIsNone(self.users.lookup_user_info('12345'))


if __name__ == '__main__':
    unittest.main()
