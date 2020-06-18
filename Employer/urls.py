from django.urls import path,include
from Employer import views
app_name='Employer'
urlpatterns = [
    path('home',views.employer_home,name="employer_home"),
    path('employer_profile',views.employer_profile,name="employer_profile")
]