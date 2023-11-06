from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from authentik.models import StockHolding, Portfolio


class Command(BaseCommand):
    def handle(self):
        portfolios = Portfolio.objects.all()
        for portfolio in portfolios:
            holdings = StockHolding.objects.filter(portfolio__id=portfolio.id)
            stock_value = sum(
                [holding.stock.price * holding.quantity for holding in holdings]
            )
            portfolio.total_value = portfolio.cash_value + stock_value
            portfolio.save()