# Generated by Django 3.0.6 on 2020-07-01 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employer', '0010_auto_20200629_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_post',
            name='max_salary',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='job_post',
            name='min_salary',
            field=models.IntegerField(),
        ),
    ]