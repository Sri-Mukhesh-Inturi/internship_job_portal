from django.urls import path,include,re_path
from Employer import views
app_name='Employer'
urlpatterns = [
    path('home',views.employer_home,name="employer_home"),
    path('employer_profile',views.employer_profile,name="employer_profile"),
    path('employer_update_profile_basic',views.employer_update_profile_basic,name="employer_update_profile_basic"),
    path('edit_company/<str:company_name>/',views.edit_company,name="edit_company"),
    path('employer_post_job/<int:id>/', views.employer_post_job, name="employer_post_job"),
    path('employer_post_job_crud/<str:operation>/<int:id>/', views.employer_post_job_crud, name="post_job_crud"),
    path('employer_view_jobs',views.employer_view_jobs,name="employer_view_jobs"),
    path('toggle_job_post_activity/<int:id>/',views.toggle_job_post_activity,name='toggle_job_post_activity'),
    path('employer_view_job/<int:id>/',views.employer_view_job,name="employer_view_job"),
    path('job_post_update_skill_set/<str:operation>/<int:id>/<str:name>',views.job_post_update_skill_set,name="job_post_update_skill_set"),
    path('job_post_view_applications/<int:id>',views.job_post_view_applications,name="job_post_view_applications"),
    path('job_post_view_applications_full_profile/<str:username>',views.job_post_view_applications_full_profile,name="job_post_view_applications_full_profile")

]