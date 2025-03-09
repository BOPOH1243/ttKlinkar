import pytest
from app.models import Ticker
from decimal import Decimal
from datetime import datetime

@pytest.mark.django_db
def test_ticker_creation():
    ticker = Ticker.objects.create(
        symbol="BTCUSDT",
        price=Decimal("50000.00"),
        trade_time=datetime.now()
    )
    
    assert Ticker.objects.count() == 1
    assert ticker.symbol == "BTCUSDT"
    assert ticker.price == Decimal("50000.00")
