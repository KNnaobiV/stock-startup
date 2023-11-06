from random import uniform

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from authentik.models import Stock

class Command(BaseCommand):

    def handle(self):
        stocks = Stock.objects.all()
        for stock in stocks:
            stock.price += round(uniform(-0.2, 0.2), 2)
            stock.save()
