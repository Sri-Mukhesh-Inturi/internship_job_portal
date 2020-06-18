from django.contrib import admin
from .models import Employer_basic,Job_type,Job_post,Job_location,Job_post_activity,Job_post_skill_set,Company,Announcement
# Register your models here.

admin.site.register(Employer_basic)
admin.site.register(Job_type)
admin.site.register(Job_post)
admin.site.register(Job_location)
admin.site.register(Job_post_activity)
admin.site.register(Job_post_skill_set)
admin.site.register(Company)
admin.site.register(Announcement)