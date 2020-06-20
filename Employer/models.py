from django.db import models
from django.contrib.auth.models import User
from Accounts.models import User_type
from Jobseeker.models import Skill_set,Jobseeker_basic
# Create your models here.
class Company(models.Model):
    company_name = models.CharField(max_length=50)
    company_logo = models.ImageField(upload_to='company_logos',default='../static/images/default_company_logo.png')
    company_description = models.TextField()
    def __str__(self):
        return self.company_name


class Employer_basic(models.Model):
    user = models.OneToOneField(User_type, on_delete=models.CASCADE, primary_key=True)
    company = models.ForeignKey(Company,on_delete=models.PROTECT,blank=True)
    profile_picture = models.ImageField(upload_to='pictures/', default='../static/images/default_profile_picture.png')
    description = models.TextField(blank=True)
    def __str__(self):
        return self.user.user.username
class Job_type(models.Model):
    job_type_name = models.CharField(max_length=50)

class Job_location(models.Model):
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.IntegerField()
    def __str__(self):
        return self.city
class Job_post(models.Model):
    posted_by_id = models.ForeignKey(Employer_basic,on_delete=models.CASCADE)
    job_type_name = models.CharField(max_length=50,default="Not Selected")
    is_company_name_hidden = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    job_title = models.CharField(max_length=200,default="Job Post")
    job_description = models.TextField()
    job_location_id = models.ForeignKey(Job_location,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_fresher = models.BooleanField(default=True)
    is_work_from_home = models.BooleanField(default=False)
    min_salary = models.IntegerField(default=0)
    max_salary = models.IntegerField(default=0)

class Job_post_skill_set(models.Model):
    skill_set_id = models.ForeignKey(Skill_set,on_delete=models.CASCADE)
    job_post_id = models.ForeignKey(Job_post,on_delete=models.CASCADE)

class Job_post_activity(models.Model):
    job_post_id = models.ForeignKey(Job_post,on_delete=models.CASCADE)
    applied_by_id = models.ForeignKey(Jobseeker_basic,on_delete=models.CASCADE)
    applied_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10,default='pending')

class Announcement(models.Model):
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    posted_by_id = models.ForeignKey(Employer_basic,on_delete=models.CASCADE)
    announcement_text = models.TextField()
    last_updated = models.DateField(auto_now=True)