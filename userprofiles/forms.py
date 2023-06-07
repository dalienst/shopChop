from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "w-full p-2 border border-gray-200"}
            ),
            "password1": forms.PasswordInput(
                attrs={"class": "w-full p-2 border border-gray-200"}
            ),
            "password2": forms.PasswordInput(
                attrs={"class": "w-full p-2 border border-gray-200"}
            ),
        }
