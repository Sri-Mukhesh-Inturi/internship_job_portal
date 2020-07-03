from django.contrib import admin
from .models import Employer_basic,Job_post,Job_post_activity,Job_post_skill_set,Announcement,Company
# Register your models here.

admin.site.register(Employer_basic)
admin.site.register(Job_post)
admin.site.register(Job_post_activity)
admin.site.register(Job_post_skill_set)
admin.site.register(Announcement)
admin.site.register(Company)