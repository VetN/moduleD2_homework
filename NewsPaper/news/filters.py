from django import forms
from django_filters import FilterSet, CharFilter, ChoiceFilter



from .models import*

class PostFilter(FilterSet):
    name = CharFilter(field_name='title', 
                      widget=forms.TextInput(), 
                      label='ПОИСК ПО ЗАГОЛОВКУ', 
                      lookup_expr='iregex',
                      required = False,
                      )
    author = CharFilter(
                      field_name='author__authorUser__first_name',
                      widget=forms.TextInput(attrs={'placeholder':'фамилия автора',
                                                   'class':'get-started-btn_f scrollto'  }),
                      label='АВТОР',
                      lookup_expr='iregex',
                      required = False
                    )
    content = CharFilter(
                      field_name='content',
                      widget=forms.TextInput(),
                      label='ТЕКСТ',
                      lookup_expr='iregex',
                     required = False
                    )
    categoryType = ChoiceFilter(label='КАТЕГОРИЯ',
                                choices = [
                                    ('AR', 'СТАТЬЯ'),
                                    ('NW', 'НОВОСТЬ'),
                                ]
                               )
    postCategory = ChoiceFilter(label='РАЗДЕЛ',
                                choices = [
                                    ('1', 'город'),
                                    ('2', 'дети'),
                                    ('3', 'культура'),
                                    ('4', 'образование'),
                                    ('5', 'красота'),
                                    ('6', 'животные'),
                            
                                ])
