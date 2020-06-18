from django.db import models
from django.contrib.auth.models import User
from Accounts.models import User_type


# Create your models here.
# 1) for jobseeker basic information

class Jobseeker_basic(models.Model):
    user = models.OneToOneField(User_type,on_delete=models.CASCADE,primary_key=True)
    profile_picture = models.ImageField(upload_to='pictures/',default='../static/images/default_profile_picture.png')
    salary_expectation = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    highest_education = models.CharField(max_length=50,default='none')
    resume = models.FileField(upload_to='resumes/',blank=True)
    job_type_name = models.CharField(max_length=50,default='none')

class Jobseeker_education(models.Model):
    user = models.ForeignKey(Jobseeker_basic,on_delete=models.CASCADE)
    degree_type = models.CharField(max_length=40,default="")
    degree_name = models.CharField(max_length=70,default="")
    institute = models.CharField(max_length=70)
    start_date = models.DateField()
    end_date = models.DateField()
    cgpa = models.FloatField()
class Jobseeker_experience(models.Model):
    user = models.ForeignKey(Jobseeker_basic,on_delete=models.CASCADE)
    job_title = models.CharField(max_length=60)
    company_name = models.CharField(max_length=60)
    job_location_city = models.CharField(max_length=30)
    job_description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

class Skill_set(models.Model):
    skill_set_name = models.CharField(max_length=30)

class Jobseeker_skill_set(models.Model):
    user = models.ForeignKey(Jobseeker_basic,on_delete=models.CASCADE)
    skill_set_id = models.ForeignKey(Skill_set,on_delete=models.CASCADE)
    skill_level = models.IntegerField()