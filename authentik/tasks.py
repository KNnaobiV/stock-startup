from datetime import datetime, timedelta

from celery import task
from authentik.models import *


def calculate_portfolio_pnl(portfolio, value):
    return portfolio.pnl - value


@task
def calculate_portfolio_value():
    portfolios = Portfolio.objects.all()
    for portfolio in portfolios:
        stock_holdings = StockHolding.objects.filter(portfolio=portfolio)
        stock_value = sum(stock.quantity * stock.stock.price for stock in stock_holdings)
        portfolio_value = stock_value + portfolio.cash_value
        portfolio.pnl = calculate_portfolio_pnl(portfolio, portfolio_value)
        portfolio.save()