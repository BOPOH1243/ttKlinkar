from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/ticker/", consumers.TickerConsumer.as_asgi()),
]
