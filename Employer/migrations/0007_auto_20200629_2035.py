# Generated by Django 3.0.6 on 2020-06-29 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employer', '0006_auto_20200629_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_post',
            name='job_title',
            field=models.CharField(max_length=200),
        ),
    ]
