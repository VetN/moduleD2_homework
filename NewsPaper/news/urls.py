from django.urls import path, re_path
from .views import *

from django.views.decorators.cache import cache_page # импортируем декоратор 
#для кэширования отдельного представления

urlpatterns = [


    # кеширование страницы
    #path('',cache_page(60)( NewsListMain.as_view()), name = 'home' ),
    
    path('', NewsListMain.as_view(), name = 'home' ),
    re_path(r'^index/', NewsListMain.as_view(), name = 'home'),
    re_path(r'^news/', NewsList.as_view(), name = 'news_page' ),
    
    path('<int:pk>', NewsDetail.as_view(), name = 'o_news'),
    path('search', SearchList.as_view(), name = 'search' ),

    #path('edit/', cache_page(10)(NewsEditView.as_view()), name = 'edit'),
    path('edit/', NewsEditView.as_view(), name = 'edit'),
    #path('<int:pk>/', NewsDetail.aus_view(), name = 'detail_news'),

    #страница закеширована 
    #path('add_news/', cache_page(5)(AddNewsCreate.as_view()), name = 'add_news' ),
    path('add_news/', AddNewsCreate.as_view(), name = 'add_news' ),
    
    path('update_news/<int:pk>/', NewsUpdateView.as_view(), name = 'edit_news'),
    path('delete/<int:pk>/', NewsDeleteView.as_view(), name='news_delete'),
   
    #path('category_news/<slug:category_name>/', NewsCategory.as_view(), name = 'category') тоже работает в строке дает назв категории
    path('category_news/<int:pk>', NewsCategory.as_view(), name = 'category'),
    
    path('subscribe/<int:pk>/', subCategory, name ='subcat'),
    path('unsubscribe/<int:pk>/', unsubCategory, name ='unsubcat'),
    
    
    #path('one_news/', news, name='one_news'),
]
