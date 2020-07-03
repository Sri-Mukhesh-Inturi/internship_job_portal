# Generated by Django 3.0.6 on 2020-06-25 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Accounts', '0001_initial'),
        ('Jobseeker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('company_logo', models.ImageField(default='../static/images/default_company_logo.png', upload_to='ompany_logos/')),
                ('company_description', models.TextField(blank=True, default='none')),
            ],
        ),
        migrations.CreateModel(
            name='Employer_basic',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Accounts.User_type')),
                ('profile_picture', models.ImageField(default='../static/images/default_profile_picture.png', upload_to='pictures/')),
                ('description', models.TextField(default='none')),
                ('is_owner', models.BooleanField(default=False)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Employer.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Job_location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=30)),
                ('zip_code', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Job_post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_type_name', models.CharField(default='Not Selected', max_length=50)),
                ('job_length', models.CharField(default='Full Time', max_length=20)),
                ('is_company_name_hidden', models.BooleanField(default=False)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('job_title', models.CharField(default='Job Post', max_length=200)),
                ('job_description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_fresher', models.BooleanField(default=True)),
                ('is_work_from_home', models.BooleanField(default=False)),
                ('min_salary', models.IntegerField(default=0)),
                ('max_salary', models.IntegerField(default=0)),
                ('job_location_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Employer.Job_location')),
                ('posted_by_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employer.Employer_basic')),
            ],
        ),
        migrations.CreateModel(
            name='Job_post_skill_set',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employer.Job_post')),
                ('skill_set_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Jobseeker.Skill_set')),
            ],
        ),
        migrations.CreateModel(
            name='Job_post_activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applied_date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(default='pending', max_length=10)),
                ('applied_by_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Jobseeker.Jobseeker_basic')),
                ('job_post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employer.Job_post')),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('announcement_text', models.TextField()),
                ('last_updated', models.DateField(auto_now=True)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employer.Company')),
                ('posted_by_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employer.Employer_basic')),
            ],
        ),
    ]
