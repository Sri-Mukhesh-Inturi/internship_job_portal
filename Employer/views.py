from django.shortcuts import render
from django.http import HttpResponse
from Accounts.models import User_type
from django.contrib.auth.models import User

# Create your views here.
def employer_home(request):
    user_type_user = User_type.objects.get(user=request.user)
    return render(request,'Employer/employer_index.html',{'user_type':user_type_user})

def employer_profile(request):
    html = "<html><body>Employer profile page</body></html>"
    return HttpResponse(html)