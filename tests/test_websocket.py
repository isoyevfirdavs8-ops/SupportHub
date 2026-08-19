import pytest

from channels.testing import WebsocketCommunicator

from config.asgi import application

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_unauthenticated_websocket_is_rejected():
    communicator = WebsocketCommunicator(
        application,
        "/ws/tickets/1/",
    )

    connected, _ = await communicator.connect()

    assert connected is False

    await communicator.disconnect()