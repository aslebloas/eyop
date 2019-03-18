from django.shortcuts import render, redirect
from .forms import RegisterForm, InvitationForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    PasswordChangeForm, AdminPasswordChangeForm
)
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from social_django.models import UserSocialAuth
from .models import Code, Relationship, Profile, Brand, Invitation


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
    invitations = Invitation.objects.filter(email=user.email)
    return render(
        request, 'referral_app/profile.html',
        {'codes': codes, 'relationships': relationships,
         'invitations': invitations})


@login_required
def home(request):
    user = request.user
    codes = Code.objects.filter(owner=user)
    relationships = Relationship.objects.filter(
        from_person=request.user.profile)
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.sender = user
            obj.save()
            obj.send()
            print("obj saved!")
            email = form.cleaned_data['email']
            messages.success(
                request, 'We sent your invitation to {}'.format(email))
            return redirect('/')
    else:
        form = InvitationForm()
    return render(
        request, 'referral_app/code_list.html',
        {'codes': codes, 'relationships': relationships,
         'form': form})


@login_required
def settings(request):
    """ Social OAuth settings and password change begin """
    user = request.user

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() >
                      1 or user.has_usable_password())

    return render(request, 'referral_app/settings.html', {
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'referral_app/password.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'referral_app/password.html', {'form': form})


""" Social OAuth settings and password change end """


class CodeCreate(LoginRequiredMixin, CreateView):
    model = Code
    fields = ['brand', 'code', 'description']
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


class BrandCreate(LoginRequiredMixin, CreateView):
    model = Brand
    fields = ['brand_name', 'logo']
    success_url = '/codes/new'
