import os

from van import logs
from van.utils.ids import (
    find_user_id,
    print_user_ids,
)


logs.init_logging()
LOGGER = logs.get_logger('van.print_user_ids')

bot_token = os.environ.get('BOT_API_TOKEN')
print_user_ids(bot_token)

LOGGER.info('BOT ID is {}'.format(find_user_id(bot_token, 'resq')))
