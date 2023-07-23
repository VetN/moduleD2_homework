

from django import forms
from .models import *
from django.forms import ModelForm, BooleanField # Импортируем true-false поле
from allauth.account.forms import SignupForm, BaseSignupForm


# если берем форму джанго то modelForm  
class AddNewsForm(ModelForm):
    
    consent = BooleanField(label='согласие на обработку данных')
    class Meta:
        model = Post
        #fields = '__all__'
        fields = ['title', 'author', 'categoryType', 'postCategory','content','photo', 'consent'] 
        labels = {
            'title': 'ЗАГОЛОВОК',
            'author': 'АВТОР',
            'categoryType': 'КАТЕГОРИЯ',
            'postCategory': 'РАЗДЕЛ',
            'content': 'ТЕКСТ',
            'photo': 'фото'
        }

        widgets = {
            
            'title': forms.TextInput(attrs={
                'class': 'get-started-btn_0 scrollto',
                'placeholder': 'название статьи / новости'
            }),

            'author': forms.Select(attrs={
                'class': 'get-started-btn_1 scrollto',
            }), 

            'categoryType': forms.Select(attrs={
                'class': 'get-started-btn_2 scrollto',
            }), 
           
             'postCategory': forms.SelectMultiple(attrs={
                'class': 'get-started-btn_3 scrollto',
            }),

            'content': forms.Textarea(attrs={
                'class': 'get-started-btn_4 scrollto',
                'placeholder': 'текст статьи / новости'
            }),
        }

class CommonSignupForm(SignupForm, BaseSignupForm):
  
   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[("password1")] = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'get-started-btn_3 scrollto'}),
                                                     required=True, label=("ПАРОЛЬ"), )
        self.fields[("password2")] = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'get-started-btn_3 scrollto'}),
                                                     required=True, label=("ПАРОЛЬ"), )
        self.fields[("username")] = forms.CharField(widget=forms.TextInput(attrs={'class': 'get-started-btn_3 scrollto'}),
                                                     required=True, label=("ИМЯ"), )
        self.fields[("first_name")] = forms.CharField(widget=forms.TextInput(attrs={'class': 'get-started-btn_3 scrollto'}),
                                                     required=True, label=("ФАМИЛИЯ"), )
        self.fields[("email")] = forms.CharField(widget=forms.TextInput(attrs={'class': 'get-started-btn_3 scrollto'}),
                                                    required=True, label=("E-mail"), )

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.username = self.cleaned_data['username']
        #user.first_name = self.cleaned_data['fist_name']
        user.email = self.cleaned_data['email']
        user.save()
        return user
