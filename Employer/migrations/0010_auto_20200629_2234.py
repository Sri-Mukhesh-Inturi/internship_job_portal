# Generated by Django 3.0.6 on 2020-06-29 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employer', '0009_auto_20200629_2037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job_post',
            name='job_location_id',
        ),
        migrations.AddField(
            model_name='job_post',
            name='city',
            field=models.CharField(default='Not Selected', max_length=30),
        ),
        migrations.DeleteModel(
            name='Job_location',
        ),
    ]
