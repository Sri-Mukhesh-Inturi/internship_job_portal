# Generated by Django 3.0.6 on 2020-06-18 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Jobseeker', '0003_auto_20200616_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseeker_education',
            name='degree_type',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='jobseeker_education',
            name='degree_name',
            field=models.CharField(default='', max_length=70),
        ),
    ]
