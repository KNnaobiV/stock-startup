from datetime import datetime, timedelta
import random
import string

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from faker import Faker
from faker.providers.person.en import Provider

from authentik.models import Trade, Portfolio, Stock, StockHolding

fake = Faker()
User = get_user_model()

class Command(BaseCommand):
    help = "Generates and saves dummy data to the db."

    def handle(self, *args, **kwargs):
        traders = User.objects.filter(is_manager=False, is_staff=False)
        symbols = ["AAPL", "GOOG", "AMD", "MSFT", "JPM", "IBM", ]
        stocks = Stock.objects.all()
        for trader in traders:
            portfolio, created = Portfolio.objects.get_or_create(
                trader=trader, name=f"{trader.username.title()}'s Portfolio_1",
            )
            portfolio.cash_value = 100.00
            portfolio.start_cash = 100.00
            portfolio.save()

            trade_range = random.randrange(10, 11)
            order_types = ['buy', 'sell']
        for _ in range(trade_range):
            trade = Trade.objects.create(
                stock=random.choice(stocks),
                portfolio=portfolio,
                order_type=random.choice(order_types),
                quantity=random.randint(1, 15)
            )
            trade.save()