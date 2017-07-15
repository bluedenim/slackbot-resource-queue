from van.message_formatting import format_users, format_user


class ResourceEventListener:
    """
    Listener for events to append additional responses depending on the state of
    the reservation queues. For example, when a user is removed from the queue of
    a resource, the next user in the queue is notified.
    """

    def __init__(self, users):
        self.users = users

    def _env_and_user(self, **kwargs):
        return kwargs.get('env_reservation'), kwargs.get('user')

    def _format_queue_status(self, resource,
                             queue, env_reservation):
        if queue:
            return "*{}* queued with *{}*".format(
               resource,
               ', '.join(format_users(queue, active=False, users=self.users)))
        else:
            return "*{}* is open".format(resource)

    def post_user_removed(self, bot_event, **kwargs):
        """
        A user has been removed
        :param bot_event: the BotEvent associated with the user removed event
        :param kwargs:
            env_reservation - the EnvReservation instance
            user - the user removed
        :return: responses to the event
        """
        responses = []
        env_reservation, queue_head_pre_remove = self._env_and_user(**kwargs)
        if env_reservation and queue_head_pre_remove:
            responses.append(
                "Removed {} from {}.".format(
                    format_user(bot_event.user, users=self.users),
                    bot_event.resource)
            )
            if bot_event.user == queue_head_pre_remove:
                # The event user (the one removed) WAS the head of the queue
                # before the remove.
                queue = env_reservation.get_queued(bot_event.resource)
                responses.append(self._format_queue_status(
                    bot_event.resource,
                    queue, env_reservation))
                if queue:
                    # Notify new head of queue
                    responses.append(
                        "{}: you are up for *{}*! :thumbsup:".format(
                            format_user(queue[0], users=self.users),
                            bot_event.resource))
        return responses

    def post_user_added(self, bot_event, **kwargs):
        """
        A user has been added to a resource's queue
        :param bot_event: the BotEvent associated with the user added event
        :param kwargs: 
            env_reservation - the EnvReservation instance
            user - the user added
        :return: responses to the event
        """
        responses = []
        env_reservation, added_user = self._env_and_user(**kwargs)
        if env_reservation and added_user:
            queue = env_reservation.get_queued(bot_event.resource)
            responses.append(self._format_queue_status(
                bot_event.resource,
                queue, env_reservation))
            if queue:
                if queue[0] == added_user:
                    responses.append(
                        "{}: you are up for *{}* since you're first."
                        " :thumbsup:".format(
                            format_user(added_user, users=self.users),
                            bot_event.resource))
        return responses

    def post_all_users_removed(self, bot_event, **kwargs):
        """
        All users have been removed from a resource's queue
        :param bot_event: the BotEvent associated with the remove event
        :param kwargs: 
            env_reservation - the EnvReservation instance
            removed_users - the users removed from the resource, if any         
        :return: 
        """
        responses = []
        env_reservation, _ = self._env_and_user(**kwargs)
        removed_users = kwargs.get('removed_users')
        if env_reservation and removed_users:
            responses.append(
                "Removed {} from *{}*".format(
                    ', '.join(format_users(
                        removed_users, active=False, users=self.users)),
                    bot_event.resource))
        responses.append("*{}* is open".format(bot_event.resource))
        return responses
