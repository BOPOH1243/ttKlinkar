import asyncio
import json
import websockets
from django.core.management.base import BaseCommand
from app.models import Ticker
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
from datetime import datetime
from decimal import Decimal

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"

class Command(BaseCommand):
    help = "Подключается к Binance WebSocket API и сохраняет данные"

    def handle(self, *args, **options):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.listen())

    async def listen(self):
        channel_layer = get_channel_layer()
        async with websockets.connect(BINANCE_WS_URL) as websocket:
            while True:
                try:
                    data = await websocket.recv()
                    data_json = json.loads(data)
                    
                    symbol = data_json.get("s")
                    price = Decimal(data_json.get("p"))
                    trade_time = datetime.fromtimestamp(data_json.get("T") / 1000.0)
                    
                    # Обёртываем синхронный вызов в sync_to_async
                    await sync_to_async(Ticker.objects.create)(
                        symbol=symbol, 
                        price=price, 
                        trade_time=trade_time
                    )

                    update_data = {
                        "symbol": symbol,
                        "price": str(price),
                        "trade_time": trade_time.isoformat()
                    }
                    await channel_layer.group_send("ticker_updates", {
                        "type": "ticker_update",
                        "data": update_data
                    })
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error: {e}"))
                    await asyncio.sleep(1)
