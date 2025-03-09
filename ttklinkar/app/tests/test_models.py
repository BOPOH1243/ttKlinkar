from django.utils import timezone
import pytest
from app.models import Ticker
from decimal import Decimal

@pytest.mark.django_db
def test_ticker_creation():
    #Ticker.objects.all().delete()  # Очистка таблицы перед тестом
    prev_count = Ticker.objects.count()
    ticker = Ticker.objects.create(
        symbol="BTCUSDT",
        price=Decimal("50000.00"),
        trade_time=timezone.now()
    )

    assert Ticker.objects.count() > prev_count
