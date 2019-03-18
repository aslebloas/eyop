from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Profile, Relationship, Invitation


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city']


class UserUpdateForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email']


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'image']


class InvitationForm(ModelForm):
    email = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'email'}))

    class Meta:
        model = Invitation
        fields = ['email']
