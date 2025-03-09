from django.urls import path
from .views import TickerListAPIView, HomePageView
from . import consumers

urlpatterns = [
    path('api/tickers/', TickerListAPIView.as_view(), name='ticker-list'),
    #path("ws/ticker/", consumers.TickerConsumer.as_asgi()),
    path('', HomePageView.as_view(), name='home'),
]
