from django.shortcuts import render
from .models import Profile


# This view display the home page.
def index(request):
    return render(request, 'index.html')


# This view display the profile list page.
def profiles_index(request):
    profiles_list = Profile.objects.all()
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles_index.html', context)


# This view display the profile detail of a user.
def profile(request, username):
    profile = Profile.objects.get(user__username=username)
    context = {'profile': profile}
    return render(request, 'profile.html', context)
