import mock

from van.responses import (
    Distribution,
    Responder,
    Response,
)


@mock.patch.object(Responder, '_broadcast')
def test_broadcast_response(mocked_broadcast):
    response = Response('hello', Distribution.BROADCAST)
    responder = Responder('channel', mock.MagicMock)
    responder.respond(response)

    mocked_broadcast.assert_called_once_with('hello')


@mock.patch.object(Responder, '_broadcast')
def test_direct_response(mocked_broadcast):
    response = Response('hello', Distribution.DIRECT)
    responder = Responder('channel', mock.MagicMock)
    responder.respond(response)

    mocked_broadcast.assert_not_called()
