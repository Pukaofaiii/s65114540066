from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from web_app.models import User_Profile
from web_app.forms import UserprofileForm
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def index(req):
    return render(req,"index.html")

def service_rates(req):
    return render(req,"Service_rates.html")


def contact(req):
    return render(req,"contact.html")

@login_required
def user_profile(req):
    try:
        user_profile = User_Profile.objects.get(user=req.user)
        return render(req, 'user_profile.html', {'user_profile': user_profile})  
    except ObjectDoesNotExist:
        return redirect('edit_profile')



def update_profile_image(request):
    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        if profile_image:
            user_profile, created = User_Profile.objects.get_or_create(user=request.user)
            user_profile.profile_image = profile_image
            user_profile.save()
    return redirect('user_profile')  

def edit_profile(request):
    user_profile, created = User_Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserprofileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  
    else:
        form = UserprofileForm(instance=user_profile)
    return render(request, 'edit_profile.html', {'form': form })
        