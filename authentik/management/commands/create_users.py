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
        manager, created = User.objects.get_or_create(
            username="johndoe",
            email = fake.email(),
            is_manager = True,
        )
        manager.set_password("Fake_pwd")
        manager.save()

        traders = []
        # Create traders
        for _ in range(10):
            username = fake.unique.user_name()
            email = fake.email()
            password = "fake_pwd"
            trader, created = User.objects.get_or_create(
                username=username,
                email=email,
                supervisor=manager
            )
            trader.set_password(password)
            trader.save()
            traders.append(trader)

        symbols = ["AAPL", "GOOG", "AMD", "MSFT", "JPM", "IBM", ]
        stocks = list()
        for symbol in symbols:
            stock, create = Stock.objects.get_or_create(
                symbol=symbol,
                price = round(random.uniform(0.5, 1.2), 2)
            )
            stock.save()
            stocks.append(stock)

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