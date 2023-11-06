from contextlib import suppress
import random

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from authentik.models import Stock

class Command(BaseCommand):
    help = "Generates dummy stocks and trades which it adds to the db."

    def handle(self, *args, **kwargs):
        with suppress(IntegrityError, ValidationError):
            traders = User.objects.filter(is_manager=False, is_staff=False)
            stock_symbols = ["AAPL", "GOOG", "AMD", "MSFT", "JPM", "IBM"]
            for symbol in stock_symbols:
                stock, created = Stock.objects.get_or_create(
                    symbol=symbol,
                    price=round(random.uniform(0.5, 1.2), 2)
                )