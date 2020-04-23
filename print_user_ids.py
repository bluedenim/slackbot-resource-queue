import os

from van import logs
from van.utils.ids import (
    print_user_ids,
)


logs.init_logging()
LOGGER = logs.get_logger('van.print_user_ids')

bot_token = os.environ.get('BOT_API_TOKEN')
print_user_ids(bot_token)
