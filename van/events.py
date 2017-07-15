from sets import Set
from enum import Enum


class EventType(Enum):
    user_removed = 'user_removed'
    user_added = 'user_added'
    all_users_removed = 'all_users_removed'
    hello = 'hello'
    help = 'help'
    status = 'status'

_LISTENERS = Set()


class BotEvent:
    """
    BOT events are sent to listeners when an event source calls notify(). Listeners
    are managed via the add_listener() and remove_listeners() functions.
    
    Listeners should implement post_<event name> methods for each event they are interested
    in responding to by returning a collection/list of responses from the method.
    
    Event names are values of the EventType enum above. (E.g. "user_added" event will
    be handled by a post_user_added() method on a listener interested in responding
    to the event.)
    """
    def __init__(self, type, channel=None, user=None, resource=None):
        """
        Construct an instance of a BOT event object.

        :param type: the event type
        :param channel: the channel used to trigger the event
        :param user: the user who triggered the event
        :param resource: the resource the event applies to
        """
        self.type = type
        self.channel = channel
        self.user = user
        self.resource = resource


def add_listener(listener):
    _LISTENERS.add(listener)


def remove_listener(listener):
    if listener in _LISTENERS:
        _LISTENERS.remove(listener)


def notify(bot_event, **kwargs):
    method_name = "post_{}".format(bot_event.type)
    responses = []
    for listener in _LISTENERS:
        try:
            obj_method = getattr(listener, method_name)
            if obj_method:
                responses.extend(obj_method(bot_event, **kwargs))
        except AttributeError as e:
            print "Listener {} does not handle {}".format(
                listener, method_name)
        except Exception as e:
            print "Cannot notify listener {} of {}: {}:{}".format(
                listener, bot_event, e.__class__.__name__, e.message)
    return responses
