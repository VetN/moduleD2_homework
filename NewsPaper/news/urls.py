from django.urls import path, re_path
from .views import *

urlpatterns = [

    
    path('', NewsListMain.as_view(), name = 'home' ),
    re_path(r'^index/', NewsListMain.as_view(), name = 'home'),
    re_path(r'^news/', NewsList.as_view(), name = 'news_page' ),
    path('one_news/', news, name='one_news'),
    path('one_news/<int:pk>', NewsDetail.as_view(), name = 'o_news'),
    path('search', SearchList.as_view(), name = 'search' ),
    path('add_news', AddList.as_view(), name = 'add_news' ),
  
   
    #path('category_news/<slug:category_name>/', NewsCategory.as_view(), name = 'category') тоже работает в строке дает назв категории
    path('category_news/<int:pk>', NewsCategory.as_view(), name = 'category'),
    
]
