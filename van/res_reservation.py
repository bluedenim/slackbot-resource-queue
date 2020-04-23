from collections import (
    OrderedDict,
    defaultdict,
    namedtuple,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    OrderedDict as OrderedDictType,
)

from slack import WebClient

from van.userstore import UserStore
from van.logs import get_logger


HandlerEntry = namedtuple('HandlerEntry', ['method', 'help_info'])
ProcessResult = namedtuple('ProcessResult', ['channel', 'text'])

LOGGER = get_logger(__name__)


class ResourceReservation:
    """
    Tracks resource reservations to user IDs.
    """
    def __init__(self):
        self.resources = defaultdict(OrderedDictType[str, str])

    def queue(self, resource: str, user_id: str, to_front=False) -> bool:
        """
        Adds a user_id to the queue for a resource.

        :returns: True if a change was made.
        """
        updated = False
        if resource and user_id:
            resource_queue = self.resources[resource]
            if user_id not in resource_queue:
                resource_queue[user_id] = user_id
                resource_queue.move_to_end(user_id, not to_front)
                updated = True
        return updated

    def remove(self, resource: str, user_id: str) -> bool:
        """
        Removes a user_id from the queue for a resource.

        :returns: True if a change was made.
        """
        updated = False
        if resource and user_id:
            resource_queue = self.resources[resource]
            if user_id in resource_queue:
                del resource_queue[user_id]
                updated = True
        return updated

    def remove_all(self, resource: str) -> bool:
        """
        Removes all reservations from the queue for a resource.

        :returns: True if a change was made.
        """
        updated = False
        if resource and resource in self.resources:
            self.resources[resource] = OrderedDict()
            updated = True
        return updated

    def get_resources(self) -> Dict[str, OrderedDictType[str, str]]:
        """
        Returns all the reserved resources along with the user IDs in their queues.

        :returns: a dict keyed by resource name to the queued user IDs to the resource
        """
        return self.resources


class ResourceReservationProcessor:
    """
    Resource reservation processor that will maintain a queue of users for named resources.
    """

    def __init__(self, user_store: UserStore) -> None:
        self.reservations = ResourceReservation()
        self.user_store = user_store

        self.command_handlers = {
            'hello': HandlerEntry(method=self.hello, help_info='*hello* - prints hello back to you'),
            'status': HandlerEntry(method=self.status, help_info='*status* - status of resources'),
            'add': HandlerEntry(method=self.add, help_info='*add x* - adds you to the resource x'),
            'remove': HandlerEntry(method=self.remove, help_info='*remove x* - removes you from resource x'),
            'remove-all': HandlerEntry(method=self.remove_all, help_info='*remove-all x* - frees up resource x'),
            'help': HandlerEntry(method=self.help, help_info='*help* - this message')
        }

    def _user_name_for_id(self, user_id: str, slack_client: WebClient) -> str:
        user_name = None
        if user_id and slack_client:
            user = self.user_store.get_cached_user_info(user_id, slack_client) or {}
            user_name = user.get('real_name')
        return user_name or user_id

    def hello(self, params: List[str], context_dict: Dict[str, Any]) -> List[str]:
        """
        A user (context_dict['user_id']) sent a 'Hello' message.

        :param params: parameter map
        :param context_dict: context dictionary where user can be
            obtained

        :return: response messages
        """
        return [
            'Hello back, {}!'.format(self._user_name_for_id(context_dict['user_id'], context_dict['web_client']))
        ]

    def add(self, params: List[str], context_dict: Dict[str, Any]) -> List[str]:
        """
        A user (context_dict['user_id']) requested to be queued for a resource (params[0])

        :param params: parameter map where resource name can be
            obtained
        :param context_dict: context dictionary where user can be
            obtained

        :return: response messages
        """
        response = []
        user_id = context_dict['user_id']
        if params:
            resource = params[0]
            if self.reservations.queue(resource, user_id):
                user = self._user_name_for_id(user_id, context_dict['web_client'])
                response.append(
                    f'{user} queued for resource *{resource}*'
                )
        return response

    def status(self, params: List[str], context_dict: Dict[str, Any]) -> List[str]:
        """
        A user has requested status of reserved resources.

        :param params: parameter map
        :param context_dict: context dictionary where user can be obtained

        :return: response messages
        """
        web_client = context_dict['web_client']
        response = []
        for resource, queue in self.reservations.get_resources().items():
            queued_users = ', '.join([
                self._user_name_for_id(user_id, web_client)
                for user_id in queue.keys()
            ])
            response.append(f'*{resource}*: {queued_users}')
        return response

    def remove(self, params: List[str], context_dict: Dict[str, Any]) -> List[str]:
        """
        A user (context_dict['user']) is releasing a previously-held resource (params[0])

        :param params: parameter map where resource name can be obtained
        :param context_dict: context dictionary where user can be obtained

        :return: response messages
        """
        response = []
        user_id = context_dict['user_id']
        if params:
            resource = params[0]
            if self.reservations.remove(resource, user_id):
                user = self._user_name_for_id(user_id, context_dict['web_client'])
                response.append(f'{user} removed from resource *{resource}*')
        return response

    def remove_all(self, params: List[str], context_dict: Dict[str, Any]) -> List[str]:
        """
        A user (context_dict['user']) is releasing all queued users from a resource (params[0]).

        :param params: parameter map
        :param context_dict: context dictionary where user can be obtained

        :return: response messages
        """
        response = []
        user_id = context_dict['user_id']
        if params:
            resource = params[0]
            if self.reservations.remove_all(resource):
                user = self._user_name_for_id(user_id, context_dict['web_client'])
                response.append(f'{user} removed *everyone* from resource *{resource}*')

        return response

    def help(self, params, context_dict) -> List[str]:
        """
        A user (context_dict['user']) is requested help

        :param params: parameter map
        :param context_dict: context dictionary where user can be obtained

        :return: response messages
        """
        return [
            f'{handler_entry.help_info}'
            for handler_entry in self.command_handlers.values()
        ]

    def _get_handler_method(self, command: str) -> Optional[Callable]:
        """
        Look up a handler method for a command. The handler will in turn be
        called with a parameter map and context map.

        :param command: the command name to look up a handler for

        :return: handler for the command (or None)
        """
        handler = None
        if command:
            command = command.lower()
            handler_entry = self.command_handlers.get(command)
            if handler_entry:
                handler = handler_entry[0]
        return handler

    def process_message_text(self, message_tokens: List[str], context_dict: Dict) -> List[str]:
        """
        Process a message text and return a ProcessResult or None if there is nothing processed.

        :param message_tokens: the message text tokens to process (e.g. ["add", "printer-1"])
        :param context_dict: the context dictionary with information about the environment/context of the message
            (e.g. the user that sent this message)
        :return: responses to send back
        """
        result = []
        if message_tokens:
            command = message_tokens.pop(0)
            handler = self._get_handler_method(command)
            if handler:
                responses = handler(message_tokens, context_dict)
                if responses:
                    result.extend(responses)
        return result
