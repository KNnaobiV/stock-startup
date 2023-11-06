from datetime import datetime, timedelta
import random
import os
import sys
from celery import Celery, shared_task
import django
from django.conf import settings
import requests
sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stockStartup.settings")
django.setup()

app = Celery("stockStartup")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

sys.path.append("..")
from authentik.models import Stock, Portfolio

__all__ = [
    "calculate_portfolio_value",
    "update_stock_prices",
]

@shared_task
def calculate_portfolio_value():
    portfolios = Portfolio.objects.all()
    for portfolio in portfolios:
        stock_holdings = StockHolding.objects.filter(portfolio=portfolio)
        stock_value = sum(stock.quantity * stock.stock.price for stock in stock_holdings)
        portfolio_value = stock_value + portfolio.cash_value
        portfolio.pnl = calculate_portfolio_pnl(portfolio, portfolio_value)
        portfolio.save()


@shared_task
def update_stock_prices():
    stocks = Stock.objects.all()
    for stock in stocks:
        price = stock.price
        price += round(random.uniform(0.01, 0.1), 2)
        stock.price = price
        stock.save()