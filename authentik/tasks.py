from datetime import datetime, timedelta

from celery import task
from authentik.models import *


def calculate_portfolio_pnl(portfolio, value):
    return portfolio.pnl - value


@task
def calculate_portfolio_value():
    portfolios = Portfolio.objects.all()
    for portfolio in portfolios:
        stocks = portfolio.stock_set.all()
        stock_value = sum([stock.price * stock.value for stock in stocks])
        portfolio_value = stock_value + portfolio.cash_value
        portfolio.pnl = calculate_portfolio_pnl(portfolio, portfolio_value)
        portfolio.save()