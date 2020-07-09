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
    path('jobseeker_search',views.jobseeker_search,name="jobseeker_search"),
    path('jobseeker_search_view_job/<int:id>',views.jobseeker_search_view_job,name="jobseeker_search_view_job"),
    path('Jobseeker_apply_job/<int:id>',views.jobseeker_apply_job,name="jobseeker_apply_job"),
    path('jobseeker_view_job/<int:id>', views.jobseeker_view_job, name="jobseeker_view_job"),
    path('jobseeker_view_jobs',views.jobseeker_view_jobs,name="jobseeker_view_jobs"),
    path('jobseeker_cancel_application/<int:id>',views.jobseeker_cancel_application,name="jobseeker_cancel_application")
]