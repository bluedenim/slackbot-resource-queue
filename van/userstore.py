from typing import (
    Dict,
    List,
    Optional,
)

from slack import WebClient

from van.logs import get_logger

LOGGER = get_logger(__name__)


class UserStore:
    """
    User information query with cache, using the SlackClient as the underlying
    implementation and data source.
    """

    def __init__(self) -> None:
        self.users = {}

    def _load_users(self, slack_client: WebClient) -> List[Dict]:
        """

        """
        users = []
        try:
            api_call = slack_client.api_call('users.list')
            if api_call.get('ok'):
                users = api_call.get('members')
        except Exception:
            LOGGER.exception('Cannot get users')
        return users

    def lookup_user_info(self, user_id: str, slack_client: WebClient) -> Optional[Dict]:
        """
        Consults the underlying implementation/store for user info given a user ID.
        :param user_id: the user ID to look up user info for
        :param slack_client: the Slack client to use to talk to Slack

        :return: the user info found or None
        """
        user_info = None
        try:
            if slack_client:
                user_info = slack_client.users_info(user=user_id)
        except Exception:
            LOGGER.exception('Cannot get user info for {}'.format(user_id))
        return user_info

    def get_users(self, slack_client: WebClient) -> Dict[str, Dict]:
        # Expire this periodically?
        if not self.users:
            users = self._load_users(slack_client)
            self.users = {user['id']: user for user in users}
        return self.users

    def get_cached_user_info(self, user_id: str, slack_client: WebClient) -> Optional[Dict]:
        """
        Gets the user information dict for a user ID. Once this is called,
        the information is cached.

        :param user_id: the user ID to get user info for
        :param slack_client: the Slack client to use to talk to Slack
        :return: acquired user info dict or None
        """
        return self.get_users(slack_client).get(user_id)

    def search_for_user(self, user_name: str, slack_client: WebClient) -> Optional[Dict]:
        """
        Consults the underlying implementation/store for user info given a user name.
        :param user_name: the user name look up user info for
        :param slack_client: the Slack client to use to talk to Slack
        :return: the user info found or None
        :raises Exception:
        """
        user = None
        users = self.get_users(slack_client)
        if users:
            user = next((
                user
                for _, user in users.items()
                if user['name'] == user_name or user['real_name'] == user_name
            ), None)
        return user
