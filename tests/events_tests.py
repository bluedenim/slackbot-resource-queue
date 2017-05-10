import unittest
from unittest import TestCase
from van import events
from van.events import EventType


class TestEvents(TestCase):

    CHANNEL = 'my_channel'
    TEST_USER = 'testUser'
    TEST_RESOURCE = 'testResource'

    def setUp(self):
        self.add_user_count = 0
        self.remove_user_count = 0
        events.add_listener(self)

    def tearDown(self):
        events.remove_listener(self)

    def test_notify_user_added(self):
        events.notify(events.BotEvent(type=EventType.user_added,
                                      channel=TestEvents.CHANNEL,
                                      user=TestEvents.TEST_USER,
                                      resource=TestEvents.TEST_RESOURCE))
        self.assertEqual(1, self.add_user_count)

    def test_notify_user_removed(self):
        events.notify(events.BotEvent(type=EventType.user_removed,
                                      channel=TestEvents.CHANNEL,
                                      user=TestEvents.TEST_USER,
                                      resource=TestEvents.TEST_RESOURCE))
        self.assertEqual(1, self.remove_user_count)

    def test_unhandled(self):
        events.notify(events.BotEvent(type=EventType.all_users_removed,
                                      channel=TestEvents.CHANNEL,
                                      user=TestEvents.TEST_USER,
                                      resource=TestEvents.TEST_RESOURCE))
        self.assertEqual(0, self.add_user_count)
        self.assertEqual(0, self.remove_user_count)

    def test_removed_listener(self):
        events.remove_listener(self)
        events.notify(events.BotEvent(type=EventType.user_added,
                                      channel=TestEvents.CHANNEL,
                                      user=TestEvents.TEST_USER,
                                      resource=TestEvents.TEST_RESOURCE))
        self.assertEqual(0, self.add_user_count)

    def post_user_added(self, bot_event, **kwargs):
        self.add_user_count += 1
        return []

    def post_user_removed(self, bot_event, **kwargs):
        self.remove_user_count += 1
        return []


if __name__ == '__main__':
    unittest.main()
