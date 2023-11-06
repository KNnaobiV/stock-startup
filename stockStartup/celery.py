from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stockStartup.settings")
app = Celery("stockStartup")
app.config_from_object("django.conf")#, namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30.0, update_stock_prices())
    sender.add_periodic_task(30.0, calculate_portfolio_value())


@app.task
def calculate_portfolio_value():
    portfolios = Portfolio.objects.all()
    for portfolio in portfolios:
        stock_holdings = StockHolding.objects.filter(portfolio=portfolio)
        stock_value = sum(stock.quantity * stock.stock.price for stock in stock_holdings)
        portfolio_value = stock_value + portfolio.cash_value
        portfolio.save()


@app.task
def update_stock_prices():
    stocks = Stock.objects.all()
    for stock in stocks:
        price = stock.price
        price += round(random.uniform(0.01, 0.1), 2)
        stock.price = price
        stock.save()


app.conf.beat_schedule = {
    'calculate_portfolio_value': {
        'task': 'tasks.calculate_portfolio_value',
        'schedule': crontab(minute="*/1"),
    },
    'update_stock_prices': {
        'task': 'tasks.update_stock_prices',
        'schedule': crontab(minute="*/1"),
    }
}
app.conf.timezone = 'UTC'