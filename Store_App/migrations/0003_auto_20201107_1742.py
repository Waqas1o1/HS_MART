# Generated by Django 3.1.2 on 2020-11-07 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store_App', '0002_bill_khaata_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='khaata',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
