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
        manager = User.objects.create(
            username="johndoe",
            email=fake.email(),
            is_manager=True)
        )
        manager.set_password("Fake_pwd")
        manager.save()

        traders = []
        # Create traders
        for _ in range(10):
            usernames = list(set(Provider.first_names))
            random.seed(4321)
            shuffle(usernames)
            username = fake.unique.user_name()
            email = fake.email()
            password = "fake_pwd"
            trader = User.objects.create_user(
                username=username,
                email=email,
                manager=manager
            )
            trader.set_password(password)
            traders.append(trader)

        
        for trader in traders:
            portfolio, created = Portfolio.objects.get_or_create(
                trader=trader, name=f"{trader.username.title()}'s Portfolio_1",
            )
            portfolio.cash_value = 100.00
            portfolio.start_cash = 100.00
            portfolio.save()










        for _ in range(120):
            username = fake.unique.user_name()
            email = fake.email()
            password = "fake_pwd"
            user = DefaultUser.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.groups.add(borrowers)

        users = User.objects.all()

        # create bank account
        owner = random.choice(users)
        account_number = generate_ten_digit_number(1123)
        balance = random.uniform(0, 100000)
        bvn = generate_ten_digit_number(2233)
        is_activated = random.choice([True, False])
        Bank.account.objects.create(
            owner=owner,
            account_number=account_number,
            balance=balance,
            bvn=bvn,
            is_activated=is_activated
        )

        random_lender = random.choice(User.objects.filter(
            groups=lenders, is_activated=True, bankaccount__is_activated=True
        ))
        random_borrower = random.choice(User.objects.filter(
            groups=borrowers, is_activated=True, bankaccount__is_activated=True
        ))

        for _ in range(10000):
            random_user = random.choice(users)
            is_lender = lenders in random_user.groups.all()
            is_borrower = borrower in random_user.groups.all()

            if is_borrower:
                requester = random_borrower
                amount = random.uniform(100, 10000)
                requested_date = fake.date_between(start_date="-30d", end_date="today")
                is_approved = random.choice([True, False])
                LoanRequest.objects.create(
                    requester=requester,
                    amount=amount,
                    requested_date=requested_date,
                    is_approved=is_approved
                )

            if is_lender:
                lender = random_lender
                borrower = random.choice(random_borrower)
                amount = random.uniform(100, 10000)
                loan_date = fake.date_between(start_date="-30d", end_date="today")
                is_repaid = random.choice([True, False])
                Loan.objects.create(
                    lender=lender,
                    borrower=borrower,
                    amount=amount,
                    loan_date=loan_date,
                    is_repaid=is_repaid
                )

                Transaction.objects.create(
                    amount=amount,
                    description=f"Loan to {borrower.username}",
                    date=loan_date,
                    category="loan",
                    sender=lender.username,
                    receiver=borrower.username
                )
            
            if is_borrower and Loan.objects.filter(borrower=random_borrower, is_repaid=True).exists():
                loan = Loan.objects.filter(borrower=random_borrower, is_repaid=True).first()
                amount = random.uniform(10, loan.amount)
                repaid = fake.date_between(start_date=loan.date, end_date="today")
                LoanRepayment.objects.create(
                    loan=loan,
                    repaid=repaid,
                    amount=amount
                )

        # create transactions
        amount = random.uniform(1, 100)
        description = fake.text(max_nb_chars=20)
        date = fake.date_between(start_date="-30d", end_date="today")
        category = rnadom.choice(
            ["clothing", "food", "health care", 
            "hobbies", "housing", "subsciption", 
            "transportation", "utilities", "other"
        ])
        notes = fake.text(max_nb_char=30)
        sender = random.choice(list(BankAccount.objects.all()))
        receiver = random.choice(list(BankAccount.objects.all()))
        if sender is receiver:
            while sender is receiver:
                receiver = random.choice(list(BankAccount.objects.all()))
        Transaction.objects.create(
            amount=amount,
            description=description,
            date=date,
            category=category,
            notes=notes,
            sender=bank_account,
            receiver=bank_account
        )
