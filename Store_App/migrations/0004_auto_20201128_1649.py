# Generated by Django 3.1.2 on 2020-11-28 11:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store_App', '0003_auto_20201128_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='cash_deposit',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='cash_return',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='genrated_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 28, 16, 49, 44, 567457)),
        ),
    ]
