
from django import forms
from .models import *
from django.forms import ModelForm, BooleanField # Импортируем true-false поле



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
