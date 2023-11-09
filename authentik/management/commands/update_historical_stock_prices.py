from datetime import datetime
from django.core.management.base import BaseCommand

from authentik.models import HistoricalStockPrice, Stock

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        now = datetime.now()
        stocks = Stock.objects.all()
        for stock in stocks:
            HistoricalStockPrice.objects.create(
                symbol=stock.symbol,
                price=stock.price,
                time=now
            )
