
from django import forms



class TitleForms(forms.Form):
    title__icontains = forms.CharField(label = "заголовок",
                                       widget = forms.TextInput
                                       (attrs ={
                                           'type': 'content',
                                           'name': 'title',
                                           'placeholder': 'поиск по названию',
                                           'required': False,

                                       }))
       