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

]