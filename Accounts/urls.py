
from django.urls import path,include
from Accounts import views
app_name='Accounts'
urlpatterns = [
    path('register',views.register,name="register"),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_login/', views.user_login, name='user_login'),
]