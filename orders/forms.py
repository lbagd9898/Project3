from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    firstname = forms.CharField(max_length=64, label = "First name")
    lastname = forms.CharField(max_length=64, label = "Last Name")
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["firstname", "lastname", "username", "email", "password1", "password2"]
