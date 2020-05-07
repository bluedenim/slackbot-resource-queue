from slack import WebClient

from van.userstore import UserStore


def format_at_user(user_id):
    """
    Formats a user ID with the <@ > tag. This is used in messages
    to flag the user's attention and also to provide a link to the
    user. If the user_id is None, then "nobody" is returned.

    :param user_id: the user ID
    :return: a formatted string suitable for use in a post
    """
    if user_id:
        return "<@{}>".format(user_id)
    else:
        return None


def format_user(user_id, user_store: UserStore, slack_client: WebClient, active: bool = True):
    """
    Formats the user either as an active "link" or simply the user's name.
    This method uses the users collaborator to get at user names.
    :param user_id: the user ID to format
    :param user_store: UserStore object used to obtain cached user information as needed.
    :param slack_client: WebClient to get user info as needed.
    :param active: if True, then an active link to the user is returned.
        If False, then the user name is returned.
    :return: the formatted value for the user ID provided or None
    """
    formatted = None
    if active:
        formatted = format_at_user(user_id)
    else:
        if user_id:
            user_profile = user_store.get_cached_user_info(user_id)
            if user_profile:
                formatted = "{}".format(user_profile['name'])
    return formatted


def format_users(user_ids, user_store: UserStore, slack_client: WebClient, active=True):
    """
    Formats a collection of user IDs
    :param user_ids: user IDs to format
    :param user_store: UserStore to use to extract user info
    :param slack_client: WebClient to use to get user info from Slack
    :param active: if True, then an active link to the user is returned.
        If False, then the user name is returned.
    :return: formatted values for the user IDs provided. If any user ID cannot
        be formatted, it will be skipped from the returned list.
        The returned list CAN be empty.
    """
    if user_ids:
        formatted_values = [
            format_user(user_id, user_store, slack_client, active=active)
            for user_id in user_ids if user_id]
        return [formatted_value for formatted_value in formatted_values
                if formatted_value]
    else:
        return []
