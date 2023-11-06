# Generated by Django 4.2.7 on 2023-11-06 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentik', '0002_alter_trade_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='total_value',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
    ]
