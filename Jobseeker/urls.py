from django.urls import path,include
from Jobseeker import views
app_name='Jobseeker'
urlpatterns = [
    path('home',views.jobseeker_home,name="jobseeker_home"),
    path('jobseeker_profile',views.jobseeker_profile,name = "jobseeker_profile"),
    path('jobseeker_update_profile_basic',views.jobseeker_update_profile_basic,name="jobseeker_update_profile_basic"),
    path('Jobseeker_update_education',views.jobseeker_update_education,name="jobseeker_update_education"),
    path('jobseeker_update_education/<str:operation>/<int:id>',views.jobseeker_update_education_crud,name="education_crud"),
]