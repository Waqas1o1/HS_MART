# Generated by Django 3.1.2 on 2020-11-25 10:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store_App', '0013_auto_20201125_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='genrated_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 25, 15, 52, 52, 439966)),
        ),
    ]
