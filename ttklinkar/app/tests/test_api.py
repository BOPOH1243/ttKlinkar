import pytest
from django.urls import reverse
from app.models import Ticker
from decimal import Decimal
from datetime import datetime

@pytest.mark.django_db
def test_get_ticker_list(client):
    Ticker.objects.create(symbol="BTCUSDT", price=Decimal("50000.00"), trade_time=datetime.now())

    url = reverse("ticker-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["symbol"] == "BTCUSDT"
