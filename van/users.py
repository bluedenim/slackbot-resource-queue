class Users:
    """
    User information query with cache, using the SlackClient as the underlying
    implementation and data source.
    """

    def __init__(self, slack_client):
        self.slack_client = slack_client
        self.users = {}

    def get_user_info(self, user_id):
        """
        Gets the user information dict for a user ID. Once this is called,
        the information is cached.
        
        :param user_id: the user ID to get user info for 
        :return: acquired user info dict or None
        """
        user_info = self.users.get(user_id)
        if not user_info:
            user_info = self.lookup_user_info(user_id)
            if user_info:
                self.users[user_id] = user_info
        return user_info

    def lookup_user_info(self, user_id):
        """
        Consults the underlying implementation/store for user info given
        a user ID.
        :param user_id: the user ID to look up user info for 
        :return: the user info found or None
        """
        user_info = None
        result = {}
        if self.slack_client:
            result = self.slack_client.api_call('users.info', user=user_id)
        if 'ok' in result:
            user_info = result['user']
            self.users[user_id] = user_info
        return user_info
