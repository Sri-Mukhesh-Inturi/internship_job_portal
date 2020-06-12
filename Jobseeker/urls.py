from django.urls import path,include
from Jobseeker import views
app_name='Jobseeker'
urlpatterns = [
    path('home',views.jobseeker_home,name="jobseeker_home"),
]