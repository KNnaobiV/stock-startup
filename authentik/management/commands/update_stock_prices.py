from decimal import Decimal
from random import uniform

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from authentik.models import Stock, Portfolio

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        stocks, portfolios = Stock.objects.all(), Portfolio.objects.all()
        for stock in stocks:
            price = round(float(stock.price), 2)
            price += round(uniform(-0.2, 0.2), 2)
            if price < 0.19 or price > 3.90:
                continue
            stock.price = price
            stock.save()
        [portfolio.save() for portfolio in portfolios]
