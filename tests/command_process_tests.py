import unittest
from unittest import TestCase
from van.command_process import Processor
from van.users import Users


class TestProcessor(TestCase):

    class TestingProcessor(Processor):

        PROCESSED_MSG = 'returned from test_method(...)'

        def __init__(self, users):
            super(self.__class__, self).__init__(users)

        def test_method(self, params, context_dict):
            return [
                TestProcessor.TestingProcessor.PROCESSED_MSG
            ]

        def dispatch(self, command):
            if command == 'test_method':
                return self.test_method
            else:
                return super(self.__class__, self).dispatch(command)

    def setUp(self):
        self.users = Users(None)
        self.users.users['12345'] = {'name': 'John Smith'}
        self.testing_processor = TestProcessor.TestingProcessor(self.users)

    def test_not_handled(self):
        """
        Test the case when a unhandled command is processed.
        """
        context_dict = {
            'channel': 'blah_channel'
        }
        result = self.testing_processor.process_message(
            'command one two three', context_dict)
        self.assertEqual(context_dict['channel'], result['channel'])
        self.assertEqual(Processor.NOT_IMPLEMENTED_MSG, result['text'])

    def test_handled(self):
        """
        Test the case when the test processor handles a message.
        """
        context_dict = {
            'channel': 'blah_channel'
        }
        result = self.testing_processor.process_message(
            'test_method one two three', context_dict)
        self.assertEqual(context_dict['channel'], result['channel'])
        self.assertEqual(TestProcessor.TestingProcessor.PROCESSED_MSG,
                         result['text'])

    def test_format_user(self):
        """
        Test the user name formatting function when an active "link" is desired
        """
        self.assertEqual('<@12345>',
                         self.testing_processor.format_user('12345'))
        self.assertIsNone(self.testing_processor.format_user(None))

    def test_inactive_format_user(self):
        """
        Test the user name formatting function when just the user name is desired
        """
        self.assertEqual('John Smith',
                         self.testing_processor.format_user(
                             '12345', active=False))
        self.assertIsNone(self.testing_processor.format_user(None, active=False))

    def test_format_users(self):
        """
        Test formatting multiple user IDs
        """
        ids = ['12345', '67890', None, '12345']
        self.assertEqual(['<@12345>', '<@67890>', '<@12345>'],
                         self.testing_processor.format_users(ids))
        self.assertEqual(['John Smith', 'John Smith'],
                         self.testing_processor.format_users(ids, active=False))


if __name__ == '__main__':
    unittest.main()
