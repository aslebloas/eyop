from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    """ redirects to home page """
    return render(request, 'referral_app/index.html')


def register(request):
    if request.method == 'POST':
      form = RegisterForm(request.POST)
      if form.is_valid():
        form.save()
        username = form.cleaned_data['username']
        messages.success(request, f'Account created for {username}')
        return redirect('login')
    if request.method == 'GET':
      form = RegisterForm()
    return render(request, 'referral_app/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'referral_app/profile.html')
