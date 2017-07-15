import re

import events
from command_process import Processor
from events import BotEvent, EventType


class ResourceReservation(Processor):
    """
    Resource reservation processor that will maintain a queue of users for
    arbitrary resources identified by a unique name.
    """

    def __init__(self, users):
        super(self.__class__, self).__init__(users)
        self.reservations = {}
        self._HANDLERS = {
            'hello': (self.hello,
                      '*hello* - prints hello back to you'),
            'status': (self.status,
                       '*status x, y, z, ...* - status of resources'),
            'add': (self.add,
                    '*add x* - adds you to the resource x'),
            'remove': (self.remove,
                       '*remove x* - removes you from resource x'),
            'remove-all': (self.remove_all,
                           '*remove-all x* - frees up resource x'),
            'help': (self.help,
                     '*help* - this message')
        }

    def _cleanse_env_name(self, env_name):
        if env_name:
            pattern = re.compile('[,;.]')
            return pattern.sub('', env_name)
        else:
            return env_name

    def _get_queued_to(self, env_name):
        if env_name:
            return self.reservations.get(env_name) or []
        else:
            return []

    def _queued_entries(self):
        return self.reservations.keys()

    def _queue(self, env_name, user):
        success = False
        if env_name:
            current_owners = self._get_queued_to(env_name)
            if user and (not current_owners or user not in current_owners):
                current_owners.append(user)
                self.reservations[env_name] = current_owners
                success = True
        return success

    def _remove(self, env_name, user):
        success = False
        if env_name:
            current_owners = self._get_queued_to(env_name)
            if user and user in current_owners:
                current_owners.remove(user)
                success = True
        return success

    def _remove_all(self, env_name):
        if env_name and env_name in self.reservations:
            del self.reservations[env_name]
            return True
        else:
            return False

    def _statuses(self, env_names):
        env_names = env_names or []
        return [(self._cleanse_env_name(env_name),
                self._get_queued_to(self._cleanse_env_name(env_name)))
                for env_name in env_names]

    def get_queued(self, env_name):
        return self._get_queued_to(env_name)

    def hello(self, params, context_dict):
        """
        A user (context_dict['user']) sent a 'Hello' message.

        :param params: parameter map
        :param context_dict: context dictionary where user can be
            obtained

        :return: response messages
        """
        return events.notify(BotEvent(EventType.hello,
                                      channel=context_dict['channel'],
                                      user=context_dict['user']))

    def add(self, params, context_dict):
        """
        A user (context_dict['user']) requested to be queued for a
        resource (params[0])

        :param params: parameter map where resource name can be
            obtained
        :param context_dict: context dictionary where user can be
            obtained

        :return: response messages
        """
        params = params or []
        context_dict = context_dict or {}
        user = context_dict['user']
        if user:
            self.users.lookup_user_info(user)
            if params:
                resource = self._cleanse_env_name(params[0])
                if self._queue(resource, user):
                    return events.notify(BotEvent(EventType.user_added,
                                                  channel=context_dict['channel'],
                                                  user=user,
                                                  resource=resource),
                                         user=user,
                                         env_reservation=self)
        return None

    def status(self, params, context_dict):
        """
        A user has requested status of reserved resources.

        :param params: parameter map
        :param context_dict: context dictionary where user can be
            obtained

        :return: response messages
        """
        params = params or []
        context_dict = context_dict or {}
        resources = self._queued_entries()
        return events.notify(BotEvent(EventType.status,
                                      channel=context_dict['channel'],
                                      user=context_dict['user']),
                             statuses=self._statuses(resources))

    def remove(self, params, context_dict):
        """
        A user (context_dict['user']) is releasing a previously-held
        resource (params[0])

        :param params: parameter map where resource name can be
            obtained
        :param context_dict: context dictionary where user can be
            obtained

        :return: response messages
        """
        params = params or []
        context_dict = context_dict or {}
        user = context_dict['user']
        if user and params:
            env_name = self._cleanse_env_name(params[0])
            current_users = self._get_queued_to(env_name)
            if len(current_users) > 0:
                head = current_users[0]
                if self._remove(env_name, user):
                    return events.notify(BotEvent(
                                EventType.user_removed,
                                channel=context_dict['channel'],
                                user=user,
                                resource=env_name),
                            user=head,
                            env_reservation=self)
        return None

    def remove_all(self, params, context_dict):
        """
        A user (context_dict['user']) is releasing all previously-held
        resources (by anyone).

        :param params: parameter map
        :param context_dict: context dictionary where user can be
            obtained

        :return: response messages
        """
        params = params or []
        context_dict = context_dict or {}
        user = context_dict['user']
        env_name = self._cleanse_env_name(params[0])
        if env_name in self._queued_entries():
            curr_owners = self._get_queued_to(env_name)
            if self._remove_all(env_name):
                return events.notify(
                    BotEvent(EventType.all_users_removed,
                             channel=context_dict['channel'],
                             user=user,
                             resource=env_name),
                    removed_users=curr_owners,
                    env_reservation=self)
        return None

    def help(self, params, context_dict):
        """
        A user (context_dict['user']) is requested help

        :param params: parameter map
        :param context_dict: context dictionary where user can be
            obtained

        :return: response messages
        """
        return events.notify(
            BotEvent(EventType.help, channel=context_dict['channel'],
                     user=context_dict['user']),
            env_reservation=self)

    def dispatch(self, command):
        """
        Look up a handler for a command. The handler will in turn be
        called with a parameter map and context map.

        :param command: the command name to look up a handler for

        :return: handler for the command (or None)
        """
        if command:
            command = command.lower()
            handler_vals = self._HANDLERS.get(command)
            if handler_vals:
                return handler_vals[0]
            return None
        else:
            return None

