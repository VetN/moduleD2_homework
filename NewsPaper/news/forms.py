
from django import forms
from .models import *



class NewsForms(forms.Form):
    time_create_gt = forms.DateField(label = "дата написания",
                                     widget = forms.TextInput
                                       (attrs ={
                                           'type': 'date',
                                           'name': 'date',
                                           'placeholder': 'дата',
                                          
                                           }),required = False)
    title__icontains = forms.CharField(label = "заголовок",
                                       widget = forms.TextInput
                                       (attrs ={
                                           'type': 'content',
                                           'name': 'title',
                                           'placeholder': 'поиск по названию',
                                           

                                       }),required = False)
    author_in = forms.ModelChoiceField(queryset=Author.objects.all(), required = False,)
    categoryType_in  = forms.ModelChoiceField(queryset=Category.objects.all(), required = False, )                         
       