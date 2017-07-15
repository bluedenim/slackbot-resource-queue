from message_formatting import format_users


class ConversationListener:
    """
    Listener for conversational / read-only events.
    """

    def __init__(self, users):
        self.users = users

    def post_hello(self, bot_event, **kwargs):
        """
        A user has sent a "hello" message.

        :param bot_event: a BotEvent containing the context for the message
        :param kwargs: additional parameters (if any)

        :return: a list containing the response to the hello message
        """
        return ["Hello back, <@{}>".format(bot_event.user)]

    def post_help(self, bot_event, **kwargs):
        """
        A user has sent a "help" message.

        :param bot_event: a BotEvent containing the context for the message
        :param kwargs: additional parameters (if any)

        :return: the help information to display
        """
        return [
            handler_vals[1] for handler_vals in sorted(
                kwargs.get('env_reservation')._HANDLERS.values(),
                key=lambda t: t[1])
        ]

    def post_status(self, bot_event, **kwargs):
        """
        A user has requested status on resources

        :param bot_event: a BotEvent containing the context for the message
        :param kwargs: additional parameters (if any)

        :return: status of resources
        """
        statuses = kwargs['statuses']
        return ["*{}* queued with *{}*".format(
                    env_name,
                    ','.join(format_users(queued_users, active=False, users=self.users)))
                for env_name, queued_users in statuses]
