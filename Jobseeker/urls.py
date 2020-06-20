from django.urls import path,include
from Jobseeker import views
app_name='Jobseeker'
urlpatterns = [
    path('home',views.jobseeker_home,name="jobseeker_home"),
    path('jobseeker_profile',views.jobseeker_profile,name = "jobseeker_profile"),
    path('jobseeker_update_profile_basic',views.jobseeker_update_profile_basic,name="jobseeker_update_profile_basic"),
    path('Jobseeker_update_education/<int:id>',views.jobseeker_update_education,name="jobseeker_update_education"),
    path('jobseeker_update_education/<str:operation>/<int:id>',views.jobseeker_update_education_crud,name="education_crud"),
    path('Jobseeker_update_experience/<int:id>', views.jobseeker_update_experience, name="jobseeker_update_experience"),
    path('jobseeker_update_experience/<str:operation>/<int:id>', views.jobseeker_update_experience_crud,name="experience_crud"),
    path('Jobseeker_update_skill_set/<int:id>', views.jobseeker_update_skill_set, name="jobseeker_update_skill_set"),
    path('jobseeker_update_skill_set/<str:operation>/<int:id>', views.jobseeker_update_skill_set_crud,name="skill_set_crud"),
]