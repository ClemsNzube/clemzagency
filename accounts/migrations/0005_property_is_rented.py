# Generated by Django 5.1.5 on 2025-01-27 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customuser_eth_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='is_rented',
            field=models.BooleanField(default=False),
        ),
    ]
