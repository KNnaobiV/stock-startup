from contextlib import suppress
import random

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from authentik.models import Portfolio, Stock, Trade

User = get_user_model()

class Command(BaseCommand):
    help = "Generates dummy trades which it adds to the db."

    def handle(self, *args, **kwargs):
        with suppress(ValidationError):
            traders = User.objects.filter(is_manager=False, is_staff=False)
            stock_objects = Stock.objects.all()

            for trader in traders:
                portfolio, created = Portfolio.objects.get_or_create(
                    trader=trader, name=f"{trader.username.title()}'s Portfolio_1",
                )
                portfolio.cash_value = 100.00
                portfolio.start_cash = 100.00
                portfolio.save()

                order_types = ['buy', 'sell']
                for _ in range(100):
                    stock = random.choice(stock_objects)
                    print(f"Selected stock: {stock}")
                    trade = Trade.objects.create(
                        stock=stock,
                        portfolio=portfolio,
                        order_type=random.choice(order_types),
                        quantity=random.randint(1, 15)
                    )
                    trade.save()