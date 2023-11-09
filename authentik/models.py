import datetime
import uuid

from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from authentik.validators import *
# Create your models here.

__all__ = [
    "HistoricalStockPrice",
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
    supervisor = models.ForeignKey(
        "self", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="trader_manager"
    )

    def save(self, *args, **kwargs):
        if not self.is_staff:
            if not self.is_manager and not self.supervisor:
                raise ValidationError("Non-managers must have a manager assigned.")
        super().save()

    def __str__(self):
        if self.supervisor:
            if not self.is_manager:
                return f"Trader {self.username}, managed by {self.supervisor.username}."
            return f"Manager {self.username}, managed by {self.supervisor.username}."
        return f"Manager {self.username}."

    def get_absolute_url(self):
        return reverse("authentik:profile", kwargs={username:self.username})


class Stock(models.Model):
    symbol = models.CharField(max_length=6, blank=False, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False, default=0.00)

    def __str__(self):
        return self.symbol

    def get_absolute_url(self):
        return reverse("authentik:stock", kwargs={symbol:self.symbol})


class HistoricalStockPrice(models.Model):
    symbol = models.CharField(max_length=7, blank=False)
    time = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=False)

    def get_absolute_url(self):
        return reverse("authentik:historical_prices", kwargs={"id":self.id})


class Portfolio(models.Model):
    cash_value = models.DecimalField(max_digits=8, decimal_places=2)
    name = models.CharField(max_length=15, unique=True, blank=False)
    pnl = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    stocks = models.ManyToManyField(Stock, through="StockHolding")
    start_cash = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        null=False, 
        blank=False, 
        editable=False, 
        default=100
    )
    trader = models.OneToOneField(DefaultUser, on_delete=models.DO_NOTHING)
    total_value = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}"

    def calaculate_pnl(self):
        return self.total_value - self.start_cash

    def save(self,  *args, **kwargs):
        if not self.pk:
            self.cash_value = self.start_cash
        stock_holdings = StockHolding.objects.filter(portfolio=self)
        total_stock_value = sum(
            stock.quantity * stock.stock.price for stock in stock_holdings
        )
        self.total_value = self.cash_value + total_stock_value
        self.pnl = self.calaculate_pnl()
        super().save()

    def get_absolute_url(self):
        return reverse("authentik:portfolio", kwargs={"name":self.name})


class StockHolding(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(blank=False, default=0)

    def __str__(self):
        return f"{self.quantity} {self.stock}"


class Trade(models.Model):
    ORDER_CHOICES = (("buy", "BUY"), ("sell", "SELL"))
    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.DO_NOTHING)
    order_type = models.CharField(max_length=5, choices=ORDER_CHOICES)
    quantity = models.PositiveIntegerField(blank=False)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"""
            {self.quantity} {self.stock.symbol} {self.order_type.capitalize()}
            by {self.portfolio.name }
        """
    def transaction_size(self):
        if self.order_type == "buy":
            return self.stock.price * self.quantity
        return self.stock.price  * self.quantity

    def save(self, *args, **kwargs):
        if self.order_type == "sell":
            holding = StockHolding.objects.filter(
                portfolio=self.portfolio, 
                stock=self.stock
            )
            if not holding:
                raise ValidationError(f"""
                    You are trying to sell {self.stock.symbol} 
                    and you don't have any.
                """)
            if self.quantity > holding.quantity:
                raise ValidationError(
                    f"""
                    You have {holding.quantity} {self.stock.symbol}. 
                    You are attempting to sell more stock than you have.
                    """
                )

        if (self.order_type == "buy" 
        and self.transaction_size() > self.portfolio.cash_value):
                raise ValidationError(f"""
                    Insufficent funds. 
                    AVAILABLE BALANCE:{self.portfolio.balance}
                """)
        super().save(* args, **kwargs)

    def get_absolute_url(self):
        return reverse("authentik:trade", kwargs={uuid:self.uuid})