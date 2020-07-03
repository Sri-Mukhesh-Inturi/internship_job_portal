from django.db import models
from django.contrib.auth.models import User
from Accounts.models import User_type
from Jobseeker.models import Skill_set,Jobseeker_basic
# Create your models here.

class Company(models.Model):
    company_name = models.CharField(primary_key=True,max_length=50)
    company_logo = models.ImageField(upload_to='ompany_logos/',default='../static/images/default_company_logo.png')
    company_description = models.TextField(blank=True,default="none")
    def __str__(self):
        return self.company_name



class Employer_basic(models.Model):
    user = models.OneToOneField(User_type, on_delete=models.CASCADE, primary_key=True)
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True,blank=True)
    profile_picture = models.ImageField(upload_to='pictures/', default='../static/images/default_profile_picture.png')
    description = models.TextField(default="none")
    is_owner = models.BooleanField(default=False)
    def __str__(self):
        return self.user.user.username


class Job_post(models.Model):
    posted_by_id = models.ForeignKey(Employer_basic,on_delete=models.CASCADE)
    job_type_name = models.CharField(max_length=50,default="Not Selected")
    job_length = models.CharField(max_length=20, default="Full Time")
    is_company_name_hidden = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    job_title = models.CharField(max_length=200)
    job_description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_work_from_home = models.BooleanField(default=False)
    min_salary = models.IntegerField()
    max_salary = models.IntegerField()
    min_experience = models.IntegerField(default=0)
    city = models.CharField(max_length=30,default="Not Selected")

    def __str__(self):
        return self.job_title



class Job_post_skill_set(models.Model):
    skill_set_id = models.ForeignKey(Skill_set,on_delete=models.CASCADE)
    job_post_id = models.ForeignKey(Job_post,on_delete=models.CASCADE)
    def __str__(self):
        return self.skill_set_id.skill_set_name+'-'+self.job_post_id.job_title



class Job_post_activity(models.Model):
    job_post_id = models.ForeignKey(Job_post,on_delete=models.CASCADE)
    applied_by_id = models.ForeignKey(Jobseeker_basic,on_delete=models.CASCADE)
    applied_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10,default='pending')
    def __str__(self):
        return self.job_post_id+self.status



class Announcement(models.Model):
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    posted_by_id = models.ForeignKey(Employer_basic,on_delete=models.CASCADE)
    announcement_text = models.TextField()
    last_updated = models.DateField(auto_now=True)