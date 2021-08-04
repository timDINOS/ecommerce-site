from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from backend.user_network.user_models import MyProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = MyProfile
        fields = ['bio', 'image']

