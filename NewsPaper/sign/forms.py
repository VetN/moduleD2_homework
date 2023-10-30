from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # не забываем импортировать класс формы аутентификации
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import Group
from news.forms import SignupForm



class RegisterForm(UserCreationForm):
   password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='ПА')
   password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm Password')
  
   class Meta:
       model = User
       fields = (
         "username", # опционально
         "first_name",
         "email",
         "password1",
         "password2",
           )
       widgets = {
           'username': forms.TextInput(attrs={'class': 'form-control'}),
           'first_name': forms.TextInput(attrs={'class': 'form-control'}),
           'email': forms.EmailInput(attrs={'class': 'get-started-btn_1 scrollto'}),
       }
      
   def clean(self):
       username = self.cleaned_data.get('username')
       email = self.cleaned_data.get('email')
       if User.objects.filter(username=username).exists():
           raise forms.ValidationError("Пользователь с таким именем уже существует")
       if User.objects.filter(email=email).exists():
           raise forms.ValidationError("Пользователь с таким email уже существует")
       return super().clean()

# Добавляем новую форму для аутентификации пользователя
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = (
         "username",
         "password",
           )
        widgets = {
           'username': forms.TextInput(attrs={'class': 'my_form'}),
            #'first_name': forms.TextInput(attrs={'class': 'form-control'}),
           'email': forms.EmailInput(attrs={'class': 'get-started-btn_1 scrollto'}),
       }
