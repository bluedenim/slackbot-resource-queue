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


if __name__ == '__main__':
    unittest.main()
