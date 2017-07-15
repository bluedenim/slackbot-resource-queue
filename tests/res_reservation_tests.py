import unittest
from unittest import TestCase
from van.res_reservation import ResourceReservation
from van.users import Users


class ResourceReservationTests(TestCase):

    def setUp(self):
        self.users = Users(None)
        self.users.users['12345'] = {'name': 'John Smith'}
        self.resReservation = ResourceReservation(self.users)

    def test_cleanse_env_name(self):
        self.assertEqual(
            'abcdef',
            self.resReservation._cleanse_env_name('abcdef,'))
        self.assertEqual(
            'abcdef',
            self.resReservation._cleanse_env_name('abcdef.'))

    def test_queue(self):
        self.assertTrue(self.resReservation._queue('envABC', 'user123'))
        self.assertEqual(['user123'],
                         self.resReservation._get_queued_to('envABC'))

    def test_queue_missing_params(self):
        self.assertFalse(self.resReservation._queue(None, None))
        self.assertFalse(self.resReservation._queue('envABC', None))
        self.assertFalse(self.resReservation._queue(None, 'user123'))
        self.assertEqual([],
                         self.resReservation._get_queued_to('envABC'))

    def test_remove(self):
        self.resReservation._queue('envABC', 'user123')
        self.resReservation._remove('envABC', 'user123')
        self.assertEqual([],
                         self.resReservation._get_queued_to('envABC'))

    def test_remove_missing_params(self):
        self.assertFalse(self.resReservation._remove(None, None))
        self.assertFalse(self.resReservation._remove('envABC', None))
        self.assertFalse(self.resReservation._remove(None, 'user123'))

    def test_remove_all(self):
        self.assertTrue(self.resReservation._queue('envABC', 'user123'))
        self.assertTrue(self.resReservation._queue('envABC', 'user456'))
        self.assertTrue(self.resReservation._remove_all('envABC'))
        self.assertEqual([],
                         self.resReservation._get_queued_to('envABC'))


if __name__ == '__main__':
    unittest.main()
