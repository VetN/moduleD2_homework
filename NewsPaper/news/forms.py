

from django import forms
from .models import *
from django.forms import ModelForm, BooleanField # Импортируем true-false поле
from allauth.account.forms import SignupForm, BaseSignupForm, LoginForm
from django.contrib.auth.models import Group

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
        self.fields[("username")] = forms.CharField(widget=forms.TextInput(attrs={'class': 'get-started-btn_6 scrollto'}),
                                                     required=True, label=("ИМЯ"), )
        self.fields[("first_name")] = forms.CharField(widget=forms.TextInput(attrs={'class': 'get-started-btn_2 scrollto'}),
                                                     required=True, label=("ФАМИЛИЯ"), )
        self.fields[("email")] = forms.CharField(widget=forms.TextInput(attrs={'class': 'get-started-btn_6 scrollto'}),
                                                    required=True, label=("E-mail"), )

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        
        user.username = self.cleaned_data['username']
        #user.first_name = self.cleaned_data['fist_name']
        user.email = self.cleaned_data['email']
        common_group = Group.objects.get_or_create(name='common')[0]
        common_group.user_set.add(user)
        user.save()
        #common_group = Group.objects.get[1]
        #common_group.user_set.add(user)
        return user

 

class CommonLoginForm(LoginForm):
       
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'get-started-btn_3 scrollto',
                                                                 'placeholder': 'введите пароль'}),
                                                     required=True, label=("ПАРОЛЬ"), )
     
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["login"] =forms.EmailField(widget=forms.TextInput(attrs={'class': 'get-started-btn_6 scrollto',
                                                                               'placeholder': 'адрес почты'}),
                                                    required=True, label=("E-mail"), ) 
    
    def save(self, request):
        user = super(CommonLoginForm, self).save(request)
        #user.username = self.cleaned_data['username']
        user.password = self.cleaned_data['password']
        user.login= self.cleaned_data['email']
        user.save()
        return user