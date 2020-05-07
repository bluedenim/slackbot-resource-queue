import os
from typing import Callable

from slack import WebClient
from slack.rtm.client import RTMClient

from responses import Responder
from van import logs
from van.logs import get_logger
from van.res_reservation import ResourceReservationProcessor
from van.userstore import UserStore


logs.init_logging()
LOGGER = get_logger(name='van.slackbot')


def message_processor(bot_id: str, user_store: UserStore, processor: ResourceReservationProcessor) -> Callable:
    """
    A thunk to return a message processor callback to handle message events from Slack.

    :return: a callback that can be passed to RTMClient.on()
    """
    at_bot = '<@{}>'.format(bot_id)

    def callback(**payload):
        LOGGER.debug('Got message: {}'.format(payload))

        data = payload['data']
        text = data.get('text')
        if text:
            tokens = text.strip().split()
            if tokens[0] == at_bot:
                context = {
                    'channel': data['channel'],
                    'thread_ts': data['ts'],
                    'user_id': data['user'],
                    'rtm_client': payload['rtm_client'],
                    'web_client': payload['web_client'],
                }

                responder = Responder(data['channel'], payload['web_client'])
                for response in processor.process_message_text(tokens[1:], context):
                    responder.respond(response)

    return callback


if '__main__' == __name__:
    bot_token = os.environ.get('BOT_API_TOKEN')
    bot_id = os.environ.get('BOT_ID')
    if bot_token and bot_id:
        rtm_client = RTMClient(token=bot_token, auto_reconnect=True)
        user_store = UserStore(WebClient(token=bot_token))
        processor = ResourceReservationProcessor(user_store=user_store)

        RTMClient.on(event='message', callback=message_processor(bot_id, user_store, processor))
        rtm_client.start()
    else:
        LOGGER.error('Set environment variables BOT_API_TOKEN and BOT_ID and try again.')
