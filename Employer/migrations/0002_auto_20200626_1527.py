# Generated by Django 3.0.6 on 2020-06-26 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Employer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer_basic',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Employer.Company'),
        ),
    ]
