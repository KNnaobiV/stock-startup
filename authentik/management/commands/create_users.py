from datetime import datetime, timedelta
import random
import string

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from faker import Faker
from faker.providers.person.en import Provider

from authentik.models import Trade, Portfolio, Stock, StockHolding

fake = Faker()
User = get_user_model()

class Command(BaseCommand):
    help = "Generates and saves dummy data to the db."

    def handle(self, *args, **kwargs):
        manager, created = User.objects.get_or_create(
            username="johndoe",
            email = fake.email(),
            is_manager = True,
        )
        manager.set_password("Fake_pwd")
        manager.save()

        traders = []
        # Create traders
        for _ in range(10):
            username = fake.unique.user_name()
            email = fake.email()
            password = "fake_pwd"
            trader, created = User.objects.get_or_create(
                username=username,
                email=email,
                supervisor=manager
            )
            trader.set_password(password)
            trader.save()