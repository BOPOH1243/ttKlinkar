import pytest
import json
from channels.testing import WebsocketCommunicator
from ttklinkar.asgi import application
from app.models import Ticker
from decimal import Decimal
from datetime import datetime

from asgiref.sync import sync_to_async

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_websocket_last_ticker():
    # Создаём тестовый тикер в базе с использованием sync_to_async
    await sync_to_async(Ticker.objects.create)(symbol="BTCUSDT", price=Decimal("50000.00"), trade_time=datetime.now())

    # Проверка, что тикер был успешно создан
    last_ticker = await sync_to_async(Ticker.objects.last)()
    assert last_ticker is not None
    assert last_ticker.symbol == "BTCUSDT"
    assert last_ticker.price == Decimal("50000.00")
