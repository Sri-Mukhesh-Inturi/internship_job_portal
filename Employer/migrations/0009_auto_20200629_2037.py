# Generated by Django 3.0.6 on 2020-06-29 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Employer', '0008_auto_20200629_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_post',
            name='job_location_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Employer.Job_location'),
        ),
    ]
