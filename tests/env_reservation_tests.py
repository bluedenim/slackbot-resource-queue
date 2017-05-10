import unittest
from unittest import TestCase
from van.env_reservation import EnvReservation
from van.users import Users


class EnvReservationTests(TestCase):

    def setUp(self):
        self.users = Users(None)
        self.users.users['12345'] = {'name': 'John Smith'}
        self.envReservation = EnvReservation(self.users)

    def test_cleanse_env_name(self):
        self.assertEqual(
            'abcdef',
            self.envReservation._cleanse_env_name('abcdef,'))
        self.assertEqual(
            'abcdef',
            self.envReservation._cleanse_env_name('abcdef.'))

    def test_queue(self):
        self.assertTrue(self.envReservation._queue('envABC', 'user123'))
        self.assertEqual(['user123'],
                         self.envReservation._get_queued_to('envABC'))

    def test_queue_missing_params(self):
        self.assertFalse(self.envReservation._queue(None, None))
        self.assertFalse(self.envReservation._queue('envABC', None))
        self.assertFalse(self.envReservation._queue(None, 'user123'))
        self.assertEqual([],
                         self.envReservation._get_queued_to('envABC'))

    def test_remove(self):
        self.envReservation._queue('envABC', 'user123')
        self.envReservation._remove('envABC', 'user123')
        self.assertEqual([],
                         self.envReservation._get_queued_to('envABC'))

    def test_remove_missing_params(self):
        self.assertFalse(self.envReservation._remove(None, None))
        self.assertFalse(self.envReservation._remove('envABC', None))
        self.assertFalse(self.envReservation._remove(None, 'user123'))

    def test_remove_all(self):
        self.assertTrue(self.envReservation._queue('envABC', 'user123'))
        self.assertTrue(self.envReservation._queue('envABC', 'user456'))
        self.assertTrue(self.envReservation._remove_all('envABC'))
        self.assertEqual([],
                         self.envReservation._get_queued_to('envABC'))


if __name__ == '__main__':
    unittest.main()
