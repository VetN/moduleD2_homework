from django import forms
from django_filters import FilterSet
import django_filters as filters

from .forms import NewsForms # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import*

class PostFilter(FilterSet):
    

    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т.е. подбираться) информация о товарах
    class Meta:
        model = Post


        #fields = ('name', 'price', 'quantity', 'category') # поля, которые мы будем фильтровать (т.е. отбирать по каким-то критериям, имена берутся из моделей)
        # если сделать корректировку дизайна
        fields = {
            
            'title': ['iregex'], # мы хотим чтобы нам выводило имя хотя бы отдалённо похожее на то, что запросил пользователь
            'author': ['in'], # количество товаров должно быть больше или равно тому, что указал пользователь
            #'categoryType': ['in'],
            'content': ['iregex'],
            'time_create':['gt'],# цена должна быть меньше или равна тому, что указал пользователь
        }
        widgets = {
            'time_create': forms.DateField(label='Дата создания'),
            'title': forms.CharField( label='Заголовок', required = False),
            'author_in': forms.ModelChoiceField(queryset=Author.objects.all(), required = False,),
            'categoryType': forms.ModelChoiceField(queryset=Category.objects.all(), required = False, )                         
       
        }
                    

       
        #fields=('title', 'author', 'postCategory', 'time_create')