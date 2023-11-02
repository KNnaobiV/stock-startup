from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction

from authentik.models import StockHolding, Trade
from authentik.email import send_email_on_account_number_generation


def update_stock_holding(portfolio, stock, quantity_change):
    stock_holding, created = portfolio.stockholding_set.get_or_create(stock=stock)
    stock_holding.quantity += quantity_change
    if stock_holding.quantity <= 0:
        stock_holding.delete()
    stock_holding.save()


@receiver(post_save, sender=Trade)
def update_portfolio_on_trade(sender, instance, **kwargs):
    """Changes the balance if there is a sell order."""
    portfolio = instance.portfolio
    if instance.order_type == 'sell':
        transaction_size, quantity = instance.transaction_size(), -(instance.quantity)
    elif instance.order_type == 'buy':
        transaction_size, quantity = -(instance.transaction_size()), instance.quantity
    portfolio.cash_value += instance.quantity
    update_stock_holding(portfolio, instance.stock, instance.quantity)
    portfolio.save()

