from datetime import datetime
from django.core.management.base import BaseCommand

from authentik.models import HistoricalStockPrices, Stock

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        now = datetime.now()
        stocks = Stock.objects.all()
        for stock in stocks:
            HistoricalStockPrices.objects.create(
                symbol=stock.symbol,
                price=stock.price,
                time=now
            )
