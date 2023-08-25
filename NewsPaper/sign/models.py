from django.db import models

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    username = forms.CharField(label = "Имя") # опционально, можно не указывать
    first_name = forms.CharField(label = "Фамилия") # опционально

    class Meta:
        model = User
        fields = ("username", 
                  "first_name", # опционально
                 
                  "email", 
                  "password1", 
                  "password2", )
