# Generated by Django 3.1.2 on 2020-11-29 11:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store_App', '0003_auto_20201129_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='genrated_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 29, 16, 16, 15, 218308)),
        ),
    ]
