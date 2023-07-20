from django import forms
from django_filters import FilterSet, CharFilter, ChoiceFilter, DateTimeFilter



from .models import*

class PostFilter(FilterSet):
    name = CharFilter(field_name='title', 
                      widget=forms.TextInput(attrs={'placeholder':'текст заголовка',
                                                   'class':'get-started-btn_fp scrollto'  }), 
                      label='ПОИСК ПО ЗАГОЛОВКУ', 
                      lookup_expr='iregex',
                      required = False,
                      )
    author = CharFilter(
                      field_name='author__authorUser__first_name',
                      widget=forms.TextInput(attrs={'placeholder':'фамилия автора',
                                                   'class':'get-started-btn_fp scrollto',
                                                 }),
                      label='ПОИСК ПО АВТОРУ',
                      lookup_expr='iregex',
                      required = False
                    )
    content = CharFilter(
                      field_name='content',
                      widget=forms.TextInput(attrs={'placeholder':'текст новости',
                                                   'class':'get-started-btn_fp scrollto',
                                                 }),
                      label='ПОИСК ПО ТЕКСТУ',
                      lookup_expr='iregex',
                     required = False
                    )
    categoryType = ChoiceFilter(label='КАТЕГОРИЯ',
                                 widget=forms.Select(attrs={'class':'get-started-btn_fp scrollto'}),
                                choices = [
                                    ('AR', 'СТАТЬЯ'),
                                    ('NW', 'НОВОСТЬ'),
                                ]
                                )
                               
    postCategory = ChoiceFilter(label='РАЗДЕЛ',
                                widget=forms.Select(attrs={'class':'get-started-btn_fp scrollto'}),
                                choices = [
                                    ('1', 'город'),
                                    ('2', 'дети'),
                                    ('3', 'культура'),
                                    ('4', 'образование'),
                                    ('5', 'красота'),
                                    ('6', 'животные'),
                            
                                ])
    time_create = DateTimeFilter(widget=forms.TimeInput(attrs={'placeholder':'позже даты',
                                                               'class':'get-started-btn_f scrollto',
                                                        }),
                               label='ПОИСК ПО ДАТЕ',
                               lookup_expr='gt',
                               required = False)