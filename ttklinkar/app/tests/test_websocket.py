import pytest
import json
from channels.testing import WebsocketCommunicator
from ttklinkar.asgi import application
from app.models import Ticker
from decimal import Decimal
from datetime import datetime

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_websocket_last_ticker():
    # Создаём тестовый тикер в базе
    Ticker.objects.create(symbol="BTCUSDT", price=Decimal("50000.00"), trade_time=datetime.now())

    communicator = WebsocketCommunicator(application, "/ws/ticker/")
    connected, _ = await communicator.connect()
    assert connected

    response = await communicator.receive_json_from()
    
    assert response["symbol"] == "BTCUSDT"
    assert response["price"] == "50000.00"

    await communicator.disconnect()
