from django.contrib import admin
from .models import Jobseeker_basic,Jobseeker_education,Jobseeker_experience,Jobseeker_skill_set,Skill_set
# Register your models here.
admin.site.register(Jobseeker_basic)
admin.site.register(Jobseeker_education)
admin.site.register(Jobseeker_experience)
admin.site.register(Jobseeker_skill_set)
admin.site.register(Skill_set)