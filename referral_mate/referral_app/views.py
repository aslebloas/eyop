from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .models import Code, Relationship, Profile, Brand


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(
                request, 'Account created for {}'.format(username))
            return redirect('login')
    if request.method == 'GET':
        form = RegisterForm()
    return render(request, 'referral_app/register.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    codes = Code.objects.filter(owner=user)
    relationships = Relationship.objects.filter(
        from_person=request.user.profile)
    return render(
        request, 'referral_app/profile.html',
        {'codes': codes, 'relationships': relationships})


@login_required
def home(request):
    user = request.user
    codes = Code.objects.filter(owner=user)
    relationships = Relationship.objects.filter(
        from_person=request.user.profile)
    return render(
        request, 'referral_app/code_list.html',
        {'codes': codes, 'relationships': relationships})


class CodeCreate(LoginRequiredMixin, CreateView):
    model = Code
    fields = ['brand', 'code', 'amount', 'UOM', 'criteria']
    success_url = '/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CodeUpdate(LoginRequiredMixin, UpdateView):
    model = Code


class CodeDelete(LoginRequiredMixin, DeleteView):
    model = Code
    success_url = '/'


class FriendDetail(LoginRequiredMixin, DetailView):
    model = Profile


class CodeDetail(LoginRequiredMixin, DetailView):
    model = Code


@login_required
def brand_detail(request, pk):
    brand = Brand.objects.get(pk=pk)
    relationships = Relationship.objects.filter(
        from_person=request.user.profile)

    friends = []
    for element in relationships:
        friends.append(element.to_person)

    referrers = {}
    for friend in friends:
        code = Code.objects.filter(brand=brand).filter(owner=friend.user)
        if code:
            referrers[friend] = code[0].id

    return render(
        request, 'referral_app/brand_detail.html',
        {'brand': brand, 'referrers': referrers})
