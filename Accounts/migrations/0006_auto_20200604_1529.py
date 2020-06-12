# Generated by Django 3.0.6 on 2020-06-04 09:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0005_auto_20200604_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_type',
            name='phone_number',
            field=models.IntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(9999999999), django.core.validators.MinValueValidator(1000000000)]),
        ),
    ]
