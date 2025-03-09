import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from app.models import Ticker

class TickerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("ticker_updates", self.channel_name)
        await self.accept()

        # Отправляем последнее обновление из БД при подключении
        last_ticker = await self.get_last_ticker()
        if last_ticker:
            await self.send(text_data=json.dumps(last_ticker))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("ticker_updates", self.channel_name)

    async def ticker_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    @sync_to_async
    def get_last_ticker(self):
        ticker = Ticker.objects.order_by("-trade_time").first()
        if ticker:
            return {
                "symbol": ticker.symbol,
                "price": str(ticker.price),
                "trade_time": ticker.trade_time.isoformat(),
            }
        return None
