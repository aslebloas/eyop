from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def home(request):
    """ redirects to home page """
    return render(request, 'referral_app/index.html')


def register(request):
    form = UserCreationForm()
    return render(request, 'referral_app/register.html', {'form': form})
