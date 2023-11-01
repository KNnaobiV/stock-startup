import uuid

from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from authentik.validators import *
# Create your models here.

__all__ = [
    "Portfolio",
    "Stock",
    "StockHolding",
    "Trade",
]


class DefaultUser(AbstractUser):
    phone = models.PositiveIntegerField(
        null=True, blank=True, validators=[validate_phone_number] 
    )
    is_manager = models.BooleanField(default=False)
    manager = models.ForeignKey(
        "self", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="trader_manager"
    )

    def save(self):
        if not self.is_manager and not self.manager:
            raise ValidationError("Non-managers must have a manager assigned.")
        super().save()

    def __str__(self):
        if manager:
            if not is_manager:
                return f"Trader {self.username}, managed by {self.manager.username}."
            return f"Manager {self.username}, managed by {self.manager.username}."
        return f"Manager {self.username}."

    def get_absolute_url(self):
        return reverse("authentik:user", kwargs={username:self.username, pk:self.pk})

class Stock(models.Model):
    symbol = models.CharField(max_length=6, blank=False, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False)

    def get_absolute_url(self):
        return reverse("authentik:stock", kwargs={symbol:self.symbol})


class Portfolio(models.Model):
    name = models.CharField(max_length=15, unique=True, blank=False)
    trader = models.OneToOneField(DefaultUser, on_delete=models.DO_NOTHING)
    cash_value = models.DecimalField(max_digits=8, decimal_places=2)
    stocks = models.ManyToManyField(Stock, through="StockHolding")
    start_cash = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        null=False, 
        blank=False, 
        editable=False, 
        default=0
    )

    def pnl(self):
        return self.start_cash - self.initial_balance

    def get_all_stocks(self):
        total_stocks = dict()
        stock_holding = self.stockholding_set.all()

        for stock in stock_holding:
            symbol = stock.symbol
            quantity =stock.quantity
            if symbol in total_stock:
                total_stocks[symbol] += quantity
            else:
                total_stocks[symbol] -= quantity
        return total_stocks

    def save(self):
        if not self.pk:
            self.cash_value = self.start_cash
        super().save()

    def get_absolute_url(self):
        return reverse("authentik:portfolio", kwargs={name:self.name})


class StockHolding(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.DO_NOTHING)
    #quantity = models.PositiveIntegerField(blank=False, default=0)


class Trade(models.Model):
    ORDER_CHOICES = (("buy", "BUY"), ("sell", "SELL"))
    stock = models.OneToOneField(Stock, on_delete=models.DO_NOTHING)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.DO_NOTHING)
    order_type = models.CharField(max_length=5, choices=ORDER_CHOICES)
    quantity = models.PositiveIntegerField(blank=False)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    time = models.DateTimeField(auto_now_add=True)

    def transaction_size(self):
        if self.order_type == "buy":
            return self.stock.price * quantity
        return self.stock.price  * quantity

    def save(self):
        if self.order_type == "sell":
            if self.quantity > total_stock:
                raise ValidationError(
                    f"""
                    You have {total_stock} {symbol}. You are attempting to sell 
                    more stock than you have.
                    """
                )

        if (self.order_type == "buy" 
        and self.transaction_size > self.portfolio.cash_value):
                raise ValidationError(f"""
                    Insufficent funds. 
                    AVAILABLE BALANCE:{self.trader.portfolio.balance}
                """)

    def clean(self):
        if self.order_type == "sell":
            if not self.sell_price:
                raise ValidationError("Sell orders should have sell price.")
            if self.buy_price:
                raise ValidationError("Sell orders should not have buy price.")

        if self.order_type == "buy":
            if not self.buy_price:
                raise ValidationError("Buy orders should have buy price.")
            if self.sell_price:
                raise ValidationError("Buy orders should not have sell price.")

    def get_absolute_url(self):
        return reverse("authentik:trade", kwargs={uuid:self.uuid})