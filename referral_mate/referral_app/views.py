from django.shortcuts import render

# Create your views here.
def home(request):
  """ redirects to home page """
  return render(request, 'referral_app/index.html')