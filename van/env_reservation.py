import re

import events
from command_process import Processor
from events import BotEvent, EventType


class EnvReservation(Processor):

    def __init__(self, users):
        super(self.__class__, self).__init__(users)
        self.reservations = {}
        self._HANDLERS = {
            'hello': (self.hello, '*hello* - prints hello back to you'),
            'status': (self.status, '*status x, y, z, ...* - status of resources'),
            'status-all': (self.status_all, '*status-all* - status of everything I know of'),
            'add': (self.add, '*add x* - adds you to the resource x'),
            'remove': (self.remove, '*remove x* - removes you from resource x'),
            'remove-all': (self.remove_all, '*remove-all x* - frees up resource x'),
            'help': (self.help, '*help* - this message')
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

    def get_queued(self, env_name):
        return self._get_queued_to(env_name)

    def hello(self, params, context_dict):
        return ["Hello back, <@{}>".format(context_dict['user'])]

    def status(self, params, context_dict):
        params = params or []
        context_dict = context_dict or {}
        statuses = [(self._cleanse_env_name(env_name),
                     self._get_queued_to(self._cleanse_env_name(env_name)))
                    for env_name in params]
        responses = []
        for env_name, queued_users in statuses:
            if queued_users:
                responses.append("*{}* queued with *{}*".format(
                    env_name,
                    ','.join(self.format_users(queued_users, active=False))))
            else:
                responses.append("*{}* is open".format(env_name))
        return responses

    def status_all(self, params, context_dict):
        params = params or []
        context_dict = context_dict or {}
        env_names = self._queued_entries()
        if env_names:
            return self.status(env_names, context_dict)
        else:
            return ["Nothing queued at the moment."]

    def add(self, params, context_dict):
        params = params or []
        context_dict = context_dict or {}
        user = context_dict['user']
        if user:
            self.users.lookup_user_info(user)
            if params:
                env_name = self._cleanse_env_name(params[0])
                if self._queue(env_name, user):
                    responses = ["{}: added you to *{}*.".format(
                        self.format_user(user), env_name)]
                    responses.extend(
                        events.notify(BotEvent(EventType.user_added,
                                               channel=context_dict['channel'],
                                               user=user,
                                               resource=env_name),
                                      user=user,
                                      env_reservation=self))
                    return responses
                else:
                    return ["{}: are you already in the list for *{}*?".format(
                        self.format_user(user), env_name)]
        else:
            return None

    def remove(self, params, context_dict):
        params = params or []
        context_dict = context_dict or {}
        user = context_dict['user']
        if user and params:
            env_name = self._cleanse_env_name(params[0])
            current_users = self._get_queued_to(env_name)
            if len(current_users) > 0:
                head = current_users[0]
                if self._remove(env_name, user):
                    responses = ["{}: removed you from *{}*.".format(
                        self.format_user(user), env_name)]
                    responses.extend(
                        events.notify(BotEvent(
                                EventType.user_removed,
                                channel=context_dict['channel'],
                                user=user,
                                resource=env_name),
                            user=head,
                            env_reservation=self))
                    return responses
            else:
                return [
                    "{}: *{}* has no one queued, let alone you.".format(
                        self.format_user(user), env_name)
                ]
        else:
            return None

    def remove_all(self, params, context_dict):
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
        else:
            return [
                "*{}* is already unreserved.".format(env_name)
            ]

    def help(self, params, context_dict):
        return [
            handler_vals[1] for handler_vals in sorted(
                self._HANDLERS.values(),
                key=lambda t: t[1])
        ]

    def dispatch(self, command):
        if command:
            command = command.lower()
            handler_vals = self._HANDLERS.get(command)
            if handler_vals:
                return handler_vals[0]
            return None
        else:
            return None

