from enum import Enum
from typing import (
    NamedTuple,
)

from slack import WebClient

from van.logs import get_logger


class Distribution(Enum):
    BROADCAST = 1
    DIRECT = 2


class Response(NamedTuple):
    message: str
    distribution: Distribution

    @classmethod
    def broadcast_response(cls, message: str) -> 'Response':
        return Response(message, Distribution.BROADCAST)


LOGGER = get_logger('van.responses')


class Responder:
    """
    Responder of responses.
    """
    def __init__(self, channel: str, web_client: WebClient) -> None:
        if not channel and not web_client:
            raise ValueError('Need channel and web_client')
        self.web_client = web_client
        self.channel = channel

    def _broadcast(self, message: str):
        """
        Broadcast a message to everyone
        """
        self.web_client.chat_postMessage(
            channel=self.channel,
            text=message,
            # thread_ts=data['ts']
        )

    def respond(self, response: Response) -> None:
        """
        Send out the response
        """
        if response:
            if response.distribution.value == Distribution.BROADCAST.value:
                self._broadcast(response.message)
            else:
                LOGGER.warning(f'No implementation for distribution {response.distribution} yet.')
