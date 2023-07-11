
from django import forms
from .models import *
from django.forms import ModelForm, BooleanField # Импортируем true-false поле




class NewsForms(forms.Form):
    time_create_gt = forms.DateField(label = "дата написания",
                                     widget = forms.TextInput
                                     (attrs ={
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
# если берем форму джанго то modelForm       
class AddNewsForm(ModelForm):
   
    consent = BooleanField(label='согласие на обработку данных')
    class Meta:
        model = Post
        #fields = '__all__'
        fields = ['title', 'author', 'categoryType', 'postCategory','content','photo', 'consent'] 
        

#если делаем форму не завяз на модели
#class AddNewsForm(forms.Form):   
    #title = forms.CharField(label="Заголовок")
    #author  = forms.ModelChoiceField(label='Автор', queryset=Author.objects.all())
    #postCategory = forms.ModelChoiceField(label='Раздел',  queryset=Category.objects.all())
    #categoryType = forms.ModelChoiceField(label='Категория',  choices=(('NW', "Новость"), ('AR', 'Статья')))
    #content = forms.CharField(label="Текст", widget = forms.Textarea(attrs={'cols': 60, 'rows':10}))
    #photo = forms.ImageField(label= 'Фото')
    #consent = forms.BooleanField(label='согласие на обработку данных')

    #class Meta:
       # model=Post
        #fields =['title', 'author', 'content']