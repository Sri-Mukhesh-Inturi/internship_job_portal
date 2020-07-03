# Generated by Django 3.0.6 on 2020-06-29 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employer', '0004_auto_20200629_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_location',
            name='state',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='job_location',
            name='street_address',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='job_location',
            name='zip_code',
            field=models.IntegerField(blank=True),
        ),
    ]
