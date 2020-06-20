from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class User_type(models.Model):
    user_type_choices=[
        ('employer','employer'),
        ('jobseeker','jobseeker')
    ]
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    user_type_name = models.CharField(max_length=10,default="jobseeker",choices=user_type_choices)
    phone_number = models.CharField(max_length=10)
    current_city = models.CharField(max_length=30)
    def __str__(self):
        return self.user.username


