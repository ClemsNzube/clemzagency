# Generated by Django 5.1.5 on 2025-01-27 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_propertyimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='eth_address',
            field=models.CharField(blank=True, max_length=42, null=True),
        ),
    ]
