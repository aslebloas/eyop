from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models.functions import Lower
from django.forms import ModelForm

from .models import Profile, Relationship, Invitation, Code, Brand


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city']


class UserUpdateForm(ModelForm):
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


class CodeCreateForm(ModelForm):
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.order_by(Lower('brand_name')))

    class Meta:
        model = Code
        ordering = ['brand']
        fields = ['code', 'brand', 'description']
