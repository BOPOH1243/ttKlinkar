import pytest
import websockets
import asyncio
import json
from decimal import Decimal
from datetime import datetime
from django.utils import timezone
from asgiref.sync import sync_to_async
from app.models import Ticker
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_binance_ws_mock():
    mock_data = json.dumps({
        "s": "BTCUSDT",
        "p": "50000.00",
        "T": int(timezone.now().timestamp() * 1000)
    })

    async def mock_recv():
        return mock_data  # Убрали sleep, если тесты проходят нормально

    mock_ws = AsyncMock()
    mock_ws.recv = mock_recv  # Мокаем метод recv

    # Мокаем асинхронный контекстный менеджер
    mock_connect = AsyncMock()
    mock_connect.__aenter__.return_value = mock_ws

    with patch("websockets.connect", return_value=mock_connect):
        from app.management.commands.binance_ws import Command
        command = Command()

        # Запускаем асинхронно с таймаутом
        try:
            await asyncio.wait_for(command.listen(), timeout=0.5)
        except asyncio.TimeoutError:
            pass  # Нормально, если поток был остановлен принудительно

    # Проверяем, записался ли тикер
    last_ticker = await sync_to_async(Ticker.objects.last, thread_sensitive=True)()
    assert last_ticker is not None
    assert last_ticker.symbol == "BTCUSDT"
    assert last_ticker.price == Decimal("50000.00")
