from slack.web.client import WebClient

from van import logs


logs.init_logging()
LOGGER = logs.get_logger(__name__)


def _get_users(bot_token):
    users = []
    if bot_token:
        try:
            slack_client = WebClient(token=bot_token)

            api_call = slack_client.api_call('users.list')
            if api_call.get('ok'):
                users = api_call.get('members')
        except Exception:
            LOGGER.exception('Cannot get users')
    return users


def print_user_ids(bot_token):
    if bot_token:
        for user in _get_users(bot_token):
            LOGGER.info('ID for "{name}" is {id}'.format(name=user['name'], id=user.get('id')))
    else:
        LOGGER.warning('Need to set BOT_API_TOKEN env var')


def find_user_id(bot_token, user_name_to_look_up):
    user_id = None
    if bot_token and user_name_to_look_up:
        user = next((user for user in _get_users(bot_token) if user.get('name') == user_name_to_look_up), None)
        if user:
            user_id = user['id']
    return user_id
