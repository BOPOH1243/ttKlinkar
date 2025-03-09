from rest_framework import generics
from .models import Ticker
from .serializers import TickerSerializer
from django.views.generic import TemplateView

class TickerListAPIView(generics.ListAPIView):
    queryset = Ticker.objects.all().order_by("-trade_time")
    serializer_class = TickerSerializer

class HomePageView(TemplateView):
    template_name = "app/index.html"