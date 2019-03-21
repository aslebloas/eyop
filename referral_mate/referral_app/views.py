from django.shortcuts import render, redirect
from .forms import (
    RegisterForm, InvitationForm, UserUpdateForm,
    ProfileUpdateForm, CodeCreateForm
)
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    PasswordChangeForm, AdminPasswordChangeForm
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, UpdateView, DeleteView, DetailView
)

from social_django.models import UserSocialAuth
from .models import Code, Relationship, Profile, Brand, Invitation, User

import uuid


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            messages.success(
                request, 'Account created for {}'.format(username))
            obj, created = Relationship.objects.get_or_create(
                from_person=get_object_or_404(User, id=2).profile,
                to_person=user.profile,
                status=1)
            obj, created = Relationship.objects.get_or_create(
                from_person=user.profile,
                to_person=get_object_or_404(User, id=2).profile,
                status=1)
            password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=password)
            login(request, user)

            return redirect('/')
    if request.method == 'GET':
        form = RegisterForm()
    return render(request, 'referral_app/register.html', {'form': form})


@login_required
def profile(request):
    cache_id = uuid.uuid4()
    user = request.user
    codes = Code.objects.filter(owner=user)
    relationships = Relationship.objects.filter(
        from_person=request.user.profile)
    invitations = Invitation.objects.filter(email=user.email)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request, 'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(
        request, 'referral_app/profile.html',
        {'codes': codes, 'relationships': relationships,
         'invitations': invitations,
         'u_form': u_form, 'p_form': p_form, 'cache_id': cache_id})


@login_required
def invitation_accept(request, pk):
    invitation = get_object_or_404(Invitation, pk=pk)
    if request.method == 'POST':
        obj, created = Relationship.objects.get_or_create(
            from_person=invitation.sender.profile,
            to_person=get_object_or_404(User, email=invitation.email).profile,
            status=1)
        obj, created = Relationship.objects.get_or_create(
            from_person=get_object_or_404(User, email=invitation.email).profile,
            to_person=invitation.sender.profile,
            status=1)
        print(obj)
        print(invitation)
        invitation.delete()
        print(invitation)
        return redirect('profile')
    return redirect('profile')


@login_required
def invitation_deny(request, pk):
    invitation = get_object_or_404(Invitation, pk=pk)
    if request.method == 'POST':
        obj, created = Relationship.objects.get_or_create(
            from_person=invitation.sender.profile,
            to_person=get_object_or_404(User, email=invitation.email).profile,
            status=2)
        obj, created = Relationship.objects.get_or_create(
            from_person=get_object_or_404(User, email=invitation.email).profile,
            to_person=invitation.sender.profile,
            status=2)
        invitation.delete()
        return redirect('profile')
    return redirect('profile')


@login_required
def home(request):
    cache_id = uuid.uuid4()
    user = request.user
    codes = Code.objects.filter(owner=user)
    relationships = Relationship.objects.filter(
        from_person=request.user.profile)
    brands = Brand.objects.all().order_by('brand_name')
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.sender = user
            obj.save()
            obj.send()
            email = form.cleaned_data['email']
            messages.success(
                request, 'We sent your invitation to {}'.format(email))
            return redirect('/')
    else:
        form = InvitationForm()
    return render(
        request, 'referral_app/code_list.html',
        {'codes': codes, 'brands': brands, 'relationships': relationships,
         'cache_id': cache_id, 'form': form})


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


@login_required
def code_create(request):
    """Create a new referral code"""
    if request.method == 'POST':
        form = CodeCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            if obj.code.startswith('http://'):
                obj.code = obj.code[7:]
            if obj.code.startswith('https://'):
                obj.code = obj.code[8:]
            obj.save()
            messages.success(
                request, 'Code {} Created, Add a new one:'.format(obj.code))
            return redirect('/codes/new')
    else:
        form = CodeCreateForm()
    return render(request, 'referral_app/code_form.html', {'form': form})


class CodeCreate(LoginRequiredMixin, CreateView):
    model = Code
    fields = ['code', 'brand', 'description']
    success_url = '/profile'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CodeUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Code
    fields = [ 'code', 'brand', 'description']
    success_url = '/profile'

    def test_func(self):
        return self.get_object().owner == self.request.user


class CodeDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Code
    success_url = '/profile'

    def test_func(self):
        return self.get_object().owner == self.request.user


@login_required
def friend_detail(request, pk):
    cache_id = uuid.uuid4()
    friend = Profile.objects.get(pk=pk)
    codes = Code.objects.filter(owner=friend.user)
    relationships = Relationship.objects.filter(
        from_person=friend)
    friends = []
    for element in relationships:
        friends.append(element.to_person)
    return render(request, 'referral_app/friend_detail.html',
        {'object': friend, 'codes': codes,
         'friends': friends, 'cache_id': cache_id})


class CodeDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Code

    def test_func(self):
        friends = [self.request.user.profile]
        rels = Relationship.objects.filter(
            from_person=self.request.user.profile)
        for element in rels:
            friends.append(element.to_person)
        return self.get_object().owner.profile in friends


@login_required
def brand_detail(request, pk):
    cache_id = uuid.uuid4()
    brand = Brand.objects.get(pk=pk)
    relationships = Relationship.objects.filter(
        from_person=request.user.profile)

    form = InvitationForm()

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
        {'brand': brand, 'referrers': referrers,
         'cache_id': cache_id, 'form': form})


class BrandCreate(LoginRequiredMixin, CreateView):
    model = Brand
    fields = ['brand_name', 'logo']
    success_url = '/codes/new'
